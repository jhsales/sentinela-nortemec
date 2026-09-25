import pytest
import sentinela as sn

@pytest.mark.parametrize("versao", ["v1", "v2"])
def test_saida_pipeline_binaria(versao):
    """
    Garante que a predição retornada pelo pipeline seja estritamente 
    uma decisão binária (0 ou 1) para todas as linhas de teste.
    """
    dados_teste = sn.dados.carregar("teste")
    saida = sn.pipeline.executar(dados_teste, versao=versao, limiar=0.5)
    
    # Verifica se a coluna de predição existe
    assert "predicao" in saida.columns, f"A coluna 'predicao' está ausente na versão {versao}."
    
    # Verifica se os valores são estritamente 0 ou 1
    valores_unicos = saida["predicao"].unique()
    for val in valores_unicos:
        assert val in [0, 1], f"Valor inválido encontrado na predição da versão {versao}: {val}"

@pytest.mark.parametrize("versao", ["v1", "v2"])
def test_consistencia_tamanho_dataset(versao):
    """
    Verifica se o pipeline não descarta linhas indevidamente durante a execução,
    mantendo o mesmo número de linhas do dataset de entrada.
    """
    dados_teste = sn.dados.carregar("teste")
    saida = sn.pipeline.executar(dados_teste, versao=versao, limiar=0.5)
    
    assert len(saida) == len(dados_teste), \
        f"O pipeline ({versao}) alterou o número de linhas entre a entrada e a saída."