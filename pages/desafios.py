import streamlit as st
from supabase import create_client
from datetime import date

# ==========================
# CONFIG SUPABASE
# ==========================

SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

st.title("📚 Gestão de Desafios")

# ==========================
# BUSCAR DISCIPLINAS
# ==========================

disciplinas_response = supabase.table("disciplinas").select("*").execute()
disciplinas = disciplinas_response.data if disciplinas_response.data else []

if not disciplinas:
    st.warning("Cadastre uma disciplina antes de criar um desafio.")
    st.stop()

nomes_disciplinas = [d["nome_disciplina"] for d in disciplinas]

# ==========================
# CRIAR DESAFIO
# ==========================

st.subheader("➕ Novo Desafio")

with st.form("form_desafio"):

    titulo = st.text_input("Título")
    descricao = st.text_area("Descrição")
    disciplina_escolhida = st.selectbox("Disciplina", nomes_disciplinas)
    data_lancamento = st.date_input("Data de Lançamento", value=date.today())
    data_apresentacao = st.date_input("Data de Apresentação")
    ativo = st.checkbox("Definir como ativo")

    submitted = st.form_submit_button("Salvar")

    if submitted:

        if titulo and data_apresentacao:

            disciplina_id = next(
                d["id"] for d in disciplinas if d["nome_disciplina"] == disciplina_escolhida
            )

            # Se marcar como ativo, desativa todos
            if ativo:
                supabase.table("desafios").update(
                    {"ativo": False}
                ).neq("id", 0).execute()

            supabase.table("desafios").insert({
                "titulo": titulo,
                "descricao": descricao,
                "data_lancamento": str(data_lancamento),
                "data_apresentacao": str(data_apresentacao),
                "ativo": ativo,
                "fk_disciplina": disciplina_id
            }).execute()

            st.success("Desafio criado com sucesso!")
            st.rerun()

        else:
            st.warning("Preencha os campos obrigatórios.")

# ==========================
# LISTAR DESAFIOS
# ==========================

st.subheader("📋 Lista de Desafios")

response = supabase.table("desafios").select(
    "*, disciplinas(nome_disciplina)"
).order("id").execute()

if response.data:

    for desafio in response.data:

        nome_disciplina = (
            desafio["disciplinas"]["nome_disciplina"]
            if desafio.get("disciplinas")
            else "Não vinculada"
        )

        with st.expander(f"{desafio['id']} - {desafio['titulo']}"):

            st.write("📘 Disciplina:", nome_disciplina)
            st.write("📝 Descrição:", desafio["descricao"])
            st.write("📅 Lançamento:", desafio["data_lancamento"])
            st.write("🎤 Apresentação:", desafio["data_apresentacao"])
            st.write("🔥 Ativo:", "✅ Sim" if desafio["ativo"] else "❌ Não")

            col1, col2, col3 = st.columns(3)

            # ATIVAR
            if col1.button("Ativar", key=f"ativar_{desafio['id']}"):

                supabase.table("desafios").update(
                    {"ativo": False}
                ).neq("id", 0).execute()

                supabase.table("desafios").update(
                    {"ativo": True}
                ).eq("id", desafio["id"]).execute()

                st.success("Desafio ativado!")
                st.rerun()

            # EDITAR
            if col2.button("Editar", key=f"editar_{desafio['id']}"):
                st.session_state["editar_id"] = desafio["id"]

            # EXCLUIR
            if col3.button("Excluir", key=f"excluir_{desafio['id']}"):

                supabase.table("desafios").delete().eq(
                    "id", desafio["id"]
                ).execute()

                st.success("Desafio excluído!")
                st.rerun()

else:
    st.info("Nenhum desafio cadastrado.")

# ==========================
# EDIÇÃO
# ==========================

if "editar_id" in st.session_state:

    desafio_id = st.session_state["editar_id"]

    desafio_edit = supabase.table("desafios").select("*").eq(
        "id", desafio_id
    ).execute().data[0]

    st.subheader("✏️ Editar Desafio")

    novo_titulo = st.text_input("Título", value=desafio_edit["titulo"])
    nova_descricao = st.text_area(
        "Descrição", value=desafio_edit["descricao"]
    )

    disciplina_index = next(
        i for i, d in enumerate(disciplinas)
        if d["id"] == desafio_edit["fk_disciplina"]
    )

    nova_disciplina = st.selectbox(
        "Disciplina",
        nomes_disciplinas,
        index=disciplina_index
    )

    nova_data_lancamento = st.date_input(
        "Data de Lançamento",
        value=date.fromisoformat(desafio_edit["data_lancamento"])
    )

    nova_data_apresentacao = st.date_input(
        "Data de Apresentação",
        value=date.fromisoformat(desafio_edit["data_apresentacao"])
    )

    novo_ativo = st.checkbox(
        "Ativo",
        value=desafio_edit["ativo"]
    )

    if st.button("Atualizar"):

        nova_disciplina_id = next(
            d["id"] for d in disciplinas
            if d["nome_disciplina"] == nova_disciplina
        )

        if novo_ativo:
            supabase.table("desafios").update(
                {"ativo": False}
            ).neq("id", 0).execute()

        supabase.table("desafios").update({
            "titulo": novo_titulo,
            "descricao": nova_descricao,
            "data_lancamento": str(nova_data_lancamento),
            "data_apresentacao": str(nova_data_apresentacao),
            "ativo": novo_ativo,
            "fk_disciplina": nova_disciplina_id
        }).eq("id", desafio_id).execute()

        del st.session_state["editar_id"]

        st.success("Desafio atualizado!")
        st.rerun()