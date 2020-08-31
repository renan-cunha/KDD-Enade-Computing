import pandas as pd
import numpy as np
from src import util

# TODO; Automatic Clean classificacao database

code = 12025  # código do curso de ciência da computação da ufpa

csv = pd.read_csv("data/MICRODADOS_ENADE_2017.txt", sep=";", decimal =',', 
                  dtype={"DS_VT_ESC_OFG":str, 
                         "DS_VT_ESC_OCE": str,
                         "DS_VT_ACE_OCE": str})
classificacao_tema = pd.read_csv("data/classificacao_charao.csv")

# Filtrar dados apenas dos estudantes do curso
csv_curso = csv.loc[csv["CO_CURSO"] == 12025]

# Mapear codigo de presenção pra label
# TODO: Do this automatically with all labels by using the dictionary csv
csv_curso.loc[:, "TP_PRES_LABEL"] = csv_curso["TP_PRES"].map({222:"Ausente", 
                                                       555:"Presente",
                                                       })

# Filtrar dados apenas dos estudantes que prestaram o exame
csv_curso_presentes = csv_curso.loc[csv_curso["TP_PRES_LABEL"] == "Presente"]


csv_curso_presentes = util.add_correct_columns(csv_curso_presentes)

# Filtrar dados das questões apenas do exame de 2017
classificacao_tema = classificacao_tema.loc[classificacao_tema["ano"] == 2017]


print(util.get_subject_valid_questions("Teoria da Computação", classificacao_tema,
                                  csv_curso_presentes))




