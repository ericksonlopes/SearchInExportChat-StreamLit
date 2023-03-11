import pandas as pd
import plotly.express as px
import streamlit as st

from src.clear_file import BaseClearDataFile

data = st.file_uploader('Escolha o arquivo para analise de dados', type=['txt'])

if data is None:
    st.stop()

# read file as a string data
file = data.getvalue().decode("utf-8").split("\n")

# clear data
base = BaseClearDataFile(file_data=file)

st.title('Messages')
df_messages = pd.DataFrame([m.__dict__ for m in base.messages])
st.dataframe(df_messages, use_container_width=True)

st.title('Info Messages')
df_info_messages = pd.DataFrame([m.__dict__ for m in base.info_messages])
st.dataframe(df_info_messages, use_container_width=True)

st.title('Quantidade de mensagens por dia')
# Transforma a coluna date em datetime
df_messages['date'] = pd.to_datetime(df_messages['date'])
# Cria uma nova coluna com a data sem a hora
df_messages["newdate"] = df_messages.apply(lambda x: x['date'].date(), axis=1)
# Agrupa as mensagens por data e conta a quantidade de mensagens
df_messages['newdate'] = pd.to_datetime(df_messages['newdate'])
# Cria um novo dataframe com a soma das mensagens por dia
df_soma = df_messages.groupby('newdate')['message'].count().reset_index()
# Renomeia as colunas
df_soma.rename(columns={'newdate': 'Data', 'message': 'Quantidade de mensagens'}, inplace=True)
# Cria o gráfico
st.bar_chart(df_soma, x='Data', y='Quantidade de mensagens', use_container_width=True)

st.title('Quantidade de mensagens por pessoa')
st.markdown(
    "#### Objetivo mostrar a quantidade de mensagens trocadas por cada pessoa em uma conversa no aplicativo WhatsApp")
st.subheader('Total de mensagens: {}'.format(len(df_messages)))
# Agrupa as mensagens por pessoa e conta a quantidade de mensagens
df_soma = df_messages.groupby('phone')['message'].count().reset_index()
# Renomeia as colunas
df_soma.rename(columns={'phone': 'Pessoa', 'message': 'Quantidade de mensagens'}, inplace=True)
# Ordena o dataframe
df_soma = df_soma.sort_values(by='Quantidade de mensagens', ascending=True)
c = px.bar(df_soma, x='Pessoa', y='Quantidade de mensagens')
st.plotly_chart(c, use_container_width=True)
