import streamlit as st
import charts
import scraping
import datetime

st.title('Prague Real Estate prices visualization')
with st.form("my_form"):
    date = st.date_input('Select day', value = datetime.datetime.strptime("2022-02-28", "%Y-%m-%d")).strftime("%Y-%m-%d")
    type = st.selectbox('House or Flat',('house', 'flat'), index = 0)
    # Every form must have a submit button.
    submitted = st.form_submit_button("Submit")

st.header('Map Visualization')
if submitted == True:

    try:
        st.plotly_chart(charts.selected(date, type))
    except:
        print("Error")
        """    
        print("Scraping started")
        #scraping.RE(type) 
        st.plotly_chart(charts.selected(date, type))
        """    