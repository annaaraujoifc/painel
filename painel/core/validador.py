from painel.core.entidades import Aluno, Nota


def validar_alunos(registros):
    alunos = []
    erros = []
    matriculas = set()

    for linha, registro in registros:
        matricula = (registro.get("matricula") or "").strip()
        nome = (registro.get("nome") or "").strip()
        turma = (registro.get("turma") or "").strip()

        if not matricula or not nome or not turma:
            erros.append({
                "arquivo": "alunos.csv",
                "linha": linha,
                "mensagem": "campo obrigatório vazio",
            })
            continue

        try:
            matricula_num = int(matricula)
        except ValueError:
            erros.append({
                "arquivo": "alunos.csv",
                "linha": linha,
                "mensagem": f"matrícula inválida ({matricula})",
            })
            continue

        if matricula_num in matriculas:
            erros.append({
                "arquivo": "alunos.csv",
                "linha": linha,
                "mensagem": f"matrícula {matricula_num} já cadastrada",
            })
            continue

        matriculas.add(matricula_num)
        alunos.append(Aluno(matricula_num, nome, turma))

    return alunos, erros


def validar_notas(registros, alunos, nota_maxima):
    notas = []
    erros = []
    matriculas_validas = {aluno.matricula for aluno in alunos}
    avaliacoes = set()

    for linha, registro in registros:
        matricula = (registro.get("matricula") or "").strip()
        disciplina = (registro.get("disciplina") or "").strip()
        avaliacao = (registro.get("avaliacao") or "").strip()
        valor = (registro.get("nota") or "").strip()

        if not matricula or not disciplina or not avaliacao or not valor:
            erros.append({
                "arquivo": "notas.csv",
                "linha": linha,
                "mensagem": "campo obrigatório vazio",
            })
            continue

        try:
            matricula_num = int(matricula)
        except ValueError:
            erros.append({
                "arquivo": "notas.csv",
                "linha": linha,
                "mensagem": f"matrícula inválida ({matricula})",
            })
            continue

        try:
            nota_num = float(valor)
        except ValueError:
            erros.append({
                "arquivo": "notas.csv",
                "linha": linha,
                "mensagem": f"nota inválida ({valor!r})",
            })
            continue

        if nota_num < 0 or nota_num > nota_maxima:
            erros.append({
                "arquivo": "notas.csv",
                "linha": linha,
                "mensagem": f"nota fora do intervalo ({valor})",
            })
            continue

        if matricula_num not in matriculas_validas:
            erros.append({
                "arquivo": "notas.csv",
                "linha": linha,
                "mensagem": f"matrícula inexistente ({matricula_num})",
            })
            continue

        chave = (matricula_num, disciplina, avaliacao)
        if chave in avaliacoes:
            erros.append({
                "arquivo": "notas.csv",
                "linha": linha,
                "mensagem": "avaliação duplicada",
            })
            continue

        avaliacoes.add(chave)
        notas.append(Nota(matricula_num, disciplina, avaliacao, nota_num))

    return notas, erros
