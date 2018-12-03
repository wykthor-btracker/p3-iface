# -*- coding: utf-8 -*-
#imports
import engine
#imports#

#variables
logo = """ _)   _|
  |  |     _` |   __|   _ \\
  |  __|  (   |  (      __/
 _| _|   \\__,_| \\___| \\___|
 Bem vindo ao iFace, cadastre-se ou faça login!
"""
#variables#

#classes

#classes#

#functions
def user(userInst,userList):
    if(not userInst.active):
        return None
    firstScreen = """
    1. Enviar mensagem
    2. Adicionar alguém
    3. Entrar numa comunidade
    4. Criar uma comunidade
    5. Admnistrar comunidade.
    5. Recuperar suas informações
    6. Deletar conta(Cuidado!)
    7. Editar perfil
    8. Sair
    """
    if(choice=='1'):
        name = input("Para quem deseja enviar a mensagem?")
        attempt = userList.retrieveUser(name)
        if(attempt):
            if(isInstance(attempt,list)):
                print("Escolha qual amigo para mandar a mensagem:")
                for us in range(len(attempt)):
                    print(attempt[us],us)


    # if(choice=='2'):
    # if(choice=='3'):
    # if(choice=='4'):
    # if(choice=='5'):
    # if(choice=='6'):
    # if(choice=='7'):
    # if(choice=='8'):
#functions#

#main
def main():
    print(logo)

    return None
#main#
if(__name__ == "__main__"):
    main()
