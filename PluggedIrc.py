import socket
import sys
import time
import threading
import datetime
import MessageSaver

class Log:
    def __init__(self):
        pass
    def _now(self):
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    def print(self, message):
        print(f"[{self._now()}] {message}")



class Server:
    def __init__(self, serverName) -> None:
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conns = {}
        self.log = Log()
        self.ServerConfig = {
            "name": serverName,
            "adress": "test.com",
            "version": "1.0"
        }
        self.messageSaver = MessageSaver.MessageSaver()
        
        self.ServerConfig["host"] = f"irc.{self.ServerConfig['name']}.com"
        self.channels = {}
    def Forever(self):
        self.s.bind(('0.0.0.0', 6667))
        self.s.listen(5)
        self.log.print('####################')
        self.log.print('## IRC Server v1.0')
        self.log.print('####################')
        self.log.print('Listening on port 6667')
        while True:
            conn, addr = self.s.accept()
            self.log.print('Connected by' + str(addr))
            self.conns[conn] = {"nick": None, "user": None, "host": None, "realname": None, "channels": []}
            threading.Thread(target=self.Handle, args=(conn, addr)).start()
            
    def Handle(self, conn, addr):
        while True:
            data = conn.recv(1024)
            if not data:
                break
            data_raw = data.decode('utf-8')
            data_raw.strip()
            
            data = data_raw.split('\r\n')
            if len(data) < 2:
                data = data_raw.split('\n')
            
            # if data has no \r\n, it will be a list with one element
            # if data has \r\n, it will be a list with multiple elements

            
            self.log.print("------------------")
            self.log.print(f"Received: {data}")
            self.log.print("------------------")
            for line in data:
                if line == '':
                    continue
                self.CommandHandler(conn , line)
            
    def BroadcastChannel(self, message, channel, author):
        # self.messageSaver.save(message=message, channel=channel, author=self.conns[conn]['nick'])

        for conn in self.conns:
            print(self.conns[conn]["nick"])
            print(self.conns[conn]["channels"], end="")
            print(" -> " + channel)

            if channel in self.conns[conn]["channels"] and self.conns[conn]["nick"] != author:
                self.log.print(f"Broadcasting to {self.conns[conn]['nick']} in {channel}")
                conn.send(message.encode('utf-8'))
    def CommandHandler(self, conn, data):
        if data.startswith('NICK'):
            #check if nick is valid
            nick = data.split(' ')[1]
            
            #check if nick is already in use
            for c in self.conns:
                if self.conns[c]["nick"] == nick:
                    conn.send(f"\r\n:{self.ServerConfig['host']} 433 * {nick} :Nickname is already in use\r\n".encode('utf-8'))
                    return
            self.conns[conn]['nick'] = data.split(' ')[1].split('@')[0]
            self.log.print(f"Set nick to {self.conns[conn]['nick']}")
        elif data.startswith('USERHOST'):
            conn.send(f":{self.ServerConfig['host']} 302 {self.conns[conn]['nick']} :{self.conns[conn]['nick']}={self.conns[conn]['user']}@{self.conns[conn]['host']}\r\n".encode('utf-8'))
            
        elif data.startswith('USER'):
            self.log.print(f"Set user to {data.split(' ')[1]}")
            login = False
            if self.conns[conn]['user'] is None:
                login = True
            self.conns[conn]['user'] = data.split(' ')[1]
            self.conns[conn]['host'] = data.split(' ')[2]
            self.conns[conn]['realname'] = data.split(' ')[3]
            if login:
                banner = """
   ___  __                      __  ____       
  / _ \/ /_ _____ ____ ____ ___/ / /  _/_______
 / ___/ / // / _ `/ _ `/ -_) _  / _/ // __/ __/
/_/  /_/\_,_/\_, /\_, /\__/\_,_/ /___/_/  \__/ 
        /___//___/                         
                """
                loginPayload = [
                    f":{self.ServerConfig['name']} 001 {self.conns[conn]['nick']} :Welcome to the Internet Relay Network {self.conns[conn]['nick']}!{self.conns[conn]['user']}@{self.conns[conn]['host']}",
                    f":{self.ServerConfig['name']} 002 {self.conns[conn]['nick']} :Your host is {self.ServerConfig['name']}, running version {self.ServerConfig['version']}",
                    f":{self.ServerConfig['name']} 003 {self.conns[conn]['nick']} :This server was created 2021-01-01",
                    f":{self.ServerConfig['name']} 004 {self.conns[conn]['nick']} {self.ServerConfig['name']} {self.ServerConfig['version']} iow biklmnopstv",
                    f":{self.ServerConfig['name']} 005 {self.conns[conn]['nick']} CHANTYPES=# EXCEPTS INVEX CHANMODES=eIbq,k,flj,CFLMPQScgimnprstz CHANLIMIT=#:120 PREFIX=(ov)@+ MAXLIST=bqeI:100 MODES=4 NETWORK=PluggedIRC KNOCK STATUSMSG=@+ CALLERID=g CASEMAPPING=ascii :are supported by this server",
                    f":{self.ServerConfig['name']} 251 {self.conns[conn]['nick']} :There are 0 users and 0 invisible on 1 servers",
                    f":{self.ServerConfig['name']} 252 {self.conns[conn]['nick']} 0 :operator(s) online",
                    f":{self.ServerConfig['name']} 253 {self.conns[conn]['nick']} 0 :unknown connection(s)",
                    f":{self.ServerConfig['name']} 254 {self.conns[conn]['nick']} 0 :channels formed",
                    f":{self.ServerConfig['name']} 255 {self.conns[conn]['nick']} :I have 0 clients and 1 servers",
                    f":{self.ServerConfig['name']} 265 {self.conns[conn]['nick']} 0 0 :Current local users 0, max 0",
                    f":{self.ServerConfig['name']} 266 {self.conns[conn]['nick']} 0 0 :Current global users 0, max 0",
                    f":{self.ServerConfig['name']} 375 {self.conns[conn]['nick']} :- {self.ServerConfig['name']} Message of the Day - ",
                    f":{self.ServerConfig['name']} 372 {self.conns[conn]['nick']} :- Welcome to the PluggedIRC Server",
                    f":{self.ServerConfig['name']} 376 {self.conns[conn]['nick']} :End of /MOTD command.",
                ]
                for payload in loginPayload:
                    conn.send(payload.encode('utf-8') + b'\r\n')
                for line in banner.split('\n'):
                    conn.send(f":{self.ServerConfig['name']} NOTICE {self.conns[conn]['nick']} :{line}".encode('utf-8') + b'\r\n')
                self.log.print(f"Sent login payload to {self.conns[conn]['nick']}")
        elif data.startswith('PING'):
            #send to the client the pong with the code
            #syntax: <server> PONG <server> :<code>
            conn.send(f"\r\n:{self.ServerConfig['name']} PONG {self.ServerConfig['name']} :{data.split(' ')[1]}".encode('utf-8') + b'\r\n')


        elif data.startswith('JOIN'):
            channel = data.split(' ')[1]
            if channel not in self.channels:
                self.channels[channel] = {"Users": []}
            self.channels[channel]['Users'].append({self.conns[conn]['nick']:conn})
            #topic
            self.channels[channel]['Topic'] = "No topic is set"
            self.log.print(f"User {self.conns[conn]['nick']} joined channel {channel}")
            self.conns[conn]['channels'].append(channel)
            conn.send(f"\r\n:{self.conns[conn]['nick']} JOIN {channel}\r\n".encode('utf-8') + b'\r\n')
        elif data.startswith('PART'):
            self.log.print(f"{self.conns[conn]['nick']} left {data.split(' ')[1]}")
            self.conns[conn]['channels'].remove(data.split(' ')[1])
        elif data.startswith('QUIT'):
            # break
            pass
        elif data.startswith('CAP'):
            conn.sendall('CAP * ACK :multi-prefix sasl'.encode('utf-8'))
        elif data.startswith('LIST'):
            conn.sendall(f":{self.ServerConfig['name']} 321 {self.conns[conn]['nick']} Channel :Users Name".encode('utf-8'))
            for channel in self.channels:
                try:
                    conn.sendall(f":{self.ServerConfig['name']} 322 {self.conns[conn]['nick']} {channel} 0 :{self.channels[channel]['topic']}".encode('utf-8'))
                except KeyError:
                    conn.sendall(f":{self.ServerConfig['name']} 322 {self.conns[conn]['nick']} {channel} 0 :No topic is set".encode('utf-8'))
            conn.sendall(f":{self.ServerConfig['name']} 323 {self.conns[conn]['nick']} :End of /LIST".encode('utf-8'))
        elif data.startswith('PRIVMSG'):
            if data.split(' ')[1].startswith('#'):
                try:
                    for conn2 in self.channels[data.split(' ')[1]]['Users']:
                        for nick in conn2:
                            if conn2[nick] != conn:
                                message = "".join(data.split(':')[1:])
                                # conn2[nick].sendall(f":{self.conns[conn]['nick']}!{self.conns[conn]['user']}@{self.conns[conn]['host']} PRIVMSG {data.split(' ')[1]} :{message}\r\n".encode('utf-8'))
                                self.BroadcastChannel(f":{self.conns[conn]['nick']}!{self.conns[conn]['user']}@{self.conns[conn]['host']} PRIVMSG {data.split(' ')[1]} :{message}\r\n", data.split(' ')[1], author=self.conns[conn]['nick'])
                except KeyError:
                    conn.sendall(f":{self.ServerConfig['name']} 403 {self.conns[conn]['nick']} {data.split(' ')[1]} :No such channel".encode('utf-8'))            
        elif data.startswith('WHO'):
            for conn2 in self.conns:
                if conn2 != conn:
                    # conn2.sendall(data.encode('utf-8'))
                    pass
        else:
            print(data)

if __name__ == '__main__':
    server = Server("Test")
    server.Forever()
    