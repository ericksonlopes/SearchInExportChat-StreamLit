import plotly.express as px
import streamlit as st

from src.stream_lit import SearchWhatsappStreamlit

st.set_page_config(page_title='WhatsApp Analyzer', page_icon='📊', layout='wide', initial_sidebar_state='auto')

st.title('WhatsApp Analyzer')

st.markdown('''
Projeto desenvolvido para analise de dados do WhatsApp


### Desenvolvido por:
> - [![GitHub](https://img.shields.io/badge/-Erickson%20Lopes-181717?&logo=GitHub&logoColor=FFFFFF)](https://github.com/ericksonlopes/ericksonlopes)
[![Linkedin](https://img.shields.io/badge/-Erickson%20Lopes-0A66C2?&logo=Linkedin&logoColor=FFFFFF)](https://www.linkedin.com/in/ericksonlopes/)

### Tecnologias utilizadas:

> - ![Streamlit](https://img.shields.io/badge/-Streamlit-FF4B4B?&logo=Streamlit&logoColor=FFFFFF)
![Pandas](https://img.shields.io/badge/-Pandas-150458?&logo=Pandas&logoColor=FFFFFF)
![Plotly](https://img.shields.io/badge/-Plotly-239120?&logo=Plotly&logoColor=FFFFFF)

''')
data = st.file_uploader('Escolha o arquivo para analise de dados', type=['txt'])

if data is None:
    st.warning('Por favor, escolha um arquivo para analise de dados')
    st.stop()

swsl = SearchWhatsappStreamlit(file_data=data)
st.info('Arquivo carregado com sucesso')

# ====================================================================================================
st.title('Informações do arquivo')

col_amount_messages, col_amount_medias, col_amount_numbers = st.columns(3)
col_amount_messages.metric("Total de mensagens", swsl.amount_of_messages)
col_amount_medias.metric("Total de mídias enviadas", swsl.amount_of_media)
col_amount_numbers.metric("Total de participantes", swsl.amount_of_numbers)

col_first_date, col_end_date, _ = st.columns(3)
col_first_date.metric("Primeira mensagem", swsl.get_init_date_format("%d/%m/%Y %H:%M:%S"))
col_end_date.metric("Ultima mensagem", swsl.get_end_date_format("%d/%m/%Y %H:%M:%S"))

# ====================================================================================================
st.title('Mensagens')

message = st.text_input('Pesquisar texto:', value='')
numbers = st.multiselect('Pesquisar por contato:', swsl.list_of_numbers)
init_date = st.date_input('Data inicial', value=swsl.init_date)
end_date = st.date_input('Data final', value=swsl.end_date)

filter_message = swsl.filter_messages(message=message, numbers=numbers, init_date=init_date, end_date=end_date)

col_amout_message, col_init_date, colcol_end_date = st.columns(3)
col_amout_message.metric("Total de mensagens", filter_message.amount_filter)
col_init_date.metric("Data inicial", init_date.strftime('%d/%m/%Y'))
colcol_end_date.metric("Data final", end_date.strftime('%d/%m/%Y'))
st.dataframe(filter_message.data_frame, use_container_width=True)

graphic_messages = swsl.graphic_filter_messages(filter_message.data_frame)
figure = px.bar(graphic_messages, x='Horário', y='Mensagens', title=f'Mensagens por hora')
st.plotly_chart(figure, use_container_width=True)

# ====================================================================================================
st.title('Mensagens do sistema')

df_rename_if = swsl.df_info_messages.rename(columns={'phone': 'Contato', 'date': 'Data', 'message': 'Mensagem'})
st.dataframe(df_rename_if, use_container_width=True)

# ====================================================================================================
st.title('Quantidade de mensagens por dia')
info_dates = swsl.get_info_amount_dates()

col1, col2, col3 = st.columns(3)
col1.metric("Data inicial:", swsl.get_init_date_format("%d/%m/%Y"))
col2.metric("Data final", swsl.get_end_date_format("%d/%m/%Y"))
col3.metric("Total de dias", info_dates.amount_od_days)

col1, col2, col3 = st.columns(3)
col1.metric("Média de mensagens por dia", info_dates.average_per_day)
col2.metric("Média de mensagens por semana", info_dates.average_per_week)
col3.metric("Média de mensagens por mês", info_dates.average_per_month)

col1, col2, _ = st.columns(3)
col1.metric(label="Dia com mais mensagens",
            value=info_dates.day_with_more_messages,
            delta=info_dates.amout_day_more_messages,
            delta_color="off"
            )
col2.metric(label="Dia com menos mensagens",
            value=info_dates.day_with_less_messages,
            delta=info_dates.amout_day_less_messages,
            delta_color="off"
            )

figure = px.bar(info_dates.data_frame, x='Data', y='Quantidade de mensagens', title=f'Quantidade de mensagens por dia')
st.plotly_chart(figure, use_container_width=True)

# ====================================================================================================

st.title('Quantidade de mensagens por pessoa')
st.subheader('Total de numeros de telefone: {}'.format(len(swsl.df_info_messages)))

df_rating_person = swsl.get_message_rating_by_person()

c = px.bar(df_rating_person, x='Pessoa', y='Quantidade de mensagens')
st.plotly_chart(c, use_container_width=True)

# ====================================================================================================
