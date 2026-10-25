"""Pipeline ETL com IA generativa (Santander 2025 - Ciência de Dados com Python).

Extract: lê usuários de um CSV.
Transform: gera uma mensagem de marketing personalizada com IA (ou fallback local).
Load: salva o resultado em um novo CSV.
"""
import os
from pathlib import Path

import pandas as pd

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

BASE_DIR = Path(__file__).parent
ENTRADA = BASE_DIR / "data" / "SDW2023.csv"
SAIDA = BASE_DIR / "data" / "saida_mensagens.csv"
MODELO = os.getenv("OPENAI_MODEL", "gpt-4o-mini")


def extract(caminho=ENTRADA):
    df = pd.read_csv(caminho)
    print(f"[Extract] {len(df)} usuários lidos de {caminho.name}")
    return df


def _cliente_openai():
    chave = os.getenv("OPENAI_API_KEY")
    if not chave:
        return None
    try:
        from openai import OpenAI
        return OpenAI(api_key=chave)
    except ImportError:
        return None


def gerar_mensagem(usuario, cliente=None):
    nome = usuario["Nome"]
    if cliente is not None:
        try:
            resposta = cliente.chat.completions.create(
                model=MODELO,
                messages=[
                    {"role": "system", "content": "Você é um especialista em marketing bancário."},
                    {
                        "role": "user",
                        "content": f"Crie uma mensagem para {nome} sobre a importância dos investimentos (máximo de 100 caracteres)",
                    },
                ],
            )
            return resposta.choices[0].message.content.strip('"')
        except Exception as erro:
            print(f"[Transform] Falha na IA para {nome} ({erro}); usando mensagem padrão.")
    return f"{nome}, investir hoje é garantir um futuro mais tranquilo!"


def transform(df):
    cliente = _cliente_openai()
    origem = "IA generativa" if cliente else "mensagem padrão (sem OPENAI_API_KEY)"
    print(f"[Transform] Gerando mensagens via {origem}")
    df = df.copy()
    df["news"] = df.apply(lambda linha: gerar_mensagem(linha, cliente), axis=1)
    return df


def load(df, caminho=SAIDA):
    df.to_csv(caminho, index=False, encoding="utf-8")
    print(f"[Load] Resultado salvo em {caminho}")


def main():
    load(transform(extract()))


if __name__ == "__main__":
    main()
