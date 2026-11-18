from dataclasses import dataclass, field


@dataclass
class Aluno:
    matricula: int
    nome: str
    turma: str
    notas: list = field(default_factory=list)

    def media(self):
        if not self.notas:
            return 0.0
        return sum(n.nota for n in self.notas) / len(self.notas)

    def situacao(self, media_aprovacao, media_recuperacao):
        media = self.media()
        if media >= media_aprovacao:
            return "aprovado"
        if media >= media_recuperacao:
            return "recuperação"
        return "reprovado"


@dataclass
class Nota:
    matricula: int
    disciplina: str
    avaliacao: str
    nota: float
