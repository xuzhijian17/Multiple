#coding=utf-8
'''
Created on 2011-1-13
将其他厂商的病毒名转换为卡巴的病毒名，转换为卡巴的病毒名
@author: zhukeding
'''
import sys,os

class NodtoKav(object):
    '''
    将nod32的名转换成卡巴的病毒名
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.invalidsign = ["/", "!", ":", "\\"," "]
        #需要替换成.的符号
        self.invalidstring = ["a variant of", 
                              "probably a variant of",
                              "potentially unwanted program",
                              "probably",
                               ]
        #需要去掉的字符串
        self.repheadword = [("generic", "Gen"),  #替换的关键字
                            ("trojan", "Trojan"),
                            ("not-a-virus","Not-a-virus"),
                            ("worm", "Worm"),
                            ("application", "Not-a-virus"),
                            ("Win32/Adware", "Adware.Win32"),
                            ("Win32/TrojanDownloader", "-Downloader.Win32"),
                            ("Win32/TrojanClicker", "-Clicker.Win32"),
                            ("Win32/TrojanDropper", "-Dropper.Win32"),
                            ("Win32/PSW", "-PSW.Win32"),  #自己添加的病毒类型，有可能不是Trojan
                            ("Win32/Spy", "-Spy.Win32"),  #同上
                            ("HTML/Exploit", "Exploit.HTML"),
                            ("VBS/TrojanDownloader", "-Downloader.VBS"),
                            ("HTML/TrojanDownloader", "-Downloader.HTML"),
                            ("JS/TrojanDownloader", "-Downloader.JS"),
                            ("Win32/TrojanProxy", "-Proxy.Win32"),
                            ("Win32/HackTool", "-HackTool.Win32"),
                            ("Win32/Spy", "-Spy.Win32"),
                            ("Win32/Dialer", "Porn-Dialer.Win32"),
                            ("Win32/PSWTool", "PSWTool.Win32"),
                            ("Win32/NetTool", "NetTool.Win32"),
                            ("Win32/RemoteAdmin", "RemoteAdmin.Win32"),
                            ("Win32/RiskWare", "RiskTool.Win32"),
                            ("Win32/DDoS", "DDoS.Win32"),
                            ("NSIS/TrojanDownloader", "-Downloader.NSIS"),
                            ("Java/TrojanDownload", "Trojan.Java.Downloader"),
                            ("Win32/Packed", "Packed.Win32"),
                            ("TR/", "Trojan."),
			    ("Eicar test file","Eicar-test-file"),
                            ("SWF/Exploit", "Exploit.SWF"),
                            ("PDF/Exploit", "Exploit.PDF"),
                            ]
    
    def replacesign(self, name):
        
        """将无效的病毒名符号去掉"""
        
        for sign in self.invalidsign:
            name = name.replace(sign, ".")
        return name
    
    def replacestring(self, string):
        
        """去除无效的字符串"""
        
        for item in self.invalidstring:
            string = string.replace(item, "")
        return string.strip()
    
    def replaceheadword(self, name):
        
        """替换不合法的字符"""
        
        for item in self.repheadword:
            if item[0] not in name:
                continue
            else:
                name = name.replace(item[0], item[1])
                continue
        return name
    
    def spliceName(self, name):
        
        """将病毒的类型分离，然后拼接"""
        
        item = name.split()
        if len(item) == 2:
            if item[0][0] == "-":
                name = item[1] + item[0]
            else:
                name = item[1] + "." + item[0]
        elif len(item) == 1:
        #如果没有找到类型标识
            if name[0] == "-":
                #名字前面带-的
                name = "Trojan" + name
            elif name[0] == name[0].upper():
                pass
            else:
                name = "Trojan." + name
        return name
            
    
    def upperhead(self, name):
        
        """将第一个字母变为大写"""
        
        name = name[0].upper() + name[1:]
        return name
    
    def run(self, name):
        
        """主过程"""
        name = self.replacestring(name)
        name = self.replaceheadword(name)
        name = self.upperhead(name)
        name = self.spliceName(name)
        name = self.replacesign(name)
        return name

    
if __name__ == "__main__":
#    os.chdir(sys.path[0])
#    filename = sys.argv[1]
#    fread = open(filename)
#    fwrite = open("vrslst.txt", "w")
#    for line in fread:
#        line = line.strip()
#        N2K = NodtoKav()
#        newname = N2K.run(line).strip()
#        if newname == line:
#            continue
#        else:
#            print line + ";" + newname
#            fwrite.write(line + ";" + newname.strip() + "\n")
#    fread.close()
#    fwrite.close()

    N2K = NodtoKav()
    newname = N2K.run("probably unknown NewHeur_PE virus").strip()
    print newname

