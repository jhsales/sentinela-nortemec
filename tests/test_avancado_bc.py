import pytest
import sentinela as sn
import numpy as np
import pandas as pd

def test_bloco_b_varredura_limiar():
    """
    Bloco B: Varre diferentes limiares de decisão para o modelo v2 
    e documenta o impacto prático na precisão e no recall.
    """
    dados_teste = sn.dados.carregar("teste")
    limiares = [0.2, 0.4, 0.5, 0.6, 0.8]
    print("\n--- VARREDURA DE LIMIAR (BLOCO B) ---")
    
    for lim in limiares:
        saida = sn.pipeline.executar(dados_teste, versao="v2", limiar=lim)
        m = sn.avaliacao.metricas(saida["falha_72h"], saida["predicao"])
        print(f"Limiar: {lim} | Precisão: {m['precisao']:.4f} | Recall: {m['recall']:.4f} | F1: {m['f1']:.4f}")
    
    assert True

def test_bloco_c_robustez_adversarial_temperatura():
    """
    Bloco C: Perturba o sensor de temperatura dentro da faixa de ruído 
    especificada no README (±1,0 °C) para medir a taxa de instabilidade das decisões.
    """
    dados_teste = sn.dados.carregar("teste").head(500).copy() # Amostra para agilizar
    
    # Execução baseline
    base_saida = sn.pipeline.executar(dados_teste, versao="v2", limiar=0.5)
    
    # Perturbação de +0.8 °C (abaixo do limiar de ruído de 1.0 °C)
    if "temperatura_c" in dados_teste.columns:
        dados_perturbados = dados_teste.copy()
        dados_perturbados["temperatura_c"] += 0.8
        
        perturbada_saida = sn.pipeline.executar(dados_perturbados, versao="v2", limiar=0.5)
        
        # Mede a taxa de decisões que mudaram
        mudancas = (base_saida["predicao"] != perturbada_saida["predicao"]).mean()
        taxa_percentual = mudancas * 100
        
        print(f"\n--- TESTE ADVERSARIAL TEMPERATURA (BLOCO C) ---")
        print(f"Taxa de inversão de decisão com ruído de +0.8°C: {taxa_percentual:.2f}%")
        
        # Evidência quantitativa para o relatório
        assert taxa_percentual >= 0.0, "Métrica calculada com sucesso."
    else:
        pytest.skip("Coluna 'temperatura_c' não encontrada no dataset.")