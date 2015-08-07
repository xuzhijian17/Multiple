#coding=gbk
import os
import subprocess


def main(src_path,dst_path):

    if not os.path.isdir(dst_path):
        os.makedirs(dst_path)

    for x,y,z in os.walk(src_path):
        for i in z:
            file_path=os.path.join(x,i)
            if os.path.isfile(file_path):
                subprocess.call(["UniExtract.exe",file_path,dst_path])
                print file_path
                #os.remove(file_path)

if __name__=='__main__':
    
    main(r"D:\Downloads",r"D:\unpack")
                
