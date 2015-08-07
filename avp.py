#coding=gbk
import os, re
import rename
import subprocess
from scan import Multiple_Scan

DstDir = Multiple_Scan().Detected

def avp_log(log_name):

    dct = {}
    patt = re.compile(r'.*?\t(.*?)\tdetected\t.*?(\w+\.\w+\.\w+\..*)')
    with open(log_name,'r') as fp:
        pattern = patt.findall(fp.read())
        if pattern:
            for path, virus in pattern:
                path = re.sub("/.*", "", path)
                dct[path] = virus
                
    new_dct = rename.del_same_file(dct)
    for file_name, virus_name in new_dct.items():
        rename.copy_file(file_name,DstDir)
        new_path=os.path.join(DstDir,os.path.basename(file_name))
        rename.sample_rename(new_path, virus_name)
        
def scan(avp_path, scan_path, log_path):
    
    if os.path.isfile(log_path):
        os.remove(log_path)
        
    try:
        Avp = subprocess.Popen([avp_path, 'scan', '/fa', '/i0', '/e:60', scan_path, r'/RA:%s' % log_path])
        Avp.wait()
    except:
        print "Call AVP engine failure!"



