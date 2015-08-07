#coding=gbk
import time
import socket
import subprocess

class TcpSocket:

    def __init__(self):
        
        self.addr=('0.0.0.0',8080)
        self.tcpSocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.tcpSocket.bind(self.addr)
        self.tcpSocket.listen(1)

    def run(self):
        
        while True:
            print 'waiting for connection'
            sc,sa=self.tcpSocket.accept()
            while True:
                try:
                    action=sc.recv(2048)
                    context='connection from %s,send command with %s %s'%(sa,action,time.ctime())
                    print context
                except socket.error:
                    break
                    
                if action=='scan':
                    
                    subprocess.call(['python','scan.pyc'])
                    
                    with open('hashQuery.log') as fp:
                        cont=fp.read()
                    try:
                        sc.sendall(cont)
                    except:
                        sc.sendall("扫描结果发送失败")

                else:
                    break
                                    
        TcpSocket().run()
        sa.close()
        sc.close()
    
if __name__=='__main__':
    
    TcpSocket().run()
