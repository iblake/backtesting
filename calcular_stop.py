
# Import libraries
import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image

import datetime


# F.US.EPZ20.scid_BarData.csv

# Add a tittle and an image
st.title("Título")

st.write("""
# Stock Market Web App
**Aplicacion para calcular el StopLoss mas opmito**
""")

#image = "/home/iblake/backtesting/img/ironman.jpg"
#st.image(image)

# Create a sidebar header
st.sidebar.header("Parámetros para StopLoss")
st.sidebar.subheader("Datos")

# Load DataSet
DATA_URL = ("/home/iblake/backtesting/csv/F.US.EPZ20.scid_BarData.csv")

@st.cache(persist=True)
def load_dataset():
  ''' funtion to load historical ES csv'''
  data = pd.read_csv(DATA_URL, parse_dates=[['Date', 'Time']])
  data.set_index('Date_Time', inplace=True)
  return data

# User Parameters input
def get_user_input():
  start_date = st.sidebar.text_input("Fecha de entrada", "2020/9/09")
#start_time = st.sidebar.time_input("Hora de entrada",datetime.time(8, 45))
  start_time = st.sidebar.text_input("Hora de entrada", "09:00:00")
  enter_price = float(st.sidebar.text_input("Precion de Entrada", "3371.50"))
  stop_loss = float(st.sidebar.text_input("Stop Losses", "4"))
  long_sort = st.sidebar.radio('Dirección', ('Long','Short'))
  return start_date, start_time, enter_price, stop_loss, long_sort

########################################################################################################################
########################################################################################################################


future_mes = load_dataset()
start_date, start_time, enter_price, stop_loss, long_sort = get_user_input()

# dataframe with the time slice for best stop_loss calculation
date_time_trade = start_date + ' ' + start_time
end_day = start_date + ' ' + "15:01:00"
date_time_trade = pd.to_datetime(date_time_trade)
end_day = pd.to_datetime(end_day)
# Filter
mask = (future_mes.index >= date_time_trade) & (future_mes.index < end_day)
time_slice = future_mes[mask]

for index, prices in time_slice.iterrows():
  price_high = int(prices['High'])
  price_low = int(prices['Low'])
  out_price = enter_price - stop_loss

  if long_sort == "Long" and out_price > price_low:
    st.write("Stop loss tocado {} StopLoss: {} Max: {} Min: {}".format(index,out_price,price_high,price_low))
    status = 1
    break
  else:
    status = 0

  if long_sort == "short" and out_price < price_high:
    st.write("Stop loss tocado {} StopLoss: {} Max: {} Min: {}".format(index,out_price,price_high,price_low))
    status = 1
    break
  else:
    status = 0


#st.dataframe(time_slice)
#st.write(stop_loss)

