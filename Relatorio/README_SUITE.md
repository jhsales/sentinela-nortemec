```markdown
# Relatório Técnico: Avaliação e Testes Automatizados do Sistema Sentinela
**Curso:** Pós-Graduação em IA e MLOps — IEC PUC Minas  
**Aluno:** Jorge Henrique  
**Trilha:** 1 (ML Clássico / Manutenção Preditiva Industrial)

---

## 1. Introdução
Este relatório documenta a suíte de testes automatizados desenvolvida externamente para o sistema preditivo **Sentinela** (Nortemec). Seguindo as diretrizes da Trilha 1, o pacote oficial não foi modificado; em vez disso, foram implementados testes para auditar contratos de dados, integridade do pipeline, métricas estatísticas e robustez adversarial, expondo falhas estruturais reais da aplicação.

---

## 2. Bloco A — Testes Unitários do Pipeline e Contratos de Dados

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

A acurácia isolada ($\sim 84,4\%$) é enganosa devido à prevalência de classes ($\sim 15\%$ de falhas). Um modelo que nunca prevê falhas atinge alta acurácia mas falha na missão principal da manutenção. A avaliação via varredura de limiar para o modelo `v2` demonstra o compromisso (*trade-off*) operacional:

| Limiar de Decisão | Precisão | Recall (Sensibilidade) | F1-Score | Impacto Operacional na Planta (Nortemec) |
| :---: | :---: | :---: | :---: | :--- |
| **0.2** (Agressivo) | 43.18% | 94.20% | 59.21% | Poucos motores queimados (alto recall), mas gera exaustivos falsos alarmes e equipes acionadas à toa. |
| **0.5** (Padrão) | 71.64% | 81.37% | 76.20% | Ponto de equilíbrio moderado entre custos de reparo de falhas reais e falsos positivos. |
| **0.8** (Conservador)| 94.24% | 42.44% | 58.53% | Poucas viagens desnecessárias, porém deixa mais da metade das falhas reais passarem sem aviso. |

---

## 4. Bloco C — Testes de Robustez Adversarial

### Instabilidade sob Ruído no Sensor de Temperatura
1. **O teste que falha:** `test_bloco_c_robustez_adversarial_temperatura` (`tests/test_avancado_bc.py`).
2. **A evidência medida:** Uma perturbação controlada de apenas **$+0.8$ °C** aplicada ao sensor de temperatura — valor mantido conscientemente abaixo da margem de ruído oficial do sensor ($\pm 1,0$ °C especificada no README) — provocou uma **taxa de inversão de decisão de 6.20%** nas predições do modelo `v2`.
3. **A causa raiz:** O modelo opera de forma muito sensível em suas fronteiras de decisão, reagindo a variações que representam apenas a incerteza inerente ao hardware de medição.
4. **O impacto na planta (Nortemec):** O sistema sofre de instabilidade frente a ruídos comuns de instrumentação industrial, gerando ordens de serviço oscilantes e contraditórias para o mesmo ativo em curtos intervalos.
