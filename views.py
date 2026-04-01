import stripe
from django.conf import settings
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Agendamento
from .serializers import AgendamentoSerializer


@api_view(["GET", "POST"])
def agendamentos(request):
    """
    GET  /api/agendamentos/  → lista todos os agendamentos
    POST /api/agendamentos/  → cria um novo agendamento
    """
    if request.method == "GET":
        qs = Agendamento.objects.all()
        serializer = AgendamentoSerializer(qs, many=True)
        return Response(serializer.data)

    serializer = AgendamentoSerializer(data=request.data)
    if serializer.is_valid():
        agendamento = serializer.save()
        return Response(AgendamentoSerializer(agendamento).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def agendamento_detail(request, pk):
    """
    GET /api/agendamentos/<pk>/  → retorna um agendamento específico
    """
    try:
        agendamento = Agendamento.objects.get(pk=pk)
    except Agendamento.DoesNotExist:
        return Response({"erro": "Agendamento não encontrado."}, status=status.HTTP_404_NOT_FOUND)

    serializer = AgendamentoSerializer(agendamento)
    return Response(serializer.data)


@api_view(["POST"])
def criar_payment_intent(request, pk):
    """
    POST /api/agendamentos/<pk>/pagamento/

    Body (opcional):
        { "valor_centavos": 5000 }   ← padrão: R$ 50,00

    Cria um PaymentIntent no Stripe (modo teste) e retorna o client_secret.
    """
    try:
        agendamento = Agendamento.objects.get(pk=pk)
    except Agendamento.DoesNotExist:
        return Response({"erro": "Agendamento não encontrado."}, status=status.HTTP_404_NOT_FOUND)

    if not settings.STRIPE_SECRET_KEY:
        return Response(
            {"erro": "STRIPE_SECRET_KEY não configurada. Adicione ao arquivo .env."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    stripe.api_key = settings.STRIPE_SECRET_KEY

    valor_centavos = request.data.get("valor_centavos", 5000)

    try:
        payment_intent = stripe.PaymentIntent.create(
            amount=valor_centavos,
            currency="brl",
            metadata={
                "agendamento_id": agendamento.id,
                "provedor": agendamento.nome_do_provedor,
                "cliente_email": agendamento.email_do_cliente,
            },
            description=f"Agendamento #{agendamento.id} — {agendamento.nome_do_provedor}",
        )
    except stripe.error.StripeError as e:
        return Response({"erro": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    return Response(
        {
            "payment_intent_id": payment_intent.id,
            "client_secret": payment_intent.client_secret,
            "valor_centavos": payment_intent.amount,
            "moeda": payment_intent.currency,
            "status": payment_intent.status,
            "agendamento": AgendamentoSerializer(agendamento).data,
        },
        status=status.HTTP_201_CREATED,
    )
