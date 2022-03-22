#RETRIEVING CHECKPOINT SCRIPT
import time
import paramiko
import sys
import re


def getCheckpointPathCommand(deviceAccess):
    while True:
        try:
            check_point_path = input("Enter the check point path :-")
            if not check_point_path:
                raise ValueError('check point path is not defined')
            cmd = f'docker exec -it hdfs-datanode hdfs dfs -cat {check_point_path}'
            check_point_cmd = execute_command(deviceAccess,cmd,True)
            break
        except ValueError as e:
            print("Sorry, I didn't understand that.", e)
            continue
    return check_point_cmd

def getCheckpointsCommand(deviceAccess,checkPointPath):
    cmd = f'docker exec -it hdfs-datanode hdfs dfs -ls {checkPointPath}'
    execute_command(deviceAccess,cmd,False)

def getCheckPointPath(commandOutputList):
    checkpoints = []
    for checkpoint in commandOutputList:
        if "checkpoint:" in checkpoint:
            checkpoints.append(checkpoint)
        elif "checkpointLocation:" in checkpoint:
            checkpoints.append(checkpoint)
        else:
            pass
    checkpoint_path_retrieved = checkpoints[0].split(': ')[1]
    return checkpoint_path_retrieved


def execute_command(deviceAccess,command,isCheckPointPathRequired):
    try:
        deviceAccess.send(command+"\n")
        print(f"{'#' * 50} Command Executing... {'#' * 50}")
        time.sleep(4.0)
        output = deviceAccess.recv(65000)
        if not output:
            print("Output List is empty")
        else:
            print(output.decode(), end='\n')
            print(f"{'#' * 50} Command Executed Successfully {'#' * 50}")
        if isCheckPointPathRequired:
            try:
                commandOutputList = output.decode().split('\n')
                path=getCheckPointPath(commandOutputList)
                return path
            except ValueError:
                print ("Error while getting the check points")
    except:
        print(f'Error while executing the command {command}')
        exit()


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
            print(f"{'#' * 50} Connecting to the Device {hostname} {'#' * 50}")
            client.connect(hostname,port =22, username=user, pkey=k)
            print(f"{'#' * 50} Connecting Established with {hostname} {'#' * 50}")
            commands_to_exec = 'sudo -i'
            DEVICE_ACCESS = client.invoke_shell()
            while not DEVICE_ACCESS.recv_ready():
                time.sleep(4.0)
            execute_command(DEVICE_ACCESS, commands_to_exec, False)
            #checkpoint
            checkPointPath = getCheckpointPathCommand(DEVICE_ACCESS)
            print(f"{'#' * 50} Retrieving the checkpoints... {'#' * 50}")
            time.sleep(1.5)
            if checkPointPath:
                getCheckpointsCommand(DEVICE_ACCESS,checkPointPath)
            else:
                print("Checkpoint path is incorrect.Please try again...")
            client.close()
            break
        except IOError as e:
            print("Invalid input", e)
            continue
        except ValueError as e:
            print("Sorry, I didn't understand that.", e)
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

#C:/Users/gaurav.sikka01/.ssh/opensshkey
#172.31.101.116 --odhat12e
#hdfs:///processing-conf/spark_eosdtv_eosstb_eosstb_streamparser_nl-conf.yml-e1bbecf6a60aebc1ccce65d237cf05ee.yml
#172.23.112.20 --odhecx37e
#hdfs:///processing-conf/spark_eosdtv_uservices_metrics4_v4_gb-conf.yml-9a8df0f7116184176ed26495e2c832db.yml