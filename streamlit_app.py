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

# Carrega os dados nos dataframes
df_messages = pd.DataFrame([m.__dict__ for m in base.messages])
df_info_messages = pd.DataFrame([m.__dict__ for m in base.info_messages])

# ====================================================================================================
st.title('Informações do arquivo')

qtd_messages = len(df_messages)
st.write(f"Total de mensagens:  {qtd_messages}")

qtd_messages_media = len(df_messages[df_messages['message'].str.contains('<Arquivo de mídia oculto>')])
st.write(f"Total de mídias enviadas:  {qtd_messages_media}")

qtd_numbers = len(df_messages['phone'].unique())
st.write(f"Total de participantes:  {qtd_numbers}")

init_date = df_messages['date'].min()
st.write(f"Primeira mensagem:  {init_date.strftime('%d/%m/%Y %H:%M:%S')}")

end_date = df_messages['date'].max()
st.write(f"Ultima mensagem:  {end_date.strftime('%d/%m/%Y %H:%M:%S')}")

# ====================================================================================================
st.title('Mensagens')
st.info("Os filtros valem apenas para neste bloco.")

message = st.text_input('Pesquisar texto:', value='')
numbers = st.multiselect('Pesquisar por contato:', df_messages['phone'].unique())
init_date = st.date_input('Data inicial', value=df_messages['date'].min())
end_date = st.date_input('Data final', value=df_messages['date'].max())

df_filter = df_messages
qtd_filter = len(df_messages)
qtd_numbers = "Todos"

if message:
    df_filter = df_filter[df_filter['message'].str.contains(message)]
    qtd_filter = len(df_filter)

if numbers:
    df_filter = df_filter[df_filter['phone'].isin(numbers)]
    qtd_filter = len(df_filter)
    qtd_numbers = ', '.join(df_filter['phone'].unique())

if init_date and end_date:
    df_filter['date'] = pd.to_datetime(df_filter['date'])

    df_filter = df_filter.loc[(df_filter['date'] >= init_date.strftime('%d/%m/%Y')) &
                              (df_filter['date'] <= end_date.strftime('%d/%m/%Y'))]

st.write(f"Total de mensagens:  {qtd_filter}")
st.write(f"Data inicial:  {init_date.strftime('%d/%m/%Y')}")
st.write(f"Data final:  {end_date.strftime('%d/%m/%Y')}")
st.write(f"Contatos:  {'Todos' if qtd_numbers == 'Todos' else qtd_numbers}")
st.dataframe(df_filter, use_container_width=True)

df_filter['just_hour_int'] = df_filter.apply(lambda x: x['date'].hour, axis=1)
df_filter['just_hour'] = df_filter.apply(lambda x: x['date'].time(), axis=1)

df_soma = df_filter.groupby('just_hour_int')['just_hour'].count().reset_index()
df_soma['just_hour_int'] = df_soma['just_hour_int'].apply(lambda x: str(x) + 'h')

df_soma.rename(columns={'just_hour_int': 'Horário', 'just_hour': 'Mensagens'}, inplace=True)

c = px.bar(df_soma, x='Horário', y='Mensagens', title=f'Mensagens por hora')

st.plotly_chart(c, use_container_width=True)

# ====================================================================================================
st.title('Mensagens do sistema')

st.dataframe(df_info_messages, use_container_width=True)

# ====================================================================================================

st.title('Quantidade de mensagens por dia')
# Transforma a coluna date em datetime
df_messages['date'] = pd.to_datetime(df_messages['date'])
# Cria uma nova coluna com a data sem a hora
df_messages["just_date"] = df_messages.apply(lambda x: x['date'].date(), axis=1)
# Agrupa as mensagens por data e conta a quantidade de mensagens
df_messages['just_date'] = pd.to_datetime(df_messages['just_date'])
# Cria um novo dataframe com a soma das mensagens por dia
df_soma = df_messages.groupby('just_date')['message'].count().reset_index()
# Renomeia as colunas
df_soma.rename(columns={'just_date': 'Data', 'message': 'Quantidade de mensagens'}, inplace=True)
# Cria o gráfico
st.bar_chart(df_soma, x='Data', y='Quantidade de mensagens', use_container_width=True)

# ====================================================================================================

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

# ====================================================================================================
