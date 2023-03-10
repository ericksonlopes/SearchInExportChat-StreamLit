import pandas as pd
import streamlit as st

from clear_file import BaseClearDataFile

data = st.file_uploader('Escolha o arquivo para analise de dados', type=['txt'])

if data is None:
    st.stop()

# read file as a string data
file = data.getvalue().decode("utf-8").split("\n")

# clear data
base = BaseClearDataFile(file_data=file)

# show dataframes
st.title('Messages')
df = pd.DataFrame([m.__dict__ for m in base.messages])
st.write(df)

st.title('Info Messages')
df = pd.DataFrame([m.__dict__ for m in base.info_messages])
st.write(df)
