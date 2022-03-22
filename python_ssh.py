import paramiko
import sys
results = []

def ssh_conn():
        try:
                client = paramiko.SSHClient()
                client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                client.load_system_host_keys()
                #hostname = input("Enter the hostname:-")
                # if not hostname:
                #         raise ValueError('Hostname is not defined')
                # sshpath=input("Enter the path to your ssh key:-")
                # if not sshpath:
                #         raise ValueError('SSH Path is not defined')
                # user=input("Enter the username:-")
                # if not user:
                #         raise ValueError('Username is not defined')
                k = paramiko.RSAKey.from_private_key_file('C:/Users/gaurav.sikka01/.ssh/opensshkey')
                client.connect('172.16.100.217',port=22, username='gsikka', pkey=k)
                ssh_stdin, ssh_stdout, ssh_stderr = client.exec_command('ls -al; ls -l')

        except IOError as e:
                print("Invalid input",e)
        except ValueError as e:
                print(e)
        except paramiko.SSHException as sshException:
                print("Unable to establish SSH connection: %s" % sshException)
        except paramiko.AuthenticationException:
                print("Authentication Error!!")
        except:
                print("Unexpected error:", sys.exc_info()[0])
                raise
        else:
                for line in ssh_stdout:
                        results.append(line.strip('\n'))

ssh_conn()

for i in results:
        print(i.strip())

sys.exit()

#172.16.100.217

#C:/Users/gaurav.sikka01/.ssh/opensshkey