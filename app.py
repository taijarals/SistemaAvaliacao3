import streamlit as st
from supabase import create_client, Client

# ==========================
# CONFIGURAÇÃO SUPABASE
# ==========================

SUPABASE_URL = "https://iqeqnsobhcknizaowius.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImlxZXFuc29iaGNrbml6YW93aXVzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzE3MjM3NDMsImV4cCI6MjA4NzI5OTc0M30.lq5a232elsZyMxg6qT-LXX_2WTsF790RN0X8S8ulTvY"


supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# ==========================
# CONFIG DA PÁGINA
# ==========================

st.set_page_config(
    page_title="Sistema de Avaliação",
    layout="wide"
)

st.title("🏆 Sistema de Avaliação de Desafios")

# ==========================
# MENU LATERAL
# ==========================

#menu = st.sidebar.radio(
#    "Navegação",
#    ["Votação", "Gestão de Alunos", "Gestão de Desafios"]
#)

# ==========================
# TELA VOTAÇÃO
# ==========================

if menu == "Votação":

    st.header("Desafio Ativo")

    # Buscar desafio ativo
    desafio = supabase.table("desafios").select("*").eq("ativo", True).execute()

    if desafio.data:
        desafio_ativo = desafio.data[0]
        st.subheader(desafio_ativo["titulo"])
        st.write(desafio_ativo["descricao"])

        # Buscar alunos
        alunos = supabase.table("alunos").select("*").execute()

        if alunos.data:
            nomes = [aluno["nome"] for aluno in alunos.data]
            aluno_escolhido = st.selectbox("Selecione o aluno", nomes)

            if st.button("Votar"):
                aluno_id = next(a["id"] for a in alunos.data if a["nome"] == aluno_escolhido)

                supabase.table("votos").insert({
                    "aluno_id": aluno_id,
                    "desafio_id": desafio_ativo["id"]
                }).execute()

                st.success("Voto registrado com sucesso!")

        else:
            st.warning("Nenhum aluno cadastrado.")

    else:
        st.warning("Nenhum desafio ativo encontrado.")