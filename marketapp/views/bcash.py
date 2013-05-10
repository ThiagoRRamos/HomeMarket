'''
Created on May 9, 2013

@author: thiagorramos
'''
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from marketapp.models import Compra
from marketapp.services.bcash import validar_entrada


@csrf_exempt
def compra_confirmacao(request, compra_id):
    compra = get_object_or_404(Compra, id=compra_id)
    id_transacao = request.POST['id_transacao']
    if validar_entrada(id_transacao, compra.supermercado.chave_bcash, **request.POST):
        status = request.POST['status']
        if status == u'Aprovada':
            compra.status_pagamento = 'pa'
        elif status == u'Cancelada':
            compra.status_pagamento = 'pc'
        else:
            compra.status_pagamento = 'pi'
        compra.save()
    return redirect('compras.views.compra.minhas_compras')


@csrf_exempt
def compra_aviso(request, compra_id):
    compra = Compra.objects.get(id=compra_id)
    if 'status' in request.POST:
        id_transacao = request.POST.pop('id_transacao')
        if validar_entrada(id_transacao, compra.supermercado.chave_bcash, **request.POST):
            status = request.POST['status']
            if status == u'Aprovada':
                compra.status_pagamento = 'pa'
            elif status == u'Cancelada':
                compra.status_pagamento = 'pc'
            else:
                compra.status_pagamento = 'pi'
            compra.save()
    return redirect('compras.views.compra.minhas_compras')
