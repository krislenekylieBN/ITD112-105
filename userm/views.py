#%matplotlib notebook
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from .forms import UserRegisterForm
from django.contrib import messages
import numpy as np
from django.shortcuts import render
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import LinearRegression
from sklearn.metrics import accuracy_score
import geopandas as gpd
import io
import plotly.graph_objects as go


# Create your views here.
def home (request):
    return render (request, "userm/base.html" )

def homepage (request):
    return render (request, "userm/homepage.html" )

def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Hi {username}, your account was created successfully')
            return redirect('homepage')
    else:
        form = UserRegisterForm()

    return render(request, 'userm/register.html', {'form': form})


def project1(request):
    return render(request, "userm/milkQuality.html")

def result(request):

    data = pd.read_csv(r'/home/yeahpoy/Kylieeee/DjangoProject/visproject/userm/static/userm/csv/milk_quality.csv')

    x = data.drop('grade', axis=1)
    y = data['grade']

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.20)

    model = LogisticRegression()
    model.fit(x_train, y_train)

    val1 = float(request.GET['n1'])
    val2 = float(request.GET['n2'])
    val3 = float(request.GET['n3'])
    val4 = float(request.GET['n4'])
    val5 = float(request.GET['n5'])
    val6 = float(request.GET['n6'])
    val7 = float(request.GET['n7'])


    pred = model.predict([[val1,val2,val3,val4,val5,val6,val7]])

    result1 = ""
    if pred == [0]:
        result1 = "Low"
    elif pred == [1]:
        result1 = "Medium"
    else:
        result1 = "High"
    return render(request,"userm/milkQuality.html",{"result2":result1})

def project2(request):
    return render(request, "userm/mobilePrice.html")

def resulta(request):
    data = pd.read_csv(r'/home/yeahpoy/Kylieeee/DjangoProject/visproject/userm/static/userm/csv/Mobile_phone_price.csv')
    data = data.drop(['product_id'], axis=1)
    x = data.drop('price', axis=1)
    y = data['price']
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.20)
    model = LinearRegression()
    model.fit(x_train, y_train)

    kaj1 = float(request.GET['p1'])
    kaj2 = float(request.GET['p2'])
    kaj3 = float(request.GET['p3'])
    kaj4 = float(request.GET['p4'])
    kaj5 = float(request.GET['p5'])
    kaj6 = float(request.GET['p6'])
    kaj7 = float(request.GET['p7'])
    kaj8 = float(request.GET['p8'])

    pred = model.predict(np.array([kaj1,kaj2,kaj3,kaj4,kaj5,kaj6,kaj7,kaj8]).reshape(1,-1))
    pred = round(pred[0])

    price = "The predicted price is $"+str(pred)

    return render(request, "userm/mobilePrice.html", {"resulta": price})


def project3(request):

    location = None
    
    if request.method == 'POST' and 'lugar' in request.POST:

        location = request.POST['lugar']

    # reads the csv file

    dataset = pd.read_csv('/home/yeahpoy/Kylieeee/DjangoProject/visproject/userm/static/userm/csv/dengue-data-2016-2021.csv')
    dataset.rename({'loc': 'location', 'Region': 'region'}, 
                    axis=1, inplace=True)
    dataset.drop(index=dataset.index[0], inplace=True)

    dataset['year'] = dataset['date'].str.split('/', expand=True)[2]
    dataset['year'] = dataset['year'].astype(int)
    dataset['cases'] = dataset['cases'].astype(float)
    dataset['deaths'] = dataset['deaths'].astype(float)

    locations = pd.unique(dataset['location'])

    def get_result(type):
        
        total = {}

        for loc in locations:

            location_df = dataset[dataset['location'] == loc]
            total_result = location_df[type].sum()
            total[loc] = total_result

        sorted_total = sorted(
                total.items(), key=lambda item: item[1], reverse=True)

        return sorted_total

    total_case_locations = get_result('cases')
    total_death_locations = get_result('deaths')

    boards= {
        'board_case': total_case_locations[:10],
        'board_deaths': total_death_locations[:10]
    }
    

    def show_region():
        

        table = pd.DataFrame(columns=['year', 'cases', 'deaths'])
        for year in pd.unique(dataset['year']):
            if location:
                rows = (dataset['year'] == year) & (dataset['location'] == location)
            else:
                rows = (dataset['year'] == year)
            cases = dataset[rows]['cases'].sum()
            deaths = dataset[rows]['deaths'].sum()
            table = table.append(
                {'year': year, 'cases': cases, 'deaths' : deaths},
                ignore_index=True
            )

        sum_of_cases = table['cases'].sum()
        sum_of_deaths = table['deaths'].sum()

        fig = plt.figure()

        plt.plot(table['year'], table['cases'], label='Cases')
        plt.plot(table['year'], table['deaths'], label='Deaths')
        plt.xlabel('Year')
        plt.title(f'Dengue Records Year - 2016 - 2021')
        plt.ylabel('Cases/Deaths')
        plt.legend()

        imgdata = io.StringIO()
        fig.savefig(imgdata, format='svg')
        imgdata.seek(0)

        
        context = {
            'data': imgdata.getvalue(),
            'cases': sum_of_cases,
            'deaths': sum_of_deaths,
            'location': 'Overall' if location is None else location, 
        }

        return context

    context = show_region()
    context['locations'] =  locations



    return render(request, 'userm/dengue.html', {'context': context,'boards': boards})




def project4(request):
    countries_path = r'/home/yeahpoy/Kylieeee/DjangoProject/visproject/userm/static/userm/csv//pizza_hut_locations.csv'
    df = pd.read_csv(countries_path)

    df['text'] = df['type'] + ', ' + df['city']+ ', ' + df['open_hours'] + ', ' + df['postal_code'].astype(str)

    fig = go.Figure(data=go.Scattergeo(
            lon = df['longitude'],
            lat = df['latitude'],
            text = df['text'],
            mode = 'markers',
            marker_color = df['postal_code'],
            ))

    fig.update_layout(
            geo_scope='usa',
            margin=dict(l=0, r=0, b=0, t=0),
            height=500,
        )
    #fig.show()

    # Generate the SVG plot as an HTML div element
    plot_div = fig.to_html(full_html=False, include_plotlyjs='cdn')

    context = {
        'figure': plot_div,
    }
    return render(request, 'userm/geoPlot.html', context)


def project5 (request):

    df = pd.read_csv('/home/yeahpoy/Kylieeee/DjangoProject/visproject/userm/static/userm/csv/global-plastics-production.csv') 
    df.columns = ['Entity','Code','Year','Global plastics production (million tonnes)']
    df_all=df[(df['Year']>1950) & (df['Year'] <2015)]

    fig = px.line(df_all, x="Year", y="Global plastics production (million tonnes)")
    #fig.show()

    # Generate the SVG plot as an HTML div element
    plot_div = fig.to_html(full_html=False, include_plotlyjs='cdn')

    context = {
        'figure': plot_div,
    }
    return render(request, 'userm/plastic.html', context)