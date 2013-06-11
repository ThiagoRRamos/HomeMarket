from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.core import serializers
from marketapp.models import Supermercado, ProdutoSupermercado, Compra, \
    ListaCompras, ProdutoCarrinho, CompraAgendada, RegiaoAtendida, \
    AvaliacaoSupermercado

import marketapp.services.carrinho as carrinho_service
import marketapp.services.compras as compras_service
from marketapp.utils.autorizacao import apenas_cliente

import marketapp.repository.produto as produto_repository
from marketapp.services.regiao_atendimento import get_supermercados_que_atendem
from marketapp.services.carrinho import limpar_carrinho, \
    SupermercadoNaoAtendeUsuario, CarrinhoComOutroSupermercado
from django.http.response import Http404
from marketapp.utils.decorators import jsonify
from marketapp import services


@apenas_cliente
def home(request):
    compras = Compra.objects.filter(consumidor=request.user.consumidor)
    listas_compras = ListaCompras.objects.filter(consumidor=request.user.consumidor)
    supermercados = get_supermercados_que_atendem(request.user)
    return render(request,
                  'cliente/home.html',
                  {'compras': compras,
                   'listas_compras': listas_compras,
                   'supermercados': supermercados})
    
def ver_historico_compras(request):
    compras = Compra.objects.filter(consumidor=request.user.consumidor, status_pagamento='ee').order_by('data_compra')[:10]
    return render(request,
                  'cliente/historico.html',
                  {'compras': compras})

@login_required
def agendar_compra(request):
    if request.method == 'POST':
        data = request.POST['dataAgendada']
        services.compras.gerar_compra_agendada(request.user.consumidor, carrinho_service.get_carrinho_usuario(request.user).produtocarrinho_set.all(), data)
    return render(request, 'cliente/agendamento.html')

@login_required
def agendar_compra_frequencia(request):
    if request.method == 'POST':
        data = request.POST['frequenciaAgendada']
        services.compras.gerar_compra_agendada(request.user.consumidor, carrinho_service.get_carrinho_usuario(request.user).produtocarrinho_set.all(), data)
    return render(request, 'cliente/agendamento_frequencia.html')

    
def ver_produtos_supermercado(request, nome):
    supermercado = get_object_or_404(Supermercado, nome_url=nome)
    produtos = ProdutoSupermercado.objects.filter(supermercado=supermercado)
    categorias = {}
    for p in produtos:
        if p.produto.categoria not in categorias:
            categorias[p.produto.categoria] = []
        categorias[p.produto.categoria].append(p)
    return render(request,
                  'cliente/ver_produtos_supermercado.html',
                  {'categorias': categorias,
                   'supermercado': supermercado})


@apenas_cliente
def adicionar_produto_carrinho(request, produto_id):
    produto = get_object_or_404(ProdutoSupermercado, id=produto_id)
    carrinho_service.adicionar_produto(request.user, produto)
    return redirect('marketapp.views.cliente.ver_carrinho')


@apenas_cliente
@jsonify
def json_adicionar_produto_carrinho(request, produto_id):
    produto = get_object_or_404(ProdutoSupermercado, id=produto_id)
    carrinho_service.adicionar_produto(request.user, produto)
    return {"ok": True}


@login_required
def ver_carrinho(request):
    carrinho = carrinho_service.get_carrinho_usuario(request.user)
    return render(request,
                  'cliente/carrinho.html',
                  {'carrinho': carrinho})


@login_required
def apagar_carrinho(request):
    limpar_carrinho(request.user)
    return redirect('marketapp.views.cliente.ver_carrinho')


@login_required
def remover_produto_carrinho(request, produtocarrinho_id):
    ProdutoCarrinho.objects.filter(id=produtocarrinho_id).delete()
    return redirect('marketapp.views.cliente.ver_carrinho')


@login_required
def comparar_supermercados(request):
    if 'ids' in request.GET:
        try:
            supermercados = request.GET.getlist('ids')
            supermercado_1 = Supermercado.objects.get(id=int(supermercados[0]))
            supermercado_2 = Supermercado.objects.get(id=int(supermercados[1]))
        except (KeyError, Supermercado.DoesNotExist):
            supermercados = Supermercado.objects.all()[:2]
            supermercado_1 = supermercados[0]
            supermercado_2 = supermercados[1]
    else:
        supermercados = Supermercado.objects.all()[:2]
        supermercado_1 = supermercados[0]
        supermercado_2 = supermercados[1]
    produtos = produto_repository.get_produtos_que_estejam_em_dois_supermercados(supermercado_1,
                                                                                 supermercado_2)
    return render(request,
                  'cliente/comparacao_supermercados.html',
                  {'produtos': produtos,
                   's1': supermercado_1,
                   's2': supermercado_2})


@login_required
def pagina_compra(request):
    produtos = carrinho_service.get_carrinho_usuario(request.user).produtocarrinho_set.all()
    compra = compras_service.gerar_compra(request.user.consumidor,
                                          produtos)
    carrinho_service.gerar_lista_de_compras(carrinho_service.get_carrinho_usuario(request.user))
    return redirect('marketapp.views.cliente.completar_compra',
                    compra_id=compra.id)


@login_required
def completar_compra(request, compra_id):
    compra = get_object_or_404(Compra, id=compra_id)
    if compra.status_pagamento != 'pn' or compra.consumidor != request.user.consumidor:
        raise Http404
    return render(request,
                  'cliente/pagina_compra.html',
                  {'compra': compra})

@login_required
def pagamento_dinheiro(request, compra_id):
    compra = get_object_or_404(Compra, id=compra_id)
    compra.modo_pagamento = 'di'
    compra.status_pagamento = 'pd'
    compra.save()
    return redirect('marketapp.views.cliente.home')


@apenas_cliente
def gerar_lista(request):
    nome_lista = request.POST.get('nome', '')
    carrinho_service.gerar_lista_de_compras(carrinho_service.get_carrinho_usuario(request.user),
                                            nome_lista)
    carrinho_service.limpar_carrinho(request.user)
    return redirect('/')


@apenas_cliente
def ver_lista_compras(request, lista_id):
    lista = get_object_or_404(ListaCompras, id=lista_id)
    return render(request,
                  '',
                  {'lista': lista})

@jsonify
def json_informacoes_supermercado(request):
    supermercados = Supermercado.objects.all()
    jsonDic = {}
    jsonDic['supermercados'] = []
    for mercado in supermercados:
        mercadoJson = {}
        mercadoJson["nome_exibicao"] = mercado.nome_exibicao
        regioes = RegiaoAtendida.objects.filter(supermercado=mercado)
        data = serializers.serialize("json", regioes, fields=('cep_inicio',
                                                            'cep_final',
                                                            'preco',
                                                            'tempo'))
        mercadoJson["regioes"] = data[0]
        avaliacoes = AvaliacaoSupermercado.objects.filter(supermercado=mercado)
        data = serializers.serialize("json", avaliacoes, fields=('nota',
                                                                 'avaliacao',
                                                                 'consumidor'))
        mercadoJson["avaliacoes"] = data[0]
        jsonDic['supermercados'].append(mercadoJson)
    return jsonDic