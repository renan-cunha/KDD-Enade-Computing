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
CODE_COURSE = '12025' #13881
STUDENT_CODE_PRESENT = 555
STUDENT_CODE_ABSENT = 222
PRESENCE_COLUMN = "TP_PRES"
ENADE_DATA_DIR = os.path.join(DATA_DIR, "enade")
SUBJECT_DF_NAME = "classificacao_charao.csv"
SUBJECT_DF_PATH = os.path.join(DATA_DIR, SUBJECT_DF_NAME)
SUBJECT_CONTENT_COLUMNS = ["conteudo1", "conteudo2", "conteudo3"]

DTYPES = {"DS_VT_ESC_OFG": str,
          "DS_VT_ESC_OCE": str,
          "DS_VT_ACE_OCE": str,
          "DS_VT_ACE_OFG": str,
          "NT_OBJ_CE": str,
          "CO_IES": str,
          "CO_CURSO": str,
          "co_curso": str,
          "CO_MUNIC_CURSO": str,
          "vt_esc_ofg": str,
          "vt_esc_oce": str,
          "vt_ace_oce": str,
          "vt_ace_ofg": str,
          "nt_obj_ce": str,
          "co_grupo": int,
          "nt_fg_d2": float,
          "nt_ce_d1": float,
          "nt_ce_d2": float,
          "nt_ce_d3": float,
          "nt_ce_d4": float,
          "nt_ce_d5": float,
          "nt_ce_d6": float,
          "nt_ce_d7": float,
          "nt_ce_d8": float,
          "nt_ce_d9": float,
          "nt_ce_d10": float,
          "nt_ce_d11": float,
          "nt_ce_d12": float,
          "nt_ce_d13": float,
          "nt_ce_d14": float,
          "nt_ce_d15": float,
          "nt_ce_d16": float,
          "nt_dis_ce": float
          }

for i in range(1, 40+1):
    DTYPES[f"TP_SCE_D{i}"] = float
    DTYPES[f"tp_sce_d{i}"] = float
    DTYPES[f"TP_SFG_D{i}"] = float
    DTYPES[f"tp_sfg_d{i}"] = float
