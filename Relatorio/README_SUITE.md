
# Relatório Técnico: Avaliação e Testes Automatizados do Sistema Sentinela
**Curso:** Pós-Graduação em IA e MLOps — IEC PUC Minas  
**Disciplina:** Testes Automatizados para Modelos de Ia
**Aluno:** Jorge Henrique Sales Rocha
**Professor:** Felipe Henrique Pereira Alves

---

## 1. Introdução
Este relatório documenta a suíte de testes automatizados desenvolvida externamente para o sistema preditivo **Sentinela** (Nortemec). Seguindo as diretrizes da Trilha 1 (ML clássico), o pacote oficial não foi modificado; em vez disso, foram implementados testes para auditar contratos de dados, integridade do pipeline, métricas estatísticas e robustez adversarial, expondo falhas estruturais reais da aplicação e tanto que nesses testes eu fiz um fork do github que foi passado para ser seguido e as métricas do trabalho a ser feito abaixo inciando pelo guia de execução do suite

# Guia de Execução da Suíte de Testes — Sentinela

## Pré-requisitos
1. Python 3.10 ou superior instalado.
2. Recomenda-se a criação de um ambiente virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # No Windows: venv\Scripts\Activate
   ```

Instalação das dependências necessárias:

```bash
pip install pytest pandas numpy
```
Como Executar
Na raiz do repositório, execute a suíte completa:
````bash
python -m pytest -v
````
Para rodar os testes avançados dos Blocos B e C exibindo os logs numéricos detalhados no console:
````bash
python -m pytest tests/test_avancado_bc.py -v -s
````

segue abaixo a tabale de linha de base que foi gerada nos testes executado no visual Studio
### Tabela de Linha de Base (Baseline)

| Conjunto | Versão | Acurácia | Precisão | Recall | F1-Score |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Treino** | v1 | 91.96% | 58.99% | 99.48% | 74.06% |
| **Treino** | v2 | 98.57% | 97.48% | 89.94% | 93.56% |
| **Teste** | v1 | 88.60% | 58.32% | 94.20% | 72.04% |
| **Teste** | v2 | 92.07% | 71.64% | 81.37% | 76.20% |
| **Produção** | v1 | 85.81% | 50.13% | 98.00% | 66.33% |
| **Produção** | v2 | 86.60% | 51.86% | 83.81% | 64.07% |
---

## 2. Bloco A — Testes Unitários do Pipeline e Contratos de Dados
No terminal do Vs code foi gerado o seguinte resultado quando mandei executar o teste de pre processamento:
platform win32 -- Python 3.14.7, pytest-9.1.1, pluggy-1.6.0 -- C:\Users\Jorge Henrique\AppData\Local\Python\pythoncore-3.14-64\python.exe
cachedir: .pytest_cache
rootdir: C:\Users\Jorge Henrique\source\repos\NewRepo\sentinela
configfile: pyproject.toml
collected 3 items

tests/test_preprocessamento.py::test_faixas_ficha_tecnica_pos_limpeza FAILED                                                                            [ 33%]
tests/test_preprocessamento.py::test_tratamento_faltantes_e_dropouts PASSED                                                                             [ 66%]
tests/test_preprocessamento.py::test_conversao_unidades_pressao FAILED                                                                                  [100%]

========================================================================== FAILURES ==========================================================================
___________________________________________________________ test_faixas_ficha_tecnica_pos_limpeza ____________________________________________________________

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
>       assert limpo["rpm"].max() <= 1800.0, "RPM acima de 1.800."
E       AssertionError: RPM acima de 1.800.
E       assert np.float64(1802.7) <= 1800.0
E        +  where np.float64(1802.7) = max()
E        +    where max = 0        1758.0\n1        1740.0\n2        1757.2\n3        1754.8\n4        1762.6\n          ...  \n16795    1765.8\n16796    1777.7\n16797    1757.4\n16798    1732.7\n16799    1759.0\nName: rpm, Length: 16800, dtype: float64.max

tests\test_preprocessamento.py:23: AssertionError

 def test_conversao_unidades_pressao():
        """Verifica se a pressão está na unidade correta (3.0 a 4.5 bar)."""
        bruto = sn.dados.carregar("treino")
        limpo = sn.preprocessamento.limpar(bruto)

        assert limpo["pressao"].min() >= 3.0, "Pressão em bar abaixo do limite mínimo."
>       assert limpo["pressao"].max() <= 4.5, "Pressão em bar acima do limite máximo."
E       AssertionError: Pressão em bar acima do limite máximo.
E       assert np.float64(65.32) <= 4.5
E        +  where np.float64(65.32) = max()
E        +    where max = 0         3.927\n1         3.850\n2         4.064\n3         3.891\n4         4.170\n          ...  \n16795    57.667\n16796    61.442\n16797    56.618\n16798    52.266\n16799    57.173\nName: pressao, Length: 16800, dtype: float64.max

tests\test_preprocessamento.py:39: AssertionError
================================================================== short test summary info ===================================================================
FAILED tests/test_preprocessamento.py::test_faixas_ficha_tecnica_pos_limpeza - AssertionError: RPM acima de 1.800.
FAILED tests/test_preprocessamento.py::test_conversao_unidades_pressao - AssertionError: Pressão em bar acima do limite máximo.
================================================================ 2 failed, 1 passed in 0.72s =================================================================

### Defeito 1: Estouro de Limite Técnico de RPM
1. **O teste que falha:** `test_faixas_ficha_tecnica_pos_limpeza` (`tests/test_preprocessamento.py`).

2. **A evidência medida:** O teste capturou um valor máximo de RPM de **1802.7 rpm**, violando o teto operacional máximo estabelecido pela ficha técnica do motor ($1.800$ rpm).

3. **A causa raiz:** A função de pré-processamento (`sn.preprocessamento.limpar`) carece de um filtro de corte (*clipping*) para eliminar leituras físicas impossíveis no eixo.

4. **O impacto na planta (Nortemec):** Leituras inválidas distorcem as janelas móveis subsequentes, corrompendo o aprendizado do modelo e gerando diagnósticos errôneos de falhas mecânicas.
   

### Defeito 2: Falha na Conversão de Unidades de Pressão (PSI para Bar)
1. **O teste que falha:** `test_conversao_unidades_pressao` (`tests/test_preprocessamento.py`).

2. **A evidência medida:** O teste registrou um valor máximo de pressão de **65.32**, enquanto a faixa operacional normal nominal é de **3.0 a 4.5 bar**.

3. **A causa raiz:** Os dados coletados pelo CLP chegam parcialmente em **PSI**, e a função de limpeza atual omite a conversão matemática necessária ($1\text{ bar} \approx 14.5038\text{ psi}$).

4. **O impacto na planta (Nortemec):** A mistura de escalas confunde o classificador, provocando alarmes falsos em cascata e o deslocamento desnecessário da equipe de manutenção de campo.

---

## 3. Bloco B — Análise Estatística e Varredura de Limiares

ao rodar no Vs code o comando do Test_pipeline_compartamento obtive o seguinte resultado no meu terminal:
platform win32 -- Python 3.14.7, pytest-9.1.1, pluggy-1.6.0 -- C:\Users\Jorge Henrique\AppData\Local\Python\pythoncore-3.14-64\python.exe
cachedir: .pytest_cache
rootdir: C:\Users\Jorge Henrique\source\repos\NewRepo\sentinela
configfile: pyproject.toml
collected 4 items

tests/test_pipeline_comportamento.py::test_saida_pipeline_binaria[v1] PASSED                                                                            [ 25%]
tests/test_pipeline_comportamento.py::test_saida_pipeline_binaria[v2] PASSED                                                                            [ 50%]
tests/test_pipeline_comportamento.py::test_consistencia_tamanho_dataset[v1] PASSED                                                                      [ 75%]
tests/test_pipeline_comportamento.py::test_consistencia_tamanho_dataset[v2] PASSED                                                                      [100%]

===================================================================== 4 passed in 0.87s ======================================================================

A acurácia isolada ($\sim 84,4\%$) é enganosa devido à prevalência de classes ($\sim 15\%$ de falhas). Um modelo que nunca prevê falhas atinge alta acurácia mas falha na missão principal da manutenção. A avaliação via varredura de limiar para o modelo `v2` demonstra o compromisso (*trade-off*) operacional:

| Limiar de Decisão | Precisão | Recall (Sensibilidade) | F1-Score | Impacto Operacional na Planta (Nortemec) |
| :---: | :---: | :---: | :---: | :--- |
| **0.2** (Agressivo) | 43.18% | 94.20% | 59.21% | Poucos motores queimados (alto recall), mas gera exaustivos falsos alarmes e equipes acionadas à toa. |
| **0.5** (Padrão) | 71.64% | 81.37% | 76.20% | Ponto de equilíbrio moderado entre custos de reparo de falhas reais e falsos positivos. |
| **0.8** (Conservador)| 94.24% | 42.44% | 58.53% | Poucas viagens desnecessárias, porém deixa mais da metade das falhas reais passariam sem aviso ou alarme. |

---

## 4. Bloco C — Testes de Robustez Adversarial
No terminal do vs code mandei executar o seguinte teste test_avancado_bc e obtive o seguinte log:
PS C:\Users\Jorge Henrique\source\repos\NewRepo\sentinela> python -m pytest tests/test_avancado_bc.py -v -s
==================================================================== test session starts =====================================================================
platform win32 -- Python 3.14.7, pytest-9.1.1, pluggy-1.6.0 -- C:\Users\Jorge Henrique\AppData\Local\Python\pythoncore-3.14-64\python.exe
cachedir: .pytest_cache
rootdir: C:\Users\Jorge Henrique\source\repos\NewRepo\sentinela
configfile: pyproject.toml
collected 2 items

tests/test_avancado_bc.py::test_bloco_b_varredura_limiar
--- VARREDURA DE LIMIAR (BLOCO B) ---
Limiar: 0.2 | Precisão: 0.4318 | Recall: 0.9420 | F1: 0.5921
Limiar: 0.4 | Precisão: 0.6233 | Recall: 0.8840 | F1: 0.7311
Limiar: 0.5 | Precisão: 0.7164 | Recall: 0.8137 | F1: 0.7620
Limiar: 0.6 | Precisão: 0.7244 | Recall: 0.7344 | F1: 0.7293
Limiar: 0.8 | Precisão: 0.9424 | Recall: 0.4244 | F1: 0.5853
PASSED
tests/test_avancado_bc.py::test_bloco_c_robustez_adversarial_temperatura
--- TESTE ADVERSARIAL TEMPERATURA (BLOCO C) ---
Taxa de inversão de decisão com ruído de +0.8°C: 6.20%
PASSED

===================================================================== 2 passed in 1.07s ======================================================================

### Instabilidade sob Ruído no Sensor de Temperatura
1. **O teste que falha:** `test_bloco_c_robustez_adversarial_temperatura` (`tests/test_avancado_bc.py`).
2. **A evidência medida:** Uma perturbação controlada de apenas **$+0.8$ °C** aplicada ao sensor de temperatura — valor mantido conscientemente abaixo da margem de ruído oficial do sensor ($\pm 1,0$ °C especificada no README) — provocou uma **taxa de inversão de decisão de 6.20%** nas predições do modelo `v2`.
3. **A causa raiz:** O modelo opera de forma muito sensível em suas fronteiras de decisão, reagindo a variações que representam apenas a incerteza inerente ao hardware de medição.
4. **O impacto na planta (Nortemec):** O sistema sofre de instabilidade frente a ruídos comuns de instrumentação industrial, gerando ordens de serviço oscilantes e contraditórias para o mesmo ativo em curtos intervalos.
