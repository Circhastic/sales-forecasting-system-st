import streamlit as st
import pandas as pd
from modules import *

def main():

  st.set_page_config(
      page_title="Sales Forecasting System",
      page_icon="📈",
      layout="wide",
      initial_sidebar_state="expanded",
  )

  if 'uploaded' not in st.session_state:
    st.session_state.uploaded = 'uploaded'

  # Sidebar Menu
  with st.sidebar:
      uploaded_file = st.file_uploader("Upload your Store Data here (must atleast contain Date and Sale)", type=["csv"])
      err = 0
      if uploaded_file is not None:
        if uploaded_file.type != 'text/csv':
              err = 1
              st.info('Please upload in CSV format only...')

        else: 
          st.success("File uploaded successfully!")
          df = pd.read_csv(uploaded_file, parse_dates=True)

          st.write("Your uploaded data:")
          st.write(df)

          # Data pre-processing
          df = preprocessor.drop(df)
          df = preprocessor.date_format(df)
          preprocessor.merge_sort(df)
          df = preprocessor.group_to_three(df)
          st.session_state.uploaded = True


      with open('sample.csv', 'rb') as f:
         st.download_button("Download our sample CSV", f, file_name='sample.csv')

  # Main Body Dashboard
  st.title("Sales Forecasting Dashboard")
  st.write("Welcome User, start by uploading your file on the left sidebar")

  if (st.session_state.uploaded):
    st.line_chart(df)

    forecast_button_clicked = st.button(
      'Start Forecasting',
      key='forecast_button',
      type="primary",
      disabled=st.session_state.uploaded,
    )

  # if (forecast_button_clicked):
    # TODO call arima here

    # pass

if __name__ == "__main__":
    main()
