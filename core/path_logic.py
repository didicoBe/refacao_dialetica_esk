import os
import shutil
import logging
import time
from PyPDF2 import PdfReader

logging.basicConfig(
    filename='enviar_lote.log',
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def pega_pasta_lote_capa(gramatura, tipo, formato):
    # Convertendo para maiúsculo para padronizar a comparação
    tipo = tipo.upper()
    gramatura = gramatura.upper()
    formato = formato.upper()

    # Definindo as pastas para cada combinação possível
    pastas = {
        "140X210": {
            "FOSCO": {
                "300": r"D:\B2B\EDITORA DIALETICA\MONTALOTE\CAPAS\CAPA 300 FOSCO\CAPA 300 FOSCO 14X21",
                "250": r"D:\B2B\EDITORA DIALETICA\MONTALOTE\CAPAS\CAPA 250 FOSCO\CAPA 250 FOSCO 14X21"
            },
            "BRILHO": {
                "300": r"D:\B2B\EDITORA DIALETICA\MONTALOTE\CAPAS\CAPA 300 BRILHO\CAPA 300 BRILHO 14X21"
            }
        },
        "115X180": {
            "FOSCO": {
                "300": r"D:\B2B\EDITORA DIALETICA\MONTALOTE\CAPAS\CAPA 300 FOSCO\CAPA 300 FOSCO 115X180",
                "250": r"D:\B2B\EDITORA DIALETICA\MONTALOTE\CAPAS\CAPA 300 FOSCO\CAPA 300 FOSCO 115X180"
            },
            "BRILHO": {
                "300": r"D:\B2B\EDITORA DIALETICA\MONTALOTE\CAPAS\CAPA 300 BRILHO\CAPA 300 BRILHO 115X180"
            }
        },
        "110X180": {
            "FOSCO": {
                "300": r"D:\B2B\EDITORA DIALETICA\MONTALOTE\CAPAS\CAPA 300 FOSCO\CAPA 300 FOSCO 11X18"
            },
            "BRILHO": {
                "300": r"D:\B2B\EDITORA DIALETICA\MONTALOTE\CAPAS\CAPA 300 BRILHO\CAPA 300 BRILHO 11X18"
            }
        },
        "155X230": {
            "FOSCO": {
                "300": r"D:\B2B\EDITORA DIALETICA\MONTALOTE\CAPAS\CAPA 300 FOSCO\CAPA 300 FOSCO 155X230"
            },
            "BRILHO": {
                "300": r"D:\B2B\EDITORA DIALETICA\MONTALOTE\CAPAS\CAPA 300 BRILHO\CAPA 300 BRILHO 155X230"
            }
        },
        "210X297": {
            "FOSCO": {
                "300": r"D:\B2B\EDITORA DIALETICA\MONTALOTE\CAPAS\CAPA 300 FOSCO\CAPA 300 FOSCO 210X297"
            },
            "BRILHO": {
                "300": r"D:\B2B\EDITORA DIALETICA\MONTALOTE\CAPAS\CAPA 300 BRILHO\CAPA 300 BRILHO 210X297"
            }
        },
        "150X220": {
            "FOSCO": {
                "300": r"D:\B2B\EDITORA DIALETICA\MONTALOTE\CAPAS\CAPA 300 FOSCO\CAPA_300_150X220_TO_155X230_FOSCO"
            },
            "BRILHO": {
                "300": r"D:\B2B\EDITORA DIALETICA\MONTALOTE\CAPAS\CAPA 300 BRILHO\CAPA_300_150X220_TO_155X230_BRILHO"
            }
        },
        "160X230": {
            "FOSCO": {
                "300": r"D:\B2B\EDITORA DIALETICA\MONTALOTE\CAPAS\CAPA 300 FOSCO\CAPA_300_150X220_TO_155X230_FOSCO"
            },
            "BRILHO": {
                "300": r"D:\B2B\EDITORA DIALETICA\MONTALOTE\CAPAS\CAPA 300 BRILHO\CAPA_300_150X220_TO_155X230_BRILHO"
            }
        },
        "200X200": {
            "FOSCO": {
                "300": r"D:\B2B\EDITORA DIALETICA\MONTALOTE\CAPAS\CAPA 300 FOSCO\CAPA 300 FOSCO 200X200"
            },
            "BRILHO": {
                "250": r"D:\B2B\EDITORA DIALETICA\MONTALOTE\CAPAS\CAPA 250 BRILHO\200X200"
            }
        },
        "148X210": {
            "FOSCO": {
                "300": r"D:\B2B\EDITORA DIALETICA\MONTALOTE\CAPAS\CAPA 300 FOSCO\CAPA 300 FOSCO 155X230"
            },
            "BRILHO": {
                "300": r"D:\B2B\EDITORA DIALETICA\MONTALOTE\CAPAS\CAPA 300 BRILHO\CAPA 300 BRILHO 155X230"
            }
        },
        "138X210": {
            "FOSCO": {
                "300": r"D:\B2B\EDITORA DIALETICA\MONTALOTE\CAPAS\CAPA 300 FOSCO\CAPA 300 FOSCO 155X230"
            },
            "BRILHO": {
                "300": r"D:\B2B\EDITORA DIALETICA\MONTALOTE\CAPAS\CAPA 300 BRILHO\CAPA 300 BRILHO 155X230"
            }
        }
    }

    # Usando o dicionário para encontrar a pasta correta
    try:
        final = pastas[formato][tipo][gramatura]
    except KeyError:
        final = ""  # Se não houver correspondência, retornamos uma string vazia

    return final

def pega_pasta_lote_miolo(cores_miolo, papel_miolo, gramatura_miolo, formato_miolo):
    # Convertendo para maiúsculo para padronizar a comparação
    cores_miolo = cores_miolo.upper()
    papel_miolo = papel_miolo.upper()
    gramatura_miolo = gramatura_miolo.upper()
    formato_miolo = formato_miolo.upper()

    # Definindo as pastas para cada combinação possível
    pastas = {
        "1X1": {
            "POLEN": {
                "80": {
                    "110X180": r"D:\B2B\EDITORA DIALETICA\MONTALOTE\MIOLOS\MIOLO 1X1\POLEN 80\MIOLO_POLEN_80_11X18",
                    "210X140": r"D:\B2B\EDITORA DIALETICA\MONTALOTE\MIOLOS\MIOLO 1X1\POLEN 80\MIOLO_POLEN_80_21X14",
                    "140X210": r"D:\B2B\EDITORA DIALETICA\MONTALOTE\MIOLOS\MIOLO 1X1\POLEN 80\MIOLO_POLEN_80_21X14",
                    "155X230": r"D:\B2B\EDITORA DIALETICA\MONTALOTE\MIOLOS\MIOLO 1X1\POLEN 80\MIOLO_POLEN_80_155X230",
                    "115X180": r"D:\B2B\EDITORA DIALETICA\MONTALOTE\MIOLOS\MIOLO 1X1\POLEN 80\MIOLO_POLEN_80_115X180",
                    "148X210": r"D:\B2B\EDITORA DIALETICA\MONTALOTE\MIOLOS\MIOLO 1X1\POLEN 80\MIOLO_POLEN_80_148X210",
                    "138X210": r"D:\B2B\EDITORA DIALETICA\MONTALOTE\MIOLOS\MIOLO 1X1\POLEN 80\MIOLO_POLEN_80_138X210",
                    "210X297": r"D:\B2B\EDITORA DIALETICA\MONTALOTE\MIOLOS\MIOLO 1X1\POLEN 80\MIOLO_POLEN_80_210X297",
                    "160X230": r"D:\B2B\EDITORA DIALETICA\MONTALOTE\MIOLOS\MIOLO 1X1\POLEN 80\MIOLO_POLEN_80_155X230_DISTORCIDO",
                }
            },
            "OFFSET": {
                "75": {
                    "140X210": r"D:\B2B\EDITORA DIALETICA\MONTALOTE\MIOLOS\MIOLO 1X1\OFFSET 75\MIOLO-OFFSET75_14X21",
                    "155X230": r"D:\B2B\EDITORA DIALETICA\MONTALOTE\MIOLOS\MIOLO 1X1\OFFSET 75\MIOLO_OFFSET75_155X230",
                    "115X180": r"D:\B2B\EDITORA DIALETICA\MONTALOTE\MIOLOS\MIOLO 1X1\OFFSET 75\MIOLO_OFFSET75_115X180",
                    "148X210": r"D:\B2B\EDITORA DIALETICA\MONTALOTE\MIOLOS\MIOLO 1X1\OFFSET 75\MIOLO_OFFSET75_148X210",
                    "138X210": r"D:\B2B\EDITORA DIALETICA\MONTALOTE\MIOLOS\MIOLO 1X1\OFFSET 75\MIOLO_OFFSET75_138X210",
                    "210X297": r"D:\B2B\EDITORA DIALETICA\MONTALOTE\MIOLOS\MIOLO 1X1\OFFSET 75\MIOLO_OFFSET75_210X297",
                    "160X230": r"D:\B2B\EDITORA DIALETICA\MONTALOTE\MIOLOS\MIOLO 1X1\OFFSET 75\MIOLO_OFFSET_75_155X230_DISTORCIDO",
                },
                "63": {
                    "155X230": r"D:\B2B\EDITORA DIALETICA\MONTALOTE\MIOLOS\MIOLO 1X1\OFFSET 63\MIOLO_OFFSET63_155X230",
                    "205X275": r"D:\B2B\EDITORA DIALETICA\MONTALOTE\MIOLOS\MIOLO 1X1\OFFSET 63\MIOLO_OFFSET63_205X275",
                },
                "90": {
                    "140X210": r"D:\B2B\EDITORA DIALETICA\MONTALOTE\MIOLOS\MIOLO 1X1\OFFSET 90\MIOLO_OFFSET90_14X21",
                },
                "120": {
                    "140X210": r"D:\B2B\EDITORA DIALETICA\MONTALOTE\MIOLOS\MIOLO 1X1\OFFSET 120\MIOLO_OFFSET_120_14X21",
                }
            },
            "COUCHE": {
                "150": {
                    "140X210": r"D:\B2B\EDITORA DIALETICA\MONTALOTE\MIOLOS\MIOLO 1X1\COUCHE FOSCO 150\MIOLO_COUCHE FOSCO_150_14X21",
                    "230X155": r"D:\B2B\EDITORA DIALETICA\\INPUT\\MIOLOS\\MIOLO 4X4\\COUCHE_BRILHO_150\\MIOLO_COUCHE_BRILHO_150_230X155_PAISAGEM",
                }
            }
        },
        "4X4": {
            "POLEN": {
                "80": {
                    "155X230": r"D:\B2B\EDITORA DIALETICA\MONTALOTE\MIOLOS\MIOLO 4X4\POLEN80\MIOLO_POLEN80_155X230",
                    "210X140": r"D:\B2B\EDITORA DIALETICA\MONTALOTE\MIOLOS\MIOLO 4X4\POLEN80\MIOLO_POLEN80_210X140",
                    "115X180": r"D:\B2B\EDITORA DIALETICA\MONTALOTE\MIOLOS\MIOLO 4X4\POLEN80\MIOLO_POLEN80_115X180",
                    "148X210": r"D:\B2B\EDITORA DIALETICA\MONTALOTE\MIOLOS\MIOLO 4X4\POLEN80\MIOLO_POLEN80_148X210",
                    "150X220": r"D:\B2B\EDITORA DIALETICA\MONTALOTE\MIOLOS\MIOLO 4X4\POLEN80\MIOLO_POLEN80_150X220_TO_155X230",
                    "200X200": r"D:\B2B\EDITORA DIALETICA\MONTALOTE\MIOLOS\MIOLO 4X4\POLEN80\MIOLO_POLEN80_200X200",
                    "205X275": r"D:\B2B\EDITORA DIALETICA\MONTALOTE\MIOLOS\MIOLO 4X4\POLEN80\MIOLO_POLEN80_205X275",
                    "210X297": r"D:\B2B\EDITORA DIALETICA\MONTALOTE\MIOLOS\MIOLO 4X4\POLEN80\MIOLO_POLEN80_210X297",
                }
            },
            "OFFSET": {
                "75": {
                    "155X230": r"D:\B2B\EDITORA DIALETICA\MONTALOTE\MIOLOS\MIOLO 4X4\OFFSET75\MIOLO_OFFSE75_155X230",
                    "210X140": r"D:\B2B\EDITORA DIALETICA\MONTALOTE\MIOLOS\MIOLO 4X4\OFFSET75\MIOLO_OFFSET75_210X140",
                    "200X200": r"D:\B2B\EDITORA DIALETICA\MONTALOTE\MIOLOS\MIOLO 4X4\OFFSET75\MIOLO_OFFSET75_200X200",
                }
            },
            "COUCHE": {
                "150": {
                    "155X230": r"D:\B2B\EDITORA DIALETICA\MONTALOTE\MIOLOS\MIOLO 4X4\COUCHE_BRILHO_150\MIOLO_COUCHE_BRILHO_150_155X230",
                    "230X155": r"D:\B2B\EDITORA DIALETICA\MONTALOTE\MIOLOS\MIOLO 4X4\COUCHE_BRILHO_150\MIOLO_COUCHE_BRILHO_150_230X155_PAISAGEM",
                    "200X200": r"D:\B2B\EDITORA DIALETICA\MONTALOTE\MIOLOS\MIOLO 4X4\COUCHE_BRILHO_150\MIOLO_COUCHE_BRILHO_150_200X00",
                }
            }
        }
    }

    # Usando o dicionário para encontrar a pasta correta
    try:
        final = pastas[cores_miolo][papel_miolo][gramatura_miolo][formato_miolo]
    except KeyError:
        final = ""  # Se não houver correspondência, retornamos uma string vazia

    return final

def pega_pasta_lote_capa_dura(gramatura, tipo, formato):
    # Convertendo para maiúsculo para padronizar a comparação
    tipo = tipo.upper()
    gramatura = gramatura.upper()  # Embora a gramatura não esteja sendo usada, deixei a conversão para possível uso futuro.
    formato = formato.upper()

    # Definindo as pastas para cada combinação possível de capa dura
    pastas = {
        "155X230": {
            "FOSCO": r"D:\B2B\EDITORA DIALETICA\MONTALOTE\CAPAS\CAPAS DURA\CAPADURA_230X155",
            "BRILHO": r"D:\B2B\EDITORA DIALETICA\MONTALOTE\CAPAS\CAPAS DURA\CAPADURA_230X155"
        },
        "230X155": {
            "FOSCO": r"D:\B2B\EDITORA DIALETICA\MONTALOTE\CAPAS\CAPAS DURA\230X155_RETRATO",
            "BRILHO": r"D:\B2B\EDITORA DIALETICA\MONTALOTE\CAPAS\CAPAS DURA\230X155_RETRATO"
        },
        "140X210": {
            "FOSCO": r"D:\B2B\EDITORA DIALETICA\MONTALOTE\CAPAS\CAPAS DURA\CAPADURA_140X210",
            "BRILHO": r"D:\B2B\EDITORA DIALETICA\MONTALOTE\CAPAS\CAPAS DURA\CAPADURA_140X210"
        },
        "200X200": {
            "FOSCO": r"D:\B2B\EDITORA DIALETICA\MONTALOTE\CAPAS\CAPAS DURA\CAPADURA_200X200",
            "BRILHO": r"D:\B2B\EDITORA DIALETICA\MONTALOTE\CAPAS\CAPAS DURA\CAPADURA_200X200"
        }
    }

    # Usando o dicionário para encontrar a pasta correta
    try:
        final = pastas[formato][tipo]
    except KeyError:
        final = ""  # Se não houver correspondência, retornamos uma string vazia

    return final

def pega_pasta_capa(gramatura, tipo, formato):
    # Convertendo para maiúsculo para padronizar a comparação
    formato = formato.upper()
    tipo = tipo.upper()
    gramatura = gramatura.upper()

    # Definindo as pastas para cada combinação possível de capa sem lote
    pastas = {
        "140X210": {
            "FOSCO": {
                "300": r"D:\B2B\EDITORA DIALETICA\INPUT\CAPAS\CAPA 300 FOSCO\CAPA 300 FOSCO 14X21",
                "250": r"D:\B2B\EDITORA DIALETICA\INPUT\CAPAS\CAPA 250 FOSCO\CAPA 250 FOSCO 14X21"
            },
            "BRILHO": {
                "300": r"D:\B2B\EDITORA DIALETICA\INPUT\CAPAS\CAPA 300 BRILHO\CAPA 300 BRILHO 14X21",
                "250": r"D:\B2B\EDITORA DIALETICA\INPUT\CAPAS\CAPA 250 BRILHO\CAPA 250 BRILHO 14X21"
            }
        },
        "110X180": {
            "FOSCO": {
                "300": r"D:\B2B\EDITORA DIALETICA\INPUT\CAPAS\CAPA 300 FOSCO\CAPA 300 FOSCO 11X18",
                "250": r"D:\B2B\EDITORA DIALETICA\INPUT\CAPAS\CAPA 250 FOSCO\CAPA 250 FOSCO 11X18"
            },
            "BRILHO": {
                "300": r"D:\B2B\EDITORA DIALETICA\INPUT\CAPAS\CAPA 300 BRILHO\CAPA 300 BRILHO 11X18",
                "250": r"D:\B2B\EDITORA DIALETICA\INPUT\CAPAS\CAPA 250 BRILHO\CAPA 250 BRILHO 11X18"
            }
        },
        "155X230": {
            "FOSCO": {
                "300": r"D:\B2B\EDITORA DIALETICA\INPUT\CAPAS\CAPA 300 FOSCO"
            }
        },
        "200X200": {
            "FOSCO": {
                "300": r"D:\B2B\EDITORA DIALETICA\INPUT\CAPAS\CAPA 300 FOSCO\CAPA 300 FOSCO 200X200"
            }
        }
    }

    # Usando o dicionário para encontrar a pasta correta
    try:
        final = pastas[formato][tipo][gramatura]
    except KeyError:
        final = ""  # Se não houver correspondência, retornamos uma string vazia

    return final

def pega_pasta_capa_dura_input(gramatura, tipo, formato):
    # Convertendo para maiúsculo para padronizar a comparação
    formato = formato.upper()
    tipo = tipo.upper()
    gramatura = gramatura.upper()

    # Definindo as pastas para cada combinação possível de capa dura
    pastas = {
        "230X155": {
            "FOSCO": r"D:\B2B\EDITORA DIALETICA\INPUT\CAPAS\CAPAS DURA\CAPADURA_230X155",
            "BRILHO": r"D:\B2B\EDITORA DIALETICA\INPUT\CAPAS\CAPAS DURA\CAPADURA_230X155"
        },
        "140X210": {
            "FOSCO": r"D:\B2B\EDITORA DIALETICA\INPUT\CAPAS\CAPAS DURA\CAPADURA_140X210",
            "BRILHO": r"D:\B2B\EDITORA DIALETICA\INPUT\CAPAS\CAPAS DURA\CAPADURA_140X210"
        },
        "DEFAULT": {
            "FOSCO": r"D:\B2B\EDITORA DIALETICA\INPUT\CAPAS\CAPAS DURA\CAPADURA_GENERICO",
            "BRILHO": r"D:\B2B\EDITORA DIALETICA\INPUT\CAPAS\CAPAS DURA\CAPADURA_GENERICO"
        }
    }

    # Usando o dicionário para encontrar a pasta correta
    try:
        final = pastas[formato][tipo]
    except KeyError:
        # Se não houver correspondência específica, usar o valor padrão
        final = pastas["DEFAULT"][tipo]

    return final

def pega_pasta_miolo(cores_miolo, papel_miolo, gramatura_miolo, formato_miolo):
    # Convertendo para maiúsculo para padronizar a comparação
    cores_miolo = cores_miolo.upper()
    papel_miolo = papel_miolo.upper()
    gramatura_miolo = gramatura_miolo.upper()
    formato_miolo = formato_miolo.upper()

    # Definindo as pastas para cada combinação possível de miolos
    pastas = {
        "1X1": {
            "POLEN": {
                "80": {
                    "110X180": r"D:\B2B\EDITORA DIALETICA\INPUT\MIOLOS\MIOLO 1X1\POLEN 80\MIOLO_POLEN_80_11X18",
                    "210X140": r"D:\B2B\EDITORA DIALETICA\INPUT\MIOLOS\MIOLO 1X1\POLEN 80\MIOLO_POLEN_80_21X14",
                    "140X210": r"D:\B2B\EDITORA DIALETICA\INPUT\MIOLOS\MIOLO 1X1\POLEN 80\MIOLO_POLEN_80_21X14",
                    "155X230": r"D:\B2B\EDITORA DIALETICA\INPUT\MIOLOS\MIOLO 1X1\POLEN 80\MIOLO_POLEN_80_155X230",
                    "115X180": r"D:\B2B\EDITORA DIALETICA\MONTALOTE\MIOLOS\MIOLO 1X1\POLEN 80\MIOLO_POLEN_80_115X180"
                }
            },
            "OFFSET": {
                "75": {
                    "140X210": r"D:\B2B\EDITORA DIALETICA\INPUT\MIOLOS\MIOLO 1X1\OFFSET 75\MIOLO-OFFSET75_14X21",
                    "155X230": r"D:\B2B\EDITORA DIALETICA\INPUT\MIOLOS\MIOLO 1X1\OFFSET 75\MIOLO_OFFSET75_155X230",
                    "115X180": r"D:\B2B\EDITORA DIALETICA\INPUT\MIOLOS\MIOLO 1X1\OFFSET 75\MIOLO_OFFSET75_115X180"
                },
                "90": {
                    "140X210": r"D:\B2B\EDITORA DIALETICA\INPUT\MIOLOS\MIOLO 1X1\OFFSET 90\MIOLO_OFFSET90_14X21"
                },
                "120": {
                    "140X210": r"D:\B2B\EDITORA DIALETICA\INPUT\MIOLOS\MIOLO 1X1\OFFSET 120\MIOLO_OFFSET_120_14X21"
                }
            },
            "COUCHE FOSCO": {
                "150": {
                    "140X210": r"D:\B2B\EDITORA DIALETICA\INPUT\MIOLOS\MIOLO 1X1\COUCHE FOSCO 150\MIOLO_COUCHE FOSCO_150_14X21"
                }
            }
        },
        "4X4": {
            "POLEN": {
                "80": {
                    "155X230": r"D:\B2B\EDITORA DIALETICA\INPUT\MIOLOS\MIOLO 4X4\POLEN80\MIOLO_POLEN80_155X230",
                    "210X140": r"D:\B2B\EDITORA DIALETICA\INPUT\MIOLOS\MIOLO 4X4\POLEN80\MIOLO_POLEN80_210X140"
                }
            },
            "OFFSET": {
                "75": {
                    "155X230": r"D:\B2B\EDITORA DIALETICA\INPUT\MIOLOS\MIOLO 4X4\OFFSET75\MIOLO_OFFSE75_155X230",
                    "210X140": r"D:\B2B\EDITORA DIALETICA\INPUT\MIOLOS\MIOLO 4X4\OFFSET75\MIOLO_OFFSET75_210X140",
                    "200X200": r"D:\B2B\EDITORA DIALETICA\INPUT\MIOLOS\MIOLO 4X4\OFFSET75\MIOLO_OFFSET75_200X200"
                }
            },
            "COUCHE": {
                "150": {
                    "155X230": r"D:\B2B\EDITORA DIALETICA\INPUT\MIOLOS\MIOLO 4X4\COUCHE_BRILHO_150\MIOLO_COUCHE_BRILHO_150_155X230",
                    "230X155": r"D:\B2B\EDITORA DIALETICA\INPUT\MIOLOS\MIOLO 4X4\COUCHE_BRILHO_150\MIOLO_COUCHE_BRILHO_150_230X155_PAISAGEM",
                    "200X200": r"D:\B2B\EDITORA DIALETICA\INPUT\MIOLOS\MIOLO 4X4\COUCHE_BRILHO_150\MIOLO_COUCHE_BRILHO_150_200X00"
                }
            }
        }
    }

    # Usando o dicionário para encontrar a pasta correta
    try:
        final = pastas[cores_miolo][papel_miolo][gramatura_miolo][formato_miolo]
    except KeyError:
        final = ""  # Se não houver correspondência, retornamos uma string vazia

    return final

def enviar_lote(origem, destino, limite):
    try:
        # Verifica se o diretório de destino existe; se não, cria-o
        if not os.path.exists(destino):
            os.makedirs(destino)

        # Obtém os arquivos no diretório de origem, limitado ao valor fornecido
        arquivos = os.listdir(origem)[:limite]  # Limita a quantidade de arquivos a serem movidos

        for arquivo in arquivos:
            origem_arquivo = os.path.join(origem, arquivo)
            destino_arquivo = os.path.join(destino, arquivo)

            # Move o arquivo do diretório de origem para o destino
            shutil.move(origem_arquivo, destino_arquivo)
            logging.info(f"Arquivo movido: {origem_arquivo} -> {destino_arquivo}")

    except Exception as e:
        logging.error(f"Erro ao mover arquivos do lote de {origem} para {destino}: {e}")
        raise


def enviar_tudo_lote():
    # Configuração do logging
    logging.basicConfig(
        filename='enviar_tudo_lote.log',
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    caminhos_capa = [
        (r"D:\B2B\EDITORA DIALETICA\MONTALOTE\CAPAS\CAPA 300 FOSCO\CAPA 300 FOSCO 14X21", r"D:\B2B\EDITORA DIALETICA\INPUT\CAPAS\CAPA 300 FOSCO\CAPA 300 FOSCO 14X21"),
        (r"D:\B2B\EDITORA DIALETICA\MONTALOTE\CAPAS\CAPA 250 FOSCO\CAPA 250 FOSCO 14X21", r"D:\B2B\EDITORA DIALETICA\INPUT\CAPAS\CAPA 250 FOSCO\CAPA 250 FOSCO 14X21"),
        (r"D:\B2B\EDITORA DIALETICA\MONTALOTE\CAPAS\CAPA 300 BRILHO\CAPA 300 BRILHO 14X21", r"D:\B2B\EDITORA DIALETICA\INPUT\CAPAS\CAPA 300 BRILHO\CAPA 300 BRILHO 14X21"),
        (r"D:\B2B\EDITORA DIALETICA\MONTALOTE\CAPAS\CAPA 300 FOSCO\CAPA 300 FOSCO 115X180", r"D:\B2B\EDITORA DIALETICA\INPUT\CAPAS\CAPA 300 FOSCO\CAPA 300 FOSCO 115X180"),
        (r"D:\B2B\EDITORA DIALETICA\MONTALOTE\CAPAS\CAPA 300 BRILHO\CAPA 300 BRILHO 115X180", r"D:\B2B\EDITORA DIALETICA\INPUT\CAPAS\CAPA 300 BRILHO\CAPA 300 BRILHO 115X180"),
        (r"D:\B2B\EDITORA DIALETICA\MONTALOTE\CAPAS\CAPA 300 FOSCO\CAPA 300 FOSCO 11X18", r"D:\B2B\EDITORA DIALETICA\INPUT\CAPAS\CAPA 300 FOSCO\CAPA 300 FOSCO 11X18"),
        (r"D:\B2B\EDITORA DIALETICA\MONTALOTE\CAPAS\CAPA 300 BRILHO\CAPA 300 BRILHO 11X18", r"D:\B2B\EDITORA DIALETICA\INPUT\CAPAS\CAPA 300 BRILHO\CAPA 300 BRILHO 11X18"),
        (r"D:\B2B\EDITORA DIALETICA\MONTALOTE\CAPAS\CAPA 300 FOSCO\CAPA 300 FOSCO 155X230", r"D:\B2B\EDITORA DIALETICA\INPUT\CAPAS\CAPA 300 FOSCO\CAPA 300 FOSCO 155X230"),
        (r"D:\B2B\EDITORA DIALETICA\MONTALOTE\CAPAS\CAPA 300 BRILHO\CAPA 300 BRILHO 155X230", r"D:\B2B\EDITORA DIALETICA\INPUT\CAPAS\CAPA 300 BRILHO\CAPA 300 BRILHO 155X230"),
        (r"D:\B2B\EDITORA DIALETICA\MONTALOTE\CAPAS\CAPA 300 FOSCO\CAPA 300 FOSCO 210X297", r"D:\B2B\EDITORA DIALETICA\INPUT\CAPAS\CAPA 300 FOSCO\CAPA 300 FOSCO 210X297"),
        (r"D:\B2B\EDITORA DIALETICA\MONTALOTE\CAPAS\CAPA 300 BRILHO\CAPA 300 BRILHO 210X297", r"D:\B2B\EDITORA DIALETICA\INPUT\CAPAS\CAPA 300 BRILHO\CAPA 300 BRILHO 210X297"),
        (r"D:\B2B\EDITORA DIALETICA\MONTALOTE\CAPAS\CAPA 300 FOSCO\CAPA_300_150X220_TO_155X230_FOSCO", r"D:\B2B\EDITORA DIALETICA\INPUT\CAPAS\CAPA 300 FOSCO\CAPA_300_150X220_TO_155X230_FOSCO"),
        (r"D:\B2B\EDITORA DIALETICA\MONTALOTE\CAPAS\CAPA 300 BRILHO\CAPA_300_150X220_TO_155X230_BRILHO", r"D:\B2B\EDITORA DIALETICA\INPUT\CAPAS\CAPA 300 BRILHO\CAPA_300_150X220_TO_155X230_BRILHO"),
        (r"D:\B2B\EDITORA DIALETICA\MONTALOTE\CAPAS\CAPA 300 FOSCO\CAPA 300 FOSCO 200X200", r"D:\B2B\EDITORA DIALETICA\INPUT\CAPAS\CAPA 300 FOSCO\CAPA 300 FOSCO 200X200"),
        (r"D:\B2B\EDITORA DIALETICA\MONTALOTE\CAPAS\CAPAS DURA\CAPA DURA_230X155_PAISAGEM", r"D:\B2B\EDITORA DIALETICA\INPUT\CAPAS\CAPAS DURA\CAPA DURA_230X155_PAISAGEM"),
        (r"D:\B2B\EDITORA DIALETICA\MONTALOTE\CAPAS\CAPAS DURA\CAPADURA_140X210", r"D:\B2B\EDITORA DIALETICA\INPUT\CAPAS\CAPAS DURA\CAPADURA_140X210"),
        (r"D:\B2B\EDITORA DIALETICA\MONTALOTE\CAPAS\CAPAS DURA\CAPADURA_200X200", r"D:\B2B\EDITORA DIALETICA\INPUT\CAPAS\CAPAS DURA\CAPADURA_200X200"),
        (r"D:\B2B\EDITORA DIALETICA\MONTALOTE\CAPAS\CAPAS DURA\CAPADURA_230X155", r"D:\B2B\EDITORA DIALETICA\INPUT\CAPAS\CAPAS DURA\CAPADURA_230X155"),
    ]


    # Caminhos para envio dos lotes de miolo
    # Caminhos para envio dos lotes de miolo
    caminhos_miolo = [
        (r"D:\B2B\EDITORA DIALETICA\MONTALOTE\MIOLOS\MIOLO 1X1\POLEN 80\MIOLO_POLEN_80_11X18", r"D:\B2B\EDITORA DIALETICA\INPUT\MIOLOS\MIOLO 1X1\POLEN 80\MIOLO_POLEN_80_11X18"),
        (r"D:\B2B\EDITORA DIALETICA\MONTALOTE\MIOLOS\MIOLO 1X1\POLEN 80\MIOLO_POLEN_80_21X14", r"D:\B2B\EDITORA DIALETICA\INPUT\MIOLOS\MIOLO 1X1\POLEN 80\MIOLO_POLEN_80_21X14"),
        (r"D:\B2B\EDITORA DIALETICA\MONTALOTE\MIOLOS\MIOLO 1X1\POLEN 80\MIOLO_POLEN_80_155X230", r"D:\B2B\EDITORA DIALETICA\INPUT\MIOLOS\MIOLO 1X1\POLEN 80\MIOLO_POLEN_80_155X230"),
        (r"D:\B2B\EDITORA DIALETICA\MONTALOTE\MIOLOS\MIOLO 1X1\POLEN 80\MIOLO_POLEN_80_115X180", r"D:\B2B\EDITORA DIALETICA\INPUT\MIOLOS\MIOLO 1X1\POLEN 80\MIOLO_POLEN_80_115X180"),
        (r"D:\B2B\EDITORA DIALETICA\MONTALOTE\MIOLOS\MIOLO 1X1\OFFSET 75\MIOLO-OFFSET75_14X21", r"D:\B2B\EDITORA DIALETICA\INPUT\MIOLOS\MIOLO 1X1\OFFSET 75\MIOLO-OFFSET75_14X21"),
        (r"D:\B2B\EDITORA DIALETICA\MONTALOTE\MIOLOS\MIOLO 1X1\OFFSET 75\MIOLO_OFFSET75_155X230", r"D:\B2B\EDITORA DIALETICA\INPUT\MIOLOS\MIOLO 1X1\OFFSET 75\MIOLO_OFFSET75_155X230"),
        (r"D:\B2B\EDITORA DIALETICA\MONTALOTE\MIOLOS\MIOLO 1X1\OFFSET 75\MIOLO_OFFSET75_115X180", r"D:\B2B\EDITORA DIALETICA\INPUT\MIOLOS\MIOLO 1X1\OFFSET 75\MIOLO_OFFSET75_115X180"),
        (r"D:\B2B\EDITORA DIALETICA\MONTALOTE\MIOLOS\MIOLO 1X1\OFFSET 75\MIOLO_OFFSET75_210X297", r"D:\B2B\EDITORA DIALETICA\INPUT\MIOLOS\MIOLO 1X1\OFFSET 75\MIOLO_OFFSET75_210X297"),
        (r"D:\B2B\EDITORA DIALETICA\MONTALOTE\MIOLOS\MIOLO 1X1\OFFSET 90\MIOLO_OFFSET90_14X21", r"D:\B2B\EDITORA DIALETICA\INPUT\MIOLOS\MIOLO 1X1\OFFSET 90\MIOLO_OFFSET90_14X21"),
        (r"D:\B2B\EDITORA DIALETICA\MONTALOTE\MIOLOS\MIOLO 1X1\OFFSET 120\MIOLO_OFFSET_120_14X21", r"D:\B2B\EDITORA DIALETICA\INPUT\MIOLOS\MIOLO 1X1\OFFSET 120\MIOLO_OFFSET_120_14X21"),
        (r"D:\B2B\EDITORA DIALETICA\MONTALOTE\MIOLOS\MIOLO 1X1\COUCHE FOSCO 150\MIOLO_COUCHE FOSCO_150_14X21", r"D:\B2B\EDITORA DIALETICA\INPUT\MIOLOS\MIOLO 1X1\COUCHE FOSCO 150\MIOLO_COUCHE FOSCO_150_14X21"),
        (r"D:\B2B\EDITORA DIALETICA\MONTALOTE\MIOLOS\MIOLO 4X4\POLEN80\MIOLO_POLEN80_155X230", r"D:\B2B\EDITORA DIALETICA\INPUT\MIOLOS\MIOLO 4X4\POLEN80\MIOLO_POLEN80_155X230"),
        (r"D:\B2B\EDITORA DIALETICA\MONTALOTE\MIOLOS\MIOLO 4X4\POLEN80\MIOLO_POLEN80_210X140", r"D:\B2B\EDITORA DIALETICA\INPUT\MIOLOS\MIOLO 4X4\POLEN80\MIOLO_POLEN80_210X140"),
        (r"D:\B2B\EDITORA DIALETICA\MONTALOTE\MIOLOS\MIOLO 4X4\OFFSET75\MIOLO_OFFSE75_155X230", r"D:\B2B\EDITORA DIALETICA\INPUT\MIOLOS\MIOLO 4X4\OFFSET75\MIOLO_OFFSE75_155X230"),
        (r"D:\B2B\EDITORA DIALETICA\MONTALOTE\MIOLOS\MIOLO 4X4\OFFSET75\MIOLO_OFFSET75_210X140", r"D:\B2B\EDITORA DIALETICA\INPUT\MIOLOS\MIOLO 4X4\OFFSET75\MIOLO_OFFSET75_210X140"),
        (r"D:\B2B\EDITORA DIALETICA\MONTALOTE\MIOLOS\MIOLO 4X4\OFFSET75\MIOLO_OFFSET75_200X200", r"D:\B2B\EDITORA DIALETICA\INPUT\MIOLOS\MIOLO 4X4\OFFSET75\MIOLO_OFFSET75_200X200"),
        (r"D:\B2B\EDITORA DIALETICA\MONTALOTE\MIOLOS\MIOLO 4X4\COUCHE_BRILHO_150\MIOLO_COUCHE_BRILHO_150_155X230", r"D:\B2B\EDITORA DIALETICA\INPUT\MIOLOS\MIOLO 4X4\COUCHE_BRILHO_150\MIOLO_COUCHE_BRILHO_150_155X230"),
        (r"D:\B2B\EDITORA DIALETICA\MONTALOTE\MIOLOS\MIOLO 4X4\COUCHE_BRILHO_150\MIOLO_COUCHE_BRILHO_150_230X155_PAISAGEM", r"D:\B2B\EDITORA DIALETICA\INPUT\MIOLOS\MIOLO 4X4\COUCHE_BRILHO_150\MIOLO_COUCHE_BRILHO_150_230X155_PAISAGEM"),
        (r"D:\B2B\EDITORA DIALETICA\MONTALOTE\MIOLOS\MIOLO 4X4\COUCHE_BRILHO_150\MIOLO_COUCHE_BRILHO_150_200X00", r"D:\B2B\EDITORA DIALETICA\INPUT\MIOLOS\MIOLO 4X4\COUCHE_BRILHO_150\MIOLO_COUCHE_BRILHO_150_200X00"),
        (r"D:\B2B\EDITORA DIALETICA\MONTALOTE\MIOLOS\MIOLO 4X4\OFFSET75\MIOLO_OFFSET75_115X180", r"D:\B2B\EDITORA DIALETICA\INPUT\MIOLOS\MIOLO 4X4\OFFSET75\MIOLO_OFFSET75_115X180"),
        (r"D:\B2B\EDITORA DIALETICA\MONTALOTE\MIOLOS\MIOLO 4X4\OFFSET75\MIOLO_OFFSET75_148X210", r"D:\B2B\EDITORA DIALETICA\INPUT\MIOLOS\MIOLO 4X4\OFFSET75\MIOLO_OFFSET75_148X210"),
        (r"D:\B2B\EDITORA DIALETICA\MONTALOTE\MIOLOS\MIOLO 4X4\OFFSET75\MIOLO_OFFSET75_150X220_TO_155X230", r"D:\B2B\EDITORA DIALETICA\INPUT\MIOLOS\MIOLO 4X4\OFFSET75\MIOLO_OFFSET75_150X220_TO_155X230"),
        (r"D:\B2B\EDITORA DIALETICA\MONTALOTE\MIOLOS\MIOLO 4X4\OFFSET75\MIOLO_OFFSET75_205X275", r"D:\B2B\EDITORA DIALETICA\INPUT\MIOLOS\MIOLO 4X4\OFFSET75\MIOLO_OFFSET75_205X275"),
        (r"D:\B2B\EDITORA DIALETICA\MONTALOTE\MIOLOS\MIOLO 4X4\OFFSET75\MIOLO_OFFSET75_210X297", r"D:\B2B\EDITORA DIALETICA\INPUT\MIOLOS\MIOLO 4X4\OFFSET75\MIOLO_OFFSET75_210X297"),
        (r"D:\B2B\EDITORA DIALETICA\MONTALOTE\MIOLOS\MIOLO 4X4\POLEN80\MIOLO_POLEN80_115X180", r"D:\B2B\EDITORA DIALETICA\INPUT\MIOLOS\MIOLO 4X4\POLEN80\MIOLO_POLEN80_115X180"),
        (r"D:\B2B\EDITORA DIALETICA\MONTALOTE\MIOLOS\MIOLO 4X4\POLEN80\MIOLO_POLEN80_148X210", r"D:\B2B\EDITORA DIALETICA\INPUT\MIOLOS\MIOLO 4X4\POLEN80\MIOLO_POLEN80_148X210"),
        (r"D:\B2B\EDITORA DIALETICA\MONTALOTE\MIOLOS\MIOLO 4X4\POLEN80\MIOLO_POLEN80_150X220_TO_155X230", r"D:\B2B\EDITORA DIALETICA\INPUT\MIOLOS\MIOLO 4X4\POLEN80\MIOLO_POLEN80_150X220_TO_155X230"),
        (r"D:\B2B\EDITORA DIALETICA\MONTALOTE\MIOLOS\MIOLO 4X4\POLEN80\MIOLO_POLEN80_200X200", r"D:\B2B\EDITORA DIALETICA\INPUT\MIOLOS\MIOLO 4X4\POLEN80\MIOLO_POLEN80_200X200"),
        (r"D:\B2B\EDITORA DIALETICA\MONTALOTE\MIOLOS\MIOLO 4X4\POLEN80\MIOLO_POLEN80_205X275", r"D:\B2B\EDITORA DIALETICA\INPUT\MIOLOS\MIOLO 4X4\POLEN80\MIOLO_POLEN80_205X275"),
        (r"D:\B2B\EDITORA DIALETICA\MONTALOTE\MIOLOS\MIOLO 4X4\POLEN80\MIOLO_POLEN80_210X297", r"D:\B2B\EDITORA DIALETICA\INPUT\MIOLOS\MIOLO 4X4\POLEN80\MIOLO_POLEN80_210X297")
    ]

    total_paginas = 0
    limite_paginas = 7200

    def mover_arquivos(caminhos):
        nonlocal total_paginas
        for src, dest in caminhos:
            try:
                # Verifica e cria o diretório de destino se necessário
                if not os.path.exists(dest):
                    os.makedirs(dest)

                # Caminha por todas as pastas e subpastas na origem
                for root, _, files in os.walk(src):
                    for file in files:
                        if file.lower().endswith('.pdf'):
                            src_file = os.path.join(root, file)
                            dest_file = os.path.join(dest, file)  # Move diretamente para o diretório destino
                            try:
                                # Lê o número de páginas do PDF
                                reader = PdfReader(src_file)
                                num_paginas = len(reader.pages)
                                total_paginas += num_paginas

                                # Move o arquivo PDF
                                shutil.move(src_file, dest_file)
                                logging.info(f"Arquivo PDF movido: {src_file} para {dest_file} - {num_paginas} páginas")

                                # Verifica se o limite foi atingido
                                if total_paginas >= limite_paginas:
                                    logging.info("Limite de páginas atingido, aguardando 20 segundos...")
                                    time.sleep(20)
                                    total_paginas = 0  # Reinicia a contagem após a pausa

                            except Exception as e:
                                logging.error(f"Erro ao processar PDF {src_file}: {e}")

            except Exception as e:
                logging.error(f"Erro ao mover arquivos de {src} para {dest}: {e}")

    try:
        # Enviar lotes de capa
        mover_arquivos(caminhos_capa)
        # Enviar lotes de miolo
        mover_arquivos(caminhos_miolo)
        
    except Exception as erro:
        logging.error(f"Erro ao processar envio de lotes: {erro}")

    logging.info("Envio de todos os lotes finalizado")
