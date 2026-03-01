# services/disciplina_service.py

from repositories.disciplina_repository import DisciplinaRepository

class DisciplinaService:

    def __init__(self):
        self.repo = DisciplinaRepository()

    def listar_disciplinas(self):
        return self.repo.listar()

    def criar_disciplina(self, nome, curso, dia):

        if not nome:
            raise ValueError("Nome da disciplina é obrigatório.")

        self.repo.criar({
            "nome_disciplina": nome,
            "nome_curso": curso,
            "dia_aula": dia
        })

    def atualizar_disciplina(self, id, nome, curso, dia):

        if not nome:
            raise ValueError("Nome da disciplina é obrigatório.")

        self.repo.atualizar(id, {
            "nome_disciplina": nome,
            "nome_curso": curso,
            "dia_aula": dia
        })

    def excluir_disciplina(self, id):

        total = self.repo.contar_desafios(id)

        if total > 0:
            raise Exception("Existem desafios vinculados.")

        self.repo.excluir(id)