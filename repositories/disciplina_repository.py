# repositories/disciplina_repository.py

from database.connection import get_supabase

class DisciplinaRepository:

    def __init__(self):
        self.db = get_supabase()

    def listar(self):
        return self.db.table("disciplinas").select("*").order("id").execute().data

    def buscar_por_id(self, id):
        return self.db.table("disciplinas").select("*").eq("id", id).execute().data[0]

    def criar(self, dados):
        return self.db.table("disciplinas").insert(dados).execute()

    def atualizar(self, id, dados):
        return self.db.table("disciplinas").update(dados).eq("id", id).execute()

    def excluir(self, id):
        return self.db.table("disciplinas").delete().eq("id", id).execute()

    def contar_desafios(self, id):
        result = self.db.table("desafios").select("id").eq("fk_disciplina", id).execute()
        return len(result.data)