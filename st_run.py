import streamlit as st
import charts
import scraping
import datetime

st.title('Pragues Real Estate prices visualization')
col1, col2 = st.columns(2)
with col1:
    with st.form("my_form"):
        date = st.date_input('Select day', value = datetime.datetime.strptime(
            datetime.datetime.today().strftime('%Y-%m-%d'), "%Y-%m-%d")
                            ).strftime("%Y-%m-%d")
        type = st.selectbox('House or Flat',('house', 'flat'), index = 0)
        # submit button
        submitted = st.form_submit_button("Submit")
    
    if submitted == True:
        
        try:
            st.plotly_chart(charts.selected(date, type))
        except:
            with col2:
                st.info("Don't have required data.")
                st.warning("Don't have required data -> initiating screaping. Data scraping is usefull if todays data is missing.")
                with st.spinner('It might take some time. Go take drink some coffee! OwO'):
                    scraping.RE(type)
                st.success('Scraping is succesfully finished! Resubmit to see result.')
                     


   
#                with st.form("my-form"):
#                    question = st.selectbox("We don't have todays data. Do you want to initiate scraping?"
#                                    ,('Yes', 'No'), index = 0)
#                    # submit button
#                    submitted2 = st.form_submit_button("Submit")
#                                               
#                if submitted2 == True and question == 'Yes':
#                    st.header('Map Visualization')
#                    
#                    with st.spinner('It might take some time. Go take drink some coffee! OwO'):
#                        #scraping.RE(type)
#                        time.sleep(5)
#                    st.success('Scraping is succesfully finished! Resubmit to see result.')
#                        
#                elif question == 'No' and submitted2 == True:
#                    st.info('You can resubmit.')                                