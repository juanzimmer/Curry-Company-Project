import streamlit as st
from PIL import Image

st.set_page_config(
    page_title="Home",
    layout="wide"
)

#image_path = '/Users/55819/Desktop/comunidade_DS/dados/repos/FTC_analise_com_python/logo.png'
image = Image.open('logo.png')
st.sidebar.image(image, width=120)

#title
st.sidebar.markdown('# Cury Company')
#subtitle
st.sidebar.markdown('## Fastest Delivery in town')
#barra separadora
st.sidebar.markdown("""___""")

st.write("# Curry Company Growth Dashboard")
st.markdown(
    """
    Growth Dashboard foi construído para acompanhar as métricas de crescimento dos Entregadores e Restaurantes.
    ### Como utilizar esse Growth Dashboard?
    - Visão Empresa:
        - Visão Gerencial: Métricas gerais de comportamento.
        - Visão Tática: Indicadores semanais de crescimento.
        - Visão Geográfica: Insights de Geolocalização.
    - Visão Entregador:
        - Acompanhamento dos indicadores semanais de crescimento.
    - Visão Restaurante:
        - Indicadores semanais de crescimento dos restaurantes.
    ### Ask for Help
        - LinkedIn: Juan Zimmermann
        - Git Hub: juanzimmer
        - Discord: Juan Zimmermann
""")




