from socket import error as socket_error
from fabric import Connection,Config
from paramiko.ssh_exception import AuthenticationException


class ExampleException(Exception):
    pass


class Host(object):
    def __init__(self,
                 host_ip,
                 username,
                 key_file_path):
        self.host_ip = host_ip
        self.username = username
        self.key_file_path = key_file_path

    def _get_connection(self):
        connect_kwargs = {'key_filename': self.key_file_path}
        config = Config(overrides={'sudo': {'user': 'root'}})
        return Connection(host=self.host_ip, user=self.username, port=22,
                          connect_kwargs=connect_kwargs, config=config)

    def get_sub_option(self,kafka_topic):
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

    def get_sub_option_2(self,kafka_topic):
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

    def get_sub_option_3(self,kafka_topic):
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

    def get_sub_option_4(self,kafka_topic):
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

    def get_sub_option_5(self,kafka_topic):
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

    def numbers_to_strings(self,argument, kafka_topic):
        switcher = {
            0: lambda: f'kafkacat -b 172.16.100.217:9092 -e -C -t {kafka_topic} -o -10 | grep timestamp',
            1: lambda: f'kafkacat -b 172.16.100.217:9092 -e -C -t {kafka_topic} -o beginning | grep timestamp',
            2: lambda: self.get_sub_option(kafka_topic),
            3: lambda: f'kafkactl get topic {kafka_topic} --describe --lag',
            4: lambda: f'kafkacat -b 172.16.100.217:9092 -e -C -t {kafka_topic} -o -10 | grep ts',
            5: lambda: self.get_sub_option_2(kafka_topic),
            6: lambda: f'kafkacat -b 172.16.100.217:9092 -e -C -t {kafka_topic} -o -10',
            7: lambda: f'kafkacat -b 172.16.100.217:9092 -e -C -t {kafka_topic} -o beginning',
            8: lambda: self.get_sub_option_3(kafka_topic),
            9: lambda: self.get_sub_option_4(kafka_topic),
            10: lambda: self.get_sub_option_5(kafka_topic)
        }
        return switcher.get(argument, lambda: "Incorrect Option")()

    def run_command(self, command):
        try:
            with self._get_connection() as connection:
                print('Running `{0}` on {1}'.format(command, self.host_ip))
                result = connection.run(command, warn=True, hide='stderr')
        except (socket_error, AuthenticationException) as exc:
            self._raise_authentication_err(exc)

        if result.failed:
            raise ExampleException(
                'The command `{0}` on host {1} failed with the error: '
                '{2}'.format(command, self.host_ip, str(result.stderr)))

    def docker_command(self):
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
                cmd = self.numbers_to_strings(option, kafka_topic)
                print("Result:", cmd)
                if cmd != "Incorrect Option":
                    self.run_command("echo '{0}' | sudo su".format(cmd))  # Classic

                else:
                    continue
                break
            except ValueError as e:
                print("Sorry, I didn't understand that.", e)
                break
            except:
                print("Something went wrong while getting respinse for this kafka topic")

    def put_file(self, local_path, remote_path):
        try:
            with self._get_connection() as connection:
                print('Copying {0} to {1} on host {2}'.format(
                    local_path, remote_path, self.host_ip))
                connection.put(local_path, remote_path)
        except (socket_error, AuthenticationException) as exc:
            self._raise_authentication_err(exc)

    def _raise_authentication_err(self, exc):
        raise ExampleException(
            "SSH: could not connect to {host} "
            "(username: {user}, key: {key}): {exc}".format(
                host=self.host_ip, user=self.username,
                key=self.key_file_path, exc=exc))


if __name__ == '__main__':
    remote_host = Host(host_ip='172.16.100.217',
                       username='gsikka',
                       key_file_path='C:/Users/gaurav.sikka01/.ssh/opensshkey')
    remote_host.docker_command()
    # remote_host.run_command("echo 'kafkacat -b 172.16.100.217:9092 -e -C -t odhecx_pr_eosdtv_gb_prd_heapp_uservices_log_v2 -o -1000' | sudo su")  # Classic
