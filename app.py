import streamlit as st
from supabase import create_client, Client

# ==========================
# CONFIGURAÇÃO SUPABASE
# ==========================

SUPABASE_URL = "https://iqeqnsobhcknizaowius.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImlxZXFuc29iaGNrbml6YW93aXVzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzE3MjM3NDMsImV4cCI6MjA4NzI5OTc0M30.lq5a232elsZyMxg6qT-LXX_2WTsF790RN0X8S8ulTvY"


supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# ==========================
# INTERFACE STREAMLIT
# ==========================

st.title("Sistema de Avaliação")

st.write("Exemplo simples de conexão com banco relacional na nuvem.")

# ==========================
# INSERIR DADOS
# ==========================

st.subheader("Adicionar novo aluno")

nome = st.text_input("Nome do aluno")

if st.button("Salvar"):
    if nome:
        supabase.table("alunos").insert({"nome": nome}).execute()
        st.success("Aluno salvo com sucesso!")
    else:
        st.warning("Digite um nome.")

# ==========================
# LISTAR DADOS
# ==========================

st.subheader("Lista de alunos")

if st.button("Carregar alunos"):
    response = supabase.table("alunos").select("*").execute()
    dados = response.data
    st.write(dados)