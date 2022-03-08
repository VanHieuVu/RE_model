import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def selected(date: str, type:str):
    
    df = pd.read_csv(f'C:\PythonProjects\RE_model_env\scraped data\{type}\{date}.csv')
    fig = px.scatter_mapbox(df, lat="Lat", lon="Lng", color="price_for_m²", 
                            size="distance in Km", 
                            color_continuous_scale=px.colors.sequential.Bluered, 
                            size_max=30, zoom=10, mapbox_style="carto-positron", hover_data=['Property names']
                            )
    
    return(fig)