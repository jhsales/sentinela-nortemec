import sentinela as sn
import pandas as pd

conjuntos = ["treino", "teste", "producao"]
versoes = ["v1", "v2"]
resultados = []

for conj in conjuntos:
    bruto = sn.dados.carregar(conj)
    for v in versoes:
        saida = sn.pipeline.executar(bruto, versao=v, limiar=0.5)
        y_real = saida["falha_72h"]
        y_pred = saida["predicao"]
        
        m = sn.avaliacao.metricas(y_real, y_pred)
        resultados.append({
            "conjunto": conj,
            "versao": v,
            "acuracia": m["acuracia"],
            "precisao": m["precisao"],
            "recall": m["recall"],
            "f1": m["f1"]
        })

df_baseline = pd.DataFrame(resultados)
print("\n--- TABELA DE LINHA DE BASE ---")
print(df_baseline.to_string(index=False))