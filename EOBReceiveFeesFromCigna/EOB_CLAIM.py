
import os
import csv

def CLAIM_INFO():
    claim_info={}
    claim_info["ID"]=""
    claim_info["CLAIM"]=""
    claim_info["DOS"]=""
    claim_info["LAST"]=""
    claim_info["FIRST"]=""
    claim_info["CHARGE"]=0.0
    claim_info["EOB"]=""
    claim_info["PAID"]=""
    claim_info["ALLOW"]=""
    claim_info["DED"]=""
    claim_info['TOPT']=0.0
    claim_info['NPI']=""
    claim_info['TAX']=""
    claim_info["NOTE"]="NO"
    claim_info["MAX"]="NO"
    claim_info["TERMINATED"]="NO"
    claim_info["NO COVER"]="NO"
    return claim_info

def reset(claim_info):
    
    claim_info["ID"]=""
    claim_info["CLAIM"]=""
    claim_info["DOS"]=""
    claim_info["LAST"]=""
    claim_info["FIRST"]=""
    claim_info["CHARGE"]=0.0
    #claim_info["EOB"]=""
    claim_info["PAID"]=""
    claim_info["ALLOW"]=""
    claim_info["DED"]=""
    claim_info['TOPT']=0.0
    #claim_info['NPI']=""
    #claim_info['TAX']=""
    claim_info["NOTE"]="NO"
    claim_info["MAX"]="NO"
    claim_info["TERMINATED"]="NO"
    claim_info["NO COVER"]="NO"
    

def save_csv(claim_info):
    filePath=os.getcwd()+r"/EOB.csv"
    with open(filePath, 'a+',newline="") as f:
                csv.writer(f).writerow([claim_info["ID"],claim_info["CLAIM"],str(claim_info["EOB"]),claim_info["LAST"],claim_info["FIRST"],claim_info["DOS"],claim_info["CHARGE"],claim_info["PAID"],claim_info["ALLOW"],claim_info["DED"],claim_info['TOPT'],claim_info["TAX"],claim_info["NPI"], claim_info["NOTE"],claim_info["MAX"],claim_info["TERMINATED"],claim_info["NO COVER"]])
    f.close()
    reset(claim_info)