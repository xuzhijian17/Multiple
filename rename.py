#-*-coding:utf-8-*-
'''
Created on 2012-1-5

@author: xuzhijian17
'''
import time
import shutil
import os, stat
import hashlib

def md5_name(file_name):

    try:
        fb = open(file_name, 'rb')
        md5 = hashlib.md5(fb.read()).hexdigest()
        fb.close()
        
        return md5
    
    except IOError:
        print "Count File MD5 Error!"
    
def ext_rename(arge):
    
    file_name, ext_name = os.path.splitext(arge)
    if ext_name:
        ext = ext_name[:-1] + '$'
        return ext
    else:
        ext = '.$'
        return ext

def del_file(file_name):
    
    try:
        os.chmod(file_name, stat.S_IWRITE)
        os.remove(file_name)
        print file_name + '\t....Delete file successed!'
    except WindowsError:
        print file_name + '\t....File deletions failure, may have does not exist!'
          
def rename_file(src_name,dst_name):
    
    try:
        os.rename(src_name, dst_name) 
        print src_name + '\t....Rename Success'
        return dst_name
    except WindowsError:
        del_file(src_name)
        return dst_name
    except IOError:
        print src_name + '\t....Rename Fail' 
        
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
        try:
            shutil.copy(file_path, folder)
            del_file(file_path)
            print file_path+"\t... Copy Sample Successfully!"
        except IOError:
            print file_path+"\t... Copy Sample failed!"
        
def del_same_file(file_path_dict):
    
    dct = {}
    for path in file_path_dict.keys():
        md5 = md5_name(path)
        dct[md5] = path
        
    new_dct = {}
    for file_path, virus_name in file_path_dict.items():
        if file_path in dct.values():
            new_dct[file_path]=virus_name
        else:
            del_file(file_path)
        
    return new_dct
        
def sample_rename(file_name, virus_name):

    if os.path.isfile(file_name):

        avp_vir = "%s(%s)%s" % (virus_name, md5_name(file_name), ext_rename(file_name))
        avp_name = os.path.join(os.path.split(file_name)[0], avp_vir)
        rename_file(file_name, avp_name)

    else:
        del_file(file_name)

