import pandas as pd
import streamlit as st

from clear_file import BaseClearDataFile

data = st.file_uploader('Escolha o arquivo', type=['txt'])

if data is None:
    st.stop()

file = data.getvalue().decode("utf-8").split("\n")
base = BaseClearDataFile(file_data=file)

st.title('Messages')
df = pd.DataFrame([m.__dict__ for m in base.messages])
st.write(df)

st.title('Info Messages')
df = pd.DataFrame([m.__dict__ for m in base.info_messages])
st.write(df)
