import streamlit as st
import pandas as pd
import json
import numpy as np
import pandas as pd
from datetime import datetime


def procesar_fecha(fecha):
    # Esta función puede ser personalizada para procesar la fecha como quieras
    return f"La fecha que ingresaste es: {fecha.strftime('%Y-%m-%d')}"

# Título de la aplicación
st.title('Hey Radar')

# Selector de fecha en la interfaz
fecha_usuario = st.date_input("Elige una fecha:")


with open("grouped_data.json", "r") as f:
  data = json.load(f)

def get_week_number(date_string):
    # Parse the date string into a datetime object
    target_date = datetime.strptime(date_string, "%Y-%m-%d")
    
    # Calculate the week number using the isocalendar() method
    week_number = target_date.isocalendar()[1]
    
    return week_number

def get_data_by_year_and_week(json_array, entrada):
    entrada = entrada.strftime('%Y-%m-%d')
    year = entrada[:4]
    week = get_week_number(entrada)

    year = int(year)
    week = int(week)

    for entry in json_array:
        if entry["year"] == year and entry["week"] == week:
            return entry
    return None


# Botón para procesar la fecha
if st.button('Realizar analisis'):
    resultado = get_data_by_year_and_week(data, fecha_usuario)
    st.write(resultado)  # Mostrar el resultado procesado