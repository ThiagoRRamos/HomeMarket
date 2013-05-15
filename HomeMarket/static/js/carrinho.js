function limparCarrinho(){
	
}

function removerProduto(produtoId){
	
}

var qtdeAdicionados = 0

function adicionarProduto(produtoId){
	pronto = false
	resultado = false
	$.get('/json/colocar-no-carrinho/'+produtoId,function(result){
		pronto = true
		if(result.ok){
			resultado = true
			qtdeAdicionados +=1;
			console.log($('#avisos div'))
			$('#avisos').html('<div class="alert fade in">'+
            '<button type="button" class="close" data-dismiss="alert">&times;</button>'+
            qtdeAdicionados + ' produto(s) adicionado(s) com sucesso.'+
          '</div>')
		}else{
			window.location = "/colocar-no-carrinho/"+produtoId
			resultado = false
		}
	})
	return false;
}