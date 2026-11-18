from painel.core.validador import validar_alunos, validar_notas
from painel.core.metricas import media_por_disciplina
from painel.infra.arquivos import ler_csv, ler_config


def processar(caminho_alunos, caminho_notas, caminho_config):
    registros_alunos = ler_csv(caminho_alunos)
    registros_notas = ler_csv(caminho_notas)
    config = ler_config(caminho_config)

    alunos, erros_alunos = validar_alunos(registros_alunos)
    notas, erros_notas = validar_notas(
        registros_notas, alunos, config["nota_maxima"]
    )

    alunos_por_matricula = {aluno.matricula: aluno for aluno in alunos}
    for nota in notas:
        alunos_por_matricula[nota.matricula].notas.append(nota)

    erros = erros_alunos + erros_notas
    return {
        "alunos": alunos,
        "notas": notas,
        "notas_invalidas": len(erros_notas),
        "erros": erros,
        "medias_disciplinas": media_por_disciplina(notas),
        "config": config,
    }
