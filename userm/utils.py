import matplotlib
import matplotlib.pyplot as plt
import geopandas as gpd
import plotly.express as px
import pandas as pd

def get_graph()
    countries_path = r'/home/yeahpoy/Kylieeee/112&105/pizza_hut_locations.csv'
    df = pd.read_csv(countries_path)

    df_geo = gpd.GeoDataFrame(df, geometry = gpd.points_from_xy(df.longitude, df.latitude))

    #get built in dataset from geopandas
    world_data = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

    #plot world map
    axis = world_data[world_data.continent == 'North America'].plot(
    color = 'lightblue', edgecolor = 'black')

    df_geo.plot(ax =  axis, color = 'black')
    plt.title('Pizza Hut location in US')

    fig = matplotlib.pyplot.gcf()
    fig.set_size_inches(5,7)
    #fig.savefig(matplot.png, dpi = 200)
    
    image = plt.show()