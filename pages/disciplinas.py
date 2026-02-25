import streamlit as st
from supabase import create_client

# ==========================
# CONFIG SUPABASE
# ==========================

SUPABASE_URL = "https://iqeqnsobhcknizaowius.supabase.co"
SUPABASE_KEY = "SUA_CHAVE_AQUI"  # Ideal usar st.secrets

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

st.title("📘 Gestão de Disciplinas")

# ==========================
# CRIAR DISCIPLINA
# ==========================

st.subheader("➕ Nova Disciplina")

with st.form("form_disciplina"):

    nome_disciplina = st.text_input("Nome da Disciplina")
    nome_curso = st.text_input("Nome do Curso")
    dia_aula = st.text_input("Dia da Aula")

    submitted = st.form_submit_button("Salvar")

    if submitted:
        if nome_disciplina:

            supabase.table("disciplinas").insert({
                "nome_disciplina": nome_disciplina,
                "nome_curso": nome_curso,
                "dia_aula": dia_aula
            }).execute()

            st.success("Disciplina criada com sucesso!")
            st.rerun()

        else:
            st.warning("O nome da disciplina é obrigatório.")

# ==========================
# LISTAR DISCIPLINAS
# ==========================

st.subheader("📋 Lista de Disciplinas")

response = supabase.table("disciplinas").select("*").order("id").execute()

if response.data:

    for disciplina in response.data:

        with st.expander(f"{disciplina['id']} - {disciplina['nome_disciplina']}"):

            st.write("🎓 Curso:", disciplina["nome_curso"])
            st.write("📅 Dia da aula:", disciplina["dia_aula"])

            # Verificar desafios vinculados
            desafios_vinculados = supabase.table("desafios").select("id").eq(
                "fk_disciplina", disciplina["id"]
            ).execute()

            total_desafios = len(desafios_vinculados.data)
            st.write("📌 Desafios vinculados:", total_desafios)

            col1, col2 = st.columns(2)

            # EDITAR
            if col1.button("Editar", key=f"editar_{disciplina['id']}"):
                st.session_state["editar_disciplina_id"] = disciplina["id"]

            # EXCLUIR
            if col2.button("Excluir", key=f"excluir_{disciplina['id']}"):

                if total_desafios > 0:
                    st.error("Não é possível excluir. Existem desafios vinculados.")
                else:
                    supabase.table("disciplinas").delete().eq(
                        "id", disciplina["id"]
                    ).execute()

                    st.success("Disciplina excluída!")
                    st.rerun()

else:
    st.info("Nenhuma disciplina cadastrada.")

# ==========================
# EDIÇÃO
# ==========================

if "editar_disciplina_id" in st.session_state:

    disciplina_id = st.session_state["editar_disciplina_id"]

    disciplina_edit = supabase.table("disciplinas").select("*").eq(
        "id", disciplina_id
    ).execute().data[0]

    st.subheader("✏️ Editar Disciplina")

    novo_nome = st.text_input(
        "Nome da Disciplina",
        value=disciplina_edit["nome_disciplina"]
    )

    novo_curso = st.text_input(
        "Nome do Curso",
        value=disciplina_edit["nome_curso"]
    )

    novo_dia = st.text_input(
        "Dia da Aula",
        value=disciplina_edit["dia_aula"]
    )

    if st.button("Atualizar Disciplina"):

        if novo_nome:

            supabase.table("disciplinas").update({
                "nome_disciplina": novo_nome,
                "nome_curso": novo_curso,
                "dia_aula": novo_dia
            }).eq("id", disciplina_id).execute()

            del st.session_state["editar_disciplina_id"]

            st.success("Disciplina atualizada!")
            st.rerun()

        else:
            st.warning("O nome da disciplina é obrigatório.")