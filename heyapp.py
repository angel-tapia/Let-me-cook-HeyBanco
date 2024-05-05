import streamlit as st
import pandas as pd
import json
import numpy as np
import pandas as pd
from datetime import datetime
import openai

import plotly.express as px
from datetime import datetime



def procesar_fecha(fecha):
    # Esta función puede ser personalizada para procesar la fecha como quieras
    return f"La fecha que ingresaste es: {fecha.strftime('%Y-%m-%d')}"

# Título de la aplicación
st.title('Hey Radar')


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

def promptApi(prompt):
  # Set up your OpenAI API key
  api_key = "KEEEEEEEYYYYYY"

  # Initialize the OpenAI client
  client = openai.OpenAI(api_key=api_key)

  # Generate a completion using the GPT-3.5-turbo model
  chat_completion = client.chat.completions.create(
      messages=[{"role": "user", "content": prompt}],
      model="gpt-3.5-turbo"
  )

  # Extract the response
  response = chat_completion.choices[0].message.content

  return response


negativity_scores = {}

for entry in data:
    if '-' in entry["date"]:
        date_format = "%Y-%m-%d"
    else:
        date_format = "%Y-%W-%w"
    date = datetime.strptime(entry["date"], date_format)
    
    negativity = entry["sentiment"]["neg"]
    #positivity = entry["sentiment"]["pos"]

    if date not in negativity_scores:
        negativity_scores[date] = []
    negativity_scores[date].append(negativity)

neg_df = pd.DataFrame.from_dict(negativity_scores, orient='index', columns=['negativity'])



fig = px.line(neg_df, x=neg_df.index, y=['negativity'], title='Sentiment Analysis Time Series')
st.plotly_chart(fig)



fecha_usuario = st.date_input("Select a date", min_value=min(neg_df.index), max_value=max(neg_df.index))


if fecha_usuario in neg_df.index:
    selected_scores = neg_df.loc[fecha_usuario]
    st.write("Negativity Score:", selected_scores['negativity'])
else:
    st.write("No data available for selected date.")

# Botón para procesar la fecha
if st.button('Realizar analisis'):
    resultado = get_data_by_year_and_week(data, fecha_usuario)
    resultado = resultado["contenido"]
    prompt = f"""
    Entre estas dos preguntas decide cual responder:
    1.- ¿Como HeyBanco se relaciona a los demás bancos NuBank, BBVA, Santander y es mejor?
    2.- ¿Como aumentar la ventaja de HeyBanco respecto a los demas bancos que son, NuBank, BBVA, Santandar?
    Tienes que ser muy especifico en tu respuesta, ademas dar contexto.
    
    El formato debe ser:
    Pregunta
    Respuesta
    
    Utiliza esta informacion que es respecto a la fecha {fecha_usuario} para responder. 
    La data es: {resultado}
    """
    st.write(promptApi(prompt))  # Mostrar el resultado procesado``