"""Cliente IA didáctico — sesión 13 oct 2026."""

from __future__ import annotations

import argparse
import json
import os
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass
class AIResponse:
    provider: str
    text: str


class AIClientError(RuntimeError):
    pass


_FAIL_ONCE = False


def complete(provider: str, prompt: str) -> AIResponse:
    global _FAIL_ONCE
    if _FAIL_ONCE:
        _FAIL_ONCE = False
        raise AIClientError("simulated transient error")

    provider = provider.lower()
    if provider == "mock":
        return AIResponse("mock", f"[mock] {prompt[:180]}")

    if provider == "openai":
        if not os.getenv("OPENAI_API_KEY"):
            raise AIClientError("Falta OPENAI_API_KEY")
        return AIResponse("openai", "(instala openai SDK y completa la llamada en clase)")

    if provider == "anthropic":
        if not os.getenv("ANTHROPIC_API_KEY"):
            raise AIClientError("Falta ANTHROPIC_API_KEY")
        return AIResponse("anthropic", "(instala anthropic SDK y completa la llamada en clase)")

    if provider in {"hf", "huggingface"}:
        if not os.getenv("HF_TOKEN"):
            raise AIClientError("Falta HF_TOKEN")
        return AIResponse("huggingface", "(instala huggingface_hub y completa la llamada en clase)")

    raise AIClientError(f"Proveedor no soportado: {provider}")


def complete_with_retry(provider: str, prompt: str, retries: int = 1) -> AIResponse:
    last: Exception | None = None
    for _ in range(retries + 1):
        try:
            return complete(provider, prompt)
        except AIClientError as exc:
            last = exc
    assert last is not None
    raise last


def main() -> None:
    global _FAIL_ONCE
    parser = argparse.ArgumentParser()
    parser.add_argument("--provider", default="mock")
    parser.add_argument("--prompt", default=None)
    parser.add_argument("--batch", type=Path, default=None)
    parser.add_argument("--output", type=Path, default=None)
    parser.add_argument("--fail-once", action="store_true")
    args = parser.parse_args()
    _FAIL_ONCE = args.fail_once

    if args.batch:
        out = args.output or Path("respuestas.jsonl")
        lines = [ln.strip() for ln in args.batch.read_text(encoding="utf-8").splitlines() if ln.strip()]
        with out.open("w", encoding="utf-8") as fh:
            for prompt in lines:
                resp = complete_with_retry(args.provider, prompt)
                fh.write(json.dumps({"prompt": prompt, **asdict(resp)}, ensure_ascii=False) + "\n")
        print(f"Wrote {len(lines)} lines -> {out}")
        return

    if not args.prompt:
        raise SystemExit("--prompt es obligatorio si no usas --batch")
    resp = complete_with_retry(args.provider, args.prompt)
    print(f"[{resp.provider}] {resp.text}")


if __name__ == "__main__":
    main()
