from rest_framework import serializers
from .models import Agendamento


class AgendamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agendamento
        fields = ["id", "nome_do_provedor", "horario_do_agendamento", "email_do_cliente", "criado_em"]
        read_only_fields = ["id", "criado_em"]

    def validate_horario_do_agendamento(self, value):
        from django.utils import timezone
        if value <= timezone.now():
            raise serializers.ValidationError("O horário do agendamento deve ser no futuro.")
        return value
