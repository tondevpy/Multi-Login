import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from contextlib import contextmanager, suppress
import os
import sys
from time import sleep

# Redirecionar erros para os.devnull
sys.stderr = open(os.devnull, 'w')

# Configuração do Chrome para desativar pop-ups
chrome_options = uc.ChromeOptions()

# Desativar notificações
chrome_options.add_experimental_option("prefs", {
    "profile.default_content_setting_values.notifications": 2,  # Bloqueia solicitações de notificações
    "credentials_enable_service": False,  # Desativa o serviço de credenciais do Chrome
    "profile.password_manager_enabled": False  # Desativa o gerenciador de senhas do Chrome
})

@contextmanager
def get_driver():
    driver = uc.Chrome(options=chrome_options)
    try:
        yield driver
    except Exception as e:
        pass  # Suprime qualquer exceção que ocorra
    finally:
        with suppress(Exception):  # Suprime possíveis erros ao fechar o driver
            driver.quit()

def loginFacebook(email, senha):
    with get_driver() as driver:
        driver.get('https://www.facebook.com/settings')
        try:
            # Esperar até que o campo de email esteja presente
            elemento = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[@id='email']"))
            )
        except Exception as e:
            print(f"Erro ao localizar o campo de email: {e}")
            return

        if elemento:
            print('Encontrou o campo de email.')
            
            # Inserir o email e a senha
            driver.find_element(By.XPATH, "//input[@id='email']").send_keys(email)
            driver.find_element(By.XPATH, "//input[@id='pass']").send_keys(senha)
            
            # Clicar no botão de login
            driver.find_element(By.XPATH, "//button[@name='login']").click()

            # Aguardar o carregamento da página após o login
            sleep(20)  # Usar sleep aqui para dar tempo de carregamento após o login (ajustável)

            # Capturar o HTML da página após o login
            source = driver.page_source
            # Verificar as mensagens específicas na página
            if 'O email que você inseriu não está conectado a uma conta' in source:
                print('O email que você inseriu não está conectado a uma conta')
            elif 'Esta é sua conta?' in source:
                print('Email informado em formato inválido...')
            elif 'Entrar como' in source:
                print('Email válido, porém a senha está incorreta...')
            elif 'A senha inserida está incorreta' in source:
                print('A senha inserida está incorreta, email é válido...')
            else:
                try:
                    elemento_login = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div[2]/div/div/div/div/div[1]/div/div/div/div[1]/div/div/div/div/div/h2/span/span').text
                    if 'Encontre a configuração de que você precisa' in elemento_login:
                        print('Login feito com sucesso...')
                except:
                    print('Ocorreu um erro ao realizar o login...')
        else:
            print('Elemento não encontrado...')

def facebook():
    print('Login Facebook')
    email = input('Informe seu email: ').strip()
    senha = input('Informe sua senha: ').strip()

    if email and senha and '@' in email:
        loginFacebook(email, senha)
    else:
        print('Informou email ou senha em formato inválido...')


def loginGmail(email, senha):
    with get_driver() as driver:
        driver.get('https://accounts.google.com/')
        sleep(5)
        try:
            # Esperar até que o campo de email esteja presente
            elemento = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[1]/div[2]/c-wiz/div/div[2]/div/div/div[1]/form/span/section/div/div/div[1]/div/div[1]/div/div[1]/input"))
            )
            print('Encontrou elemento')
        except Exception as e:
            print(f"Erro ao localizar o campo de email: {e}")
            return

        if elemento:
            driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[2]/c-wiz/div/div[2]/div/div/div[1]/form/span/section/div/div/div[1]/div/div[1]/div/div[1]/input').send_keys(email)
            driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[2]/c-wiz/div/div[3]/div/div[1]/div/div/button').click()
            sleep(10)
            try:
                email_invalido = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[1]/div[2]/c-wiz/div/div[2]/div/div/div[1]/form/span/section/div/div/div[1]/div/div[2]/div[2]/div/span"))
            )
            except:
                email_invalido = False

            try:
                email_valido = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[1]/div[2]/c-wiz/div/div[2]/div/div/div/form/span/section[2]/div/div/div[1]/div[1]/div/div/div/div/div[1]/div/div[1]/input"))
            )
            except:
                email_valido = False

            if email_invalido:
                print('O email informado é inválido..')

            if email_valido:
                print('Email válido, inserindo senha...')
                driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[2]/c-wiz/div/div[2]/div/div/div/form/span/section[2]/div/div/div[1]/div[1]/div/div/div/div/div[1]/div/div[1]/input').send_keys(senha)
                driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[2]/c-wiz/div/div[3]/div/div[1]/div/div/button').click()

                sleep(10)

                try:
                    senha_invalida = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[1]/div[2]/c-wiz/div/div[2]/div/div/div/form/span/section[2]/div/div/div[1]/div[2]/div[2]/span"))
                    )
                except:
                    senha_invalida = False

                try:
                    duas_etapas = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[1]/div[2]/c-wiz/div/div[1]/div/h1/span"))
                    )
                except:
                    duas_etapas = False

                try:
                    if 'Senha incorreta' in senha_invalida.text:
                        print('Senha incorreta...')
                except:
                    pass
                
                try:
                    if 'duas etapas' in duas_etapas.text:
                        print('Conta possui duas etapas...')
                except:
                    pass

def gmail():
    print('Login Gmail')
    email = input('Informe seu email: ').strip()
    senha = input('Informe sua senha: ').strip()

    if email and senha and '@' in email:
        loginGmail(email, senha)
    else:
        print('Informou email ou senha em formato inválido...')


print('Digite o numero da opção desejada\n\n[1] - Facebook\n[2] - Gmail')
opcao = input('Opção desejada:')
if opcao:
    if opcao == '1':
        facebook()
    elif opcao == '2':
        gmail()
    else:
        print('Escolheu uma opção inválida...')
else:
    print('Não informou uma opção...')
