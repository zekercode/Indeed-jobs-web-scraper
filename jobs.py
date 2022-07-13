# 
# Making job searching easier with web scraping
# program that scrapes indeed.com for a role given the url
# creates a csv file for the Company, Title, and Link to the job
#

import requests
from bs4 import BeautifulSoup
import pandas as pd


def extract(page):
    '''
    takes contents from given url from starting point "page" 
    '''

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}
    url = f'https://www.indeed.com/jobs?q=tech+analyst&l=New+York%2C+NY&start={page}'
    r = requests.get(url,headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    return soup


def transform(soup):
    ''' 
    scrapes company, title, and link from each job post and adds it to a dictionary
    '''
    divs = soup.find_all('div', class_ = 'cardOutline' )
    for item in divs:
        company = item.find('span' , class_ = 'companyName').text.strip()
        title = item.find('a').text.strip()
        #links for job postings dont include the site --> so adding in indeed.com
        link = 'http://www.indeed.com'  +  str(item.find( 'h2',{'class' : 'jobTitle'}).find('a')['href'])
        
        job = {
            'Company' : company,
            'Title' : title,
            'Link' : link,
        }
        joblist.append(job)
    return


joblist = []

#loop through first 4 pages of jobs -- step size is 10 because url page size is measured in 10s
for i in range(0, 30, 10):
    c = extract(0)
    transform(c)

df = pd.DataFrame(joblist)

print(df.head())
#create csv file
df.to_csv('jobs.csv')




