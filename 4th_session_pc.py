import streamlit as st
import requests
with st.sidebar:
    st.write("weather app!")
    st.image("51ZgFK-FbwL._h1_.png")
btn = st.button("click on me for get weather information!")
if btn:
    lat = str(input("enter your latitude: "))
    lon = str(input("enter your longitude: "))
    key = str(input("enter key: "))
    api = f"https://api.weatherbit.io/v2.0/current?lat={lat}&lon={lon}&key={key}&include=minutely"
    response = requests.get(api)
    st.write(response.status_code)
    st.write(response.json())
    