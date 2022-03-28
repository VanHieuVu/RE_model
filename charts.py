import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import psycopg2

def selected(date: str, type:str):
    
    conn = psycopg2.connect(
    host = "localhost",
    database = f"{type}",
    user = "postgres",
    password = "1234",
    )
    
    cur = conn.cursor()
    cur.execute(f"""
                SELECT *
                FROM "{date}"
                """
            )
    rows = cur.fetchall()
    l=[]
    for r in rows:
        data = {
        "Distance":float(r[2]),
        "Lat":float(r[4]),
        "Lng":float(r[5]),
        "Price_mSqr":float(r[6])
        }
        l.append(data)
    df = pd.DataFrame(l)
    #df = pd.read_csv(f'C:\PythonProjects\RE_model_env\scraped data\{type}\{date}.csv')
    fig = px.scatter_mapbox(df, lat="Lat", lon="Lng", color="Price_mSqr", 
                            size="Distance", 
                            color_continuous_scale=px.colors.sequential.Bluered, 
                            size_max=30, zoom=10, mapbox_style="carto-positron"
                            )
    
    return(fig)