import streamlit as st

from clear_file import BaseClearDataFile

data = st.file_uploader('Escolha o arquivo', type=['txt'])

if data is not None:
    base = BaseClearDataFile(file_data=data)

    st.write([m.__dict__ for m in base.messages])
