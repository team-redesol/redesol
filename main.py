# importando tudo o que é preciso
import subprocess
import webbrowser
from datetime import datetime
from dateutil import tz
import csv
import re
import smtplib
from email.message import EmailMessage
import os

from flask import Flask, Response, request, abort, render_template_string, send_from_directory # Importar flask, pillow
from PIL import Image
try:
    from io import StringIO  
except ImportError:
    from io import BytesIO as StringIO  
    
def install_dependencies(): # Instalar dependencias a partir do txt 
    try:
        subprocess.check_call(['pip', 'install', '-r', 'requirements.txt'])
        print("Dependências instaladas com sucesso.")
    except subprocess.CalledProcessError as e:
        print(f"Erro ao instalar as dependências: {e}")
    except FileNotFoundError:
        print("O comando pip não foi encontrado. Verifique se o Python está instalado corretamente.")

install_dependencies()


file_emails = 'emails.txt'
file_news = 'news.csv'
EMAIL_ADDRESS = 'aredesol2024@outlook.com'
#email admin: aredesol2024@outlook.com

#senha do admin é redesolpassc0de

def destinatarios (file_emails):
    email_destinatarios = []
    with open(file_emails,'r') as email_lista:
        for linhas in email_lista:
            tirar_linha = linhas.strip()
            email_destinatarios.append(tirar_linha)
    return email_destinatarios

def copiar_csv(file_news):
    csv_content = [] 
    with open(file_news, 'r', ) as csvfile: 
        reader = csv.reader(csvfile) # atribui uma variavel para ler o arquivo csv
        for col in reader: # Loop vai percorer cada linha na variavel "reader" que leu o arquivo csv todo, e mostra cada posição por linha na lista do csv
           csv_content.append(f"{col[0]}: {col[1]} - {col[2]}") # nesse caso col[0] = data, col[1] = titulo, col[2] = conteudo
    return csv_content

def newsletter_send(destinatarios, conteudo_csv, EMAIL_PASSWORD):
    for destinatario in destinatarios:
        msg = EmailMessage()
        msg['Subject'] = 'Newsletter da Redesol'
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = destinatario
        msg.set_content("\n".join(conteudo_csv))

        try:
            with smtplib.SMTP('smtp-mail.outlook.com', 587) as smtp_server:
                smtp_server.starttls()  # Habilita a criptografia TLS
                smtp_server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                smtp_server.send_message(msg)
            print(f"E-mail enviado para: {destinatario}")
        except smtplib.SMTPException as e:
            print(f"Erro ao enviar e-mail para {destinatario}: {e}")




def print_menuascii(): #menu bonitinho em ascii (i tried)
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

def view_last_events(): #Menu pra mostrar os eventos postados ao usuário 
    while True:
        print("\nSelecione uma opção: ")
        print("1 - Últimas 10 Notícias")
        print("2 - Todas")
        print("0 - Retornar ao menu principal")
        
        userinp = input("\nDigite a opção desejada: ")

        if userinp == "1":
            last_ten()
        elif userinp == "2":
            print("Exibindo todas as notícias ")
            newsletter_view()
        elif userinp == "0":
            return
        else:
            print("\nOpção inválida. Tente novamente.")
            

def last_ten():
    try:
        with open('news.csv', 'r', encoding="utf8", newline='') as csvfile: #Abre o csv em modo de leitura
            reader = csv.reader(csvfile)
            newslist = list(reader) #Transforma o csv em uma lista
            
            if len(newslist) == 0:#Checa se a lista tem 0 itens dentro dela e printa mensagem 
                print("\nAinda não há notícias postadas.")
                return
            elif len(newslist) >= 10: #Se a lista tem mais de 10 itens dentro dela, em ordem decrescente, pega 10 itens começando da ultima posição
                ultimas_news = newslist[-10:]
            else:
                ultimas_news = newslist #Se a lista não tem mais de 10 itens, faça a lista com todos os itens disponíveis 
                
            print("\nÚltimas notícias:")      
            for col in ultimas_news: #Loop vai percorer cada item na lista "ultimas_news" e vai printar cada coluna por linha da lista dada pelo csv lido
                print(f"{col[0]}: {col[1]} - {col[2]}") # nesse caso col[0] = data, col[1] = titulo, col[2] = conteudo   
            
    except FileNotFoundError:
        print("\nAinda não há notícias postadas.")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")

            
            

def post_newsletter(titulo, conteudo): # salva uma notícia no formato data/hora, título e conteúdo em CSV
    data_hora = datetime.now(tz.gettz('America/Recife')).strftime('%d/%m/%Y %H:%M:%S')
    with open('news.csv', 'a', encoding="utf8", newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([data_hora, titulo, conteudo])

def delete_news(): # Deleta notícias com base no título 
    tag = input("Digite o Título da notícia que deseja deletar: ")
    noticias = []
    with open('news.csv', 'r', encoding="utf8", newline='') as csvfile: #Lê o news.csv e o atribui a uma variável reader
        reader = csv.reader(csvfile)
        for row in reader: # Loop vai percorer cada item no reader e verificar se a tag dada pelo usuário como input não está presente na lista reader,
            if tag.lower() not in row[1].lower():  # Adiciona na lista "noticias" se a tag não estiver presente
                noticias.append(row)

    with open('news.csv', 'w', encoding="utf8", newline='') as csvfile: # Abre o news.csv em modo escrita  
        writer = csv.writer(csvfile) # Atribui uma variavel para escrever no arquivo csv
        writer.writerows(noticias) # Escreve o arquivo csv do zero, baseado nas linhas contidas na lista "noticias" 
    print("\nNotícia(s) deletada(s) com sucesso.")

def newsletter_view():  #Exibindo noticias na tela
    try:
        with open('news.csv', 'r', encoding="utf8", newline='') as csvfile: # Abre o arquivo csv no modo leitura como uma variavel csvfile
            reader = csv.reader(csvfile) # atribui uma variavel para ler o arquivo csv
            print("\nNotícias:")
            for col in reader: # Loop vai percorer cada linha na variavel "reader" que leu o arquivo csv todo, e mostra cada posição por linha na lista do csv
                print(f"{col[0]}: {col[1]} - {col[2]}") # nesse caso col[0] = data, col[1] = titulo, col[2] = conteudo
    except FileNotFoundError:
        print("\nAinda não há notícias postadas.")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")

  

def newsletter_subcribe(email): #Inscreve usuários na newsletter
    if validar_email(email):  #retorno da função de validação
        with open('emails.txt', 'r', encoding="utf8") as arquivo_inscritos: 
            email_dupli = arquivo_inscritos.readlines()

        if email + '\n' in email_dupli:
            print("Esse e-mail já está cadastrado. ")
        else:
            with open('emails.txt', 'a') as arquivo_inscritos:  #se não existir, registre o e-mail no txt
                arquivo_inscritos.write(email + '\n')
            print("\nInscrição realizada com sucesso! ")
    else:
        print("O endereço de e-mail digitado é inválido. ") 
        print("Por favor, insira um e-mail válido. ")

def validar_email(email):  #Padrão para endereço de e-mail
    email_validation = r'^[\w\.-]+@[\w\.-]+\.\w+$' 
    if re.match(email_validation, email): #Veja se o e-mail é válido
        return True #Caso seja valido retorne True
    else:
        return False #Caso não seja valido retorne False


def remover_email(email):#Remove um e-mail da lista de inscritos
    with open('emails.txt', 'r', encoding="utf8") as arquivo_inscritos:
        emails = arquivo_inscritos.readlines() 

    if email + '\n' in emails: #Procura se o e-mail está na lista de inscritos
        emails.remove(email + '\n')
        print("E-mail removido com sucesso.")
    else:
        print("O e-mail não está inscrito.") #Se não estiver na lista de inscritos, retorna a mensagem

    try:
        with open('emails.txt', 'w') as arquivo_inscritos:
            arquivo_inscritos.writelines(emails)
    except IOError:
        print("Erro ao abrir o arquivo.")

def newsletter_menu(): # Menu para operações relacionadas a newsletter
    while True:
        print("\nBem-vindo ao menu de Newsletter ")
        print("\n1 - Se inscrever para a Newsletter ")
        print("2 - Remover inscrição do Newsletter ")
        print("0 - Retornar ao Menu principal ")
        userinp = input("Selecione uma opção: ")
        if userinp == "1":
            email = input("Digite seu e-mail para se inscrever na Newsletter: ")
            newsletter_subcribe(email)
        elif userinp == "2":
            email = input("Digite seu e-mail para remover sua inscrição: ")
            remover_email(email)
        elif userinp == "0":
            return
        elif userinp == "test":
            destinatarios(file_emails)
        else:
            print("\nOpção inválida. Tente novamente.")

def instabread(): # Redirecionar para as redes sociais
    webbrowser.open("https://www.instagram.com/casadopaoaor/")

def admin_login(): # menu de login basico
    senha = "redesolpassc0de"
    while True:
        senhainput = input("\nDigite a senha do Administrador ou digite 0 para retornar ao menu anterior ")
        if senhainput == senha:
            print("\nAcesso permitido")
            admin_menu()
            break  #sair do loop de login 
        elif senhainput == "0":
            break #sair do loop de login e acaba retornando ao menu anterior
        else:
            print("\nSenha incorreta. Acesso Negado ")

def admin_menu(): # menu do admin
    while True:
        print("\n1 - Adicionar notícias ao quadro ")
        print("2 - Remover notícias no quadro ")
        print("3 - Visualizar quadro de notícias ")
        print("4 - Enviar notícias para E-mails registrados ")
        print("0 - Retornar ao Menu principal ")

        userinp = input("\nSelecione uma opção:")

        if userinp == "1":
            titulo = input("Digite o título da notícia: ")
            conteudo = input("Digite o conteúdo da notícia: ")
            post_newsletter(titulo, conteudo)
        elif userinp == "2":
            delete_news()
        elif userinp == "3":
            newsletter_view()
        elif userinp == "4":
            destinatarios_lista = destinatarios(file_emails)  
            conteudo_csv = copiar_csv(file_news)
            EMAIL_PASSWORD = input("Digite a senha do E-mail: ") 
            newsletter_send(destinatarios_lista, conteudo_csv, EMAIL_PASSWORD) 
        elif userinp == "0":
            return  # retorna pro admin_login
        else:
            print("\nOpção inválida. Tente novamente.")
            
## verificar essa parte do código porque honestamente tudo que estudei e pesquisei sobre a galeria era extremamente
## complexo e envolvia API pra caralho e muita coisa de frontend (que eu nao faço ideia)
def image(filename): # backend de uma galeria
    try:
        w = int(request.args['w'])
        h = int(request.args['h'])
    except (KeyError, ValueError):
        return send_from_directory('.', filename)

    try:
        im = Image.open(filename)
        im.thumbnail((w, h), Image.ANTIALIAS)
        io = StringIO.StringIO()
        im.save(io, format='JPEG')
        return Response(io.getvalue(), mimetype='image/jpeg')

    except IOError:
        abort(404)
    return send_from_directory('.', filename)

def index(): # backend de uma galeria II
    images = []
    for root, dirs, files in os.walk('.'):
        files.sort(key=os.path.getmtime)
        for filename in [os.path.join(root, name) for name in files]:
            if not filename.endswith('.jpg'):
                continue
            im = Image.open(filename)
            w, h = im.size
            aspect = 1.0*w/h
            if aspect > 1.0*WIDTH/HEIGHT:
                width = min(w, WIDTH)
                height = width/aspect
            else:
                height = min(h, HEIGHT)
                width = height*aspect
            images.append({
                'width': int(width),
                'height': int(height),
                'src': filename
            })

    return render_template_string(TEMPLATE, **{
        'images': images
    })

def main(): #Função principal
    while True:
        print_menuascii()
        print("Bem vindo ao site Redesol! ")
        print("Menu principal ")
        print("1 - Ver últimos eventos/notícias ")
        print("2 - Newsletter ")
        print("3 - Redes sociais da Casa do Pão ")
        print("4 - Menu de Admin ")
        print("0 - Sair ")
        userinp = input("Selecione uma opção: ")

        if userinp == "1":
            view_last_events()
        elif userinp == "2":
            newsletter_menu()
        elif userinp == "3":
            instabread()
            print("\nRedirecionando para o Instagram da Casa do Pão ")
        elif userinp == "4":
            admin_login()
        elif userinp == "0":
            break
        else:
            print("\nOpção inválida. Tente novamente.")

# Executando o aplicativo
if __name__ == "__main__":
    main()
