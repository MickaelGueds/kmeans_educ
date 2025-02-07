import streamlit as st

# Título da página
st.title("Kmeans de educação")

# Ler o arquivo HTML
with open("mapa_interativo.html", "r", encoding="utf-8") as file:
    html_content = file.read()

# Exibir o HTML no Streamlit
st.components.v1.html(html_content, height=600, scrolling=True)