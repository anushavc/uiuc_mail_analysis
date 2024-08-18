"""
Script to do text preprocessing on the mail records
"""

#Importing required libraries
import re
import pandas as pd
from datetime import datetime


def mail_content_processing(text):
    """
    pre-processes the given text input

    Args:
        text (str): input mail text 

    Returns:
        processed_text (str): text after preprocessing
    """
    try:
        if text is None:
            return "Empty Content"
        processed_text = text.lower()
        processed_text = re.sub(r'[^\w\s]', '', processed_text)
        processed_text = re.sub(r'\d+', '', processed_text)
        processed_text = re.sub(r'http\S+|www\S+|@\S+', '', processed_text)
        processed_text = ' '.join(processed_text.split())
        return processed_text
    except Exception as e:
        return "String Error"

def convert_date(date_str):
    """
    extracts the date details from the given date string

    Args:
        date_str (str): input mail text 

    Returns:
        year (str): the extracted year
        month (str): the extracted month
        day (str): the extracted day
        day_name (str): the extracted day of the week
    """
    try:
        date_obj = datetime.strptime(date_str, '%a %b %d %Y').date()
        year= date_obj.strftime('%Y')
        month= date_obj.strftime('%b')
        day = date_obj.strftime('%d')
        day_name = date_obj.strftime('%A')
        return year, month, day, day_name
    except ValueError:
        return "Unknown Year","Unknown Month","Unknown Day","Unknown Day of Week"

file_path = 'massmail_system.csv'
df = pd.read_csv(file_path)

df['day'] = None 
df['year']= None
df['month']=None
df['day_of_week']=None

df[['year','month','day','day_of_week']] = df['date'].apply(lambda x: pd.Series(convert_date(x)))
df = df.drop(columns=['header','date'])

df['content'] = df['content'].apply(mail_content_processing)
df['subject'] = df['subject'].apply(mail_content_processing)
df.to_csv('processed_massmail_system.csv', index=False)



