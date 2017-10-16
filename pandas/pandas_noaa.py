#based on a course I got at DataCamp.com "pandas Foundations"
#pandas time series manipulation, data prep
#pandas_noaa.py

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from urllib.request import urlopen
#for passing string to pandas as if IO
from io import StringIO

url = ('https://www1.ncdc.noaa.gov/pub/data/uscrn/products/'+
	'hourly02/2011/CRNH0203-2011-TX_Austin_33_NW.txt')

documentation = ('https://www1.ncdc.noaa.gov/pub/data/uscrn/products/hourly02/README.txt')

raw_data = urlopen(url)

#I don't want to manually make the column names so I'm taking the column names
#out of the raw documentation
doc_data = urlopen(documentation)
#cast to string cause it's in bytes and I want to use string methods
doc_str = str(doc_data.read())
#where the labels start and end in the documentation
start = doc_str.find('1    WBANNO                         XXXXX')
end = (doc_str.find('38   SOIL_TEMP_100                  Celsius')+
	len('38   SOIL_TEMP_100                  Celsius'))
doc_str=doc_str[start:end]
#it puts literally '\n' instead of actually seperating the lines, so replace works well
doc_str = doc_str.replace('\\n','\n')
#pandas doesn't like strings, so change it to IO data, it's seperated by differing amount
#white spaces, so set it to true, and we are only conerned about the middle one for labels
col_names = pd.read_table(StringIO(doc_str),header=None, delim_whitespace=True).iloc[:,1]

print('*'*60+'\n',col_names)

#the data is again white space seperated, no header
#but I grabbed the col names from the documentation
#since I intend on converting date seperated time and dates to datetime objects
#I'll read them in as strings, not integers
df = pd.read_csv(raw_data, header=None, names=col_names, delim_whitespace=True,
	converters={'UTC_DATE':str,'UTC_TIME':str,'LST_DATE':str,'LST_TIME':str}, na_values='-9999.0')

print('*'*60+'\n',df.head())

#so you can see we've made a readable dataframe now yet there is still much to do
#for one we should combine the date and time into one column and set it as the index
#and second there are a lot of columns with the exact same information in it
#while some of this information would be useful if I was working with all the datasets
#for NOAA, in this particular case I don't need some of this stuff

#get rid of station number, we know It's Austin, TX
#get rid of soil temperature below 10cm, there is no data for any of these
df = df.iloc[:,1:35]
print('*'*60+'\n',df.info())

#next up it the date problem
#since I read them in as strings, I just have to combine them now
index = pd.to_datetime(df.UTC_DATE + df.UTC_TIME)
df.LST_DATE = pd.to_datetime(df.LST_DATE + df.LST_TIME)
df.index = index
df = df.drop(['UTC_TIME','LST_TIME','LONGITUDE','LATITUDE','CRX_VN'], axis=1)
print('*'*60+'\n',df.info())

