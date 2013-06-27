jQuery(function($){
	if($("#id_cpf").length > 0){
		$("#id_cpf").mask("999.999.999-99");
	}
	if($("#id_cep").length > 0){
		$("#id_cep").mask("99999-999");
	}
	if($("#id_telefone").length > 0){
		$("#id_telefone").mask("(99)99999999?9");
	}
	if($("input[id^=id_regiaoatendida_set-][id$=-cep_inicio]").length > 0){
		$("input[id^=id_regiaoatendida_set-][id$=-cep_inicio]").mask("99999-999");
	}
	if($("input[id^=id_regiaoatendida_set-][id$=-cep_final]").length > 0){
		$("input[id^=id_regiaoatendida_set-][id$=-cep_final]").mask("99999-999");
	}
});