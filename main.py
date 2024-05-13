import subprocess

def install_requirements():
    subprocess.check_call(['pip', 'install', '-r', 'requirements.txt'])

install_requirements()


from datetime import datetime
from dateutil import tz
import csv
import re
import webbrowser
import os
import time


def install_package(package):
    subprocess.check_call(['pip', 'install', package])

install_package('python-dateutil')


def print_menuascii(): #menu bonitinho (i tried)
    print(
        """                                                                                                                                                                                            
                                          ≠≠≠=÷÷÷÷÷=≠≠≠       
                                         ≠≠≠≠ =÷÷÷= ≠≠≠≠      
                                           ≠≠≠=÷÷÷=≠≠≠        
                                            ≠≠≠=÷÷≠≠          
                                              ≠   ≠           
     ≠≠≠≠≠≠≠≠             ≠≠≠          ≠≠≠≠≠         ≠≠≠      
      ≠≠≠  ≠≠≠            ≠≠≠         ≠≠  ≠≠         ≠≠≠      
      ≠≠≠  ≠≠≠ ≠≠≠≠≠≠ ≠≠≠≠≠≠≠  ≠≠≠≠≠≠ ≠≠≠≠   ≠≠≠ ≠≠≠ ≠≠≠      
      ≠≠≠≠≠≠≠ ≠≠≠≠≠≠≠≠≠≠  ≠≠≠ ≠≠≠≠≠≠≠  ≠≠≠≠≠ ≠≠≠ ≠≠≠ ≠≠≠      
      ≠≠≠  ≠≠≠≠≠≠     ≠≠≠ ≠≠≠ ≠≠≠    ≠≠   ≠≠≠≠≠≠ ≠≠≠ ≠≠≠      
     ≠≠≠≠≠ ≠≠≠≠≠≠≠≠≠≠ ≠≠≠≠≠≠≠≠ ≠≠≠≠≠≠≠≠≠≠≠≠≠  ≠≠≠≠≠ ≠≠≠≠≠     

        """
    )

def view_last_events():
    print("Ainda não implementado.")



def post_newsletter(titulo, conteudo): 
    # Obtendo a data e hora atual no fuso horário 'America/Recife'
    data_hora = datetime.now(tz.gettz('America/Recife')).strftime('%d/%m/%Y %H:%M:%S')
    with open('news.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([data_hora, titulo, conteudo])

def delete_news(): #Menu para o admin deletar as noticias no csv
            tag = input("Digite a Tag da notícia que deseja deletar: ")
            noticias = []
            with open('news.csv', 'r', newline='') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    if tag.lower() not in row[1].lower():  # Verifica se a tag está presente no título da notícia
                        noticias.append(row)

            with open('news.csv', 'w', newline='') as csvfile: #Deleta a linha baseada na tag
                writer = csv.writer(csvfile)
                writer.writerows(noticias)
            print("\nNotícia(s) deletada(s) com sucesso.")

def newsletter_view(): #Menu para o admin ver as noticias no csv
            try:
                with open('news.csv', 'r', newline='') as csvfile:
                    reader = csv.reader(csvfile)
                    print("\nNotícias:")
                    for row in reader:
                        print(f"{row[0]}: {row[1]} - {row[2]}")
            except FileNotFoundError:
                print("\nAinda não há notícias postadas.")




def subscribe_to_my_newsletter(email): 
    if validar_email(email): #retorno da função de validação
        with open('emails.txt', 'r') as arquivo_inscritos: #abre a lista de e-mails para verificar se já existe o e-mail
            email_dupli = arquivo_inscritos.readlines()

        if email + '\n' in email_dupli:
            print("Esse e-mail já está cadastrado. ")
        else:
            with open('emails.txt', 'a') as arquivo_inscritos: #se não existir, registre o e-mail no txt
                arquivo_inscritos.write(email + '\n')
            print("\nInscrição realizada com sucesso! ")
    else:
        print("O endereço de e-mail digitado é inválido. ") #retorno da função de validação
        print("Por favor, insira um e-mail válido. ")

def validar_email(email): 
    email_validation = r'^[\w\.-]+@[\w\.-]+\.\w+$' #Padrão para endereço de e-mail
    if re.match(email_validation, email): #Veja se o e-mail é válido
        return True #Caso seja valido retorne True
    else:
        return False #Caso não seja valido retorne False

def remover_email(email):
    with open('emails.txt', 'r') as arquivo_inscritos:
        emails = arquivo_inscritos.readlines()

    if email + '\n' in emails: #Procura se o e-mail está na lista de inscritos
        emails.remove(email + '\n')
        print("E-mail removido com sucesso.")
    else:
        print("O e-mail não está na inscrito .") #Se não estiver na lista de inscritos, retorna a mensagem de erro

    try:
        with open('emails.txt', 'w') as arquivo_inscritos:
            arquivo_inscritos.writelines(emails)
    except IOError:
        print("Erro ao abrir o arquivo. ")


    

def newsletter_menu():
    while True:
        print("\nBem-vindo ao menu de Newsletter ")
        print("\n1. Se inscrever para a Newsletter ")
        print("2. Remover inscrição do Newsletter ")
        print("3. Retornar ao Menu principal ")
        userinp = input("Selecione uma opção: ")
        if userinp == "1":
            email = input("Digite seu e-mail para se inscrever na Newsletter: ")
            subscribe_to_my_newsletter(email)
        elif userinp == "2":
            email = input("Digite seu e-mail para remover sua inscrição: ")
            remover_email(email)
            
            
        

def instabread(): #Redirecionar para as redes sociais
    webbrowser.open("https://www.instagram.com/casadopaoaor/")

def admin_login(): #login de admin (preguiça de fazer sistema de cadastro)
    senha = "redesolpassc0de"
    while True:
        senhainput = input("Digite a senha do Administrador ")
        if senhainput == senha:
            print("\nAcesso permitido")
            admin_menu()
        else:
            print("\nSenha incorreta. Acesso Negado ")
            admin_login()
        
def admin_menu():
    while True:
        print("1. Adicionar notícias ao quadro ")
        print("2. Modificar notícias no quadro ")
        print("3. Visualizar quadro de notícias ")
        print("0. Retornar ao Menu principal ")
    
        userinp = input("\nSelecione uma opção:")
        
        if userinp == "1":
            titulo = input("Digite o título da notícia: ")
            conteudo = input("Digite o conteúdo da notícia: ")
            post_newsletter(titulo, conteudo)
        elif userinp == "2":
            delete_news()
        elif userinp == "3":
            newsletter_view()
        
            
            


def main(): # Menu principal
    while True:
        print_menuascii()
        print("Bem vindo ao aplicativo Redesol! ")
        print("Menu principal ")
        print("1 - Ver últimos eventos ")
        print("2 - Newsletter ")
        print("3 - Redes sociais da Casa do Pão ")
        print("4 - Menu de Admin ")
        userinp = input("Selecione uma opção: ")

        if userinp == "1":
            view_last_events()
        elif userinp == "2":
            newsletter_menu()
        elif userinp == "3":
            instabread()
            print("\nRedirecionando para o Instagram da Casa do pão ")
        elif userinp == "4":
            admin_login()
        else:
            print("\nOpção inválida. Tente novamente.")

# Executando aplicativo
if __name__ == "__main__":
    main()