import os

class MessageSaver:
    def __init__(self) -> None:
        self.path = os.path.join(os.path.dirname(__file__), "messages")
    
    def OpenFile(self, channel: str) -> None:
        print("Opening file")
        print(os.path.join(self.path, channel))
        if not os.path.exists(self.path+"/"+channel):
            file = open(self.path+"/"+channel, "w+")
            return file
        else:
            file = open(self.path+"/"+channel, "a")
            return file


    def save(self, message: str, channel, author, timestamp) -> None:
        file = self.OpenFile(channel)
        file.write(f"{author} : {message} --[MSGSAVE]--")
        file.close()



    def get(self, channel: str) -> str:
        file = self.OpenFile(channel)
        return file.read().split("--[MSGSAVE]--")
        file.close()