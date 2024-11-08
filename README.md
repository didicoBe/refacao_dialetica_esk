# Programa de Refação Dialética

## Objetivo
O programa de refação da Dialética foi criado para facilitar o processo de localização e manipulação de arquivos PDF relacionados a pedidos específicos. Ele oferece uma solução customizável para encontrar PDFs dentro da rede, separá-los por tipo (miolo ou capa) e aplicar alterações necessárias, como adicionar uma folha de rosto. O caminho para os arquivos pode ser alterado para que o sistema continue funcional em caso de mudanças na infraestrutura de rede.

## Funcionalidades
1. **Localização dos PDFs:** 
   - Caminho padrão configurável para acessar os arquivos na rede.
   - Utilização do ISBN (obtido através do ID do pedido) para localizar arquivos PDF relacionados.
   - Os PDFs geralmente retornados são de "miolo" e "capa", sendo automaticamente separados de acordo com o nome do arquivo.

2. **Manipulação dos PDFs: **
   - Funções para adicionar folha de rosto ou copiar conteúdo dos arquivos.
   - Todo o código de manipulação de PDFs se encontra no módulo `pdf_utils.py`, localizado dentro da pasta `core` do projeto.

## Estrutura do Projeto
- **Diretório de Rede:** `\\192.168.0.28\Dialetica\Dialetica`
  - Este caminho é utilizado para acessar os arquivos. No entanto, ele é configurável, permitindo a adaptação do sistema caso o caminho mude.

- **Identificação de Arquivos:**
  - O programa busca arquivos PDF utilizando o ISBN correspondente ao ID do pedido.
  - Após a busca, separa os arquivos entre "capa" e "miolo", verificando a presença dessas palavras no nome dos arquivos.

- **Manipulação dos Arquivos:**
  - O arquivo `pdf_utils.py` contém todas as funções necessárias para manipulação de PDFs.
  - As funcionalidades incluem copiar arquivos, adicionar uma folha de rosto, e outras funções que podem ser estendidas conforme necessário.

## Caminho Configurável
Para garantir a flexibilidade do sistema, o caminho para encontrar os PDFs na rede é configurável. Atualmente, o caminho padrão é:

```
\\192.168.0.28\Dialetica\Dialetica
```

Essa configuração pode ser alterada, conforme necessário, para adaptar o sistema a qualquer mudança na infraestrutura.

## Exemplo de Uso
1. **Localizar PDFs:** Digitar o ID do pedido para buscar os arquivos correspondentes.
2. **Separação Automática:** O programa retornará dois arquivos: um contendo "miolo" e outro contendo "capa" no nome.
3. **Manipulação:** Utilizar as funções do `pdf_utils.py` para aplicar as alterações desejadas, como adicionar folha de rosto.

## Arquivo `pdf_utils.py`
Este arquivo está localizado dentro da pasta `core` do projeto e contém as funções que realizam a manipulação dos arquivos PDF. Algumas das funções disponíveis incluem:

- **`copiar_pdf()`**: Cria uma cópia de um arquivo PDF selecionado.
- **`adicionar_folha_rosto()`**: Adiciona uma folha de rosto ao PDF, de acordo com um modelo predefinido.

## Melhorias Futuras
- **Interface Gráfica:** Implementação de uma interface amigável para facilitar o uso por operadores não técnicos.
- **Automatização Completa:** Automatizar completamente o processo de busca e manipulação, com execução em segundo plano após a inserção do ID do pedido.
- **Integração com Banco de Dados:** Implementação de uma base de dados para armazenar o histórico de manipulações realizadas nos PDFs, facilitando auditorias e rastreabilidade.

## Conclusão
O programa de refação da Dialética é uma ferramenta poderosa para otimizar o processo de manipulação de PDFs. Com funcionalidades customizáveis e caminho configurável, ele garante flexibilidade e eficiência para o trabalho diário, permitindo economizar tempo e recursos ao automatizar processos repetitivos.
