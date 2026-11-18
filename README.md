# Painel de Notas

Projeto para consolidar notas escolares a partir de arquivos CSV e JSON.

## Estrutura

- `painel/core/`: entidades, validações e métricas.
- `painel/infra/`: leitura de arquivos e geração de relatórios.
- `painel/services/`: fluxo de processamento.
- `data/`: arquivos de entrada.
- `tests/`: testes automatizados.

## Execução

Na pasta do projeto, execute:

```bash
python -m painel --alunos data/alunos.csv --notas data/notas.csv --config data/config.json --formato json --output output/
```

Para gerar o relatório em texto, troque `json` por `texto` no argumento `--formato`.

## Testes

```bash
python -m unittest discover -s tests
```
