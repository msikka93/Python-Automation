#RETRIEVING CHECKPOINT SCRIPT
import time
import paramiko
import sys
import re
import datetime
import requests
import tkinter as tk
from tkinter import ttk
from pprint import pprint
from tkinter.messagebox import askyesno

class Alert(tk.Tk):
    def __init__(self,channel, checkpoints):
        super().__init__()
        self.channel = channel
        self.checkpoints = checkpoints
        self.title('Clear Checkpoint Dialog')
        self.geometry('300x150')

        # Confirm button
        confirm_button = ttk.Button(self, text='Clear Checkpoint', command=self.confirm)
        confirm_button.pack(expand=True)

    def confirm(self):
        answer = askyesno(title='Confirmation',
                          message='Are you sure that you want to clear the checkpoints?')
        if answer:
            self.destroy()
            remove_checkpoints(self.channel, self.checkpoints)


def get_command_results(channel,command,isCheckPointPathRequired,checkPointsReceived):
    print(f"{'#' * 50} Command Executing... {'#' * 50}")
    try:
        interval = 0.1
        maxseconds = 10
        maxcount = maxseconds / interval
        bufsize = 1024
        input_idx = 0
        timeout_flag = False
        start = datetime.datetime.now()
        start_secs = time.mktime(start.timetuple())
        output = ''
        channel.setblocking(0)
        if not command.endswith("\n"):
            command += "\n"
        channel.send(command)
        while True:
            if channel.recv_ready():
                data = channel.recv(bufsize).decode('ascii')
                output += data

            if channel.exit_status_ready():
                break
            # Timeout check
            now = datetime.datetime.now()
            now_secs = time.mktime(now.timetuple())
            et_secs = now_secs - start_secs
            if et_secs > maxseconds:
                timeout_flag = True
                break
            rbuffer = output.rstrip(' ')
            if len(rbuffer) > 0 and (rbuffer[-1] == '#' or rbuffer[-1] == '>'):
                break
            time.sleep(0.200)
        if channel.recv_ready():
            data = channel.recv(bufsize)
            output += data.decode('ascii')
        print('Command Result :',output)
        commandOutputList = output.split('\n')
        if isCheckPointPathRequired:
            try:
                path=getCheckPointPath(commandOutputList)
                return path
            except:
                print ("Error while getting the checkpoints path")
        if checkPointsReceived:
            try:
                check_points_list=get_spark_checkpoints_list(commandOutputList)
                return check_points_list
            except:
                print ("Error while getting the checkpoints")
        print(f"{'#' * 50} Command Executed Successfully {'#' * 50}")
    except:
        print('Error while executing the command.Please try again')
        exit()


def getConfiguration():
    while True:
        try:
            spark_job_name = input("Enter the spark job name :-")
            if not spark_job_name:
                raise ValueError('Spark Job name is not defined')

            response = requests.get("http://connectivity.odh.lgi.io/marathon/v2/apps//spark/{0}".format(spark_job_name),
                                    auth=('odhuser', 'password'))
            data = response.json()
            if data:
                responseData = data['app']['cmd']
                hdfs_path = responseData.split(' ')[-2]
                return hdfs_path
            break
        except ValueError as e:
            print("Sorry, I didn't understand that.", e)
            continue
        except:
            print("Something went wrong while getting the response")


def getCheckpointPathCommand(channel):
    try:
        check_point_path = getConfiguration()
        cmd = f'docker exec -it hdfs-datanode hdfs dfs -cat {check_point_path}'
        check_point_cmd = get_command_results(channel,cmd,True,False)
    except:
        print("Something went wrong while getting the checkpoint path command")

    return check_point_cmd


def getCheckpointsCommand(channel,checkPointPath):
    cmd = f'docker exec -it hdfs-datanode hdfs dfs -ls {checkPointPath}'
    result = get_command_results(channel,cmd,False,True)
    return result


def getCheckPointPath(commandOutputList):
    for checkpoint in commandOutputList:
        if "checkpoint:" in checkpoint or "checkpointLocation:" in checkpoint :
            checkpoint_path_retrieved = checkpoint[checkpoint.find("hdfs"):]
        else:
            pass
    return checkpoint_path_retrieved


def remove_checkpoints(channel,checkpoints):
    for checkpoint in checkpoints:
        cmd = f'docker exec -it hdfs-datanode hdfs dfs -rm -r {checkpoint}'
        get_command_results(channel,cmd,False,False)


def get_spark_checkpoints_list(commandOutputList):
    checkpointlist = []
    for checkpoints in commandOutputList:
        if "spark-checkpoints" in checkpoints:
            hdfsPath = checkpoints[checkpoints.find("hdfs"):-1]
            checkpointlist.append(hdfsPath)
        else:
            pass
    return checkpointlist


def ssh_conn():
    print(f"{'#' * 50} Python Script For Clearing Spark CheckPoint {'#' * 50}")
    while True:
        try:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.load_system_host_keys()
            hostname = input("Enter the hostname:-")
            if not hostname:
                raise ValueError('Hostname is not defined')
            else:
                pattern = re.compile("\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}")
                ip = pattern.match(hostname)
                if not ip:
                    print("Unacceptable IP address")
                    continue
            sshpath = input("Enter the path to your ssh key:-")
            if not sshpath:
                raise ValueError('SSH Path is not defined')
            user = input("Enter the username:-")
            if not user:
                raise ValueError('Username is not defined')
            k = paramiko.RSAKey.from_private_key_file(sshpath)
            print(f"{'#' * 50} Connecting to the Device {'#' * 50}")
            client.connect(hostname,port =22, username=user, pkey=k)
            channel = client.get_transport().open_session()
            channel.get_pty()
            print(f"{'#' * 50} Connecting Established with {'#' * 50}")
            commands_to_exec = 'sudo -i'
            channel.invoke_shell()

            get_command_results(channel,commands_to_exec,False,False)
            #checkpoint
            checkPointPath = getCheckpointPathCommand(channel)
            print(f"{'#' * 50} Retrieving the checkpoints... {'#' * 50}")
            if checkPointPath:
                checkpoints = getCheckpointsCommand(channel,checkPointPath)
            else:
                print("Something went wrong while retrieving checkpoints.Please try again...")
            print(f"{'#' * 50} Deleting the checkpoints... {'#' * 50}")
            try:
                if len(checkpoints) == 0:
                    print("Checkpoints not found for this job")
                else:
                    alert = Alert(channel, checkpoints)
                    alert.mainloop()
            except:
                print("Error while deleting the checkpoints")
            client.close()
            break
        except IOError as e:
            print("Invalid input", e)
            continue
        except ValueError as e:
            print("Sorry, I didn't understand that.", e)
            continue
        except IndexError as e:
            print("Something went wrong with the index", e)
            continue
        except paramiko.SSHException as sshException:
            print("Unable to establish SSH connection: %s" % sshException)
            continue
        except paramiko.AuthenticationException:
            print("Authentication Error!!")
            continue
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise

ssh_conn()
sys.exit()


#Example
#C:/Users/gaurav.sikka01/.ssh/opensshkey --please use your local private key
#172.31.101.116 --odhat12e
#hdfs:///processing-conf/spark_eosdtv_eosstb_eosstb_streamparser_nl-conf.yml-e1bbecf6a60aebc1ccce65d237cf05ee.yml
#hdfs:///processing-conf/spark_eosdtv_eosstb_eosstb_streamparser_gb-conf.yml-4b6b6403eae7cbef72b4361df4cebd22.yml

#container restart scenario --> need to validate