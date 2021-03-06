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
 1. Fazer login
 2. Cadastrar-se
 3. Sair(Sai nao, a gente tem bolo.)
"""
#variables#

#classes

#classes#

#functions
def findUser(userList,name):
    attempt = userList.retrieveUser(name)
    choice = None
    if(attempt):
        if(isinstance(attempt,list)):
            print("Escolha qual amigo: ")
            for us in range(len(attempt)):
                print(attempt[us].name,us)
            choice = input("{}-{}".format(0,len(attempt)-1))
            try:
                choice = int(choice)
                choice = attempt[choice]
            except:
                input("Entrada invalida!")
        elif(isinstance(attempt,engine.user)):
            choice = attempt
    return(choice)
def findCommunity(userList,name):
    attempt = userList.retrieveCommunity(name)
    choice = None
    if(attempt):
        if(isinstance(attempt,list)):
            print("Escolha qual comunidade: ")
            for comm in range(len(attempt)):
                print(attempt[comm].name,comm)
            choice = input("{}-{}".format(0,len(attempt)-1))
            try:
                choice = int(choice)
                choice = attempt[choice]
            except:
                input("Entrada invalida!")
        elif(isinstance(attempt,engine.group)):
            choice = attempt
    return(choice)

def userGui(userInst,userList):
    if(not userInst.active):
        return None
    firstScreen = """
    1. Enviar mensagem
    2. Adicionar alguém
    3. Entrar numa comunidade
    4. Criar uma comunidade
    5. Admnistrar comunidade.
    6. Recuperar suas informações
    7. Deletar conta(Cuidado!)
    8. Editar perfil
    9. Sair
    """
    choice = '-1'
    while(choice!="9"):
        print(firstScreen)
        choice = input()
        if(choice=='1'):
            name = input("Para quem deseja enviar a mensagem? ")
            choice = findUser(userList,name)
            if(choice):
                message = input("Digite a mensagem: ")
                userInst.sendMessage({"sender":userInst,"receiver":choice,"body":message})
            else:
                print("Desculpe! Nao conseguimos encontrar este usuario.")

        if(choice=='2'):
            quem = input("Qual o nome dele(a)?")
            choice = findUser(userList,quem)
            if(choice):
                userInst.addFriend(choice)
                print("Pronto! Convite enviado.")
            else:
                print("Desculpe! Usuario nao encontrado")
        if(choice=='3'):
            qual = input("Qual o nome da panelinha? ")
            choice = findCommunity(userList,qual)
            if(choice):
                choice.addMember(userInst)
                print("Pronto! Agora você tem mais gente pra fofocar sobre.")
            else:
                print("Desculpe! Essa panelinha não existe... Ainda! Você pode cria-la.)")
        if(choice=='4'):
            name = input("Me diz o nome da panelinha: ")
            desc = input("Aproveita e joga uma descrição na roda: ")
            new = engine.group(name,desc,userInst)
            att = engine.attempt(userList.addCommunity,new)
            if(att == "Community name already in use"):
                print("Esse nome já tem! Pega outro.")
            else:
                print("Prooonto, agora pode fofocar à vontade.")

        if(choice=='5'):
            qual = input("Qual o nome da panelinha? ")
            choice = findCommunity(userList,qual)
            if(choice):
                if(choice.owner == userInst):
                    print("Olha quem tá aqui: ")
                    for user,value in choice.members.items():
                        print(user)
                    print("Quer remover quem? Vazio para ninguém")
                    name = input()
                    if(engine.isIn(choice.members,name)):
                        choice.members.pop(name)
                    else:
                        print("Esse aí não tem não, saraiva")
        if(choice=='6'):
            print("Seus atributos:")
            for key,value in userInst.attrs.items():
                print("{}\t= {}".format(key,value))
            print("Suas comunidades:")
            for key,value in userInst.groups.items():
                print("{}\n\t{}".format(userInst.groups[key].name,userInst.groups[key].desc))
            print("Seus amigos:")
            for key,value in userInst.friends.items():
                print(userInst.friends[key].name)
            print("Suas mensagens:")
            for message in userInst.messageBox.messages:
                print("De:{}\nPara:{}\n{}".format(message["sender"].name,message["receiver"].name,message["body"]))

        if(choice=='7'):
            choice = input("Tem certeza que deseja deletar sua conta?\nSentiremos sua falta!(E dos seus dados)\n(s/n)")
            if(choice.lower()=="s"):
                print("Bye bye")
                userInst.delete()
            elif(choice.lower()=="n"):
                print("Ufa!")
            else:
                print("Do, or do not, there is no try. -- Master Yoda")
        if(choice=='8'):
            print("Um por linha, insira seperado por :, o nome do atributo que deseja modificar, e o valor a ser salvo neste atributo.(Idade/lugar de nascimento/ideologia)\nQuando terminar, envie uma linha vazia.")
            text = "-1"
            while(text!=""):
                text = input()
                if(not ":" in text or text.count(":")>1):
                    print("Linha invalida! Separe assim, idade:29")
                    continue
                else:
                    text = text.split(":")
                    text = [part.rstrip().lstrip() for part in text]
                att = engine.attempt(userInst.addAttr,text[0],text[1])
                if(att=="Not Confirmed"):
                    choice = input("Esse atributo ja esta definido! Deseja sobreescrever?\n(s/n)")
                    if(choice.lower()=="s"):
                        att = engine.attempt(userInst.addAttr,text[0],text[1],True)
                        if(att=="Invalid string"):
                            print("Opa! Caracteres invalidos em algum lugar,\n use apenas letras e espaco para o atributo, e letras, numeros e caracteres especiais para o valor.")
                    elif(choice.lower()=="n"):
                        print("Ok! Nada mudou, feijoada.")
                    else:
                        print("Sim ou nao, nao tem talvez. -- Eu, 2018")
                elif(att=="Invalid string"):
                    print("Opa! Caracteres invalidos em algum lugar,\n use apenas letras e espaco para o atributo, e letras, numeros e caracteres especiais para o valor.")
#functions#

#main
def main():
    choice = -1
    userList = engine.users()
    while(choice!="3"):
        print(logo)
        choice = input()
        if(choice=="1"):
            user = input("Usuario:")
            passw = input("Senha:")
            user = userList.retrieveUser(user)
            if(user):
                att = engine.attempt(user.login,passw)
                if(isinstance(att,engine.user)):
                    userGui(user,userList)
                else:
                    print("Senha errada! Volte tres casas.")
            else:
                print("Usuario nao encontrado! Tem certeza que digitou certo? Letras maiusculas e minusculas importam!")
        elif(choice=="2"):
            username = input("Me diga um nome de usuario, ele deve ser unico! ")
            password = input("Me diz uma senha, pode ser qualquer uma, a gente nao vai espalhar, confia. ")
            name = input("Diz o nome pra teus amigos encontrarem, e os inimigos tambem ")
            new = engine.user()
            att = engine.attempt(new.create,username,password,name)
            if(att == "Invalid username"):
                print("Opa! Esse nome não vale, tenta outro.")
            elif(isinstance(att,engine.user)):
                print("Pronto! Agora é só fazer login e nos dar seus dados de graça")
                userList.addUser(att)
            else:
                print("Opa! Algo deu errado.")
                raise(Exception("{} is of wrong type".format(att)))

    return None
#main#
if(__name__ == "__main__"):
    main()
