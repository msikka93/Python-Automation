#KAFKATOPIC SCRIPT
import time
import paramiko
import sys
import datetime
import re


def get_sub_option(kafka_topic):
    while True:
        try:
            suboption = input("Please enter the keyword to be searched:- \n")
            if not suboption:
                raise ValueError('Keyword is not defined')
            cmd = f'kafkacat -b 172.16.100.217:9092 -e -C -t {kafka_topic} -o -10 | grep {suboption}'
            return cmd
            break
        except ValueError as e:
            print("Sorry, I didn't understand that.", e)
            continue
        except:
            print("Something went wrong while searching the keyword")


def get_sub_option_2(kafka_topic):
    while True:
        try:
            epocTimestamp = input("Please enter the EPOC Timestamp:- \n")
            if not epocTimestamp:
                raise ValueError('EPOC is not defined')
            if not epocTimestamp.isdigit():
                raise ValueError('Epoc must be a number.')
            cmd = f'kafkacat -b 172.16.100.217:9092 -e -C -t {kafka_topic} -o s@{epocTimestamp}'
            return cmd
            break
        except ValueError as e:
            print("Sorry, I didn't understand that.", e)
            continue
        except:
            print("Something went wrong with the EPOC timestamp")

def get_sub_option_3(kafka_topic):
    while True:
        try:
            epocTimestamp = input("Please enter the EPOC Timestamp:- \n")
            if not epocTimestamp:
                raise ValueError('EPOC is not defined')
            if not epocTimestamp.isdigit():
                raise ValueError('Epoc must be a number.')
            suboption = input("Please enter the keyword to be searched:- \n")
            if not suboption:
                raise ValueError('Keyword is not defined')
            cmd = f'kafkacat -b 172.16.100.217:9092 -e -C -t {kafka_topic} -o s@{epocTimestamp} | grep {suboption}'
            return cmd
            break
        except ValueError as e:
            print("Sorry, I didn't understand that.", e)
            continue
        except:
            print("Something went wrong with the EPOC timestamp or while grepping the searched keyword")

def get_sub_option_4(kafka_topic):
    while True:
        try:
            epocTimestamp = input("Please enter the EPOC Timestamp:- \n")
            if not epocTimestamp:
                raise ValueError('EPOC is not defined')
            if not epocTimestamp.isdigit():
                raise ValueError('Epoc must be a number.')
            suboption1 = input("Please enter the keyword1 to be searched:- \n")
            if not suboption1:
                raise ValueError('Keyword1 is not defined')
            suboption2 = input("Please enter the keyword2 to be searched:- \n")
            if not suboption2:
                raise ValueError('Keyword2 is not defined')
            cmd = f'kafkacat -b 172.16.100.217:9092 -e -C -t {kafka_topic} -o s@{epocTimestamp} | grep {suboption1} | grep {suboption2}'
            return cmd
            break
        except ValueError as e:
            print("Sorry, I didn't understand that.", e)
            continue
        except:
            print("Something went wrong with the EPOC timestamp or while grepping the searched keyword")

def get_sub_option_5(kafka_topic):
    while True:
        try:
            suboption1 = input("Please enter the keyword1 to be searched:- \n")
            if not suboption1:
                raise ValueError('Keyword1 is not defined')
            suboption2 = input("Please enter the keyword2 to be searched:- \n")
            if not suboption2:
                raise ValueError('Keyword2 is not defined')
            cmd = f'kafkacat -b 172.16.100.217:9092 -e -C -t {kafka_topic} -o -100 | grep {suboption1} | grep {suboption2}'
            return cmd
            break
        except ValueError as e:
            print("Sorry, I didn't understand that.", e)
            continue
        except:
            print("Something went wrong while grepping the searched keywords")

def numbers_to_strings(argument,kafka_topic):
    switcher = {
        0: lambda: f'kafkacat -b 172.16.100.217:9092 -e -C -t {kafka_topic} -o -10 | grep timestamp',
        1: lambda: f'kafkacat -b 172.16.100.217:9092 -e -C -t {kafka_topic} -o beginning | grep timestamp',
        2: lambda: get_sub_option(kafka_topic),
        3: lambda: f'kafkactl get topic {kafka_topic} --describe --lag',
        4: lambda: f'kafkacat -b 172.16.100.217:9092 -e -C -t {kafka_topic} -o -10 | grep ts',
        5: lambda: get_sub_option_2(kafka_topic),
        6: lambda: f'kafkacat -b 172.16.100.217:9092 -e -C -t {kafka_topic} -o -10',
        7: lambda: f'kafkacat -b 172.16.100.217:9092 -e -C -t {kafka_topic} -o beginning',
        8: lambda: get_sub_option_3(kafka_topic),
        9: lambda: get_sub_option_4(kafka_topic),
        10: lambda: get_sub_option_5(kafka_topic)
    }
    return switcher.get(argument,lambda :"Incorrect Option")()

def docker_command(deviceAccess):
    while True:
        try:
            kafka_topic = input("Enter the Kafka topic :-")
            if not (kafka_topic.startswith("odhecx") or kafka_topic.startswith("odhat")):
                raise ValueError('Kafka topic format must be incorrect')
            if not kafka_topic:
                raise ValueError('kafka topic is not defined')
            option = int(input(
                'Please select the option below \n '
                '0. Kafka topic logs grep with timestamp(offset ~ last 10 occurrence) \n '
                '1. Kafka topic logs grep with timestamp(offset ~ beginning) \n '
                '2. Kafka topic logs grep with searched keyword(offset ~ last 10 occurrence) \n '
                '3. Kafka topic lag check \n '
                '4. Kafka topic logs grep with ts for INPUT Topics(offset ~ last 10 occurrence) \n '
                '5. Kafka topic logs (offset ~ epoc timestamp) \n '
                '6. Kafka topic logs last 10 occurances \n '
                '7. Kafka topic logs from beginning offset without grep anything \n '
                '8. Kafka topic logs grep with searched keyword (offset ~ epoc timestamp) \n'
                '9. Kafka topic logs grep with two searched keyword (offset ~ epoc timestamp) \n'
                '10. Kafka topic logs grep with two searched keyword (offset ~ last 100x occurrence) \n'
            ))
            cmd = numbers_to_strings(option, kafka_topic)
            print("Result:", cmd)
            if cmd != "Incorrect Option":
                get_command_results(deviceAccess, cmd)
            else:
                continue
            break
        except ValueError as e:
            print("Sorry, I didn't understand that.", e)
            break
        except:
            print("Something went wrong while getting respinse for this kafka topic")


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
            client.connect('172.16.100.217',port =22, username= 'gsikka', pkey=k)
            channel = client.get_transport().open_session()
            channel.get_pty()
            print(f"{'#' * 50} Connecting Established with {'#' * 50}")
            channel.invoke_shell()
            commands_to_exec = 'sudo -i'
            get_command_results(channel, commands_to_exec)
            docker_command(channel)
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
while True:
    ssh_conn()


#Example
#C:/Users/gaurav.sikka01/.ssh/opensshkey --please use your local private key
# 172.16.100.217
# odhecx_pr_eosdtv_ch_prd_stb_flat_v1 --PR
# odhecx_in_eosdtv_ch_prd_stb_v1  --IN