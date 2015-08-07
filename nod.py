#-*-coding:utf-8-*-
'''
Created on 2011-12-29

@author: xuzhijian17
'''
import os, re
import rename
import NametoKav
import subprocess
from scan import Multiple_Scan
        
DstDir = Multiple_Scan().Detected

def nod_log(log_name):

    dct = {}
    patt=re.compile(r'name="(.*?)".*?threat="(.*?)".*')
    with open(log_name) as fp:
        pattern=patt.findall(fp.read())
        if pattern:
            for path,virus in pattern:
                path=re.sub("\s\?.*","",path)
                if virus:
                    dct[path] = virus
                    
    new_dct = rename.del_same_file(dct)
    for file_name, virus_name in new_dct.items():
        rename.copy_file(file_name,DstDir)
        avp_name=NametoKav.NodtoKav().run(virus_name).strip()
        new_name=os.path.join(DstDir,os.path.basename(file_name))
        rename.sample_rename(new_name, avp_name)

def scan(nod_path,scan_path,log_path):
    
    try:
        Nod=subprocess.Popen([nod_path,r'/log-file=%s'%log_path,r'/log-rewrite',scan_path])
        Nod.wait()
    except:
        print "Call Nod engine failure!"
        
