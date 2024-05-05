import streamlit as st
import pandas as pd
import json
import numpy as np
import pandas as pd

def procesar_fecha(fecha):
    # Esta función puede ser personalizada para procesar la fecha como quieras
    return f"La fecha que ingresaste es: {fecha.strftime('%Y-%m-%d')}"

# Título de la aplicación
st.title('Hey Radar')

# Selector de fecha en la interfaz
fecha_usuario = st.date_input("Elige una fecha:")

# Botón para procesar la fecha
if st.button('Realizar analisis'):
    resultado = procesar_fecha(fecha_usuario)
    st.write(resultado)  # Mostrar el resultado procesado
