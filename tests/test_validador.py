import unittest

from painel.core.validador import validar_alunos, validar_notas


class TestValidador(unittest.TestCase):
    def test_limpa_espacos_e_aceita_aluno(self):
        alunos, erros = validar_alunos([
            (2, {"matricula": " 1 ", "nome": " Ana ", "turma": " 3A "})
        ])
        self.assertEqual(len(alunos), 1)
        self.assertEqual(alunos[0].nome, "Ana")
        self.assertEqual(erros, [])

    def test_rejeita_matricula_duplicada(self):
        alunos, erros = validar_alunos([
            (2, {"matricula": "1", "nome": "Ana", "turma": "3A"}),
            (3, {"matricula": "1", "nome": "Bia", "turma": "3B"}),
        ])
        self.assertEqual(len(alunos), 1)
        self.assertEqual(len(erros), 1)
        self.assertEqual(erros[0]["linha"], 3)

    def test_rejeita_nota_fora_intervalo(self):
        alunos, _ = validar_alunos([
            (2, {"matricula": "1", "nome": "Ana", "turma": "3A"})
        ])
        notas, erros = validar_notas([
            (2, {"matricula": "1", "disciplina": "Matemática",
                 "avaliacao": "P1", "nota": "11"})
        ], alunos, 10.0)
        self.assertEqual(notas, [])
        self.assertEqual(len(erros), 1)
        self.assertIn("fora do intervalo", erros[0]["mensagem"])


if __name__ == "__main__":
    unittest.main()
