import hashlib
import json
from collections.abc import Callable
from datetime import datetime, timezone
from pathlib import Path

SAMPLES_DIR = Path(__file__).resolve().parent / "samples"


def gerar_hash_cache(
    customer_id: str,
    ticket: str,
    prompt_version: str,
    content_type: str = "",
) -> str:
    chave = f"{customer_id}|{ticket}|{prompt_version}|{content_type}"
    return hashlib.md5(chave.encode("utf-8")).hexdigest()


def _caminho_cache(hash_cache: str) -> Path:
    return SAMPLES_DIR / f"{hash_cache}.json"


def buscar_no_cache(
    customer_id: str,
    ticket: str,
    prompt_version: str,
    content_type: str = "",
) -> dict | None:
    hash_cache = gerar_hash_cache(customer_id, ticket, prompt_version, content_type)
    caminho = _caminho_cache(hash_cache)

    if not caminho.exists():
        return None

    with open(caminho, "r", encoding="utf-8") as f:
        return json.load(f)


def salvar_no_cache(
    customer_id: str,
    ticket: str,
    prompt_version: str,
    saida: dict,
    content_type: str = "",
) -> str:
    SAMPLES_DIR.mkdir(parents=True, exist_ok=True)

    hash_cache = gerar_hash_cache(customer_id, ticket, prompt_version, content_type)
    caminho = _caminho_cache(hash_cache)

    registro = {
        "hash": hash_cache,
        "customer_id": customer_id,
        "ticket": ticket,
        "prompt_version": prompt_version,
        "content_type": content_type,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "output": saida,
    }

    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(registro, f, ensure_ascii=False, indent=2)

    return str(caminho)


def obter_resposta_com_cache(
    customer_id: str,
    ticket: str,
    prompt_version: str,
    content_type: str,
    funcao_chamada_api: Callable[[], dict],
) -> tuple[dict, bool]:
    """Retorna o resultado em cache ou executa a chamada à API e persiste a saída."""
    cache_existente = buscar_no_cache(customer_id, ticket, prompt_version, content_type)
    if cache_existente is not None:
        return cache_existente["output"], True

    saida = funcao_chamada_api()
    salvar_no_cache(customer_id, ticket, prompt_version, saida, content_type)
    return saida, False