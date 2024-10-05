import telebot
import os
import datetime
import time

#Chave da Api
KEY_API = ""
bot = telebot.TeleBot(KEY_API) #Iniciar bot

print("Bot Active")


@bot.message_handler(commands=["help"])
def set(mensagem):
    msg = '''❓ Comando /ext- Usado para quando RETIRADA (-) for Efetuado\n
        🔑/ext -s (Valor) -d (Descrição)\n
    ❓ Comando /set- Usado para quando DEPOSITO (+) for Efetuado\n
        🔑/set -s (Valor) -d (Descrição)\n
    ❓Comando /rel- Usado para exportar dados/Informação\n
        🔑/rel \t - Retorna Informaçoes rapidas da conta\n
        🔑/rel -c \t - Retorna Documento (.xlsx) com todas as movimentaçoes registradas\n
    ❓Comando /mon- Usado para Setar despesas mensais\n
        🔑/mon -s VALOR(Ex: 10.00) -d DESCRIÇÃO -dat 01/01/1900 \n
    ❓Comando /per Usado para Setar o periodo dos relatorios \n
        🔑/per -i (DataInicial) -f (DataFinal) \n
    '''
    bot.reply_to(mensagem,msg)

@bot.message_handler(commands=["ext"])
def saida(mensagem):
    try:
        bot.reply_to(mensagem," Sucesso :)")
    except:
        bot.reply_to(mensagem," Entrada Invalida :(")

@bot.message_handler(commands=["set"])
def set(mensagem):
    try:
        bot.reply_to(mensagem," Sucesso :)")
    except:
        bot.reply_to(mensagem," Entrada Invalida :(")

@bot.message_handler(commands=["cof"])
def cof(mensagem):
    try:
        entry = mensagem.text[mensagem.text.index("cof") + 3:]
        bot.reply_to(mensagem," Sucesso :)")
    except:
        bot.reply_to(mensagem," Entrada Invalida :(")


@bot.message_handler(commands=["mon"])
def mon(mensagem):
    try:
        bot.reply_to(mensagem," Sucesso :)")
    except:
        bot.reply_to(mensagem," Entrada Invalida :(")


@bot.message_handler(commands=["per"])
def per(mensagem):
    id = mensagem.chat.id

    ent = mensagem.text[mensagem.text.index("per") + 3:]

    datStart = ent[ent.index("-i") + 2:ent.index("-f")] + "00:00"
    datEnd = ent[ent.index("-f") + 2:] + " 00:00"

    if "/" in str(datStart):
        datStart = str(datStart).replace("/","-")
        
    
    if "/" in str(datEnd):
        datEnd = str(datEnd).replace("/","-")

    print(datStart,datEnd)

    datStart = datetime.datetime.strptime(datStart.strip(),"%d-%m-%Y %H:%M")
    datEnd = datetime.datetime.strptime(datEnd.strip(),"%d-%m-%Y %H:%M")

    print(f"Periodo = ({datStart},{datEnd})")

    #Salvar entrada no log
    text = f"{id} : ('{datStart}','{datEnd}')"
    bot.reply_to(mensagem," Sucesso :)")
        # #except:
        #     bot.reply_to(mensagem," Entrada Invalida :(")

    # except:
    #     bot.reply_to(mensagem," Entrada Invalida :(")


@bot.message_handler(commands=["rel"])
def rel(mensagem):
    msg = "relatorio.xlsx"
    with open(str(os.getcwd()) + "/" + msg, "rb") as file:
        bot.send_document(mensagem.chat.id, document=file)
    #Deletar file
    os.remove(str(os.getcwd()) + "/" + msg)
       

def verificar(mensagem):
    print(f"User: {mensagem.chat.id}")
    return True

@bot.message_handler(func=verificar)
def responder(mensagem):
    texto = """ -- Finance Bot Start --
    /help\t-\t Como usar
    /ext \t-\t Retirada
    /set \t-\t Ganho
    /rel\t-\t Relatorio
        /rel -c Referente ao periodo
        /rel -a Todos os dados
        /rel -i (Data Inicial) -f (Data Final)
            ex: /rel -i 12/02/2023 -f 12/03/2023 """
    bot.reply_to(mensagem, texto)# marca a mensagem e envia


def loop(): #recursão
    try:
        bot.polling() #loop Infinito do bot
    except:
        time.sleep(5)
        loop()


loop()

    
