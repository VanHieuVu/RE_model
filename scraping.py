import pandas as pd
import math
import requests
from bs4 import BeautifulSoup
import datetime
import psycopg2



def RE(type):
    url = f'https://www.bezrealitky.com/listings/offer-sale/{type}/praha?project%5B0%5D=0&_token=-HKI6vzp8ntTC6xqEKy6cxISqsYFJ-79TQZcHWtiFUY&submit=1'
    url_ls = [0]
    url_ls_full = [url]


    while url_ls[-1] != 'javascript:void(0)':
    
        r = requests.get(url)
        r.encoding = "UTF-8"
        bs = BeautifulSoup(r.text)
        a = bs.find('ul', {'class':'pagination justify-content-md-end'})


        for a in a.find_all('a', href=True):
            url_ls.append(a['href'])
        url_ls_full.append('https://www.bezrealitky.com' + url_ls[-1])
        url = url_ls_full[-1]
    
    url_ls_full.remove('https://www.bezrealitky.comjavascript:void(0)')

    distances = []
    prices = []
    property_names = []
    space = []
    loc_lat = []
    loc_lng = []
    csv_stanice_metra = pd.read_csv('stanice metra.csv').set_index('Stanice metra')
    
    for m in range(len(url_ls_full)):
        #select url from the page
        r = requests.get(url_ls_full[m])
        r.encoding = "UTF-8"
        bs = BeautifulSoup(r.text)
         
        #each estate on the page
        estate = []
        for i in range(len(bs.find('div', {'class':'b-filter__inner pb-40'}).findAll('a', {'class': 'product__link js-product-link'}))):
            estate.append('https://www.bezrealitky.com' + bs.find('div', {'class':'b-filter__inner pb-40'}).findAll('a', {'class': 'product__link js-product-link'})[i].get('href'))
    
        
        for n in range(len(estate)):
            r = requests.get(estate[n])
            r.encoding = "UTF-8"
            bs = BeautifulSoup(r.text) 

            #list_param = bs.find("div", {"id":"detail-parameters"}).findAll("div",{"class":"row param"})
            list_value = bs.find('div', {'id':'detail-parameters'}).findAll('div',{'class':'param-value'})
            list_title = bs.find('div', {'id':'detail-parameters'}).findAll('div',{'class':'param-title'})
            #Param
            all_value = []
            all_title = []
            for i in range(len(list_value)):
                all_value.append(list_value[i].text.strip())
                all_title.append(list_title[i].text.strip())
            param_df = pd.DataFrame(data = all_value, index = all_title, columns=["Values"])
            param_df.index.names = ["Names"]

            #get prices
            try:
                prices.append(int(param_df.loc['Price'].tolist()[0].replace('CZK', '').replace(',', '')))
            except:
                prices.append(int())
            
            #get spac   
            try:
                space.append(int(param_df.loc['Plot space'].tolist()[0].replace('m²', '').replace(',','')))
            except:
                space.append(int(param_df.loc['Floor Space'].tolist()[0].replace('m²', '').replace(',','')))

            
            #location
            approx_loc_ls = []
            approx_loc = bs.find(class_ = 'col col-12 col-md-8').h2
            approx_loc_ls.append(approx_loc.text.strip())
            param_df.append(pd.DataFrame(approx_loc_ls).rename(columns={0:"Values"}, index={0:"Location"}))
            
            
            link = bs.find("div",{"id":"map"})
            LatLng = [float(link.get("data-lat")), float(link.get("data-lng"))]
            loc_lat.append(LatLng[0])
            loc_lng.append(LatLng[1])
            LatLng_df = pd.DataFrame(LatLng).T.rename(columns = {0:"Latitude", 1:"Longitude"}, index = {0:"Geografical location"})
            
            
            
            list_distances = []
            for i in range(len(csv_stanice_metra)):
                #Středový úhle
                o = math.degrees(math.acos(math.cos(math.radians(90 - csv_stanice_metra.iloc[i, 0]))*math.cos(math.radians(90 - LatLng[0])) + math.sin(math.radians(90 - csv_stanice_metra.iloc[i, 0]))*math.sin(math.radians(90 - LatLng[0]))*math.cos(math.radians(csv_stanice_metra.iloc[i,1] - LatLng[1]))))
                #délka oblouku
                list_distances.append(o*111.195)


            df_data = pd.DataFrame(list_distances).set_index(csv_stanice_metra.index).rename(columns={0:"vzdálenost_od_nemovitosti"})
            df_data_min = df_data[df_data.vzdálenost_od_nemovitosti == df_data.vzdálenost_od_nemovitosti.min()]

            #property name
            property_names.append(bs.find('div', {'data-element':'detail-title'}).h2.text.strip())#it's acutally the nearest metro station

            #get distance to list
            distances.append(df_data_min.iloc[0]['vzdálenost_od_nemovitosti'])



    # df na grafy a visualizace

    df = pd.DataFrame(list(zip(property_names, prices, distances, space, loc_lat, loc_lng))).rename(columns={0:"Property names", 1:"Prices in CZK", 2:"distance in Km", 3:"Space in m²", 4:"Lat", 5:"Lng"})

    #price in 1 m²
    p1ms =  []
    
    for m in range(len(prices)):
        p1ms.append(prices[m] / space[m])
        
    df['price_for_m²'] = p1ms

    #SAVE DATA IN PG
    date = datetime.datetime.today().strftime('%Y-%m-%d')

    conn = psycopg2.connect(
    host = "localhost",
    database = f"{type}",
    user = "postgres",
    password = "1234",
    )
    #cursor
    cur = conn.cursor()

    #create table
    cur.execute(
                f"""CREATE TABLE "{date}"
                    (
                        Name text NOT NULL,
                        Price bigint NOT NULL,
                        Distance numeric NOT NULL,
                        Space numeric,
                        Lat numeric,
                        Lng numeric,
                        Price_mSqr numeric,
                        PRIMARY KEY (Name)
                    )
                """   
                )
    #conn.commit()
    for i in range(len(df)):
        cur.execute(
            f"""
            INSERT INTO "{date}"(Name, Price, Distance, Space, Lat, Lng, Price_mSqr)
            VALUES ({i+1},{df.iloc[:,1][i]},{df.iloc[:,2][i]},{df.iloc[:,3][i]},{df.iloc[:,4][i]},{df.iloc[:,5][i]}, {df.iloc[:,6][i]})
            
            """
        )
    conn.commit()
    conn.close()
    
    
    return('done')
