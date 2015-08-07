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

def antivir_log(log_name):
    
    dct = {}
    pattern = re.compile(r"ALERT:\s\[(.*?)]\s(.*?)<<<.*")
    with open(log_name) as fp:
        patt = pattern.findall(fp.read())
        if patt:
            for virus, path in patt:
                virus = re.sub('\#.*','virus',virus)
                dct[path] = virus
                    
    new_dct = rename.del_same_file(dct)
    for file_name, virus_name in new_dct.items():
        rename.copy_file(file_name,DstDir)
        avp_name=NametoKav.NodtoKav().run(virus_name).strip()
        new_path=os.path.join(DstDir,os.path.basename(file_name))
        rename.sample_rename(new_path, avp_name)
        
def scan(antiVir_path, scan_path, log_path):
    
    try:
        AntiVir = subprocess.Popen([antiVir_path, scan_path, r'--log=%s' % log_path])
        AntiVir.wait()
    except:
        print "Call Antivir engine failure!"
        


