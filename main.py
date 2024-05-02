import os
import time
import webbrowser

def print_menuascii():
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


def newsletter_menu():
    print("Ainda não implementado.")

def instabread():
    webbrowser.open("https://www.instagram.com/casadopaoaor/")

def admin_menu():
    print("Ainda não implementado ")


# Menu principal
def main():
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
            print("Redirecionando para o Instagram da Casa do pão ")
        elif userinp == "4":
            admin_menu()
        else:
            print("Opção inválida. Tente novamente.")

# Executando aplicativo
if __name__ == "__main__":
    main()


