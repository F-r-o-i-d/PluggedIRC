
class Message:
    def __init__(self, message,channel, sender, conn):
        self.message = message
        self.channel = channel
        self.sender = sender
        self.conn = conn       

    def reply(self, message, message_author):
        #reply to the channel
        #simulates a message from the bot
        #self.conn is an socket
        #wyene!wyene@0 PRIVMSG #a :sa
        print("Replying to channel")
        print("----------------")
        print(f"PRIVMSG {self.channel} :{message_author}: {message}")
        print("----------------")

        self.conn.send((f"\r\n\r\n:{message_author}!{message_author}@0 PRIVMSG {self.channel} :{message}\r\n\r\n").encode())
      
  
    def __str__(self):
        return self.message