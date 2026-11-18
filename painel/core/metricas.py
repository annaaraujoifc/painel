def media_por_disciplina(notas):
    valores = {}
    for nota in notas:
        valores.setdefault(nota.disciplina, []).append(nota.nota)

    return {
        disciplina: sum(lista) / len(lista)
        for disciplina, lista in sorted(valores.items())
    }
