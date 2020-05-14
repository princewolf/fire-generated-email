import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from string import Template
import os
from datetime import date

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

import fire

def id_send(file_path="data_input/data.csv", id=['936','1178']):

fb = pd.read_csv(file_path, parse_dates=[1,2])
campaigns = fb[fb['campaign_id'].isin(id)]
campaigns = campaigns[campaigns.spent > 0]
    
    
grouped = campaigns.groupby(by=['campaign_id', 'age', 'reporting_start'], as_index=False)['total_conversion'].sum()

 fig = plt.figure(1, figsize=(15,6))
    
# Iterate to create 1 plot campaign at a time
  for i, campaign in enumerate(grouped.campaign_id.unique()):
    plt.subplot(1, len(id), i+1)
    
    df = grouped[grouped['campaign_id'] == campaign].loc[:,['age', 'reporting_start', 'total_conversion']]
    df['reporting_start'] = df['reporting_start'].dt.date
    pivot = df.pivot(index='age', columns='reporting_start', values='total_conversion').fillna(0)
    pivot.plot.bar(ax=plt.gca())

  fig.suptitle('Campaign Conversion per Age Group', fontsize=20)
  fig.autofmt_xdate()

  # Save file to plot folder
  imagename = 'plot/'+date.today().strftime(format="%d %b %Y")+'.png'
  fig.savefig(imagename)
  return(imagename)