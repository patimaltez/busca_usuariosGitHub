🛠️ Automação de Busca de Usuários no GitHub com Envio de Email

📋 Visão Geral
Este projeto é um script em Python que realiza as seguintes funções:

Busca usuários no GitHub com base em um termo de pesquisa.
Extrai nomes de usuários e links para os seus perfis.
Envia os resultados da busca por email usando uma conta configurada no Outlook.
Permite agendamento automático de execução utilizando o Agendador de Tarefas do Windows.

🚀 Funcionalidades
Busca Automática: Pesquisa usuários no GitHub a partir de um termo de busca especificado.
Extração de Dados: Captura o nome e o link do perfil dos usuários encontrados.
Envio de Resultados por Email: Integração com o Outlook para envio dos resultados diretamente para o email desejado.
Agendamento de Tarefas: Permite execução automatizada em horários específicos utilizando o Agendador de Tarefas.

🧩 Pré-requisitos
Python 3.8 ou superior instalado no sistema.
Dependências do Python:
Instale usando o pip: pip install selenium pywin32
Google Chrome instalado.
ChromeDriver correspondente à versão do Chrome instalado
Configure o caminho para o ChromeDriver no arquivo busca_github.py.

📄 Como Usar
1. Configuração do Email
Certifique-se de que a conta de email do remetente está configurada no Outlook no computador onde o script será executado.
2. Configuração do Script
Insira o caminho do ChromeDriver no script no método configurar_driver: caminho_chromedriver = "C:/caminho/para/seu/chromedriver.exe"
O termo de busca pode ser alterado ao passar como argumento na linha de comando: python busca_github.py "seu termo de busca"
3. Execução Manual
Execute o script diretamente no terminal ou prompt de comando
4. Agendamento de Execução Automática
Use o Agendador de Tarefas do Windows para executar o script em horários específicos:

📧 Exemplo de Envio de Email
O script enviará um email com os resultados, semelhante ao seguinte:

Assunto: Resultados da busca no GitHub: desenvolvedor python
Corpo:
Olá,

Segue abaixo os resultados da busca no GitHub para o termo: desenvolvedor python.

1. Nome: Fulano de Tal, Perfil: https://github.com/fulanodetal
2. Nome: Ciclano de Tal, Perfil: https://github.com/ciclanodetal
...

Atenciosamente,  
Seu Script de Busca

🛡️ Observações
O script utiliza o Outlook do sistema para enviar emails, sendo necessário configurá-lo previamente.
O envio de email depende do módulo pywin32.

💻 Autor
Este script foi desenvolvido para automatizar a busca de perfis no GitHub e facilitar o envio de relatórios para emails configurados.
