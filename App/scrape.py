#!/usr/bin/python3.5
import requests
from bs4 import BeautifulSoup as bs
import re
import os
import csv
from datetime import datetime as dt
from time import sleep

BSJ_URL = "http://berlinstartupjobs.com/"

class scrape_class(object):
	def __init__(self):
		self.req_header = {"User-Agent":""}
		self.jobs = []
		self.today = dt.strftime(dt.today(),'%y-%m-%d')

	def run(self):
		self._scrape_url()
		self._get_companies(self.soup)

	def _write_todays_jobs_to_csv(self, jobs, f):
		with open(f,'w+') as write_file:
			csv_write = csv.writer(write_file)
			for job in [job for company in jobs for job in company]:
				job = [item for item in job]
				csv_write.writerow(job)
				print("adding ", job)
		return self

	def _get_company_jobs(self, company):
		jobs = []
		for page in range(1,self._comp_pages(company)+1):
			comp_url = self.companies[company] + "page/{}/".format(page)
			request = requests.get(comp_url, headers=self.req_header)
			soup = bs(request.text, 'html.parser')
			data = soup.find_all('div',id=re.compile("job-[\d]+"))
			for row in data:
				job_id = row.get('id')
				row = row.text.split("\n")
				row = [item for item in row if item not in ['',' ']]
				date = dt.strptime(row[2],'%B %d, %Y')
				date = dt.strftime(date,"%Y-%m-%d")
				jobs.append([job_id, row[1].split(' // ')[0], row[0], date, row[1].split(' // ')[1]])
		return jobs

	def _comp_pages(self, company, page=1):
		# return number of pages of jobs belonging to company
		comp_url = self.companies[company] + "page/{}/".format(page)
		request = requests.get(comp_url, headers=self.req_header)
		soup = bs(request.text, 'html.parser')
		if soup.find_all('link', rel='next'):
			return self._comp_pages(company, page=page+1)
		else:
			return page

	def _get_companies(self, soup_object):
		ret_dict = {}
		soup_companies = soup_object.find_all(class_='w-section companies-container')
		for ref in soup_companies[0].find_all('a'):
			name = ref.text.split(' (')[0]
			ret_dict[name] = ref['href']
		self.companies = ret_dict
		return self

	def _scrape_url(self):
		request = requests.get(BSJ_URL, headers=self.req_header)
		self.soup = bs(request.text, "html.parser")
		return request

if __name__ == '__main__':
	init = scrape_class()
	init._scrape_url()
	init._get_companies(init.soup)
	jobs = init._get_company_jobs("Das Büro am Draht")
	with open('test.txt','w') as wf:
		wfc = csv.writer(wf)
		for row in jobs:
			wfc.writerow(row)