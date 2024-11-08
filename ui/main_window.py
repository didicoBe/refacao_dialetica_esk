import sys
import os
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QMessageBox, QTabWidget, QDesktopWidget
from PyQt5.QtCore import QThread, pyqtSignal
from core.processing import Reprocessamento
from dotenv import load_dotenv, set_key
import shutil
import logging
from core.path_logic import enviar_tudo_lote

# Configuração do logging
logging.basicConfig(
    filename='reprocessamento.log',
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Carregar variáveis do arquivo .env
load_dotenv()

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Define o caminho do ícone, adaptado para o executável empacotado
        if getattr(sys, '_MEIPASS', False):  # Verifica se está no executável criado com PyInstaller
            icon_path = os.path.join(sys._MEIPASS, "icon.ico")
        else:
            icon_path = os.path.join(os.path.dirname(__file__), "icon.ico")

        self.setWindowTitle('Refação Dialetica')
        self.setGeometry(100, 100, 150, 600)
        self.setWindowIcon(QIcon(icon_path))

        # Centraliza a janela
        self.center()

        # Layout principal para conter as abas
        layout = QVBoxLayout()
        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)

        # Criar aba Principal e aba de Configurações
        self.main_tab = QWidget()
        self.config_tab = QWidget()
        self.tabs.addTab(self.main_tab, "Principal")
        self.tabs.addTab(self.config_tab, "Configurações")

        # Configurar layout da aba Principal
        self.init_main_tab()
        self.init_config_tab()
        
        # Setar o layout principal
        self.setLayout(layout)
        self.process_thread = None

    def center(self):
        # Centraliza a janela na tela
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def init_main_tab(self):
        layout = QVBoxLayout()
        self.status_label = QLabel('Clique em "Iniciar" para começar o processamento em background')
        layout.addWidget(self.status_label)

        self.start_btn = QPushButton('Iniciar', self)
        self.start_btn.clicked.connect(self.start_processing)
        layout.addWidget(self.start_btn)

        self.stop_btn = QPushButton('Parar', self)
        self.stop_btn.clicked.connect(self.stop_processing)
        layout.addWidget(self.stop_btn)

        self.send_all_btn = QPushButton('Enviar Tudo', self)
        self.send_all_btn.clicked.connect(self.enviar_tudo)
        layout.addWidget(self.send_all_btn)

        self.main_tab.setLayout(layout)

    def init_config_tab(self):
        layout = QVBoxLayout()

        self.path_label = QLabel('Caminho da Rede:')
        layout.addWidget(self.path_label)
        self.path_input = QLineEdit(self)
        self.path_input.setText(os.getenv('PATH_REDE', r'\\rede'))
        layout.addWidget(self.path_input)

        self.save_path_btn = QPushButton('Salvar Caminho da Rede', self)
        self.save_path_btn.clicked.connect(self.save_network_path)
        layout.addWidget(self.save_path_btn)

        self.db_host_label = QLabel('Host do Banco de Dados:')
        layout.addWidget(self.db_host_label)
        self.db_host_input = QLineEdit(self)
        self.db_host_input.setText(os.getenv('DB_HOST', ''))
        layout.addWidget(self.db_host_input)

        self.db_user_label = QLabel('Usuário do Banco de Dados:')
        layout.addWidget(self.db_user_label)
        self.db_user_input = QLineEdit(self)
        self.db_user_input.setText(os.getenv('DB_USER', ''))
        layout.addWidget(self.db_user_input)

        self.db_password_label = QLabel('Senha do Banco de Dados:')
        layout.addWidget(self.db_password_label)
        self.db_password_input = QLineEdit(self)
        self.db_password_input.setEchoMode(QLineEdit.Password)
        self.db_password_input.setText(os.getenv('DB_PASSWORD', ''))
        layout.addWidget(self.db_password_input)

        self.db_name_label = QLabel('Nome do Banco de Dados:')
        layout.addWidget(self.db_name_label)
        self.db_name_input = QLineEdit(self)
        self.db_name_input.setText(os.getenv('DB_NAME', ''))
        layout.addWidget(self.db_name_input)

        self.save_db_btn = QPushButton('Salvar Configurações do Banco de Dados', self)
        self.save_db_btn.clicked.connect(self.save_db_config)
        layout.addWidget(self.save_db_btn)

        self.config_tab.setLayout(layout)

    def save_network_path(self):
        new_path = self.path_input.text()
        set_key('.env', 'PATH_REDE', new_path)
        QMessageBox.information(self, "Informação", "Caminho da rede salvo com sucesso.")

    def save_db_config(self):
        new_host = self.db_host_input.text()
        new_user = self.db_user_input.text()
        new_password = self.db_password_input.text()
        new_db_name = self.db_name_input.text()
        set_key('.env', 'DB_HOST', new_host)
        set_key('.env', 'DB_USER', new_user)
        set_key('.env', 'DB_PASSWORD', new_password)
        set_key('.env', 'DB_NAME', new_db_name)
        QMessageBox.information(self, "Informação", "Configurações do banco de dados salvas com sucesso.")

    def start_processing(self):
        if self.process_thread is None or not self.process_thread.isRunning():
            self.process_thread = Reprocessamento()
            self.process_thread.finished.connect(self.on_finished)
            self.process_thread.start()
            self.status_label.setText("Processamento em execução...")

    def stop_processing(self):
        if self.process_thread and self.process_thread.isRunning():
            self.process_thread.stop()
            self.status_label.setText("Processamento interrompido.")
        else:
            QMessageBox.warning(self, "Aviso", "Nenhum processo está em execução.")

    def enviar_tudo(self):
        try:
            enviar_tudo_lote()
            QMessageBox.information(self, "Informação", "Todos os arquivos foram enviados para as pastas finais com sucesso.")
        except Exception as e:
            logging.error(f"Erro ao enviar todos os arquivos: {e}")
            QMessageBox.critical(self, "Erro", f"Erro ao enviar todos os arquivos: {str(e)}")

    def on_finished(self, message):
        self.status_label.setText(message)
        QMessageBox.information(self, "Informação", message)

# Inicializando o aplicativo
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
