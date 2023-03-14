import plotly.express as px
import streamlit as st
from matplotlib import pyplot as plt

from src.stream_lit import SearchWhatsappStreamlit

st.set_page_config(page_title='WhatsApp Analyzer',
                   page_icon='📊',
                   layout='wide',
                   initial_sidebar_state='auto')
st.set_option('deprecation.showPyplotGlobalUse', False)

st.title('WhatsApp Analyzer')

st.markdown('''
WhatsApp Analyzer é uma aplicação desenvolvida em Python para análise de dados do WhatsApp. A aplicação permite analisar 
um arquivo extraido de uma conversa e analisar as informações como a quantidade total de mensagens, mídias e 
participantes, além de fornecer análises específicas sobre as mensagens enviadas e recebidas.

#### Contato com o desenvolvedor 

Erickson Lopes: 
[![GitHub](https://img.shields.io/badge/-GitHub-181717?&logo=GitHub&logoColor=FFFFFF)](https://github.com/ericksonlopes/)
[![Linkedin](https://img.shields.io/badge/-LinkedIn-0A66C2?&logo=Linkedin&logoColor=FFFFFF)](https://www.linkedin.com/in/ericksonlopes/)
[![Medium](https://img.shields.io/badge/-Medium-000000?&logo=Medium&logoColor=FFFFFF)](https://medium.com/@ericksonlopes)

#### Tecnologias utilizadas:

![Streamlit](https://img.shields.io/badge/-Streamlit-FF4B4B?&logo=Streamlit&logoColor=FFFFFF)
![Pandas](https://img.shields.io/badge/-Pandas-150458?&logo=Pandas&logoColor=FFFFFF)
![Plotly](https://img.shields.io/badge/-Plotly-239120?&logo=Plotly&logoColor=FFFFFF)
![Matplotlib](https://img.shields.io/badge/-Matplotlib-3776AB?&logo=Matplotlib&logoColor=FFFFFF)
''')

st.write('Para utilizar a aplicação, é necessário fazer o upload de um arquivo de texto contendo o histórico de '
         'mensagens do WhatsApp. Para isso, clique no botão "Escolha o arquivo para análise de dados" e selecione'
         ' o arquivo desejado.')
data = st.file_uploader('Escolha o arquivo para analise de dados', type=['txt'])

if data is None:
    st.warning(
        """
        Por favor, escolha um arquivo para analise de dados(Para exportar a conversa do WhatsApp, siga os passos abaixo,
         ao final clique em "Exportar chat sem mídia"):
        """)
    st.image("src/img/img.png")
    st.stop()

swsl = SearchWhatsappStreamlit(file_data=data)
st.info('Arquivo carregado com sucesso')

# ====================================================================================================
# Define o título da página
st.title('Informações do arquivo')

st.write('A representação desses dados tem como objetivo fornecer informações resumidas e relevantes sobre um arquivo '
         'de conversas em um aplicativo de mensagens')

# Define as colunas para exibir as informações de total de mensagens, total de mídias enviadas e total de participantes
col_amount_messages, col_amount_medias, col_amount_numbers = st.columns(3)

# Exibe o total de mensagens na primeira coluna
col_amount_messages.metric("Total de mensagens", swsl.amount_of_messages)

# Exibe o total de mídias enviadas na segunda coluna
col_amount_medias.metric("Total de mídias enviadas", swsl.amount_of_media)

# Exibe o total de participantes na terceira coluna
col_amount_numbers.metric("Total de participantes", swsl.amount_of_numbers)

# Define as colunas para exibir as informações da primeira mensagem e da última mensagem
col_first_date, col_end_date, _ = st.columns(3)

# Exibe a data e hora da primeira mensagem na primeira coluna
col_first_date.metric("Primeira mensagem", swsl.get_init_date_format("%d/%m/%Y %H:%M:%S"))

# Exibe a data e hora da última mensagem na segunda coluna
col_end_date.metric("Ultima mensagem", swsl.get_end_date_format("%d/%m/%Y %H:%M:%S"))

# ====================================================================================================
st.title('Análise de mensagens')

st.write("Aqui você pode filtrar as mensagens por texto, contato e data.")

# Cria as opções de entrada de dados para filtrar as mensagens
message = st.text_input('Pesquisar texto:', value='')
numbers = st.multiselect('Pesquisar por contato:', swsl.list_of_numbers)
init_date = st.date_input('Data inicial', value=swsl.init_date)
end_date = st.date_input('Data final', value=swsl.end_date)

# Filtra as mensagens com base nas opções de entrada
filter_message = swsl.filter_messages(message=message, numbers=numbers, init_date=init_date, end_date=end_date)

# Cria as colunas para exibir as métricas de quantidade e data
col_amount_message, col_init_date, col_end_date = st.columns(3)
col_amount_message.metric("Total de mensagens", filter_message.amount_filter)
col_init_date.metric("Data inicial", init_date.strftime('%d/%m/%Y'))
col_end_date.metric("Data final", end_date.strftime('%d/%m/%Y'))

# Exibe a tabela com as mensagens filtradas
st.dataframe(filter_message.data_frame, use_container_width=True)

# Cria um gráfico com a quantidade de mensagens por hora
graphic_messages = swsl.graphic_filter_messages(filter_message.data_frame)
figure = px.bar(graphic_messages, x='Horário', y='Mensagens', title=f'Quantidade de mensagens por hora')
st.plotly_chart(figure, use_container_width=True)

# ====================================================================================================
st.title('Mensagens do sistema')

st.write("Aqui você pode visualizar as mensagens do sistema.")

# Exibe a tabela com as mensagens do sistema
df_infos = swsl.rename_column_df(swsl.df_info_messages, {'phone': 'Contato', 'date': 'Data', 'message': 'Mensagem'})
st.dataframe(df_infos, use_container_width=True)

# ====================================================================================================
st.title('Análise de mensagens por tempo')

st.write("Aqui você pode visualizar as mensagens por tempo")

# Cria as colunas para exibir as métricas de quantidade e data
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

st.title('Análise de mensagens por pessoa')
st.subheader('Total de numeros de telefone: {}'.format(swsl.amount_of_numbers))

st.write("Aqui você pode visualizar as mensagens por pessoa")

# Exibe a tabela com as mensagens por pessoa
df_rating_person = swsl.get_message_rating_by_person()

# Cria um gráfico com a quantidade de mensagens por pessoa
c = px.bar(df_rating_person, x='Pessoa', y='Quantidade de mensagens')
st.plotly_chart(c, use_container_width=True)

# ====================================================================================================
st.title('Análise de palavras')

st.write("Aqui você pode visualizar as palavras mais utilizadas na conversa e filtrar por contato e palavra.")

# Cria as opções de entrada de dados para filtrar as mensagens
numbers_palavra = st.multiselect('Pesquisar por contato: ', swsl.list_of_numbers)
message_palavra = st.text_input('Pesquisar palavra:', value='')

# Exibe a tabela com as palavras mais utilizadas
df_rating_words = swsl.get_message_rating_by_words(numbers_palavra, message_palavra)
st.dataframe(df_rating_words, use_container_width=True)

# Cria um gráfico com as palavras mais utilizadas
c = px.bar(df_rating_words.head(50), x='Palavra', y='Quantidade')
st.plotly_chart(c, use_container_width=True)

# ====================================================================================================
st.title('Word Cloud')
st.write('Aqui você pode visualizar a nuvem de palavras das mensagens mais utilizadas.')
st.markdown(
    """
        A nuvem de palavras é uma representação gráfica de palavras que mais aparecem no texto. As palavras mais 
        utilizadas são as que aparecem com maior tamanho e as que aparecem menos são as que aparecem com menor tamanho
    """)

# Cria a nuvem de palavras
wordcloud = swsl.generate_word_cloud(swsl.df_messages, "message")

# Exibe a nuvem de palavras
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
st.pyplot()

# ====================================================================================================
