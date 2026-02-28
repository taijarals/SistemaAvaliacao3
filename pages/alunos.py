import streamlit as st
from supabase import create_client

# ==========================
# CONFIG SUPABASE
# ==========================

#SUPABASE_URL = "SUA_URL"
#SUPABASE_KEY = "SUA_KEY"

SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

st.title("👨‍🎓 Gestão de Alunos")

# ==========================
# BUSCAR DISCIPLINAS
# ==========================

disciplinas = supabase.table("disciplinas").select("*").order("nome_disciplina").execute().data

disciplinas_dict = {
    f"{d['nome_disciplina']} ({d['nome_curso']})": d["id"]
    for d in disciplinas
}

# ==========================
# CRIAR ALUNO
# ==========================

st.subheader("➕ Novo Aluno")

with st.form("form_aluno"):

    nome_aluno = st.text_input("Nome do Aluno")

    disciplinas_selecionadas = st.multiselect(
        "Disciplinas",
        list(disciplinas_dict.keys())
    )

    submitted = st.form_submit_button("Salvar")

    if submitted:
        if nome_aluno:

            # Criar aluno
            aluno = supabase.table("alunos").insert({
                "nome": nome_aluno
            }).execute().data[0]

            aluno_id = aluno["id"]

            # Vincular disciplinas
            for disciplina_nome in disciplinas_selecionadas:
                supabase.table("aluno_disciplinas").insert({
                    "fk_aluno": aluno_id,
                    "fk_disciplina": disciplinas_dict[disciplina_nome]
                }).execute()

            st.success("Aluno criado com sucesso!")
            st.rerun()
        else:
            st.warning("Nome do aluno é obrigatório.")

# ==========================
# LISTAR ALUNOS
# ==========================

st.subheader("📋 Lista de Alunos")

alunos = supabase.table("alunos").select("*").order("id").execute().data

if alunos:

    for aluno in alunos:

        with st.expander(f"{aluno['id']} - {aluno['nome']}"):

            # Buscar disciplinas vinculadas
            vinculos = supabase.table("aluno_disciplinas") \
                .select("fk_disciplina") \
                .eq("fk_aluno", aluno["id"]) \
                .execute().data

            disciplinas_ids = [v["fk_disciplina"] for v in vinculos]

            disciplinas_vinculadas = [
                d["nome_disciplina"]
                for d in disciplinas
                if d["id"] in disciplinas_ids
            ]

            st.write("📚 Disciplinas:", ", ".join(disciplinas_vinculadas) if disciplinas_vinculadas else "Nenhuma")

            col1, col2 = st.columns(2)

            # EDITAR
            if col1.button("Editar", key=f"editar_aluno_{aluno['id']}"):
                st.session_state["editar_aluno_id"] = aluno["id"]

            # EXCLUIR
            if col2.button("Excluir", key=f"excluir_aluno_{aluno['id']}"):

                supabase.table("alunos").delete().eq(
                    "id", aluno["id"]
                ).execute()

                st.success("Aluno excluído!")
                st.rerun()

else:
    st.info("Nenhum aluno cadastrado.")

# ==========================
# EDIÇÃO
# ==========================

if "editar_aluno_id" in st.session_state:

    aluno_id = st.session_state["editar_aluno_id"]

    aluno_edit = supabase.table("alunos") \
        .select("*") \
        .eq("id", aluno_id) \
        .execute().data[0]

    vinculos = supabase.table("aluno_disciplinas") \
        .select("fk_disciplina") \
        .eq("fk_aluno", aluno_id) \
        .execute().data

    disciplinas_ids = [v["fk_disciplina"] for v in vinculos]

    disciplinas_pre_selecionadas = [
        nome for nome, id_ in disciplinas_dict.items()
        if id_ in disciplinas_ids
    ]

    st.subheader("✏️ Editar Aluno")

    novo_nome = st.text_input(
        "Nome do Aluno",
        value=aluno_edit["nome"]
    )

    novas_disciplinas = st.multiselect(
        "Disciplinas",
        list(disciplinas_dict.keys()),
        default=disciplinas_pre_selecionadas
    )

    if st.button("Atualizar Aluno"):

        if novo_nome:

            # Atualiza nome
            supabase.table("alunos").update({
                "nome": novo_nome
            }).eq("id", aluno_id).execute()

            # Remove vínculos antigos
            supabase.table("aluno_disciplinas") \
                .delete() \
                .eq("fk_aluno", aluno_id) \
                .execute()

            # Insere novos vínculos
            for disciplina_nome in novas_disciplinas:
                supabase.table("aluno_disciplinas").insert({
                    "fk_aluno": aluno_id,
                    "fk_disciplina": disciplinas_dict[disciplina_nome]
                }).execute()

            del st.session_state["editar_aluno_id"]

            st.success("Aluno atualizado!")
            st.rerun()

        else:
            st.warning("Nome do aluno é obrigatório.")