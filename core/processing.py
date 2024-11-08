import shutil
import os
import threading  # Importação do threading para trabalhar com threads
import time  # Importação do time para o delay no loop
import logging  # Importação do módulo logging para salvar logs
from dotenv import load_dotenv  # Importação para carregar variáveis do .env

from database.db_connector import pega_dados_refacao, pega_pedido_por_id, atualiza_status_refacao
from core.pdf_utils import copia_e_add_folha_arquivo_ref
from core.path_logic import pega_pasta_capa, pega_pasta_miolo, pega_pasta_lote_capa, pega_pasta_lote_miolo, enviar_tudo_lote, pega_pasta_lote_capa_dura  # Adicionada a função enviar_tudo_lote

# Configuração do logging
logging.basicConfig(
    filename='reprocessamento.log',
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

from PyQt5.QtCore import QThread, pyqtSignal

# Carrega as variáveis do arquivo .env
load_dotenv()

class Reprocessamento(QThread):
    finished = pyqtSignal()
    error = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.should_stop = False

    def run(self):
        while not self.should_stop:
            try:
                # Verifica se é 16:00h para enviar todos os lotes automaticamente
                current_time = time.localtime()
                if current_time.tm_hour == 16 and current_time.tm_min == 0 and not self.enviado_hoje:
                    try:
                        enviar_tudo_lote()
                        logging.info("Envio automático do lote realizado com sucesso às 16:00h.")
                        self.enviado_hoje = True  # Atualiza a flag para indicar que o envio já ocorreu
                    except Exception as e:
                        logging.error(f"Erro no envio automático do lote às 16:00h: {e}")
                
                # Resetar a flag às 16:01 para que o envio possa ser feito novamente no dia seguinte
                if current_time.tm_hour != 16:
                    self.enviado_hoje = False

                # Pega as configurações do banco de dados do arquivo .env
                db_config = {
                    'host': os.getenv('DB_HOST', 'localhost'),
                    'database': os.getenv('DB_NAME', 'sis3'),
                    'user': os.getenv('DB_USER', 'root'),
                    'password': os.getenv('DB_PASSWORD', '')
                }

                # Realiza o reprocessamento dos dados
                dados = pega_dados_refacao(db_config)
                if not dados:
                    time.sleep(10)  # Esperar 10 segundos antes de verificar novamente
                    continue

                for item in dados:
                    idpedido, tipoid, id, quantidade = item.split('|')

                    # Pega as informações do pedido
                    dados_pedido = pega_pedido_por_id(idpedido, db_config)
                    for item2 in dados_pedido:
                        corta_pedido = item2.split('|')
                        nomedialetica, codproduto, tipodeproduto, numpedido, numitem, isbn, titulodolivro, \
                        subtitulo, editora_selo, tiragem, papelcapa, gramaturacapa, corescapa, \
                        formatoabertocapa, formatodalombada, medidadaorelha, acabamentocapa, papelmiolo, \
                        gramaturamiolo, coresmiolo, formatomiolo, paginasmiolototal, paginasmiolopb, \
                        paginasmiolocor, acabamentolivro, embalagemdolivro, precounitdolivro, tiragemmarcador, \
                        datapedido, data, status, idPedido, marketplace = corta_pedido

                        # Identifica o cliente
                        nomecliente = "Dialetica"

                        # Normaliza acabamentos e tipos de papel
                        acabamentocapa = self.normaliza_acabamento(acabamentocapa)
                        papelmiolo = self.normaliza_papel(papelmiolo)

                        # Encontra os caminhos das pastas
                        caminho_capa = pega_pasta_capa(gramaturacapa, acabamentocapa, formatomiolo)
                        caminho_miolo = pega_pasta_miolo(coresmiolo, papelmiolo, gramaturamiolo, formatomiolo)
                        if (tipodeproduto == "Capa dura"):
                            caminho_lote_capa = pega_pasta_lote_capa_dura(gramaturacapa, acabamentocapa, formatomiolo)
                        else:
                            caminho_lote_capa = pega_pasta_lote_capa(gramaturacapa, acabamentocapa, formatomiolo)

                        caminho_lote_miolo = pega_pasta_lote_miolo(coresmiolo, papelmiolo, gramaturamiolo, formatomiolo)

                        # Busca arquivos pelo ISBN
                        caminho_busca = os.getenv('PATH_REDE', r"\\rede")
                        arquivos = self.encontra_arquivo(caminho_busca, isbn)

                        # Verifica se encontrou os arquivos necessários
                        if not arquivos:
                            logging.warning(f"Arquivos não encontrados para ISBN: {isbn}, Pedido ID: {idpedido}")
                            logging.warning(f"Status não atualizado para PDF não localizado, Pedido ID: {id}")
                            continue

                        arquivo_capa, arquivo_miolo = self.filtra_arquivos(arquivos)

                        if not arquivo_capa:
                            logging.warning(f"Arquivo de capa não encontrado para ISBN: {isbn}, Pedido ID: {idpedido}")
                            logging.warning(f"Status não atualizado para PDF não localizado, Pedido ID: {id}")
                        if not arquivo_miolo:
                            logging.warning(f"Arquivo de miolo não encontrado para ISBN: {isbn}, Pedido ID: {idpedido}")
                            logging.warning(f"Status não atualizado para PDF não localizado, Pedido ID: {id}")

                        # Processa conforme o tipo (Capa, Miolo ou Completo)
                        self.processa_tipo(
                            tipoid, quantidade, arquivo_capa, arquivo_miolo, caminho_lote_capa, caminho_lote_miolo,
                            id, nomecliente, numpedido, isbn, tiragem, titulodolivro, editora_selo, papelmiolo,
                            formatomiolo, tipodeproduto, marketplace, paginasmiolototal, data
                        )

            except Exception as e:
                logging.error(f"Erro no processo de refação: {e}")
                self.error.emit(str(e))

            time.sleep(10)  # Espera antes de reiniciar o loop

    def processa_tipo(self, tipoid, quantidade, arquivo_capa, arquivo_miolo, caminho_lote_capa, caminho_lote_miolo, id, nomecliente, numpedido, isbn, tiragem, titulodolivro, editora_selo, papelmiolo, formatomiolo, tipodeproduto, marketplace, paginasmiolototal, data):
        quantidade = int(quantidade)
        # Pega as configurações do banco de dados do arquivo .env
        db_config = {
            'host': os.getenv('DB_HOST', 'localhost'),
            'database': os.getenv('DB_NAME', 'sis3'),
            'user': os.getenv('DB_USER', 'root'),
            'password': os.getenv('DB_PASSWORD', '')
        }
        
        for i in range(1, quantidade + 1):
            try:
                # Processo para a Capa
                if (tipoid == "Capa" or tipoid == "Completo") and arquivo_capa:
                    novo_caminho = os.path.join(
                        caminho_lote_capa, 
                        f"{id}_REF_{nomecliente}_Capa_Isbn_{isbn}_tiragem_{tiragem}_N_{i}_Pedido_{numpedido}_.pdf"
                    )
                    shutil.copy(arquivo_capa, novo_caminho)
                    if os.path.exists(novo_caminho):
                        logging.info(f"Arquivo de capa copiado com sucesso: {novo_caminho}")
                        atualiza_status_refacao(id, db_config)

                # Processo para o Miolo
                if (tipoid == "Miolo" or tipoid == "Completo") and arquivo_miolo:
                    copia_e_add_folha_arquivo_ref(
                        arquivo_miolo, editora_selo, numpedido, data, titulodolivro, isbn, paginasmiolototal,
                        papelmiolo, formatomiolo, caminho_lote_miolo,
                        f"{id}_REF_{nomecliente}_Miolo_Isbn_{isbn}_paginas_{paginasmiolototal}_tiragem_{tiragem}_N_{i}_Pedido_{numpedido}_",
                        tiragem, tipodeproduto, marketplace
                    )
                    novo_caminho_miolo = os.path.join(
                        caminho_lote_miolo, 
                        f"{id}_REF_{nomecliente}_Miolo_Isbn_{isbn}_paginas_{paginasmiolototal}_tiragem_{tiragem}_N_{i}_Pedido_{numpedido}_.pdf"
                    )
                    if os.path.exists(novo_caminho_miolo):
                        logging.info(f"Arquivo de miolo copiado e folha de rosto adicionada com sucesso: {novo_caminho_miolo}")
                        atualiza_status_refacao(id, db_config)

            except Exception as e:
                logging.error(f"Erro ao processar tipo {tipoid} para o Pedido ID: {id}. Erro: {e}")


    def normaliza_acabamento(self, acabamento):
        acabamento = acabamento.upper()
        if "FOSCA" in acabamento:
            return "FOSCO"
        elif "BRILHO" in acabamento:
            return "BRILHO"
        return acabamento

    def normaliza_papel(self, papel):
        papel = papel.upper()
        if "POLEN" in papel or "POLÉN" in papel:
            return "POLEN"
        return papel

    def encontra_arquivo(self, caminho, isbn):
        arquivos = []
        for root, dirs, files in os.walk(caminho):
            for file in files:
                if isbn in file:
                    arquivos.append(os.path.join(root, file))
        return arquivos

    def filtra_arquivos(self, arquivos):
        arquivo_capa = ""
        arquivo_miolo = ""
        for arquivo in arquivos:
            if "_CAPA" in arquivo.upper():
                arquivo_capa = arquivo
            elif "_MIOLO" in arquivo.upper():
                arquivo_miolo = arquivo
        return arquivo_capa, arquivo_miolo

    def iniciar(self):
        self.thread = self
        self.start()

    def parar(self):
        self.should_stop = True
        self.wait()
