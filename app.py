import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd



external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

data1 = pd.read_csv("/Users/alexandercampbell/OneDrive/Projects/rxcrunning/codes/data1.csv",na_values="--")

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

for i in time_vars:
    data1[i] = pd.to_timedelta(data1[i])
    
# Filter only running 
data1 = data1[data1['Activity Type']=="Running"]

fig = px.bar(data1, x="Date", y="Time")

app.layout = html.Div(children=[
    html.H1(children='Roderick Campbell\'s Running Log'),

    dcc.Graph(
        id='example-graph',
        figure=fig
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)