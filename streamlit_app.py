import pandas as pd
import plotly.express as px
import streamlit as st

from src.clear_file import BaseClearDataFile

st.set_page_config(page_title='WhatsApp Analyzer', page_icon='📊', layout='wide', initial_sidebar_state='auto')
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
qtd_messages_media = len(df_messages[df_messages['message'].str.contains('<Arquivo de mídia oculto>')])
qtd_numbers = len(df_messages['phone'].unique())
init_date = df_messages['date'].min()
end_date = df_messages['date'].max()

col1, col2, col3 = st.columns(3)
col1.metric("Total de mensagens", qtd_messages)
col2.metric("Total de mídias enviadas", qtd_messages_media)
col3.metric("Total de participantes", qtd_numbers)

col1, col2, col3 = st.columns(3)
col1.metric("Primeira mensagem", init_date.strftime('%d/%m/%Y %H:%M:%S'))
col2.metric("Ultima mensagem", end_date.strftime('%d/%m/%Y %H:%M:%S'))

# ====================================================================================================
st.title('Mensagens')

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

    df_filter = df_filter[
        (df_filter['date'] >= init_date.strftime('%Y-%m-%d')) &
        (df_filter['date'] <= end_date.strftime('%Y-%m-%d'))
        ]

    qtd_filter = len(df_filter)

col1, col2, col3 = st.columns(3)
col1.metric("Total de mensagens", qtd_filter)
col2.metric("Data inicial", init_date.strftime('%d/%m/%Y'))
col3.metric("Data final", end_date.strftime('%d/%m/%Y'))

st.write(f"Contatos:  {'Todos' if qtd_numbers == 'Todos' else qtd_numbers}")

df_rename = df_filter.rename(columns={'phone': 'Contato', 'date': 'Data', 'message': 'Mensagem'})
st.dataframe(df_rename, use_container_width=True)

df_filter['just_hour_int'] = df_filter.apply(lambda x: x['date'].hour, axis=1)
df_filter['just_hour'] = df_filter.apply(lambda x: x['date'].time(), axis=1)

df_data = df_filter.groupby('just_hour_int')['just_hour'].count().reset_index()
df_data['just_hour_int'] = df_data['just_hour_int'].apply(lambda x: str(x) + 'h')

df_data.rename(columns={'just_hour_int': 'Horário', 'just_hour': 'Mensagens'}, inplace=True)

c = px.bar(df_data, x='Horário', y='Mensagens', title=f'Mensagens por hora')

st.plotly_chart(c, use_container_width=True)

# ====================================================================================================
st.title('Mensagens do sistema')

df_rename = df_info_messages.rename(columns={'phone': 'Contato', 'date': 'Data', 'message': 'Mensagem'})
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
df_data = df_messages.groupby('just_date')['message'].count().reset_index()
# Renomeia as colunas
df_data.rename(columns={'just_date': 'Data', 'message': 'Quantidade de mensagens'}, inplace=True)

col1, col2, col3 = st.columns(3)
col1.metric("Data inicial:", df_data["Data"].min().strftime("%d/%m/%Y"))
col2.metric("Data final", df_data["Data"].max().strftime("%d/%m/%Y"))
col3.metric("Total de dias", len(df_data))

col1, col2, col3 = st.columns(3)
col1.metric("Média de mensagens por dia", round(df_data["Quantidade de mensagens"].mean()))
col2.metric("Média de mensagens por semana", round(df_data["Quantidade de mensagens"].mean() * 7))
col3.metric("Média de mensagens por mês", round(df_data["Quantidade de mensagens"].mean() * 30))

col1, col2, col3 = st.columns(3)
day_max = df_data["Data"][df_data["Quantidade de mensagens"].idxmax()].strftime("%d/%m/%Y")
day_min = df_data["Data"][df_data["Quantidade de mensagens"].idxmin()].strftime("%d/%m/%Y")

col1.metric(label="Dia com mais mensagens",
            value=day_max,
            delta=int(df_data["Quantidade de mensagens"].max()),
            delta_color="off"
            )

col2.metric(label="Dia com menos mensagens",
            value=day_min,
            delta=int(df_data["Quantidade de mensagens"].min()),
            delta_color="off"
            )

c = px.bar(df_data, x='Data', y='Quantidade de mensagens', title=f'Mensagens por hora')
st.plotly_chart(c, use_container_width=True)

# ====================================================================================================

st.title('Quantidade de mensagens por pessoa')
st.markdown(
    "#### Objetivo mostrar a quantidade de mensagens trocadas por cada pessoa em uma conversa no aplicativo WhatsApp")
st.subheader('Total de mensagens: {}'.format(len(df_messages)))
# Agrupa as mensagens por pessoa e conta a quantidade de mensagens
df_data = df_messages.groupby('phone')['message'].count().reset_index()
# Renomeia as colunas
df_data.rename(columns={'phone': 'Pessoa', 'message': 'Quantidade de mensagens'}, inplace=True)
# Ordena o dataframe
df_data = df_data.sort_values(by='Quantidade de mensagens', ascending=True)
c = px.bar(df_data, x='Pessoa', y='Quantidade de mensagens')
st.plotly_chart(c, use_container_width=True)

# ====================================================================================================
