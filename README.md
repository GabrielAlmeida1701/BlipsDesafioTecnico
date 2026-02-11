# Instruções para rodar este projeto

Este repositório contém uma API em FastAPI para gerenciamento de Leads.

Requisitos locais:
- Python 3.11 (opcional se usar Docker)
- Docker + docker-compose (recomendado)

1) Rodando com Docker (recomendado)

```bash
docker-compose up --build
```

A API ficará disponível em http://localhost:8000 e a interface OpenAPI em http://localhost:8000/docs

2) Rodando localmente sem Docker

Crie um ambiente virtual, instale dependências e execute:

```bash
python -m venv .venv
source .venv/Scripts/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
export MONGO_URL='mongodb://localhost:27017'  # Windows: set MONGO_URL=...
uvicorn app.main:app --reload --port 8000
```

Como iniciar o MongoDB
- Usando Docker (recomendado): o `docker-compose.yml` já configura um serviço `mongo`.
- Localmente: execute uma instância do MongoDB na porta padrão 27017 e aponte `MONGO_URL` para ela.

Testes manuais dos endpoints

- Criar lead (POST):

```bash
curl -X POST http://localhost:8000/leads \
-H "Content-Type: application/json" \
-d '{"name":"João","email":"joao@example.com","phone":"+5511999999999"}'
```

- Listar leads (GET):

```bash
curl http://localhost:8000/leads
```

- Obter lead por id (GET):

```bash
curl http://localhost:8000/leads/<id>
```

Comportamento da integração externa

Durante a criação de um lead (POST /leads), o serviço consome a API pública `https://dummyjson.com/users/1` e extrai o campo `birthDate` para persistir no documento como `birth_date`.

Regras adotadas em caso de falha da requisição externa:

- Se a chamada à API externa falhar por qualquer motivo (timeout, erro HTTP, resposta inválida), a aplicação define `birth_date = null` no documento criado.
- Essa decisão mantém a criação do lead resiliente (não bloqueante) — o problema externo não impede o cadastro.

Arquitetura adotada (resumo)

- Camadas simples e desacopladas:
- `app/features/leads/routes.py`: rotas e validação com `pydantic` (`app/features/leads/schemas.py`)
- `app/features/leads/repository.py`: acesso ao MongoDB (opera sobre `app/shared/db.py`)
- `app/shared/services.py`: integração externa (external API)
- `app/shared/db.py`: conexão com MongoDB (motor)
- Projeto preparado para execução em Docker com `docker-compose`.

Nota: para compatibilidade com versões anteriores, há re-exports leves nos módulos de topo (`app/routes.py`, `app/schemas.py`, `app/repository.py`, `app/db.py`, `app/services.py`) que apontam para as implementações em `app/features` e `app/shared`.

Observações finais

- O campo retornado no JSON segue o formato exigido:

```json
{
"id": "...",
"name": "...",
"email": "...",
"phone": "...",
"birth_date": "1998-02-05"
}
```

Se `birth_date` não puder ser obtido, o valor será `null`.

Rodando os testes

Instale as dependências (ou use o ambiente virtual):

```bash
pip install -r requirements.txt
```

Execute os testes com `pytest`:

```bash
py -m pytest -q
```

Os testes usam `monkeypatch` para substituir as chamadas ao repositório e ao serviço externo, portanto não precisam de um MongoDB em execução.
