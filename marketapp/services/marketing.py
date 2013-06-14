'''
Created on Jun 10, 2013

@author: thiagorramos
'''
from marketapp.models import RegiaoAtendida, Consumidor, PromocaoCombinacao
from django.template.context import Context
from django.core.mail import send_mail
from django.template.loader import get_template

NOME_ENVIO = 'Equipe HomeMarket'


def consumidores_promocao(promocao):
    supermercado = promocao.supermercado
    regioes_atendidas = RegiaoAtendida.objects.filter(supermercado=supermercado)
    for reg in regioes_atendidas:
        cep_inicio = reg.cep_inicio
        cep_final = reg.cep_final
        consumidores = Consumidor.objects.filter(cep__gte=cep_inicio)
        for consumidor in consumidores:
            if consumidor.cep <= cep_final:
                yield consumidor


def selecionar_promocoes():
    return PromocaoCombinacao.objects.all()


def enviar_emails_promocoes():
    promocoes = selecionar_promocoes()
    mapping_consumidor_promocoes = {}
    for prom in promocoes:
        for consumidor in consumidores_promocao(prom):
            if consumidor not in mapping_consumidor_promocoes:
                mapping_consumidor_promocoes[consumidor] = []
            mapping_consumidor_promocoes[consumidor].append(prom)
    for consumidor in mapping_consumidor_promocoes:
        enviar_email(consumidor, mapping_consumidor_promocoes[consumidor])


def enviar_email(consumidor, promocoes):
    mail_context = Context({'consumidor': consumidor,
                            'promocoes': promocoes})
    send_mail('HomeMarket - Promocoes para voce',
              get_template('emails/promocao.txt').render(mail_context),
              NOME_ENVIO,
              [consumidor.usuario.email],
              fail_silently=False)
