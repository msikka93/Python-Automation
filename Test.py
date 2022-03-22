# #
# # import paramiko
# #
# # class SshClient:
# #     "A wrapper of paramiko.SSHClient"
# #     TIMEOUT = 4
# #
# #     def __init__(self, host, port, username, key=None):
# #         self.username = username
# #         self.client = paramiko.SSHClient()
# #         self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# #         if key is not None:
# #             key = paramiko.RSAKey.from_private_key_file('C:/Users/gaurav.sikka01/.ssh/opensshkey')
# #         self.client.connect(host, port, username=username, pkey=key, timeout=self.TIMEOUT)
# #
# #     def close(self):
# #         if self.client is not None:
# #             self.client.close()
# #             self.client = None
# #
# #     def execute(self, command, sudo=False):
# #         feed_password = False
# #         if sudo and self.username != "root":
# #             command = "sudo -S -p '' %s" % command
# #         stdin, stdout, stderr = self.client.exec_command(command)
# #
# #         return {'out': stdout.readlines(),
# #                 'err': stderr.readlines(),
# #                 'retval': stdout.channel.recv_exit_status()}
# #
# # if __name__ == "__main__":
# #     client = SshClient(host='172.31.101.116', port=22, username='gsikka', key='C:/Users/gaurav.sikka01/.ssh/opensshkey')
# #     try:
# #        cmd = 'docker exec -it hdfs-datanode hdfs dfs -cat hdfs:///processing-conf/spark_eosdtv_eosstb_eosstb_streamparser_nl-conf.yml-e1bbecf6a60aebc1ccce65d237cf05ee.yml'
# #        ret = client.execute(cmd, sudo=True)
# #        print ("  ".join(ret["out"]), "  E ".join(ret["err"]), ret["retval"])
# #     finally:
# #       client.close()
#
# import requests
# from pprint import pprint
#
# # def test():
# #     while True:
# #         try:
# #             spark_job_name = input("Enter the spark job name :-")
# #             if not spark_job_name:
# #                 raise ValueError('Spark Job name is not defined')
# #
# #             response = requests.get("http://odh.lgi.io/marathon/v2/apps//metrics/{0}".format(spark_job_name),
# #                                     auth=('odhuser', 'password'))
# #             data = response.json()
# #             responseData = data['app']['cmd']
# #             pprint(response.json())
# #             print(responseData.split(' ')[-5])
# #             break
# #         except ValueError as e:
# #             print("Sorry, I didn't understand that.", e)
# #             continue
# #         except:
# #             print("Something went wrong while getting the response")
# # test()
#
# def test():
#     payload = {"instances": '3'}
#     response = requests.put("http://odh.lgi.io/marathon/v2/apps//kafka-es6/es6-thinkanalytics-parsing-v2-hu", json=payload,
#                             auth=('odhuser', 'password'))
#     if response.status_code == 200:
#         pprint(response.json())
#     else:
#         print('error')
#
# test()
def droppedRequest(requestTime):

    dropped = 0
	# this is to keep track of any of the element that is already dropped due to any of 3 limit violation.
    already_dropped = {}

    for i in range(len(requestTime)):
        if i > 2 and requestTime[i] == requestTime[i-3]:
            if requestTime[i] not in already_dropped or already_dropped[requestTime[i]] != i:
                already_dropped[requestTime[i]] = i
                dropped += 1
                print(i, requestTime[i])

        elif i > 19 and requestTime[i] - requestTime[i-20] < 10:
            if requestTime[i] not in already_dropped or already_dropped[requestTime[i]] != i:
                already_dropped[requestTime[i]] = i
                dropped += 1
                print(i, requestTime[i])

        elif i > 59 and requestTime[i] - requestTime[i-60] < 60:
            if requestTime[i] not in already_dropped or already_dropped[requestTime[i]] != i:
                already_dropped[requestTime[i]] = i
                dropped += 1
                print(i, requestTime[i])

    return dropped
a=droppedRequest('1200')
print(a)