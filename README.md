# bsjscraper

This script scrapes job data from berlinstartupjobs.com into a database. 
Before executing, users should declare an environment variable called
'db_local' to store the database address. To execute, run App/app.py 
using python 3.5.

This script demonstrates use of:

- Threading (concurrent.futures module)
- Logging
- SQLalchemy (an ORM tool)
- Requests/BeautifulSoup for parsing html
