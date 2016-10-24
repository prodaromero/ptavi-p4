#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import socketserver
import sys
import json
import time

class SIPRegisterHandler(socketserver.DatagramRequestHandler):
    """
    Echo server class 
    """
    dicc = {}
    attr = {}

    def register2json(self):
        file = open('registered.json', 'w')
        json.dump(self.dicc, file, sort_keys=True, 
                  indent=4, separators=(',', ':'))
        file.close()

    def handle(self):
        
        print("(IP, PORT):" + str(self.client_address))
        line = self.rfile.read()
        message = line.decode('utf-8')
        print("El cliente nos manda " '\r\n' + message)
            

        if message.split(' ')[0] == "REGISTER":
            user = message.split(' ')[1]
            user = user.split(':')[1]
            expires = message.split(' ')[3]
            expires = expires.split('\r\n')[0]
            time_expires = time.gmtime(int(expires))
            time_expires = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))

            if int(expires) == 0:
                if user in self.dicc:
                    del self.dicc[user]
                else:
                    print("ERROR: this user dont exist")
            else:
                self.attr['address'] = self.client_address[0]
                self.attr['expires'] = time_expires
                self.dicc[user] = self.attr
            self.wfile.write(b"SIP/2.0 200 OK\r\n\r\n")

            print(self.dicc)

        self.register2json()

if __name__ == "__main__":
    try:
        PORT = int(sys.argv[1])
    except:
        sys.exit("ERROR: required port")

    serv = socketserver.UDPServer(('', PORT), SIPRegisterHandler)
    print("Lanzando servidor SIP...")
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        print("Finalizado servidor")
