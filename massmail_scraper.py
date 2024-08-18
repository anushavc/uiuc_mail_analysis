"""
Script to scrape the massmail archives from https://massmail.illinois.edu/citesMassmailArchive/index.html using using BeautifulSoup
"""

#Importing required libraries
from bs4 import BeautifulSoup 
import requests
from datetime import datetime
import csv

#defining the url of the massmail website
url = 'https://massmail.illinois.edu/citesMassmailArchive/index.html'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

mail_records=[]

def mail_content_extract(link):
    """
    extracts the header and the body of the mail 

    Args:
        link (str): individual html link of the mail

    Returns:
        main_desc (str): the header of the mail
        mail_content (str): the body of the mail
    """
    response = requests.get("https://massmail.illinois.edu/citesMassmailArchive/"+str(link))
    page_content = response.content
    individual_page_soup = BeautifulSoup(page_content, 'html.parser')
    mail_content= individual_page_soup.find('xmp').get_text() or 'No body' 
    mail_desc= individual_page_soup.find('b').get_text() or 'No Header'
    return mail_desc,mail_content

#Creating the csv file
with open('massmail_system.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['date','mailing_tag_no','header','content','subject'])

#Extracting mail details
table_rows= soup.find_all('tr')
for tr in table_rows[1:]:
    mail_no_a_tag= tr.find('a')
    mail_no=mail_no_a_tag.get_text() or 'No Mail Tag'
    mail_desc,mail_content=mail_content_extract(mail_no_a_tag['href'])
    subject=tr.find(lambda tag: tag.name == 'td' and tag.get('align') == 'LEFT').get_text() or 'No Subject'
    date = tr.find(lambda tag: tag.name == 'td' and tag.get('align') == 'RIGHT').get_text() or 'Unknown Date'
    mail_records.append([date, mail_no, mail_desc, mail_content, subject])
    
#Writing mail records data to the csv file
with open('massmail_system.csv', mode='a', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerows(mail_records)