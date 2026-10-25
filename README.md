# ETL com IA generativa: mensagens personalizadas para clientes

Este projeto saiu do desafio do bootcamp Santander 2025 (Ciência de Dados com Python), na DIO. A ideia era montar um pipeline ETL completo, e eu quis fazer algo que rodasse do começo ao fim sem depender de uma API que pode cair.

## O que ele faz

Pego uma lista de clientes de um CSV, gero uma mensagem curta sobre investimentos para cada um e salvo o resultado num novo arquivo.

- **Extract:** lê `data/SDW2023.csv` com os dados (ID, nome, conta e cartão, todos fictícios).
- **Transform:** pede para a OpenAI uma mensagem de até 100 caracteres para cada pessoa. Se não houver chave configurada ou a chamada falhar, uso um texto padrão, para o pipeline nunca parar no meio.
- **Load:** grava tudo em `data/saida_mensagens.csv`, com a coluna `news`.

## Por que CSV e não a API

A API da Santander Dev Week usada nas aulas pode sair do ar a qualquer momento. Em vez de depender dela, escolhi a alternativa do próprio desafio: um arquivo completo com os dados dos clientes. O resto do fluxo continua igual.

## Como rodar

```bash
pip install -r requirements.txt
python etl.py
```

Quer usar a IA de verdade? Copie `.env.example` para `.env` e preencha `OPENAI_API_KEY`. Sem isso, o script roda normalmente com a mensagem padrão.
