import pandas as pd
import numpy as np
from src import util

# TODO; Automatic Clean classificacao database

code = 12025  # código do curso de ciência da computação da ufpa

print("Loading CSVs")
csv = pd.read_csv("data/MICRODADOS_ENADE_2017.txt", sep=";", decimal =',', 
                  dtype={"DS_VT_ESC_OFG":str, 
                         "DS_VT_ESC_OCE": str,
                         "DS_VT_ACE_OCE": str})
classificacao_tema = pd.read_csv("data/classificacao_charao.csv")
print("Finish loading")

# Filtrar dados apenas dos estudantes do curso de ciência da computação da ufpa
csv_curso = csv.loc[csv["CO_CURSO"] == 12025]

# Mapear codigo de presenção pra label
# TODO: Do this automatically with all labels by using the dictionary csv
csv_curso.loc[:, "TP_PRES_LABEL"] = csv_curso["TP_PRES"].map({222:"Ausente", 
                                                       555:"Presente",
                                                       })

# Filtrar dados apenas dos estudantes que prestaram o exame
csv_curso_presentes = csv_curso.loc[csv_curso["TP_PRES_LABEL"] == "Presente"]

csv_curso_presentes = util.add_columns_objective_score(csv_curso_presentes)

# Filtrar dados das questões apenas do exame de 2017
classificacao_tema = classificacao_tema.loc[classificacao_tema["ano"] == 2017]

subject = "Computação Gráfica e Processamento de Imagem"
csv_curso_presentes = util.add_column_score_subject(subject,
                                                    csv_curso_presentes,
                                                    classificacao_tema)
csv_curso_presentes["tmp"] = csv_curso_presentes["DS_VT_ESC_OCE"].str[26-9] +csv_curso_presentes["DS_VT_ESC_OCE"].str[27-9]
print(csv_curso_presentes[[f"SCORE_{subject}", "tmp"]])
