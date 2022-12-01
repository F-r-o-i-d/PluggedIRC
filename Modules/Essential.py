print("Module Imported")
#import a file from the parent folder
import sys
sys.path.append("../PluggedIrc")
import Message
import socket

plugName = "Essential"
historyIsEnable = False 
def init():
    print("Essential module loaded")

def messageEvent(message):
    global historyIsEnable
    #message.reply("plugin", "Essential")
    if message.message.split(":")[1] == "!help":
        message.reply("------------------", plugName)
        message.reply("Essential plugin", plugName)
        message.reply("Commands:", plugName)
        message.reply("!help", plugName)
        message.reply("!discord", plugName)
        message.reply("!github", plugName)
        message.reply("!website", plugName)
        message.reply("------------------", plugName)
        message.reply("History plugin", plugName)
        message.reply("Commands:", plugName)
        message.reply("!history <on/off>", plugName)
        message.reply("!getHistory", plugName)
        
    if message.message.split(":")[1] == "!discord":
        message.reply("https://discord.gg/K8RBKUjZ", plugName)

    if message.message.split(":")[1] == "!github":
        message.reply("https://github.com/F-r-o-i-d/PluggedIRC", plugName)

    if message.message.split(":")[1] == "!website":
        message.reply("https://f-r-o-i-d.github.io/PluggedIRC/", plugName)


    if message.message.split(":")[1].startswith("!history"):
        if message.message.split(":")[2] == "on":
            historyIsEnable = True
            message.reply("History is enable", plugName)
        if message.message.split(":")[2] == "off":
            historyIsEnable = False
            message.reply("History is disable", plugName)

    if historyIsEnable:
        historyFile = open(f"../messages/{message.channel}.txt", "a+")
        historyFile.write(f"{message.sender}: {message.message.split(':')[-1]}")
        historyFile.close()

    if message.message.split(":")[1] == "!getHistory":
        historyFile = open(f"../messages/{message.channel}.txt", "r")
        history = historyFile.read()
        message.reply(history, plugName)
        historyFile.close()

