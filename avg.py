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

DstDir = Multiple_Scan().Suspicion

def avg_log(log_name):
    
    dct = {}
    pattern=re.compile(r"(\w:\\.*?)(\:\\.*?|\s)(Trojan|Virus)\s(horse|identified)\s(.*)")
    with open(log_name) as fp:
        patt=pattern.findall(fp.read())
        if patt:
            for x1,x2,x3,x4,x5 in patt:
                path=x1
                virus=x3+re.sub('.*','.',x4)+x5.replace('/','.')
                dct[path] = virus
                
    new_dct = rename.del_same_file(dct)
    for file_name, virus_name in new_dct.items():
        rename.copy_file(file_name,DstDir)
        avp_name=NametoKav.NodtoKav().run(virus_name).strip()
        new_path=os.path.join(DstDir,os.path.basename(file_name))
        rename.sample_rename(new_path, avp_name)

def scan(avg_path,scan_path,log_path):

    try:
        Avg=subprocess.Popen([avg_path,r'/scan=%s'%scan_path,r'/report=%s'%log_path])
        Avg.wait()
    except:
        print "Call AVG engine failure!"
        
