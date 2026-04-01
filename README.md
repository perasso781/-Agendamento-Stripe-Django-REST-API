# 📅 Agendamento + Stripe — Django REST API

API simples para criar agendamentos e gerar pagamentos simulados via Stripe (modo teste).

---

## 🗂 Estrutura

```
agendamento_project/
├── core/
│   ├── __init__.py
│   ├── settings.py
│   └── urls.py
├── agendamentos/
│   ├── __init__.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
├── manage.py
├── requirements.txt
├── .env.example
└── README.md
```

---

## ⚙️ Instalação

```bash
# 1. Clone / entre na pasta
cd agendamento_project

# 2. Crie e ative o ambiente virtual
python -m venv venv
source venv/bin/activate        # Linux/Mac
# venv\Scripts\activate         # Windows

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Configure as variáveis de ambiente
cp .env.example .env
# Edite o .env e adicione sua STRIPE_SECRET_KEY de teste

# 5. Rode as migrations
python manage.py migrate

# 6. Suba o servidor
python manage.py runserver
```

---

## 🧪 Testando os Endpoints

### Criar um agendamento

```bash
curl -X POST http://localhost:8000/api/agendamentos/ \
  -H "Content-Type: application/json" \
  -d '{
    "nome_do_provedor": "Dr. Silva",
    "horario_do_agendamento": "2025-12-31T14:00:00-03:00",
    "email_do_cliente": "cliente@exemplo.com"
  }'
```

**Resposta esperada (201):**
```json
{
  "id": 1,
  "nome_do_provedor": "Dr. Silva",
  "horario_do_agendamento": "2025-12-31T14:00:00-03:00",
  "email_do_cliente": "cliente@exemplo.com",
  "criado_em": "2025-06-01T10:00:00Z"
}
```

---

### Listar agendamentos

```bash
curl http://localhost:8000/api/agendamentos/
```

---

### Buscar agendamento específico

```bash
curl http://localhost:8000/api/agendamentos/1/
```

---

## 💳 Testando o Pagamento Stripe

> **Pré-requisito:** adicione sua `STRIPE_SECRET_KEY` de teste no `.env`  
> Obtenha em: https://dashboard.stripe.com/test/apikeys

```bash
curl -X POST http://localhost:8000/api/agendamentos/1/pagamento/ \
  -H "Content-Type: application/json" \
  -d '{"valor_centavos": 5000}'
```

**Resposta esperada (201):**
```json
{
  "payment_intent_id": "pi_3Abc123...",
  "client_secret": "pi_3Abc123..._secret_xyz",
  "valor_centavos": 5000,
  "moeda": "brl",
  "status": "requires_payment_method",
  "agendamento": { ... }
}
```

> O `client_secret` pode ser usado no frontend com o [Stripe.js](https://stripe.com/docs/js) para completar o pagamento.

---

## 📌 Endpoints

| Método | URL | Descrição |
|--------|-----|-----------|
| `GET` | `/api/agendamentos/` | Lista todos os agendamentos |
| `POST` | `/api/agendamentos/` | Cria um agendamento |
| `GET` | `/api/agendamentos/<id>/` | Detalha um agendamento |
| `POST` | `/api/agendamentos/<id>/pagamento/` | Gera um PaymentIntent Stripe |
