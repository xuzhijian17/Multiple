#coding=gbk
import os, sys
import time
import getopt
import logging
import MAEReport
import subprocess

try:
    import avp
except ImportError:
    avp = None
try:
    import nod
except ImportError:
    nod = None
try:
    import avg
except ImportError:
    avg = None
try:
    import antivir
except ImportError:
    antivir = None
    
DstDir = r''

class Multiple_Scan:

    def __init__(self):

        self.name = os.path.join(os.getcwd(), 'scan')
        
        self.Detected = os.path.join(os.getcwd(), os.path.join("Detected", time.strftime("%Y%m%d", time.localtime())))
        self.Suspicion = os.path.join(os.getcwd(), os.path.join("Suspicion", time.strftime("%Y%m%d", time.localtime())))
        self.Safefile = os.path.join(os.getcwd(), os.path.join("Safefile", time.strftime("%Y%m%d", time.localtime())))

        self.Backlist = os.path.join(DstDir, 'BacklistMD5.txt')
        self.Dubious = os.path.join(DstDir, 'DubiousMD5.txt')
        self.Whlitelist = os.path.join(DstDir, 'WhitelistMD5.txt')

    def initlog(self, logfile):
        
        """获取日志句柄"""
        
        hdlr = logging.FileHandler(os.path.join(os.path.dirname(__file__), logfile), "ab")
        formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
        hdlr.setFormatter(formatter)
    
        hds = logging.StreamHandler()
        hds.setLevel(logging.INFO)
        hds.setFormatter(formatter)
        
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        logger.addHandler(hdlr)
        logger.addHandler(hds)
        return logger
            
        
    def run(self):
                
        logger = self.initlog('MAEReport.log')

        try:
            
            subprocess.call(['Uncompress/UnCompress.exe', '-r', self.name, self.name]) #先解压
                
            avp.scan(r'D:\Kaspersky Anti-Virus 2010\avp.com', self.name, 'Avp.log')
            avp.avp_log('Avp.log')
            
            nod.scan(r'D:\NOD32\ecls.exe', self.name, 'Nod.log')
            nod.nod_log('Nod.log')
            
            avg.scan(r'D:\AVG\avgscanx.exe', self.name, 'Avg.log')
            avg.avg_log('Avg.log')
            
            antivir.scan(r'D:\Avira\AntiVir Desktop\scancl.exe', self.name, 'AntiVir.log')
            antivir.antivir_log('AntiVir.log')

            subprocess.call(['python', 'hashQuery.pyo', '-s', '-m', '-c', '--file=%s' % self.name]) #删除云库中已存在的样本
                            
            for surplus_file in MAEReport.scan_files(self.name):
                MAEReport.copy_file(surplus_file, self.Safefile)

            MAEReport.Detected_md5(self.Detected, self.Backlist)
            MAEReport.Detected_md5(self.Detected, self.Dubious)
            MAEReport.Safe_md5(self.Safefile, self.Whlitelist)
            
            if os.path.isfile(self.Backlist):
                subprocess.call(['python', 'UploadCloudData.pyo', '-e0', '-r1', '-l0', '--filename=%s' % self.Backlist])
            if os.path.isfile(self.Dubious):
                subprocess.call(['python', 'UploadCloudData.pyo', '-e0', '-r1', '-l0', '--filename=%s' % self.Dubious])
            if os.path.isfile(self.Whlitelist):
                subprocess.call(['python', 'UploadCloudData.pyo', '-e0', '-r1', '-l0', '--filename=%s' % self.Whlitelist])
            
        except:
            logger.exception('')

            
if __name__ == '__main__':
    
    ms = Multiple_Scan()
    ms.run()

