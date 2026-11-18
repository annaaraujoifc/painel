from abc import ABC, abstractmethod
import json


class GeradorRelatorio(ABC):
    @abstractmethod
    def gerar(self, resultado, caminho):
        pass


class RelatorioTexto(GeradorRelatorio):
    def gerar(self, resultado, caminho):
        linhas = [
            "PAINEL DE NOTAS — RESUMO",
            f"Alunos processados: {len(resultado['alunos'])}",
            (
                f"Registros de nota válidos: {len(resultado['notas'])} | "
                f"inválidos: {resultado['notas_invalidas']}"
            ),
            "",
            "Situação dos alunos",
        ]

        for aluno in resultado["alunos"]:
            media = aluno.media()
            situacao = aluno.situacao(
                resultado["config"]["media_aprovacao"],
                resultado["config"]["media_recuperacao"],
            )
            linhas.append(
                f"  {aluno.nome:<22} {aluno.turma}  média {media:.2f}  {situacao}"
            )

        linhas.extend(["", "Média por disciplina"])
        for disciplina, media in resultado["medias_disciplinas"].items():
            linhas.append(f"  {disciplina:<14} {media:.2f}")

        linhas.extend(["", f"Erros encontrados ({len(resultado['erros'])})"])
        for erro in resultado["erros"]:
            linhas.append(
                f"  {erro['arquivo']}:{erro['linha']}  {erro['mensagem']}"
            )

        with open(caminho, "w", encoding="utf-8") as arquivo:
            arquivo.write("\n".join(linhas) + "\n")


class RelatorioJSON(GeradorRelatorio):
    def gerar(self, resultado, caminho):
        dados = {
            "alunos_processados": len(resultado["alunos"]),
            "notas_validas": len(resultado["notas"]),
            "notas_invalidas": resultado["notas_invalidas"],
            "alunos": [],
            "medias_disciplinas": {
                disciplina: round(media, 2)
                for disciplina, media in resultado["medias_disciplinas"].items()
            },
            "erros": resultado["erros"],
        }

        for aluno in resultado["alunos"]:
            media = aluno.media()
            dados["alunos"].append({
                "matricula": aluno.matricula,
                "nome": aluno.nome,
                "turma": aluno.turma,
                "media": round(media, 2),
                "situacao": aluno.situacao(
                    resultado["config"]["media_aprovacao"],
                    resultado["config"]["media_recuperacao"],
                ),
            })

        with open(caminho, "w", encoding="utf-8") as arquivo:
            json.dump(dados, arquivo, ensure_ascii=False, indent=2)
