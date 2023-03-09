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

st.set_page_config(page_title='Visao Emtregadores', page_icon='🏍️', layout='wide')

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

def top_delivers(df):
    df_aux = (df.loc[:, ['Delivery_person_ID', 'City', 'Time_taken(min)']]
                .groupby(['City', 'Delivery_person_ID'])
                .mean()
                .sort_values(['City', 'Time_taken(min)'], ascending=False).reset_index())



        #pegando os 10(dez) 1º de cada cidade
    df_metropolitian = df_aux.loc[df_aux['City'] == 'Metropolitian'].head(10)
    df_semi_urban = df_aux.loc[df_aux['City'] == 'Semi-Urban'].head(10)
    df_urban = df_aux.loc[df_aux['City'] == 'Urban'].head(10)

        #concat
    df_final = pd.concat([df_metropolitian, df_urban, df_semi_urban])
            
    return df_final

def min_delivers(df):


            df_aux = df.loc[:, ['Delivery_person_ID', 'City', 'Time_taken(min)']].groupby(['City', 'Delivery_person_ID']).max().sort_values(['City', 'Time_taken(min)'], ascending=False).reset_index()

            #pegando os 10(dez) 1º de cada cidade
            df_metropolitian = df_aux.loc[df_aux['City'] == 'Metropolitian'].head(10)
            df_semi_urban = df_aux.loc[df_aux['City'] == 'Semi-Urban'].head(10)
            df_urban = df_aux.loc[df_aux['City'] == 'Urban'].head(10)

            #concat
            df_final = pd.concat([df_metropolitian, df_urban, df_semi_urban]).reset_index(drop=True)
            
            return df_final




#-------------------------------INICIO DA INFRAESTRUTURA LÓGICA DO CÓDIGO---------------------------------


#IMPORT DATASETS

data = pd.read_csv('train.csv')



#LIMPEZA DE DADOS
df = data.copy()
df = clean_code(df)


#-------------------------------INICIO DA INFRAESTRUTURA PÁG STREAMLIT---------------------------------

#______________________________________________________
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

#______________________________________________________
# LAYOUT STREAMLIT / GRÁFICOS


#COLUNAS NO CORPO DO STREAMLIT------------------------------------------------------------------------
#cod responsavel por deixar grafico lado a lado em uma mesma linha

#primeira linha
with st.container():
    st.markdown("""___""")
    st.title('Metricas Gerais')
    col1, col2, col3, col4 = st.columns(4, gap='large')

    with col1:
        
        maior_idade = df.loc[:, ['Delivery_person_Age']].max()
        #exibindo valor
        col1.metric("Maior Idade", maior_idade)

    with col2:
        
        menor_idade = df.loc[:, ['Delivery_person_Age']].min()
        #exibindo valor
        col2.metric('Menor idade', menor_idade)

    with col3:
        
        melhor_veiculo = df.loc[:, 'Vehicle_condition'].max()
        #exibindo valor
        col3.metric('Melhor condição', melhor_veiculo)


    with col4:
        pior_veiculo = df.loc[:, 'Vehicle_condition'].min()
        #exibindo valor
        col4.metric('pior condição', pior_veiculo)


#segunda linha
with st.container():
    st.markdown("""___""")
    st.title('Avaliações')

    col1, col2 =st.columns(2)

    with col1:
        st.markdown('##### Avaliação média por entregador')

        df_aux = df.loc[:, ['Delivery_person_ID', 'Delivery_person_Ratings']].groupby(['Delivery_person_ID']).mean().reset_index()
        st.dataframe(df_aux)


    with col2:
        #1 tabela
        st.markdown('##### Avaliação média por transito')

        #utilização dos parenteses p/ "escadificar" o código
        df_aux = (df.loc[:, ['Delivery_person_Ratings', 'Road_traffic_density']].groupby(['Road_traffic_density'])
                                                                                .agg({'Delivery_person_Ratings': ['mean', 'std']}))
        
        #renomeando mult-index
        df_aux.columns = ['delivery_mean', 'delivery_std']
        df_aux = df_aux.reset_index()
        st.dataframe(df_aux)

        #2 tabela
        st.markdown('##### Avaliação média por clima')


        df_aux = (df.loc[:, ['Delivery_person_Ratings', 'Weatherconditions']].groupby(['Weatherconditions'])
                                                                             .agg({'Delivery_person_Ratings': ['mean', 'std']}))

        #renomeando mult-index
        df_aux.columns = ['delivery_mean', 'delivery_std']
        df_aux = df_aux.reset_index()
        st.dataframe(df_aux)



#terceira linha
with st.container():
    st.markdown("""___""")
    st.title('Velocidade de entrega')

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('##### Top mais rápidos')
        df_aux = top_delivers(df)
        st.dataframe(df_aux)




    with col2:
        st.markdown('##### Top mais lentos')
        df_final = min_delivers(df)
        st.dataframe(df_final)




