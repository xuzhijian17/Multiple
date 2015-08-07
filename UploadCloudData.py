#-*-coding:gbk-*-
'''
Created on 2011-12-16

@author: xuzhijian17

-e0\t不存在样本
-e1\t存在样本

-r0\t不替换已有HASH
-r1\t替换已有HASH

-l0\t不锁定HASH
-l1\t锁定HASH

--filename=[文件路径名]

for example：
D:\python\python\python\import_hash.py -e0 -r0 -l0 --filename=C:\Import_Hash.txt
'''
import os, sys
import socket
import getopt
import urllib2
import tempfile
from BeautifulSoup import BeautifulSoup
from poster.encode import multipart_encode
from poster.streaminghttp import register_openers

class Import_Hash(object):
    
    def __init__(self):
        
        self.params = {}
        self.url = "http://cloud.sucop.com/index.php?m=Hash&a=import&"
        
    def temp_file(self, filename):
    
        temp_lst = []
        if os.path.getsize(filename) < 5242880:
            with open(filename) as fp:
                lst = [x.rstrip() for x in fp.readlines()]
                len_lst = len(lst)
                if len_lst > 100:
                    COUNT = 100
                    for i in xrange(0,len_lst,100):
                        temp_name = tempfile.mktemp()
                        with open(temp_name,'w') as temp:
                            temp_upload = '\n'.join(lst[i:COUNT])
                            temp.write(temp_upload)
                            temp_lst.append(temp_name)
                            COUNT+=100
                    return temp_lst
                else:
                    return temp_lst
        else:
            print "Upload data is too long."
            sys.exit()
    
    def Inquire_Hash(self):
        
        register_openers()
        datagen, header = multipart_encode(self.params)
        
        try:
            req = urllib2.Request(self.url, datagen , header)
            req.add_header('Authorization', 'Basic c3Vjb3B1c2VyOnN1YzBwc3VjMHA5MDkw')
            page = urllib2.urlopen(req, timeout=10)
            soup = BeautifulSoup(page, fromEncoding='gbk')
            page.close()
            patt = soup.findAll('pre')
            if patt:
                for i in patt:
                    print i.text
        except urllib2.HTTPError, e:
            print e.code
            print e.msg
            print e.headers
            print e.fp.read()
            
        except urllib2.URLError, e:
            print e
        except socket.timeout,e:
            print e
        
def main():

    if len(sys.argv) < 2:  
        print 'No action specified.'  
        sys.exit()  
    
    try:                                
        opts, args = getopt.getopt(sys.argv[1:], "he:r:l:", ["help", "filename="])
    except getopt.GetoptError:
        print "parameter input error! please type -h or --help."
        sys.exit()
        
    ih = Import_Hash()
    for opt, arg in opts:               
        if opt in ("-h", "--help"):     
            print __doc__                     
            sys.exit()
        elif opt == "-e":
            if arg == '0':
                ih.params["existed"] = 0
            elif arg == '1':
                ih.params["existed"] = 1
            else:
                print "parameter input error! please type -h or --help."
        elif opt == "-r":
            if arg == '0':
                ih.params["replace"] = 0
            elif arg == '1':
                ih.params["replace"] = 1
            else:
                print "parameter input error! please type -h or --help."
        elif opt == "-l":
            if arg == '0':
                ih.params["lock"] = 0
            elif arg == '1':
                ih.params["lock"] = 1
            else:
                print "parameter input error! please type -h or --help."
        elif opt == "--filename":        
            tf = ih.temp_file(arg)
            if tf:
                for temp_name in tf:
                    with open(temp_name,'rb') as fb:
                        ih.params["datafile"] = fb
                        ih.Inquire_Hash()
                    os.remove(temp_name)
            else:
                ih.params["datafile"] = open(arg,'rb')
                ih.Inquire_Hash()
            
if __name__ == '__main__':
    
    main()
