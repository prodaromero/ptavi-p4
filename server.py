#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import socketserver
import sys


class SIPRegisterHandler(socketserver.DatagramRequestHandler):
    """
    Echo server class 
    """
    dicc = {}

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
            if int(expires) == 0:
                if user in self.dicc:
                    del self.dicc[user]
                else:
                    print("ERROR: this user dont exist")
            else:
                self.dicc[user] = self.client_address[0]

            print("SIP/2.0 200 OK" + '\r\n\r\n')

            print(self.dicc)

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
