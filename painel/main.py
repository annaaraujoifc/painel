import argparse
import logging
from pathlib import Path

from painel.services.processamento import processar
from painel.infra.relatorios import RelatorioTexto, RelatorioJSON


def configurar_logging(output):
    pasta = Path(output)
    pasta.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        filename=pasta / "painel.log",
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        encoding="utf-8",
        force=True,
    )


def main():
    parser = argparse.ArgumentParser(description="Painel de notas da turma")
    parser.add_argument("--alunos", required=True)
    parser.add_argument("--notas", required=True)
    parser.add_argument("--config", required=True)
    parser.add_argument("--formato", choices=["texto", "json"], default="texto")
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    configurar_logging(args.output)
    logging.info("Iniciando processamento")

    resultado = processar(args.alunos, args.notas, args.config)
    pasta = Path(args.output)
    pasta.mkdir(parents=True, exist_ok=True)

    if args.formato == "json":
        relatorio = RelatorioJSON()
        caminho = pasta / "painel.json"
    else:
        relatorio = RelatorioTexto()
        caminho = pasta / "painel.txt"

    relatorio.gerar(resultado, caminho)
    logging.info("Processamento concluído")
    print(f"Relatório gerado em: {caminho}")


if __name__ == "__main__":
    main()
