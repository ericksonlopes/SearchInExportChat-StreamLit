import pandas as pd
import streamlit as st

from clear_file import BaseClearDataFile

data = st.file_uploader('Escolha o arquivo', type=['txt'])

if data is not None:
    file = data.getvalue().decode("utf-8").split("\n")
    base = BaseClearDataFile(file_data=file)

    df = pd.DataFrame([m.__dict__ for m in base.messages])

    st.write(df)
