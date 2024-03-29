
# Import libraries
import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image

import datetime

# Add a tittle and an image
st.title("Calcular el StopLoss mas óptimo")


#st.write("""# Stock Market Web App **Aplicacion para calcular el StopLoss mas optimo**""")

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
  market = st.sidebar.selectbox("Mercado",['Futuro SP500','Futuro Nasdaq 100'])
  start_date = st.sidebar.text_input("Fecha de entrada", "2020/9/09")
#start_time = st.sidebar.time_input("Hora de entrada",datetime.time(8, 45))
  start_time = st.sidebar.text_input("Hora de entrada", "09:00:00")
  enter_price = float(st.sidebar.text_input("Precio de Entrada", "3381.25"))
  stop_loss = float(st.sidebar.text_input("Stop Losses", "4"))
  long_sort = st.sidebar.radio('Dirección', ('Long','Short'))
  return start_date, start_time, enter_price, stop_loss, long_sort

########################################################################################################################
#############################     MAIN     #############################################################################
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
#TODO Poner mejor que el if vaya antes de for, así no tendrá que evaluar dos veces todas las iteraciones y mejorará el rendimiento
  price_high = int(prices['High'])
  price_low = int(prices['Low'])
  out_price = enter_price - stop_loss

  if long_sort == "Long" and out_price > price_low:
    status = 1
    break
  else:
    status = 0

  if long_sort == "short" and out_price < price_high:
    status = 1
    break
  else:
    status = 0

if status == 1:
  st.write("""*Stop loss Tocado:* {} - {}""".format(index,out_price))
  st.write("Precio Max alcanzado: {} Mínimo precio alcanzado: {}".format(price_high,price_low))
else:
  st.write()
  st.write("""### *Stop loss no tocado:* {}""".format(out_price))
  st.write()



st.dataframe(time_slice[['Last','Volume']])
st.line_chart(time_slice[['Last','Volume']])

