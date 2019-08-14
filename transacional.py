# -*- coding: utf-8 -*-
#placas = ["LAS7678"]
placas = []
import csv
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
from leilao.models import *
from plugins.sistran.tasks import *
from apreensao.models import *
veiculos_nao_localizados = []
leilao_nome = 'BF5DETRO02-19'
print "Retorno Inclusao (DETRAN) ;Retorno Consulta (DETRAN) ;Patio (BRPATIO) ;Lote; GRV (BRPATIO) ;Placa (BRPATIO) ;Chassi (BRPATIO) ;Marca/Modelo (BRPATIO) ;Cor (BRPATIO) ;Tipo (BRPATIO) ;Ano Fabricacao/Ano Modelo (BRPATIO) ;Renavam (DETRAN) ;Placa (DETRAN) ;Chassi (DETRAN) ;Marca/Modelo (DETRAN) ;Cor (DETRAN) ;Tipo (DETRAN) ;Categoria (DETRAN) ;Especie (DETRAN) ;Combustivel (DETRAN) ;Motor (DETRAN) ;Municipio Emplacamento (DETRAN) ;Nome Proprietario (DETRAN) ;CPF/CNPJ Proprietario (DETRAN) ;Endereco Proprietario (DETRAN) ;Numero Endereco Proprietario (DETRAN) ;Complemento Endereco Proprietario (DETRAN) ;CEP Endereco Proprietario (DETRAN) ;Municipio Endereco Proprietario ;Nome Financiamento (DETRAN) ;CPF/CNPJ Financiamento (DETRAN) ;Endereco Financiamento (DETRAN) ;Numero Financiamento (DETRAN) ;Complemento Financiamento (DETRAN) ;CEP Endereco Financiamento (DETRAN) ;Municipio Financiamento (DETRAN) ;Data Comunicacao de Venda (DETRAN) ;Nome Comunicacao Venda (DETRAN) ;CPF/CNPJ Comunicacao Venda (DETRAN) ;Endereco Comunicacao Venda (DETRAN) ;Numero Comunicacao de Venda (DETRAN) ;Complemento Comunicacao de Venda (DETRAN) ;Bairro Comunicacao de Venda (DETRAN) ;CEP Endereco Comunicacao de Venda (DETRAN) ;Municipio Comunicacao de Venda (DETRAN) ;UF Comunicacao de Venda (DETRAN) ;Nome Financiado - SNG (DETRAN) ;CPF/CNPJ Financiado - SNG (DETRAN) ;Agente Financeiro (DETRAN) ;CPF/CNPJ Financeiro (DETRAN) ;Indicacao Financiamento (DETRAN) ;Observacoes (DETRAN) ;Restricao (DETRAN) ;Observacao Restricao (DETRAN) ;Data Limite Restricao (DETRAN) ;Sub-Restricao (DETRAN) ;Multa RENAINF (DETRAN) ;Divida Ativa (DETRAN) ;Veiculo Baixado (DETRAN) ;Roubo/Furto (DETRAN)"
if placas:
    placas = Veiculo.objects.filter(lote__leilao__nome=leilao_nome, consultado_no_detran=True, lote__arrematado=True, placa__in=placas).values_list("placa", flat=True)
    veiculos = Veiculo.objects.filter(lote__leilao__nome=leilao_nome, consultado_no_detran=True, lote__arrematado=True, placa__in=placas)
else:
    placas = Veiculo.objects.filter(lote__leilao__nome=leilao_nome, consultado_no_detran=True, lote__arrematado=True).values_list("placa", flat=True)
    veiculos = Veiculo.objects.filter(lote__leilao__nome=leilao_nome, consultado_no_detran=True, lote__arrematado=True)
for veiculo in veiculos:
    if not Grv.objects.filter(contrato__nome="DETRO", placa=veiculo.placa).exists():
        veiculos_nao_localizados.append(veiculo.placa)
    else:
        grv = Grv.objects.filter(contrato__nome="DETRO", placa=veiculo.placa).first()
        retorno_veiculo = {}
        decricao_restricoes = ""
        decricao_obs_restricoes = ""
        desc_sub_restricao = ""
        if veiculo.consultado_no_detran:
            #if type(veiculo.dicionario_da_consulta_detran) == str:
            retorno_veiculo = eval(veiculo.dicionario_da_consulta_detran) if veiculo.dicionario_da_consulta_detran else {}
            if retorno_veiculo:
                if retorno_veiculo["DescricaoRestricoes"]:
                    for id, desc_restricoes in enumerate(retorno_veiculo["DescricaoRestricoes"]):
                        if desc_restricoes != "":
                            if id > 0:
                                decricao_restricoes += ","
                            decricao_restricoes += desc_restricoes
                if retorno_veiculo["ObservacaoRestricoes"]:
                    for id, desc_obs_restricoes in enumerate(retorno_veiculo["ObservacaoRestricoes"]):
                        if desc_obs_restricoes != "":
                            if id > 0:
                                decricao_obs_restricoes += ","
                            decricao_obs_restricoes += desc_obs_restricoes
                if retorno_veiculo["DescricaoSubRestricoes"]:
                    for id, sub_restricao in enumerate(retorno_veiculo["DescricaoSubRestricoes"]):
                        if sub_restricao != "":
                            if id > 0:
                                desc_sub_restricao += ","
                            desc_sub_restricao += sub_restricao
        nome_comunicado_venda = ""
        if Entidade.objects.filter(veiculo__lote__leilao__nome=leilao_nome, tipo="comunicadovenda", veiculo=veiculo).exists():
            nome_comunicado_venda = Entidade.objects.filter(veiculo__lote__leilao__nome=leilao_nome, tipo="comunicadovenda", veiculo=veiculo)[0].nome
        MAPA_PATIOS = {
            3: 98,
            4: 99,
            5: 95,
            6: 96,
            7: 97,
            8: 89,
            

    
        }
        consultado_no_detran = veiculo.consultado_no_detran
        if "DescricaoMunicipioEmplacamento" not in retorno_veiculo:
            consultado_no_detran = False
        lote = Lote.objects.get(leilao__nome=leilao_nome, veiculos=veiculo)

        # numero cnpj proprietario, comunicado de venda e financeira
        NumeroCpfCnpj = ""
        CpfCnpjFinanciamentoEfet = ""
        CpfCnpjComunicadoVenda = ""
        if consultado_no_detran:

            if str(retorno_veiculo["NumeroCpfCnpj"]) != "" and str(retorno_veiculo["NumeroCpfCnpj"]) != "0":
                if str(retorno_veiculo["TipoDocumento"]) == "1":
                    NumeroCpfCnpj = str(retorno_veiculo["NumeroCpfCnpj"]).zfill(11)
                elif str(retorno_veiculo["TipoDocumento"]) == "2":
                    NumeroCpfCnpj = str(retorno_veiculo["NumeroCpfCnpj"]).zfill(14)

            if str(retorno_veiculo["CpfCnpjFinanciamentoEfet"]) != "" and str(retorno_veiculo["CpfCnpjFinanciamentoEfet"]) != "0":
                if str(retorno_veiculo["TipoDocumentoFinanciamentoEfet"]) == "1":
                    CpfCnpjFinanciamentoEfet = str(retorno_veiculo["CpfCnpjFinanciamentoEfet"]).zfill(11)
                elif str(retorno_veiculo["TipoDocumentoFinanciamentoEfet"]) == "2":
                    CpfCnpjFinanciamentoEfet = str(retorno_veiculo["CpfCnpjFinanciamentoEfet"]).zfill(14)

            if str(retorno_veiculo["CpfCnpjComunicadoVenda"]) != "" and str(retorno_veiculo["CpfCnpjComunicadoVenda"]) != "0":
                if str(retorno_veiculo["TipoDocumentoComunicadoVenda"]) == "1":
                    CpfCnpjComunicadoVenda = str(retorno_veiculo["CpfCnpjComunicadoVenda"]).zfill(11)
                elif str(retorno_veiculo["TipoDocumentoComunicadoVenda"]) == "2":
                    CpfCnpjComunicadoVenda = str(retorno_veiculo["CpfCnpjComunicadoVenda"]).zfill(14)

        linha = dict(
          a="OK"
        , b="OK" if consultado_no_detran else "NOK" 
        , c=MAPA_PATIOS[grv.patio.id]
        , d=grv.numero_grv
        , e=grv.placa
        , f=grv.chassi
        , g=str(veiculo.marca) + "/" + str(veiculo.modelo)
        , h=veiculo.cor
        , i=veiculo.tipo
        , j=str(veiculo.ano_fabricacao) + "/" + str(veiculo.ano_modelo)
        , k=veiculo.renavam
        , l=veiculo.placa
        , m=veiculo.chassi
        , n=str(veiculo.marca) + "/" + str(veiculo.modelo)
        , o=veiculo.cor
        , p=veiculo.tipo
        , q=veiculo.categoria
        , r=retorno_veiculo["DescricaoEspecie"] if consultado_no_detran else ""
        , s=retorno_veiculo["DescricaoCombustivel"] if consultado_no_detran else ""
        , t=veiculo.numero_motor
        , u=retorno_veiculo["DescricaoMunicipioEmplacamento"] if consultado_no_detran else ""
        , v=retorno_veiculo["NomeProprietario"] if consultado_no_detran else ""
        , x=NumeroCpfCnpj
        , z=retorno_veiculo["EnderecoProprietario"] if consultado_no_detran else ""
        , aa=retorno_veiculo["NumeroEnderecoProprietario"] if consultado_no_detran else ""
        , ab=retorno_veiculo["ComplementoEnderecoProprietario"] if consultado_no_detran else ""
        , ac=retorno_veiculo["CepEnderecoProprietario"] if consultado_no_detran else ""
        , ad=retorno_veiculo["DescricaoMunicipioEndereco"] if consultado_no_detran else ""
        , ae=retorno_veiculo["NomeFinanciamentoEfet"] if consultado_no_detran else ""
        , af=CpfCnpjFinanciamentoEfet
        , ag=retorno_veiculo["EnderecoFinanciamentoEfet"] if consultado_no_detran else ""
        , ah=retorno_veiculo["NumeroFinanciamentoEfet"] if consultado_no_detran else ""
        , ai=retorno_veiculo["ComplementoFinanciamentoEfet"] if consultado_no_detran else ""
        , aj=retorno_veiculo["CepFinanciamentoEfet"] if consultado_no_detran else ""
        , ak=retorno_veiculo["MunicipioFinanciamentoEfet"] if consultado_no_detran else ""
        , al=retorno_veiculo["DataVendaComunicadoVenda"] if consultado_no_detran else ""
        , am=retorno_veiculo["NomeComunicacaoVenda"] if consultado_no_detran else nome_comunicado_venda
        , bm=nome_comunicado_venda
        , an=CpfCnpjComunicadoVenda
        , ao=retorno_veiculo["EnderecoComunicadoVenda"] if consultado_no_detran else ""
        , ap=retorno_veiculo["NumeroComunicadoVenda"] if consultado_no_detran else ""
        , aq=retorno_veiculo["ComplementoComunicadoVenda"] if consultado_no_detran else ""
        , ar=retorno_veiculo["BairroComunicadoVenda"] if consultado_no_detran else ""
        , at=retorno_veiculo["CepComunicadoVenda"] if consultado_no_detran else ""
        , au=retorno_veiculo["MunicipioComunicadoVenda"] if consultado_no_detran else ""
        , ax=retorno_veiculo["UfComunicadoVenda"] if consultado_no_detran else ""
        , ay=retorno_veiculo["NomeFinanciadoSng"] if consultado_no_detran else ""
        , az=retorno_veiculo["CpfCnpjFinanciadoSng"] if consultado_no_detran else ""
        , ba=retorno_veiculo["NomeAgenteFinanceiro"] if consultado_no_detran else ""
        , bb=retorno_veiculo["CpfCnpjAgeteFinanceiro"] if consultado_no_detran else ""
        , bc=retorno_veiculo["IndicacaoFinanciamento"] if consultado_no_detran else ""
        , bd=retorno_veiculo["Observacoes"] if consultado_no_detran else ""
        , be=decricao_restricoes
        , bf=decricao_obs_restricoes
        , bg=retorno_veiculo["DataLimiteRestricao"] if consultado_no_detran else ""
        , bh=desc_sub_restricao
        , bi="" if not consultado_no_detran else "NAO" if retorno_veiculo["IndicacaoMultasRenainf"] in ["","NAO"] else "SIM"
        , bj="" if not consultado_no_detran else "NAO" if retorno_veiculo["IndicacaoDividaAtiva"] in ["","NAO"] else "SIM"
        , bk="" if not consultado_no_detran else "NAO" if retorno_veiculo["IndicacaoVeiculoBaixado"] in ["","NAO"] else "SIM"
        , bl="" if not consultado_no_detran else "NAO" if retorno_veiculo["IndicacaoRouboFurto"] in ["","NAO"]  else "SIM"
        , bn=lote.numero_lote
        )

        print "{a};{b};{c};{bn};{d};{e};{f};{g};{h};{i};{j};{k};{l};{m};{n};{o};{p};{q};{r};{s};{t};{u};{v};{x};{z};{aa};{ab};{ac};{ad};{ae};{af};{ag};{ah};{ai};{aj};{ak};{al};{am};{an};{ao};{ap};{aq};{ar};{at};{au};{ax};{ay};{az};{ba};{bb};{bc};{bd};{be};{bf};{bg};{bh};{bi};{bj};{bk};{bl}".format(**linha)