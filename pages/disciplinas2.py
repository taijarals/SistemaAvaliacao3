# pages/disciplinas.py

import streamlit as st
from services.disciplina_service import DisciplinaService

service = DisciplinaService()

st.title("📘 Gestão de Disciplinas")

st.subheader("➕ Nova Disciplina")

with st.form("form_disciplina"):

    nome = st.text_input("Nome da Disciplina")
    curso = st.text_input("Nome do Curso")
    dia = st.text_input("Dia da Aula")

    if st.form_submit_button("Salvar"):
        try:
            service.criar_disciplina(nome, curso, dia)
            st.success("Criada com sucesso!")
            st.rerun()
        except Exception as e:
            st.error(str(e))

st.subheader("📋 Lista de Disciplinas")

disciplinas = service.listar_disciplinas()

for disciplina in disciplinas:

    with st.expander(f"{disciplina['id']} - {disciplina['nome_disciplina']}"):

        st.write("Curso:", disciplina["nome_curso"])
        st.write("Dia:", disciplina["dia_aula"])

        col1, col2 = st.columns(2)

        if col1.button("Excluir", key=f"excluir_{disciplina['id']}"):
            try:
                service.excluir_disciplina(disciplina["id"])
                st.success("Excluída!")
                st.rerun()
            except Exception as e:
                st.error(str(e))