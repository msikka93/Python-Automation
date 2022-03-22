#KAFKATOPIC SCRIPT
import time
import paramiko
import sys
import datetime
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import askyesno

class Alert(tk.Tk):
    def __init__(self,channel, jobname, option):
        super().__init__()
        self.channel = channel
        self.jobname = jobname
        self.option = option
        self.title('Clear Checkpoint Dialog')
        self.geometry('300x150')

        # Confirm button
        confirm_button = ttk.Button(self, text='Rescale the Job', command=self.confirm)
        confirm_button.pack(expand=True)

    def confirm(self):
        answer = askyesno(title='Confirmation',
                          message='Are you sure that you want to rescale the job?')
        if answer:
            self.destroy()
            if(self.option == 0):
                rescale_logthrash_job(self.channel, self.jobname)
            else:
                rescale_spark_job(self.channel,self.jobname)

def rescale_logthrash_job(channel,job_name):
    while True:
        try:
            replicas = input("Please enter the no of instances:- \n")
            if not replicas:
                raise ValueError('No instance provided')
            commands_to_exec =[f'kubectl scale deployments/{job_name} -n logthrash-general --replicas=0',f'kubectl scale deployments/{job_name} -n logthrash-general --replicas={replicas}']
            for cmd in commands_to_exec:
                get_command_results(channel, cmd)
                time.sleep(5)
            break
        except ValueError as e:
            print("Sorry, I didn't understand that.", e)
            continue
        except:
            print("Something went wrong while searching the keyword")

def rescale_spark_job(channel,job_name):
    while True:
        try:
            replicas = input("Please enter the no of instances:- \n")
            if not replicas:
                raise ValueError('No instance provided')
            commands_to_exec =[f'kubectl scale deployments/{job_name} -n spark-odhecx --replicas=0',f'kubectl scale deployments/{job_name} -n spark-odhecx --replicas={replicas}']
            for cmd in commands_to_exec:
                get_command_results(channel, cmd)
                time.sleep(5)
            break
        except ValueError as e:
            print("Sorry, I didn't understand that.", e)
            continue
        except:
            print("Something went wrong while searching the keyword")

def commands_to_run(argument,job_name):
    switcher = {
        0: lambda: f'kubectl get pods -n logthrash-general  | grep {job_name}',
        1: lambda: f'kubectl get pods -n spark-odhecx | grep {job_name}'
    }
    return switcher.get(argument,lambda :"Incorrect Option")()

def kube_command(deviceAccess):
    while True:
        try:
            job_name = input("Enter the job name :-")
            if not job_name:
                raise ValueError('Job name is not defined')
            option = int(input(
                'Please select the option below \n 0. Get kubernetes pods of odhecx logthrash job  \n 1. Get kubernetes pods of odhecx spark job \n'))
            cmd = commands_to_run(option, job_name)
            if cmd != "Incorrect Option":
                get_command_results(deviceAccess, cmd)
                alert = Alert(deviceAccess, job_name, option)
                alert.mainloop()
            else:
                continue
            break
        except ValueError as e:
            print("Sorry, I didn't understand that.", e)
            break
        except:
            print("Something went wrong while getting respinse for this particular job")


def get_command_results(channel,command):
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
        print(f"{'#' * 50} Command Executed Successfully {'#' * 50}")
    except:
        print('Error while executing the command.Please try again')
        exit()



def ssh_conn():
    print(f"{'#' * 50} Python Script For Checking Kafka Logs {'#' * 50}")
    while True:
        try:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.load_system_host_keys()
            # hostname = input("Enter the hostname:-")
            # if not hostname:
            #     raise ValueError('Hostname is not defined')
            # else:
            #     pattern = re.compile("\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}")
            #     ip = pattern.match(hostname)
            #     if not ip:
            #         print("Unacceptable IP address")
            #         continue
            # sshpath = input("Enter the path to your ssh key:-")
            # if not sshpath:
            #     raise ValueError('SSH Path is not defined')
            # user = input("Enter the username:-")
            # if not user:
            #     raise ValueError('Username is not defined')
            k = paramiko.RSAKey.from_private_key_file('C:/Users/gaurav.sikka01/.ssh/opensshkey')
            print(f"{'#' * 50} Connecting to the Device {'#' * 50}")
            client.connect('172.23.114.25',port =22, username= 'gsikka', pkey=k)
            channel = client.get_transport().open_session()
            channel.get_pty()
            print(f"{'#' * 50} Connecting Established with {'#' * 50}")
            channel.invoke_shell()
            commands_to_exec = 'sudo -i'
            get_command_results(channel, commands_to_exec)
            kube_command(channel)
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


#Example
#C:/Users/gaurav.sikka01/.ssh/opensshkey --please use your local private key
# 172.16.100.217
# odhecx_pr_eosdtv_ch_prd_stb_flat_v1 --PR
# odhecx_in_eosdtv_ch_prd_stb_v1  --IN