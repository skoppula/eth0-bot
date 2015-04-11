import socket
import sys
import json

TEAM_NAME='SEA'
BOT_BOX_IP='52.4.171.0'
PASS='EcAyY836zTdcFnAh'
EX_PUBLIC_IP='52.5.76.103' #looking at observer
EX_PRIVATE_IP='10.0.37.99' #connecting from bot box

MARKET_INDEX = 0 #0 for slow, 1 for real, 2 for empty
JSON_PORT = 25000+MARKET_INDEX
PLAIN_TEXT_PORT = 20000+MARKET_INDEX

def main():
    s = setup_connection()  
    print send_hello(s)

def send_json(sckt, msg):
    sckt.send(json.dumps(msg))
    print 'SENT ', msg

def setup_connection():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #s.connect((EX_PRIVATE_IP, JSON_PORT))
        s.connect(('127.0.0.1', 8080))
        return s

    except:
        print 'COULD NOT CONNECT'
        return None

def get_message(sckt):
    try:
        print 'MAKING FILE for message'
        print 'Waiting for message'
	buff = sckt.recv(4096)
	print buff
        print 'READLINE LINE for message'
        #return json.loads(line) 
    except:
        print 'OH NO COULD NOT PARSE JSON OR READ FROM SOCKET'
        return None

def send_hello(sckt):
    hello_msg = {"type": "hello", "team": "SEA"}
    send_json(sckt, hello_msg)
    mkt_state = get_message(sckt)
    return mkt_state
    
if __name__ == '__main__':
    main()
