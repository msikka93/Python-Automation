# SCRIPT TO RESTART GRAPHITE CARBON CONTAINERS FOR RESOLVING GRAFANA SLOWNESS
import time
import paramiko
import sys
import datetime
import re

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
    print(f"{'#' * 50} Python Script For restarting carbon docker containers on odhecx180,odhecx181 and odhecx182 {'#' * 50}")
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
            client.connect(hostname,port =22, username= user, pkey=k)
            channel = client.get_transport().open_session()
            channel.get_pty()
            print(f"{'#' * 50} Connecting Established with {hostname} {'#' * 50}")
            channel.invoke_shell()
            commands_to_exec = ['sudo -i','docker restart carbonite-relay', 'docker restart carbonite-go-carbon', 'docker restart carbonite-carbonapi']
            for command in commands_to_exec:
                get_command_results(channel, command)
                time.sleep(10)
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
#172.23.112.163 --odhecx181e
#172.23.112.162 --odhecx180e
#172.23.112.164 --odhecx182e
#C:/Users/gaurav.sikka01/.ssh/opensshkey