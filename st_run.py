from numpy import char
import streamlit as st
import charts
import scraping
import datetime

st.title('Prague Real Estate prices visualization')
with st.form("my_form"):
    date = st.date_input('Select day', value = datetime.datetime.strptime(
        datetime.datetime.today().strftime('%Y-%m-%d'), "%Y-%m-%d")
                         ).strftime("%Y-%m-%d")
    type = st.selectbox('House or Flat',('house', 'flat'), index = 0)
    # submit button
    submitted = st.form_submit_button("Submit")

st.header('Map Visualization')
if submitted == True:

    try:
        st.plotly_chart(charts.selected(date, type))
    except:
        with st.form("my-form"):
            ask = st.selectbox("We don't have data for the day. Do you want to initiate scraping?"
                            ,('Yes', 'No'), index = 0)

            # submit button
            submitted_2 = st.form_submit_button("Submit")
        if submitted_2 == True:
            if ask == 'Yes':
                with st.spinner('It might take some time. Go take drink some coffee! OwO'):
                    scraping.RE(type)
                st.success('Scraping is succesfully finished! Resubmit to see result.')
            else:
                st.info('You can resubmit')