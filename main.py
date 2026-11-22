import json
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from groq import Groq

from cache import obter_resposta_com_cache
from prompts import (
    prompt_diagnostico,
    prompt_passo_a_passo,
    prompt_perguntas_esclarecimento,
    prompt_resumo_visual,
)

BASE_DIR = Path(__file__).resolve().parent
CLIENTES_PATH = BASE_DIR / "clientes.json"
DEFAULT_MODEL = "openai/gpt-oss-20b"


def carregar_configuracao() -> dict:
    load_dotenv()
    api_key = os.getenv("GROQ_API_KEY")
    model_name = os.getenv("GROQ_MODEL", DEFAULT_MODEL)
    if not api_key:
        print("Erro: GROQ_API_KEY não encontrada no .env.", file=sys.stderr)
        sys.exit(1)

    return {"api_key": api_key, "model_name": model_name}


def carregar_clientes() -> list[dict]:
    if not CLIENTES_PATH.exists():
        print(f"Erro: arquivo não encontrado: {CLIENTES_PATH}", file=sys.stderr)
        sys.exit(1)

    with open(CLIENTES_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def encontrar_cliente(clientes: list[dict], cliente_id: str) -> dict | None:
    return next((c for c in clientes if c.get("id") == cliente_id), None)


def _limpar_markdown_json(texto: str) -> str:
    texto = texto.strip()
    if texto.startswith("```"):
        texto = texto.removeprefix("```json").removeprefix("```")
        texto = texto.removesuffix("```")
    return texto.strip()


def chamar_groq_json(prompt: str, config: dict) -> dict:
    client = Groq(api_key=config["api_key"])
    resposta = client.chat.completions.create(
        model=config["model_name"],
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )

    conteudo = resposta.choices[0].message.content or ""
    texto_limpo = _limpar_markdown_json(conteudo)

    try:
        return json.loads(texto_limpo)
    except json.JSONDecodeError:
        return {"erro": "Falha ao converter resposta para JSON", "texto_bruto": texto_limpo}


def gerar_diagnostico(cliente: dict, ticket: str, config: dict, versao_prompt: str = "v2") -> dict:
    prompt = prompt_diagnostico(cliente, ticket, versao_prompt)
    saida, _ = obter_resposta_com_cache(
        cliente["id"],
        ticket,
        versao_prompt,
        "diagnosis",
        lambda: chamar_groq_json(prompt, config),
    )
    return saida


def gerar_passo_a_passo(cliente: dict, ticket: str, config: dict, versao_prompt: str = "v2") -> dict:
    prompt = prompt_passo_a_passo(cliente, ticket, versao_prompt)
    saida, _ = obter_resposta_com_cache(
        cliente["id"],
        ticket,
        versao_prompt,
        "steps",
        lambda: chamar_groq_json(prompt, config),
    )
    return saida


def gerar_perguntas_esclarecimento(cliente: dict, ticket: str, config: dict, versao_prompt: str = "v2") -> dict:
    prompt = prompt_perguntas_esclarecimento(cliente, ticket, versao_prompt)
    saida, _ = obter_resposta_com_cache(
        cliente["id"],
        ticket,
        versao_prompt,
        "questions",
        lambda: chamar_groq_json(prompt, config),
    )
    return saida


def gerar_resumo_visual(cliente: dict, ticket: str, config: dict, versao_prompt: str = "v2") -> dict:
    prompt = prompt_resumo_visual(cliente, ticket, versao_prompt)
    saida, _ = obter_resposta_com_cache(
        cliente["id"],
        ticket,
        versao_prompt,
        "diagram",
        lambda: chamar_groq_json(prompt, config),
    )
    return saida


TIPOS_CONTEUDO = {
    "1": ("Diagnóstico do Problema", gerar_diagnostico),
    "2": ("Passo a Passo de Resolução", gerar_passo_a_passo),
    "3": ("Perguntas de Esclarecimento", gerar_perguntas_esclarecimento),
    "4": ("Resumo Visual (Fluxograma)", gerar_resumo_visual),
}


def menu_principal(clientes: list[dict], config: dict) -> None:
    print("=" * 50)
    print("Assistente de Atendimento com IA (V-LAB)")
    print("=" * 50)

    print("\nClientes disponíveis:")
    for c in clientes:
        print(
            f"[{c['id']}] {c['nome']} "
            f"(Nível: {c['nivel_tecnico']} | Estilo: {c['estilo_comunicacao']} | Canal: {c['canal']})"
        )

    cliente_id = input("\nID do cliente (ex: cliente_01): ").strip()
    cliente = encontrar_cliente(clientes, cliente_id)
    if not cliente:
        print("Erro: cliente não encontrado.", file=sys.stderr)
        return

    ticket = input("\nDescrição do problema (Ticket):\n>> ").strip()
    if not ticket:
        print("Erro: o ticket não pode estar vazio.", file=sys.stderr)
        return

    print("\nTipo de conteúdo:")
    for num, (nome, _) in TIPOS_CONTEUDO.items():
        print(f"[{num}] {nome}")

    opcao = input("\nOpção: ").strip()
    if opcao not in TIPOS_CONTEUDO:
        print("Erro: opção inválida.", file=sys.stderr)
        return

    versao = input("\nVersão do prompt (v1 = básico, v2 = avançado) [v2]: ").strip() or "v2"
    if versao not in {"v1", "v2"}:
        print("Erro: versão inválida. Use 'v1' ou 'v2'.", file=sys.stderr)
        return

    nome_conteudo, funcao_geradora = TIPOS_CONTEUDO[opcao]
    print("\nProcessando...")

    resultado = funcao_geradora(cliente, ticket, config, versao_prompt=versao)

    print("\n" + "=" * 50)
    print(f"RESULTADO: {nome_conteudo.upper()}")
    print("=" * 50)
    print(json.dumps(resultado, indent=2, ensure_ascii=False))
    print("=" * 50)
    print("\nSaída salva em /samples.")


def main() -> None:
    config = carregar_configuracao()
    clientes = carregar_clientes()
    menu_principal(clientes, config)


if __name__ == "__main__":
    main()