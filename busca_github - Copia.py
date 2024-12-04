import modulo_email
import os
import sys
import time
import re
from datetime import datetime
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep


# --- BLOCO UTILITIES --- Implementação local das funções que seriam fornecidas pelos módulos
def registrar_informacao(mensagem: str):
    """Registra mensagens de informação."""
    print(f"[informação] {mensagem}")

def registrar_erro(mensagem: str):
    """Registra mensagens de erro."""
    print(f"[erro] {mensagem}")

def validar_destinatarios(destinatarios: str):
    
    if not destinatarios:
        return False, "Lista de destinatários vazia ou None."

    # Divide a string de destinatários em uma lista
    lista_destinatarios = [email.strip() for email in destinatarios.split(",")]

    # Regex para validar e-mails
    regex_email = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

    # Filtra os e-mails válidos
    emails_validos = [email for email in lista_destinatarios if re.match(regex_email, email)]

    if not emails_validos:
        return False, "Nenhum destinatário válido encontrado."

    return True, emails_validos

def executar_tarefa():
    """
    Função que executa a tarefa principal do script.
    Chame aqui o método principal do seu script (ex: ConsultaGitHub().executar()).
    """
    try:
        registrar_informacao("Executando a tarefa principal...")
        # Aqui você chama o método que executa a lógica principal
        termo_busca = "desenvolvedor python"
        consulta = ConsultaGitHub()
        usuarios = consulta.executar(termo_busca)
        registrar_informacao(f"Tarefa executada com sucesso. Usuários encontrados: {len(usuarios)}")
    except Exception as e:
        registrar_erro(f"Erro ao executar a tarefa: {e}")

class ConsultaGitHub:
    def __init__(self):
        self.driver = None

    def configurar_driver(self):
        """Configura o WebDriver do Selenium."""
        caminho_chromedriver = os.getenv("CHROME_DRIVER_PATH", "C:/Users/SeuUsuario/pastachrome/chromedriver.exe")
        servico = Service(caminho_chromedriver, log_path="chromedriver.log")

        from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
        capabilities = DesiredCapabilities.CHROME
        capabilities["goog:loggingPrefs"] = {"browser": "OFF"}
    
        # Configura opções do Chrome
        opcoes = webdriver.ChromeOptions()
        
        opcoes.add_argument("--disable-webgl")
        opcoes.add_argument("--disable-software-rasterizer")      
        opcoes.add_argument("--disable-features=WebRtcHideLocalIpsWithMdns")
        opcoes.add_argument("--disable-web-security")
        opcoes.add_argument("--disable-webrtc-apm-in-audio-service")
        opcoes.add_argument("--disable-webrtc")
        opcoes.add_argument("--enable-unsafe-swiftshader")
        opcoes.add_argument("--disable-gpu")
        opcoes.add_argument("--no-sandbox")
        opcoes.add_argument("--start-maximized")
        
        # Inicializa o WebDriver com as configurações definidas
        opcoes.set_capability("goog:loggingPrefs", {"browser": "OFF"})
        self.driver = webdriver.Chrome(service=servico, options=opcoes)
        registrar_informacao("Driver configurado com sucesso.")
        print("Driver configurado com sucesso.")

    def fechar_driver(self):
        """Fecha o WebDriver."""
        if self.driver:
            self.driver.quit()
            print("Driver fechado com sucesso.")

    def acessar_github(self):
        try:
            url_github = "https://github.com/"
            self.driver.get(url_github)
            print(f"Acessando o site: {url_github}")
            sleep(3)
        except Exception as e:
            registrar_erro(f"Erro ao acessar o GitHub: {e}")
            raise

    def buscar_usuarios(self, busca):
        """Busca usuários no GitHub e extrai informações básicas."""
        try:
            # Navegar para a página de busca do GitHub
            github_search_url = f"https://github.com/search?q={busca.replace(' ', '+')}&type=users"
            self.driver.get(github_search_url)
            registrar_informacao(f"Buscando usuários no GitHub com o termo: {busca}")

            sleep(5)

             # XPath para verificar a presença da seção de resultados
            xpath_resultados = "/html/body/div[1]/div[4]/main/react-app/div/div/div[1]/div/div/div[2]/div[2]/div/div[1]/div[4]/div/div"

            # Verifica se o XPath dos resultados está presente
            try:
                WebDriverWait(self.driver, 30).until(
                    EC.presence_of_element_located((By.XPATH, xpath_resultados))
                )
                registrar_informacao("Seção de resultados encontrada com sucesso.")
            except TimeoutException:
                registrar_erro("Seção de resultados não encontrada na página.")
                return []

            # Itera sobre os usuários listados no padrão de XPath identificado
            usuarios = []
            for i in range(1, 11):  # Limite de 10 resultados
                xpath_usuario = f"{xpath_resultados}/div[{i}]/div/div[1]/div[2]/h3/div/a[1]"
                try:
                    # Localiza o elemento do usuário
                    usuario_elemento = self.driver.find_element(By.XPATH, xpath_usuario)

                    # Extrai o nome do usuário
                    nome = usuario_elemento.text.strip()

                    # Extrai o link do perfil
                    link = usuario_elemento.get_attribute("href").strip()

                    # Adiciona à lista de usuários
                    usuarios.append({"nome": nome, "perfil": link})
                    registrar_informacao(f"Usuário {i} extraído: Nome - {nome}, Link - {link}")
                except Exception as e:
                    registrar_erro(f"Erro ao processar o usuário {i}: {e}")

            registrar_informacao(f"Usuários encontrados (limitado a 10): {len(usuarios)}")
            for usuario in usuarios:
                registrar_informacao(f"Nome: {usuario['nome']}, Perfil: {usuario['perfil']}")
                print(usuario)

            return usuarios

        except Exception as e:
            registrar_erro(f"Erro ao buscar usuários: {e}")
            print(f"Erro ao buscar usuários: {e}")
            raise

    def executar(self, termo_busca):
        """Executa todo o processo de busca."""
        try:
            self.configurar_driver()
            self.acessar_github()
            usuarios = self.buscar_usuarios(termo_busca)
            return usuarios
        finally:
            self.fechar_driver()

if __name__ == "__main__":

    # Verifica se há argumentos de linha de comando
    if len(sys.argv) > 1:
        termo_busca = sys.argv[1]
    else:
        # Define um valor padrão caso nenhum argumento seja passado
        termo_busca = "desenvolvedor python"

    # Continue com o resto da lógica
    consulta = ConsultaGitHub()
    usuarios = consulta.executar(termo_busca)
    for usuario in usuarios:
        print(f"Nome: {usuario['nome']}, Perfil: {usuario['perfil']}")

    registrar_informacao("Iniciando o script de agendamento...")
   
    # Registro inicial da execução com timestamp
    print(f"Iniciando execução do módulo em: {time.strftime('%Y-%m-%d %H:%M:%S')}")

    try:
        # Instancia a classe de consulta no GitHub
        consulta = ConsultaGitHub()
        
        # Executa o processo completo de busca
        usuarios = consulta.executar(termo_busca)

        # Exibe os usuarios encontrados
        print("\nUsuários encontrados:")
        for usuario in usuarios:
            print(f"Nome: {usuario['nome']}, Perfil: {usuario['perfil']}")

        if usuarios:
            corpo_email = f"Olá,\n\nSegue abaixo os resultados da busca no GitHub para o termo: {termo_busca}.\n\n"
            for i, usuario in enumerate(usuarios, 1):
                corpo_email += f"{i}. Nome: {usuario['nome']}, Perfil: {usuario['perfil']}\n"
            corpo_email += "\nAtenciosamente,\nSeu Script de Busca"

            modulo_email.enviar_email(
                assunto=f"Resultados da busca no GitHub: {termo_busca}",
                corpo=corpo_email
            )
            registrar_informacao("Email enviado com sucesso.")

    except Exception as e:
        # Registra e exibe erros ocorridos durante a execução
        print(f"Erro durante a execução: {e}")
    finally:
        # Garante que o driver será fechado ao final da execução
        consulta.fechar_driver()