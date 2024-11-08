from reportlab.lib.pagesizes import mm
from reportlab.pdfgen import canvas
import PyPDF2
import os
import logging

def copia_e_add_folha_arquivo_ref(caminho_arquivo_original, nome_cliente, num_pedido, data_pedido, titulo_pedido,
                                  isbn, qnt_paginas, papel_miolo, formato, caminho_salvar, nome_arquivo,
                                  tiragem, tipo_produto, marketplace):
    try:
        # Definir o tamanho da página em mm (140x210 mm)
        largura, altura = 140 * mm, 210 * mm

        # Nome do arquivo temporário da folha de rosto
        caminho_folha_de_rosto = os.path.join(caminho_salvar, "folha_de_rosto_temp.pdf")

        # Passo 1: Criar a folha de rosto com ReportLab
        c = canvas.Canvas(caminho_folha_de_rosto, pagesize=(largura, altura))
        c.setFont("Helvetica", 14)  # Reduzindo o tamanho da fonte para melhor centralização

        # Centralizar o texto horizontalmente e colocar no meio vertical
        y = altura - 40 * mm  # Começar próximo ao topo
        texto_linhas = [
            "REFAÇÃO",
            f"Cliente: {nome_cliente}",
            f"Título: {titulo_pedido}",
            f"Pedido nº: {num_pedido}",
            f"Data Pedido: {data_pedido}",
            f"ISBN: {isbn}",
            f"Páginas: {qnt_paginas}",
            f"Papel Miolo: {papel_miolo}",
            f"Formato: {formato}",
            f"Tiragem: {tiragem}",
            f"Acabamento: {tipo_produto}",
            f"Marketplace: {marketplace}"
        ]

        for linha in texto_linhas:
            text_width = c.stringWidth(linha, "Helvetica", 14)
            c.drawString((largura - text_width) / 2, y, linha)  # Centraliza o texto horizontalmente
            y -= 20 * mm  # Move para baixo a cada linha

        c.save()

        # Passo 2: Abrir o arquivo PDF original
        with open(caminho_arquivo_original, 'rb') as arquivo_original:
            pdf_reader = PyPDF2.PdfReader(arquivo_original)

            # Passo 3: Abrir a folha de rosto e criar o PDF final com PyPDF2
            with open(caminho_folha_de_rosto, 'rb') as folha_de_rosto:
                folha_reader = PyPDF2.PdfReader(folha_de_rosto)
                pdf_writer = PyPDF2.PdfWriter()

                # Adicionar a folha de rosto ao PDF Writer
                pdf_writer.add_page(folha_reader.pages[0])

                # Adicionar todas as páginas do PDF original ao PDF Writer
                for page in pdf_reader.pages:
                    pdf_writer.add_page(page)

                # Passo 4: Salvar o novo arquivo PDF
                caminho_novo_arquivo = os.path.join(caminho_salvar, f"{nome_arquivo}.pdf")
                with open(caminho_novo_arquivo, 'wb') as arquivo_novo:
                    pdf_writer.write(arquivo_novo)

        # Log de sucesso
        logging.info(f"Arquivo com folha de rosto criado com sucesso: {caminho_novo_arquivo}")

        # Remover o arquivo temporário da folha de rosto
        os.remove(caminho_folha_de_rosto)

        return True

    except Exception as e:
        logging.error(f"Erro ao copiar e adicionar folha de rosto ao arquivo: {e}")
        return False