#!/usr/bin/python3.5
from App import scrape
from App import db

from datetime import datetime as dt
import logging
import os
from concurrent.futures import ThreadPoolExecutor


log_file = os.path.join(os.getcwd(),'App/info.log')
logging.basicConfig(filename=log_file,level=logging.INFO)

begin = dt.today()
init = scrape.scrape_class()
init.run()

jobs = []

def get_jobs(key):
	jobs = init._get_company_jobs(key)
	print(jobs)
	return jobs

def handle_result(result):
	jobs.append(result.result())


with ThreadPoolExecutor(max_workers=8) as pool:
	for key in list(init.companies.keys())[:10]:
		_ = pool.submit(get_jobs,key)
		_.add_done_callback(handle_result)

count = 0
duplicates = 0

for company in jobs:
	for job in company:
		count += 1
		j = db.Jobs(id=job[0]
				,company=job[1]
				,title=job[2]
				,date_created=job[3]
				,category=job[4]
				)
		db.session.add(j)
		try:
			db.session.commit()
			print("add: "+ str(job))
		except db.exc.IntegrityError:
			db.session.rollback()
			print("duplicate: "+ str(job))
			duplicates += 1

end = dt.today()

print("Process complete")
print("New jobs: {0}/{1}".format(str(count - duplicates), str(count)))
print("Time taken: " + str(end-begin))

logging.info("{} - Process Complete".format(dt.today()))
logging.info("{} - Total jobs - {}".format(dt.today(), str(count)))
logging.info("{} - New jobs - {}".format(dt.today(), str(count-duplicates)))
logging.info("{} - Time taken - {}".format(dt.today(), str(end-begin)))