import pytest
import sentinela as sn
import pandas as pd

def test_faixas_ficha_tecnica_pos_limpeza():
    """
    Verifica se a função limpar() garante que os dados respeitam 
    as faixas operacionais da ficha técnica dos sensores.
    """
    bruto = sn.dados.carregar("treino")
    limpo = sn.preprocessamento.limpar(bruto)
    
    # Temperatura: 45 a 95 °C
    assert limpo["temperatura_c"].min() >= 45.0, "Temperatura abaixo da faixa mínima (45°C)."
    assert limpo["temperatura_c"].max() <= 95.0, "Temperatura acima da faixa máxima (95°C)."
    
    # Corrente: 12 a 30 A
    assert limpo["corrente_a"].min() >= 12.0, "Corrente abaixo de 12A."
    assert limpo["corrente_a"].max() <= 30.0, "Corrente acima de 30A."
    
    # RPM: 1.650 a 1.800 rpm
    assert limpo["rpm"].min() >= 1650.0, "RPM abaixo de 1.650 (eixo parado)."
    assert limpo["rpm"].max() <= 1800.0, "RPM acima de 1.800."

def test_tratamento_faltantes_e_dropouts():
    """Testa se os valores ausentes e dropouts conhecidos (ex: vibracao_rms) são tratados."""
    bruto = sn.dados.carregar("treino")
    limpo = sn.preprocessamento.limpar(bruto)
    
    assert not limpo["vibracao_rms"].isnull().any(), \
        "A coluna 'vibracao_rms' contém valores nulos não tratados após a limpeza."

def test_conversao_unidades_pressao():
    """Verifica se a pressão está na unidade correta (3.0 a 4.5 bar)."""
    bruto = sn.dados.carregar("treino")
    limpo = sn.preprocessamento.limpar(bruto)
    
    assert limpo["pressao"].min() >= 3.0, "Pressão em bar abaixo do limite mínimo."
    assert limpo["pressao"].max() <= 4.5, "Pressão em bar acima do limite máximo."