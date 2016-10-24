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
 
        for line in self.rfile:
            message = line.decode('utf-8')
            print("El cliente nos manda ", message)

            if message.split(' ')[0] == "REGISTER":
                user = message.split(':')[1]
                user = user.split('SIP')[0]
                print("SIP/2.0 200 OK" + '\r\n\r\n')

            self.dicc[user] = self.client_address[0]
            print(self.dicc)
            

if __name__ == "__main__":
    try:
        PORT = int(sys.argv[1])
    except:
        sys.exit("ERROR: required port")

    serv = socketserver.UDPServer(('', PORT), SIPRegisterHandler)
    print("Lanzando servidor UDP de eco...")
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        print("Finalizado servidor")
