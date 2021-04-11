# This script gets the data from google drive, and processes it so that i can make nice charts 

import pandas as pd
import csv

url = "https://drive.google.com/file/d/1jEaEJOgCl_1iqRl9N2jBca1evcc7ji7n/view?usp=sharing"
path = 'https://drive.google.com/uc?export=download&id='+url.split('/')[-2]
data1 = pd.read_csv(path,na_values="--")

#data1 = pd.read_csv("/Users/alexandercampbell/OneDrive/Projects/rxcrunning/codes/Garmin_running.csv",na_values="--")

# Remove data 
data1.drop(columns=['Favorite','Flow','Grit','Min Temp','Surface Interval','Decompression','Max Temp','Bottom Time'],inplace=True)

# Format data
data1['Date'] = pd.to_datetime(data1['Date'], format="%d/%m/%Y %H:%M")

# set of variables to adjust time for 
time_vars = ['Time','Best Lap Time','Avg Pace','Best Pace','Climb Time']

data1[time_vars]=data1[time_vars].astype('str')

# remove miliseconds
def foo3(arg):
    if "." in arg:
        return(arg[:-2])
    else:
        return(arg)
data1[time_vars] = data1[time_vars].applymap(lambda x: foo3(x))

# remove end zeros on climb time
def foo4(arg):
    if len(arg)==8:
        return(arg[:-3])
    else:
        return(arg)
data1['Climb Time'] = data1['Climb Time'].map(lambda x: foo4(x))

# express all as hh:mm:ss
def foo2(arg):
    if len(arg) == 5:
        return('00:'+ arg)
    else:
        return(arg)
    
data1[time_vars] = data1[time_vars].applymap(lambda x: foo2(x))

# convert to time delta
for i in time_vars:
    data1[i] = pd.to_datetime(data1[i])
    
# Filter only running 
data1 = data1[data1['Activity Type']=="Running"]

return(data1)