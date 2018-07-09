# This code cause issue and the IP will be banned by mvnrepository.com
# DO NOT USE
import requests
import logging
import csv
from bs4 import BeautifulSoup
import time

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

http_proxy = "http://localhost:8123"
https_proxy = "https://localhost:8123"

proxyDict = {
              "http": http_proxy,
              "https": https_proxy,
            }

# https://mvnrepository.com/artifact/<groupid>/<artifactid>/<version>
base_url = 'https://mvnrepository.com/artifact/{0}/{1}/{2}'
groupid = []
artifactid = []
version = []

with open('report.txt', 'r') as f:
    reader = csv.reader(f, delimiter='|')
    next(reader)
    for row in reader:
        groupid.append(row[0])
        artifactid.append(row[1])
        version.append(row[2])

with open('/tmp/report_output.txt', 'w+') as outfile:
    for i in range(0, len(groupid)):
        time.sleep(10)
        response = requests.get(base_url.format(groupid[i], artifactid[i], version[i]), proxies=proxyDict)
        soup = BeautifulSoup(response.content, "html.parser")
        for tab in soup.findAll('table'):
            if tab.th.get_text() == 'License':
                logger.info(len(tab.td))
                outLic = ''
                if(len(tab.td) == 0):
                    outLic = 'No License'
                elif(len(tab.td) == 1):
                    outLic = tab.td.get_text()
                else:
                    for license in tab.td:
                        outLic = outLic + license.get_text() + ', '
                outfile.write(groupid[i] + '|' + artifactid[i] + '|' + version[i] + '|' + outLic + '\n')
                break
