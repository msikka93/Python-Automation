#This Script is used to increase the spark core instances
from types import SimpleNamespace
import requests
import tkinter as tk
from tkinter import ttk
from pprint import pprint
from tkinter.messagebox import askyesno

class Alert(tk.Tk):
    def __init__(self,replace_spark_config,job_name):
        super().__init__()
        self.replace_spark_config = replace_spark_config
        self.job_name = job_name
        self.title('Clear Checkpoint Dialog')
        self.geometry('300x150')

        # Confirm button
        confirm_button = ttk.Button(self, text='Update Instances', command=self.confirm)
        confirm_button.pack(expand=True)

    def confirm(self):
        answer = askyesno(title='Confirmation',
                          message='Are you sure that you want to change the number of spark core instances?')
        if answer:
            self.destroy()
            Sparkjob.update_spark_instances(self,self.replace_spark_config,self.job_name)

class Sparkjob:

    def update_spark_instances(self,replace_spark_config,job_name):
        try:
            payload = {"cmd": replace_spark_config}
            response = requests.put("http://odh.lgi.io/marathon/v2/apps//metrics/{0}".format(job_name),
                            json=payload,
                            auth=('odhuser', 'password'))
            if response.status_code == 200:
                pprint(response.json())
            else:
                print('Something went wrong')
        except:
            print("Something went wrong while getting the response")


    def check_spark_core_instances(self):
        while True:
            try:
                spark_config = self.get_spark_properties()
                spark_core_cmd = spark_config.spark_core_cmd
                job_name = spark_config.job_name
                no_of_instance = input("Enter the no of instances :-")
                if not no_of_instance:
                    raise ValueError('Spark instances are not defined')
                if not no_of_instance.isdigit():
                    raise ValueError('Spark instances must be a number.')
                list_spark_config = list(spark_core_cmd.split(' '))
                for spark_cores in list_spark_config:
                    if "spark.cores.max=" in spark_cores:
                        spark_cores_retrieved = spark_cores[spark_cores.find("spark.cores.max"):]
                        if spark_cores_retrieved:
                            newSparkCores = "{}{}".format(spark_cores_retrieved[0: 16], no_of_instance)
                            list_replaced_spark_config = [s.replace(spark_cores_retrieved, newSparkCores) for s in list_spark_config]
                            replace_spark_config = ' '.join(list_replaced_spark_config).rstrip()
                            alert = Alert(replace_spark_config,job_name)
                            alert.mainloop()
                break
            except ValueError as e:
                    print("Sorry, I didn't understand that.", e)
                    continue
            except:
                print("Something went wrong while getting the response")




    def get_spark_properties(self):
        while True:
            try:
                job_name = input("Enter the spark job name :-")
                if not job_name:
                    raise ValueError('Job name is not defined')

                response = requests.get("http://odh.lgi.io/marathon/v2/apps//metrics/{0}".format(job_name),
                                        auth=('odhuser', 'password'))
                data = response.json()
                spark_core_cmd = data['app']['cmd']
                obj = SimpleNamespace()
                obj.spark_core_cmd = spark_core_cmd
                obj.job_name = job_name
                return obj
                break
            except ValueError as e:
                print("Sorry, I didn't understand that.", e)
                continue
            except:
                print("Something went wrong while getting the response")

s = Sparkjob()
s.check_spark_core_instances()
#eosstb-metrics-v2-gbpre