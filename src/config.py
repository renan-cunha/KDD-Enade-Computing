import os

DATA_DIR = os.path.join("data")
YEARS = [2017, 2014, 2011, 2008, 2005]
CODE_COURSE_NEW = 4004
CODE_COURSE_OLD = 4001
DIFFICULTIES = ["muito facil", "facil", "medio", "dificil", "muito dificil"]
MATH_SUBJECTS = ["Lógica e matemática discreta",
                 "Probabilidade e estatística"]
COMPUTING_SUBJECTS = ["Algoritmos e estruturas de dados",
                      "Arquitetura de computadores e sistemas operacionais",
                      "Sistemas digitais",
                      "Paradigmas de linguagens de programação",
                      "Teoria da computação",
                      "Teoria dos grafos",
                      "Fundamentos e técnicas de programação"]
TECHNOLOGY_SUBJECTS = ["Banco de dados",
                       "Compiladores",
                       "Computação gráfica e processamento de imagem",
                       "Engenharia de software e interação homem-computador",
                       "Inteligência artificial e computacional",
                       "Redes de computadores",
                       "Sistemas distribuídos"]
HUMAN_SUBJECTS = ["Ética, computador e sociedade"]
SENIOR_STUDENT_CODE = 0
DIR_PATH = os.path.join(os.path.dirname(__file__), "../")
NUM_ENADE_EXAM_QUESTIONS = 40
MAX_SUBJECTS_PER_QUESTION = 3
CODE_BLANK_DIS_ANSWER = 333
CODE_BLANK_OBJ_ANSWER = "."
CODE_DELETION_OBJ_ANSWER = "*"  # rasura
CODE_CANCELLED_DIS_QUESTION = 335
CODE_CANCELLED_OBJ_QUESTION = ["8", "9"]
BLANK_ANSWER_LABEL = "branco"
CANCELLED_LABEL = "nula"
DELETION_ANSWER_LABEL = "rasura"
VAlID_ANSWER_LABEL = "ok"
CODE_UFPA_COURSE = 12025 #13881
STUDENT_CODE_PRESENT = 555
STUDENT_CODE_ABSENT = 222
PRESENCE_COLUMN = "TP_PRES"
ENADE_DATA_DIR = os.path.join(DATA_DIR, "enade")
SUBJECT_DF_NAME = "classificacao_charao.csv"
SUBJECT_DF_PATH = os.path.join(DATA_DIR, SUBJECT_DF_NAME)
SUBJECT_CONTENT_COLUMNS = ["conteudo1", "conteudo2", "conteudo3"]
