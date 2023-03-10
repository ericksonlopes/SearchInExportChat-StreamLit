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

st.title('Messages')
df_messages = pd.DataFrame([m.__dict__ for m in base.messages])
st.write(df_messages)

st.title('Info Messages')
df_info_messages = pd.DataFrame([m.__dict__ for m in base.info_messages])
st.write(df_info_messages)

st.title('Quantidade de mensagens por dia')
# Transforma a coluna date em datetime
df_messages['date'] = pd.to_datetime(df_messages['date'])
# Cria uma nova coluna com a data sem a hora
df_messages["newdate"] = df_messages.apply(lambda x: x['date'].date(), axis=1)
# Agrupa as mensagens por data e conta a quantidade de mensagens
df_messages['newdate'] = pd.to_datetime(df_messages['newdate'])
# Cria um novo dataframe com a soma das mensagens por dia
df_soma = df_messages.groupby('newdate')['message'].count().reset_index()
# Mostra o gráfico
st.dataframe(df_soma)
st.line_chart(df_soma, x='newdate', y='message')
