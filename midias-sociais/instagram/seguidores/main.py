#autor: Samuel Nascimento
#Construindo um bot automatizado para alancar seguidores no instagram

from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
#aleatorizar numero
from random import randint
#biblioteca de controle de tempo
import time
from selenium.common import NoSuchElementException

#só pra aleatorizar o tempo
def wait(startTime, endTime):
    time.sleep(randint(startTime,endTime))

#classe
class InstaBot:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        #perfil que deve ser o primeiro a ser aberto
        self.username_principal_profile = 'sigo.de_.volta_'
        #servico e conecxao com o webdriver do firefox
        self.servico = Service(GeckoDriverManager().install())
        self.navegador = webdriver.Firefox(service=self.servico)

    def login(self):
        navegador = self.navegador
        # Navegue até a página de login do Instagram
        navegador.get('https://www.instagram.com/')
        wait(3,6)

        # preencher credenciais
        email = navegador.find_element(By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div/div[1]/section/main/article/div[2]/div[1]/div[2]/form/div/div[1]/div/label/input').send_keys(self.username)
        password = navegador.find_element(By.XPATH,'/html/body/div[2]/div/div/div[2]/div/div/div[1]/section/main/article/div[2]/div[1]/div[2]/form/div/div[2]/div/label/input').send_keys(self.password)

        #pressione enter
        wait(3,5)
        navegador.find_element(By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div/div[1]/section/main/article/div[2]/div[1]/div[2]/form/div/div[3]/button/div').click()

        #pressione o botão de "agora não" para salvar informações
        wait(5,8)
        navegador.find_element(By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/section/main/div/div/div/div/div').click()

        #pressione o botão "not now" das notificações
        wait(5,8)
        navegador.find_element(By.CSS_SELECTOR, "button._a9--:nth-child(2)").click()


    def buscar_seguidores(self, followers_number):
        navegador = self.navegador

        #entra no perfil que você quer começar a seguir
        wait(5,8)
        navegador.get('https://www.instagram.com/' + self.username_principal_profile)

        #entra na aba de seguidores
        wait(5,7)
        navegador.find_element(By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/header/section/ul/li[2]/a').click()
        print("entrei na lista de seguidores")
        #pegando o class name do popup
        wait(4,7)
        popup_followers = navegador.find_element(By.CLASS_NAME, "_aano")
        print("peguei o class_name no popup")

        #lista de seguidores do perfil escolhido
        followers_array = []

        i=0

        while len(followers_array) <= followers_number:
            navegador.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', popup_followers)
            print("Baixei o scroll")
            wait(4,6)

            followers = navegador.find_elements(By.CLASS_NAME, 'x1rg5ohu')
            print("encontrei o botão de seguidor")

            for follower in followers:
                if follower not in followers_array:
                    followers_array.append(follower.text)

            i+=1

        #retira a duplicação de textos na array
        new_followers_array = list(dict.fromkeys(followers_array))
        #deleta o primeiro elemento(idiomas no instagram)
        del new_followers_array[0]
        #salva a nova array
        self.followers = new_followers_array

        print(self.followers)
        #print("Tamanho do vetor: " + len(self.followers))

    def seguir_usuarios(self, number_to_follow):
        navegador = self.navegador

        #contador de seguidores
        i=0
         #auxiliar
        aux = 0

        print("Vou entrar no perfil do caba")
        for follower in self.followers:
            print(follower)
            navegador.get('https://www.instagram.com/' + follower)
            print("entrei no perfil do caba")
            wait(5,9)

            try:
                visible = navegador.find_element(By.CSS_SELECTOR, "._aa_u").text
                print(visible)
                if visible == "This Account is Private":
                #Se eles forem privados, não podemos ver sua lista de seguidores, então pule-os
                    print("Essa conta é privada, vou pular!")
                    continue
            except NoSuchElementException:
                try:
                    following = navegador.find_element(By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/header/section/div[1]/div[1]/div/div[1]/button/div/div[1]').text

                    if following == "Following":
                        # se já estiver seguindo
                        print("Essa conta já é seguida!!")
                        aux = 1
                        continue

                except:
                     if aux != 1:
                        navegador.find_element(By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/header/section/div[1]/div[1]/div/div/button').click()
                        i+=1
                        print("++++ Segui o " + follower)

            aux = 0

            if i == number_to_follow:
                break
        
            print("entrando no insta do prox")
            wait(5,9)

#main
insta = InstaBot('orrapodcast','orrapodcast#2023')
wait(3,4)

#login
insta.login()
wait(2,5)

#buscar seguidores
insta.buscar_seguidores(9)
wait(1,7)

#seguir usuários
insta.seguir_usuarios(3)
