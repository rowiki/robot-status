#!/bin/python3

from kubernetes import client
from kubernetes.config import kube_config
from kubernetes.client.configuration import Configuration
import os
import pywikibot
from pprint import pprint

TL_NAME = "Stare robot"

TL_PARAMS = [
	"nume",
	"tip",
	"ultima_rulare"
]

STATUS_PAGE = "Wikipedia:Robot/Stare"

def main():

	try:
		output = "__NOTOC__\n"
		config = Configuration()
		kube_config.load_kube_config(config_file="/data/project/patrocle/.kube/config", client_configuration=config)
		Configuration.set_default(config)

		k8s_client = client.api_client.ApiClient(configuration=config)
		v1 = client.BatchV1Api(api_client=k8s_client)

		ret = v1.list_namespaced_job(namespace="tool-patrocle")
		for i in range(len(ret.items)):
			cron_vals = ['','','']
			cron_vals[0] = ret.items[i].metadata.name
			cron_vals[1] = "normal"

			start_time = ret.items[i].status.start_time
			if start_time != None:
				cron_vals[2] += str(start_time)

			active = ret.items[i].status.active
			if active != 1:
				cron_vals[2] += " (oprit)"
			
			output += "{{" + TL_NAME
			for index in range(len(TL_PARAMS)):
				output += " | " + TL_PARAMS[index] + "=" + cron_vals[index]
			output += "}}\n"
	
		ret = v1.list_namespaced_cron_job(namespace="tool-patrocle")

		for i in range(len(ret.items)):
			cron_vals = ['','','']
			cron_vals[0] = ret.items[i].spec.job_template.spec.template.spec.containers[0].name
			cron_vals[1] = "periodic ([[Cron#Configurare|ajutor]]): " + ret.items[i].spec.schedule
			cron_vals[2] = str(ret.items[i].status.last_schedule_time)

			output += "{{" + TL_NAME
			for index in range(len(TL_PARAMS)):
				output += " | " + TL_PARAMS[index] + "=" + cron_vals[index]
			output += "}}\n"

		print(output)

		page = pywikibot.Page(pywikibot.Site(), STATUS_PAGE)
		page.put(output)
	except Exception as e:
		print("Error: ", e)
if __name__ == "__main__":
	main()
