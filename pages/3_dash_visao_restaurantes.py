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
import plotly.graph_objects as go

st.set_page_config(page_title='Visao Restaurantes', page_icon='🍽️', layout='wide')

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

def distancia(df):
    """ Função responsável por calcular distancia entre dois pontos

        Requisitos necessários:
        1. LAT / LONG - primeiro ponto
        2. LAT / LONG - segundo ponto
        3. Biblioteca responsavel por realizar a calculo haversine
        4. aplicar (apply, lambda) p/ percorrer todas as linhas da coluna LAT e LONG

        input - lat/long - primeiro e segundo ponto
        output - Distância entre pontos

    """

    #distancia media entre restaurante / local de entrega
    #apply lambda percorrendo todo do dataframe calculando distancia em km do restaurante e da entrega
    cols = ['Restaurant_latitude', 'Restaurant_longitude', 'Delivery_location_latitude', 'Delivery_location_longitude']
    df['distance'] = df.loc[:, cols].apply(lambda x: 
                        haversine(
                            (x['Restaurant_latitude'], x['Restaurant_longitude']),
                            (x['Delivery_location_latitude'], x['Delivery_location_longitude'])), axis=1)

    #media das distancias
    avg_distance = np.round(df['distance'].mean(), 1)
            
    return avg_distance

def media_entrega_fest(df):


    #tempo medio de entrega no festival
    df_aux = df.loc[:, ['Time_taken(min)', 'Festival']].groupby(['Festival']).agg({'Time_taken(min)':  ['mean', 'std']})

    #resetando o index
    df_aux.columns = ['mean_time', 'std_time']
    df_aux = df_aux.reset_index()
    #filtrando dataset
    linhas_selct = df_aux['Festival'] == 'Yes'
    df_aux = np.round(df_aux.loc[linhas_selct, 'mean_time'], 2)

    return df_aux

def std_medio_festival(df):

    #desvio padrao medio de entrega no festival
    df_aux = df.loc[:, ['Time_taken(min)', 'Festival']].groupby(['Festival']).agg({'Time_taken(min)':  ['mean', 'std']})

    #resetando o index
    df_aux.columns = ['mean_time', 'std_time']
    df_aux = df_aux.reset_index()

    #filtrando dataset
    linhas_selct = df_aux['Festival'] == 'Yes'
    df_aux = np.round(df_aux.loc[linhas_selct, 'std_time'])

    return df_aux

def media_entrg_s_festival(df):


    #tempo medio de entrega sem festival
    df_aux = df.loc[:, ['Time_taken(min)', 'Festival']].groupby(['Festival']).agg({'Time_taken(min)':  ['mean', 'std']})

    #resetando o index
    df_aux.columns = ['mean_time', 'std_time']
    df_aux = df_aux.reset_index()

    #filtrando dataset
    linhas_selct = df_aux['Festival'] == 'No'
    df_aux = np.round(df_aux.loc[linhas_selct, 'mean_time'], 2)

    return df_aux

def std_medio_s_festival(df):

    #desvio padrao medio de entrega sem festival
    df_aux = df.loc[:, ['Time_taken(min)', 'Festival']].groupby(['Festival']).agg({'Time_taken(min)':  ['mean', 'std']})

    #resetando o index
    df_aux.columns = ['mean_time', 'std_time']
    df_aux = df_aux.reset_index()

    #filtrando dataset
    linhas_selct = df_aux['Festival'] == 'No'
    df_aux = np.round(df_aux.loc[linhas_selct, 'std_time'])

    return df_aux

def grafico_entrega_cidade(df):

    df_aux = df.loc[:, ['City', 'Time_taken(min)']].groupby(['City']).agg({'Time_taken(min)':  ['mean', 'std']})

    #resetando o index
    df_aux.columns = ['avg_time', 'std_time']
    df_aux = df_aux.reset_index()

    fig = go.Figure()
    fig.add_trace(go.Bar(name = 'Control',
                            x = df_aux['City'],
                            y = df_aux['avg_time'],
                            error_y=dict(type = 'data', array = df_aux['std_time'])))

    fig.update_layout(barmode = 'group')
    return fig

def pizza_1(df):

    cols = ['Restaurant_latitude', 'Restaurant_longitude', 'Delivery_location_latitude', 'Delivery_location_longitude']
    df['distance'] = df.loc[:, cols].apply(lambda x: 
                        haversine(
                            (x['Restaurant_latitude'], x['Restaurant_longitude']),
                            (x['Delivery_location_latitude'], x['Delivery_location_longitude'])), axis=1)

    avg_distance = np.round(df.loc[:, ['City', 'distance']].groupby('City').mean().reset_index(), 3)

    #grafico
    fig = go.Figure(data=[go.Pie(labels=avg_distance['City'], values=avg_distance['distance'], textinfo='label+percent',
                        insidetextorientation='radial',
                        pull=[0, 0.2, 0])])
    fig.update_layout(autosize=False, width=500, height=500, title='Distancia média dos restaurantes e locais de entrega')
        
    return fig

def pizza_2(df):
        
    df_aux = df.loc[:, ['City', 'Time_taken(min)', 'Road_traffic_density']].groupby(['City', 'Road_traffic_density']).agg({'Time_taken(min)':  ['mean', 'std']})
    df_aux.columns = ['avg_time', 'std_time']
    df_aux = df_aux.reset_index()


    fig = px.sunburst(df_aux, path=['City', 'Road_traffic_density'], values='avg_time', 
                        color='std_time', color_continuous_scale='RdBu',
                        color_continuous_midpoint=np.average(df_aux['std_time']))
    fig.update_layout(autosize=False, width=400, height=500, title='Tempo médio e desvio padrão de entrega cidade/tipo de trafego.')
    return fig

def mostrando_df(df):

    st.markdown("""___""")
    st.title('Tempo médio e desvio padrão de entrega cidade/pedido')

    df_aux = df.loc[:, ['City', 'Time_taken(min)', 'Type_of_order']].groupby(['City', 'Type_of_order']).agg({'Time_taken(min)':  ['mean', 'std']})

    #resetando o index
    df_aux.columns = ['avg_time', 'std_time']
    df_aux = df_aux.reset_index()

    return df_aux


#-------------------------------INICIO DA INFRAESTRUTURA LÓGICA DO CÓDIGO---------------------------------

#IMPORT DATASET
data = pd.read_csv('train.csv')
df = data.copy()


#LIMPEZA DE DADOS
df = data.copy()
df = clean_code(df)

#-------------------------------INICIO DA INFRAESTRUTURA PÁG STREAMLIT---------------------------------

#______________________________________________________
# BARRA LATERAL
st.markdown('# Marketplace - Visão Restaurantes')

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

#selecionando multseleção transito
traffic_options = st.sidebar.multiselect(
    'Condiçoes de trânsito',
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

#INTERAÇÃO NO FILTRO =================================

#filtro de data
linhas_selecionadas = df['Order_Date'] < date_slider
df = df.loc[linhas_selecionadas, :]

#filtro de transito
linhas_selecionadas = df['Road_traffic_density'].isin(traffic_options)
df = df.loc[linhas_selecionadas, :]

#filtro de clima
linhas_selecionadas = df['Weatherconditions'].isin(conditions_options)
df = df.loc[linhas_selecionadas, :]


#_______________________________________________
# LAYOUT STREAMLIT / GRÁFICOS


#primeira linha ------------------------------------------------------
with st.container():
    st.markdown("""___""")
    st.title('Metricas Gerais')
    col1, col2, col3, col4, col5, col6 = st.columns(6, gap="small")

    with col1:
        qtd_entregador = len(df['Delivery_person_ID'].unique())
        col1.metric('Entregadores Únicos', qtd_entregador)

    with col2:
        avg_distance = distancia(df)
        col2.metric('Distancia Média rest / entreg', avg_distance)

    with col3:
        df_aux = media_entrega_fest(df)
        col3.metric('Tempo médio de entrega (Festival)', df_aux)
        
    with col4:
        df_aux = std_medio_festival(df)
        col4.metric('STD de entrega (Festival)', df_aux)

    with col5:
        df_aux = media_entrg_s_festival(df)
        col5.metric('Tempo médio de entrega (Sem Festival)', df_aux)

    with col6:
        df_aux = std_medio_s_festival(df)
        col6.metric('STD de entrega (Sem Festival)', df_aux)


#segunda linha ------------------------------------------------------
with st.container():
    st.markdown("""___""")
    st.title('O tempo médio e o desvio padrão de entrega por cidade')

    fig = grafico_entrega_cidade(df)
    st.plotly_chart(fig)


#terceira linha ------------------------------------------------------
with st.container():
    st.markdown("""___""")
    st.title('Distribuição do tempo')

    col1, col_extra, col2 = st.columns(3, gap = 'large')

    with col1:
        fig = pizza_1(df)
        st.plotly_chart(fig)

    with col2:
        fig = pizza_2(df)
        st.plotly_chart(fig)


#quarta linha ------------------------------------------------------
with st.container():
    df_aux = mostrando_df(df)
    st.dataframe(df_aux, use_container_width=True)