from django.db import models


class Agendamento(models.Model):
    nome_do_provedor = models.CharField(max_length=255)
    horario_do_agendamento = models.DateTimeField()
    email_do_cliente = models.EmailField()
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["horario_do_agendamento"]
        verbose_name = "Agendamento"
        verbose_name_plural = "Agendamentos"

    def __str__(self):
        return f"{self.nome_do_provedor} — {self.horario_do_agendamento:%d/%m/%Y %H:%M}"
