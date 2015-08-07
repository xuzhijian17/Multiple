#-*-coding:utf-8-*-
import os, re
import zipfile
import hashlib
import pefile
import stat
import shutil

def scan_files(folder):
    
    lst = []
    for x, y, z in os.walk(folder):
        for a in z:
            file_name = os.path.join(x, a)
            if os.path.isfile(file_name) and Filter_PE(file_name):
                lst.append(file_name)
            else:
                print file_name + "\tIt's not a PE file or empty file!"
                del_file(file_name)
    return lst

def Filter_PE(file_path):
    
    try:
        pe = pefile.PE(file_path, fast_load=True)
        pe.close()
        return True
    except:
        return False
    
def del_file(file_name):
    
    try:
        os.chmod(file_name, stat.S_IWRITE)
        os.remove(file_name)
        print file_name + '\t....Delete file successed!'
    except WindowsError:
        print file_name + '\t....File deletions failure, may have does not exist!'
        
def copy_file(file_path, folder):
    
    if not os.path.isdir(folder):
        os.makedirs(folder)
        
    i=1
    file_name=os.path.basename(file_path)
    name, ext = os.path.splitext(file_name)
    first_path = os.path.join(folder, file_name)
    if os.path.exists(first_path):
        while True:
            new_name = name+'('+str(i)+')'+ext
            new_path = os.path.join(folder,new_name)
            if os.path.exists(new_path):
                i+=1
            else:
                shutil.copy(file_path, new_path)
                del_file(file_path)
                print new_path+"\t... Copy Sample Successfully!"
                break
    else:
        shutil.copy(file_path, folder)
        del_file(file_path)
        print file_path+"\t... Copy Sample Successfully!"
    

def Detected_md5(Detected, log_path):

    if os.path.isdir(Detected):
        patt = re.compile(r'(.*?)\((.*?)\).*')
        pattern = patt.findall('\n'.join(os.listdir(Detected)))
        with open(log_path, 'w') as fp:
            if pattern:
                for virus, md5 in pattern:
                    backlist = md5 + ';' + virus
                    print backlist
                    fp.write(backlist + '\n')

def Suspicion_ZIP(Suspicion, zip_path):

    if os.path.isdir(Suspicion):
        zf = zipfile.ZipFile(zip_path, 'w', allowZip64=True)
        for file_path in scan_files(Suspicion):
            print file_path + " ... In process of compress suspicion sample file."
            try:
                zf.write(file_path)
            except IOError:
                pass
        zf.close()

def Safe_md5(Safefile, log_path):
    
    if os.path.isdir(Safefile):
        lst_md5 = []
        for file_path in scan_files(Safefile):
            md5 = hashlib.md5(open(file_path, 'rb').read()).hexdigest()
            whlitelist = md5 + ';'
            print whlitelist
            lst_md5.append(whlitelist)
            
        with open(log_path, 'w+') as fp:
            fp.write('\n'.join(list(set(lst_md5))))
        

