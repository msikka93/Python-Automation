#This Script is used to increase the logthrash instances in kafka-es6 folder
from types import SimpleNamespace
import requests
import tkinter as tk
from tkinter import ttk
from pprint import pprint
from tkinter.messagebox import askyesno

class Alert(tk.Tk):
    def __init__(self,job_name):
        super().__init__()
        self.job_name = job_name
        self.title('Clear Checkpoint Dialog')
        self.geometry('300x150')

        # Confirm button
        confirm_button = ttk.Button(self, text='Update Instances', command=self.confirm)
        confirm_button.pack(expand=True)

    def confirm(self):
        answer = askyesno(title='Confirmation',
                          message='Are you sure that you want to change the number logthrash instances?')
        if answer:
            self.destroy()
            Logthrash.update_logthrash_instances(self,self.job_name)

class Logthrash:

    def update_logthrash_instances(self,job_name):
        while True:
            try:
                no_of_instance = input("Enter the number logthrash instances :-")
                if not no_of_instance:
                    raise ValueError('Job name is not defined')
                payload = {"instances": int(no_of_instance)}
                response = requests.put("http://odh.lgi.io/marathon/v2/apps//kafka-es6/{0}".format(job_name),
                                json=payload,
                                auth=('odhuser', 'password'))
                if response.status_code == 200:
                    pprint(response.json())
                    print('Logthrash instances have been changed to',no_of_instance)
                else:
                    print('Query failed to run')
                break
            except ValueError as e:
                    print("Sorry, I didn't understand that.", e)
                    continue
            except:
                print("Something went wrong while getting the response")


    def check_logthrash_kafka_instances(self):
        logthrash_config = self.get_logthrash_properties()
        instance = logthrash_config.instances
        print("There are currently {} Logthrash instances for this parsing job.".format(instance))
        alert = Alert(logthrash_config.job_name)
        alert.mainloop()



    def get_logthrash_properties(self):
        while True:
            try:
                job_name = input("Enter the logthrash parsing job name :-")
                if not job_name:
                    raise ValueError('Job name is not defined')

                response = requests.get("http://odh.lgi.io/marathon/v2/apps//kafka-es6/{0}".format(job_name),
                                        auth=('odhuser', 'password'))
                data = response.json()
                no_logthrash_instances = data['app']['instances']
                kafka_topic = data ['app']['args'][1]
                obj = SimpleNamespace()
                obj.instances = no_logthrash_instances
                obj.topic = kafka_topic
                obj.job_name = job_name
                return obj
                break
            except ValueError as e:
                print("Sorry, I didn't understand that.", e)
                continue
            except:
                print("Something went wrong while getting the response")

l = Logthrash()
l.check_logthrash_kafka_instances()
#es6-thinkanalytics-parsing-v2-hu