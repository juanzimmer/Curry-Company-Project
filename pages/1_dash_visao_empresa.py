#BIBLIOTECAS
import pandas as pd
import numpy as np
import streamlit as st
from haversine import haversine, Unit
import plotly.graph_objects as go
from PIL import Image
import folium
from streamlit_folium import folium_static
import plotly.express as px

st.set_page_config(page_title='Visao Empresa', page_icon='📈', layout='wide')

#FUNÇÕES
def clean_code(df):
    """função com responsabilidade de limpeza do dataset
        Tipos de limpeza:
        1. Remoção de dados NaN
        2. Mudança do tipo da coluna de dados
        3. Remoção dos espaços da variaveis de texto
        4. Formatação da data
        5. Limpeza da coluna de tempo (remoção do texto 'min')

        Input: Dataframe
        Output: Dataframe
    
    """

    #EXCLUINDO NULOS
    linhas_selecionadas = df['Delivery_person_Age'] != 'NaN '
    df = df.loc[linhas_selecionadas, :]

    linhas_selecionadas = df['Road_traffic_density'] != 'NaN '
    df = df.loc[linhas_selecionadas, :]

    linhas_selecionadas = df['City'] != 'NaN '
    df = df.loc[linhas_selecionadas, :]

    linhas_selecionadas = df['Festival'] != 'NaN '
    df = df.loc[linhas_selecionadas, :]

    linhas_selecionadas = df['multiple_deliveries'] != 'NaN '
    df = df.loc[linhas_selecionadas, :]

    #TRANSFORMAÇÃO DE TIPAGEM
    df['Delivery_person_Age'] = df['Delivery_person_Age'].astype(int)

    df['Delivery_person_Ratings'] = df['Delivery_person_Ratings'].astype(float)

    df['Order_Date'] = pd.to_datetime(df['Order_Date'], format='%d-%m-%Y')

    df['multiple_deliveries'] = df['multiple_deliveries'].astype(int)

    #REMOVENDO ESPAÇOS (strings/obj/text)
    df['ID'] = df['ID'].apply(lambda x : x.strip())

    df['Delivery_person_ID'] = df['Delivery_person_ID'].apply(lambda x : x.strip())

    df['Time_Orderd'] = df['Time_Orderd'].apply(lambda x : x.strip())

    df['Time_Order_picked'] = df['Time_Order_picked'].apply(lambda x : x.strip())

    df['Weatherconditions'] = df['Weatherconditions'].apply(lambda x : x.strip())

    df['Road_traffic_density'] = df['Road_traffic_density'].apply(lambda x : x.strip())

    df['Type_of_order'] = df['Type_of_order'].apply(lambda x : x.strip())

    df['Type_of_vehicle'] = df['Type_of_vehicle'].apply(lambda x : x.strip())

    df['Festival'] = df['Festival'].apply(lambda x : x.strip())

    df['City'] = df['City'].apply(lambda x : x.strip())

    df['Time_taken(min)'] = df['Time_taken(min)'].apply(lambda x : x.strip())

    #LIMPANDO COLUNA (Time_taken(min))

    df['Time_taken(min)'] = df['Time_taken(min)'].apply(lambda x: x.replace('(min) ', ''))
    df['Time_taken(min)'] = df['Time_taken(min)'].astype(int)

    return df

def order_metric(df):
    cols = ['ID', 'Order_Date']
    #seleção de linhas
    df_aux = df.loc[:, cols].groupby(['Order_Date']).count().reset_index()

    #desenhar o gráfico de linhas
    fig = px.bar( df_aux, x='Order_Date', y='ID')

    return fig

def traffic_order_share(df):
    df_aux = df.loc[:, ['ID', 'Road_traffic_density']].groupby('Road_traffic_density').count().reset_index()
    #nova coluna
    df_aux['entregas_perc'] = df_aux['ID'] / df_aux['ID'].sum()

    fig = px.pie(df_aux, values='entregas_perc', names='Road_traffic_density')
            
    return fig

def traffic_order_city(df):
    df_aux = df.loc[:, ['ID', 'City', 'Road_traffic_density']].groupby(['City', 'Road_traffic_density']).count().reset_index()
    
    #grafico
    fig = px.scatter(df_aux, x='City', y='Road_traffic_density', size='ID', color='City')
    
    return fig

def order_by_week(df):
    #criar coluna semanas
    df['week_of_year'] = df['Order_Date'].dt.strftime('%U')

    df_aux = df.loc[:, ['ID', 'week_of_year']].groupby('week_of_year').count().reset_index()

    fig = px.line(df_aux, x='week_of_year', y='ID')
    return fig

def order_share_by_week(df):

    #quantidade de pedidos / nº unico de entregadores
    df_aux01 = df.loc[:, ['ID', 'week_of_year']].groupby(['week_of_year']).count().reset_index()
    df_aux02 = df.loc[:, ['Delivery_person_ID', 'week_of_year']].groupby(['week_of_year']).nunique().reset_index()

    #merge
    df_aux = pd.merge(df_aux01, df_aux02, how='inner')

    #conta
    df_aux['order_by_deliver'] = df_aux['ID'] / df_aux['Delivery_person_ID']

    #grafico
    fig = px.line(df_aux, x='week_of_year', y='order_by_deliver')
    
    return fig

def country_maps(df):
    #groupby
    cols = ['City', 'Road_traffic_density', 'Delivery_location_latitude', 'Delivery_location_longitude']
    df_aux = df.loc[:, cols].groupby(['City', 'Road_traffic_density']).median().reset_index()

    #mapa
    map = folium.Map()

    #iterrows transforma dataframe em obj iterativo
    for index, i in df_aux.iterrows():
        folium.Marker([i['Delivery_location_latitude'], 
                    i['Delivery_location_longitude']]).add_to(map)

    #plotando mapa
    folium_static(map, width=1024, height=600)


#-------------------------------INICIO DA INFRAESTRUTURA LÓGICA DO CÓDIGO---------------------------------


#IMPORT DATASETS

data = pd.read_csv('train.csv')
df = data.copy()


#LIMPEZA DE DADOS

df = clean_code(df)


#-------------------------------INICIO DA INFRAESTRUTURA PÁG STREAMLIT---------------------------------


#____________________________________________
# BARRA LATERAL

st.markdown('# Marketplace - Visão Cliente')

#anexando imagem
image = Image.open('logo.png')
st.sidebar.image(image, width=120)

#criando barra lateral
#title
st.sidebar.markdown('# Cury Company')
#subtitle
st.sidebar.markdown('## Fastest Delivery in town')
#barra separadora
st.sidebar.markdown("""___""")

#titulo barra interativa
st.sidebar.markdown('## Selecione uma data limite')
#barra de interação
date_slider = st.sidebar.slider(
                'Selecione um valor',
                value=pd.datetime(2022, 4, 13),
                min_value=pd.datetime(2022, 2, 11),
                max_value=pd.datetime(2022, 4, 6),
                format='DD-MM-YYYY')

#barra separadora
st.sidebar.markdown("""___""")

#selecionando multseleção
traffic_options = st.sidebar.multiselect(
    'Quais as condiçoes de trânsito',
    ['Low', 'Medium', 'High', 'Jam'],
    default=['Low', 'Medium', 'High', 'Jam'])

#selecionando multseleção clima
conditions_options = st.sidebar.multiselect(
    'Condiçoes de clima',
    ['conditions Cloudy', 'conditions Fog', 'conditions Sandstorms', 'conditions Stormy', 'conditions Sunny', 'conditions Windy'],
    default=['conditions Cloudy', 'conditions Fog', 'conditions Sandstorms', 'conditions Stormy', 'conditions Sunny', 'conditions Windy'])

#barra separadora
st.sidebar.markdown("""___""")
#assinatura
st.sidebar.markdown('### Powered by Juan Zimmermann')


#INTERAÇÃO NO FILTRO

#filtro de data
linhas_selecionadas = df['Order_Date'] < date_slider
df = df.loc[linhas_selecionadas, :]

#filtro de transito
linhas_selecionadas = df['Road_traffic_density'].isin(traffic_options)
df = df.loc[linhas_selecionadas, :]

#filtro de clima
linhas_selecionadas = df['Weatherconditions'].isin(conditions_options)
df = df.loc[linhas_selecionadas, :]


#_________________________________________________
# LAYOUT STREAMLIT / GRÁFICOS


st.markdown("""___""")
st.header('Visão Gerencial')

#1. GRÁFICO - qtd pedido por dia ------------------------------------------------------------------------

st.markdown('# Orders by day')
fig = order_metric(df)
st.plotly_chart(fig, use_container_width=True)


#2. COLUNAS NO CORPO DO STREAMLIT -----------------------------------------------------------------------

with st.container():
    col1, col2 = st.columns(2)

    #2.1 Gráfico de pizza
    with col1:
        fig = traffic_order_share(df)
        st.markdown('### Pedidos por tipo de tráfego')
        st.plotly_chart(fig, use_container_width=True)
        

    #2.2 Gráfico de dispersão
    with col2:
        fig = traffic_order_city(df)
        st.markdown('### Volume por cidade e tráfego')
        st.plotly_chart(fig, use_container_width=True)


#3. Mapa -------------------------------------------------------------------------------------------------
st.markdown("""___""")
st.header('Visão Geográfica')

#mapa
st.markdown('### Mapa Cidades')
country_maps(df)


#4. VISÃO TÁTICA ----------------------------------------------------------------------------------------
st.markdown("""___""")
st.header('Visão Tática')

#4.1 linha - Por semana
fig = order_by_week(df)
st.markdown('### Pedidos por Semana')
st.plotly_chart(fig, use_container_width=True)


#4.2 linha - Quantidade de pedidos por entregador
fig = order_share_by_week(df)
st.markdown('### Pedidos por Entregador por Semana')
st.plotly_chart(fig, use_container_width=True)
