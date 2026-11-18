import unittest

from painel.core.entidades import Aluno, Nota


class TestAluno(unittest.TestCase):
    def test_media(self):
        aluno = Aluno(1, "Ana", "3A", [
            Nota(1, "Matemática", "P1", 8.0),
            Nota(1, "Matemática", "P2", 6.0),
        ])
        self.assertEqual(aluno.media(), 7.0)

    def test_situacao_aprovado(self):
        aluno = Aluno(1, "Ana", "3A", [Nota(1, "Inglês", "P1", 8.0)])
        self.assertEqual(aluno.situacao(6.0, 4.0), "aprovado")

    def test_situacao_recuperacao(self):
        aluno = Aluno(1, "Ana", "3A", [Nota(1, "Inglês", "P1", 5.0)])
        self.assertEqual(aluno.situacao(6.0, 4.0), "recuperação")

    def test_situacao_reprovado(self):
        aluno = Aluno(1, "Ana", "3A", [Nota(1, "Inglês", "P1", 3.0)])
        self.assertEqual(aluno.situacao(6.0, 4.0), "reprovado")


if __name__ == "__main__":
    unittest.main()
