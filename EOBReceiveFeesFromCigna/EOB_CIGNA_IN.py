#!/usr/bin/env python
#encoding: utf-8

import logging.handlers
import re

import EOB_CLAIM

logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='myapp.log',
                filemode='w')






def PARSING_EOB(filePath):
    
   
    claim_info=EOB_CLAIM.CLAIM_INFO()
    data=""
    with open(filePath, 'rt') as f:
        data = f.readlines()
    f.close()
    for i in range(len(data)):
        
        if len(re.findall ( "Remittance Tracking Number: \d{12}",data[i]))>0: #tracking number
            
            claim_info["EOB"]="'"+re.findall ("Remittance Tracking Number: \d{12,15}",data[i])[0].replace("Remittance Tracking Number: ","").replace("\n","")
        
        elif len(re.findall("PATIENT NAME: [A-Z ]+ [A-Z]+ ID:",data[i]))>0: #patient name
            info=re.findall("PATIENT NAME: [A-Z ]+ [A-Z]+ ID:",data[i])
            info=info[0].replace("PATIENT NAME: ","").replace(" ID:","")
            info=info.split(" ",info.count(" "))
            
            
            claim_info["FIRST"]=info[0]
            if len(info[1])>len(info[-2]):
                claim_info["LAST"]=info[1]
            else:
                claim_info["LAST"]=info[-2]
            
        elif len(re.findall("PATIENT NAME: [A-Z ]+ [A-Z]+:",data[i]))>0: #patient name
            info=re.findall("PATIENT NAME: [A-Z ]+ [A-Z]+:",data[i])[0].replace("PATIENT NAME: ","")
            info=info.split(" ",info.count(" "))
            claim_info["FIRST"]=info[0]
            if len(info[1])>len(info[-2]):
                claim_info["LAST"]=info[1]
            else:
                claim_info["LAST"]=info[-2]
            
                
                    
        elif re.match('\d{1} \d{2}/\d{2} - \d{2}/\d{2}/\d{2}',  data[i]): #dos must has a space with the end
            info=re.findall('^\d{1} \d{2}/\d{2} - \d{2}/\d{2}/\d{2}', data[i]) 
            claim_info["DOS"]=info[0][10:18]
            
        elif len( re.findall("SUBSCRIBER ID: \d+",data[i]))>0: #member ID
            info =re.findall("SUBSCRIBER ID: \d+",data[i])
            claim_info["ID"]="'"+info[0].replace("SUBSCRIBER ID:","").replace(" ","")
            info =re.findall("CLAIM ID: \d+",data[i])
            if len(info)>0:
                claim_info["CLAIM"]="'"+info[0].replace("CLAIM ID:","").replace(" ","").replace("\n","")
        elif len(re.findall("CLAIM ID: \d+",data[i]) )>0: #claim id
            info =re.findall("CLAIM ID: \d+",data[i])
            claim_info["CLAIM"]="'"+ info[0].replace("CLAIM ID:","").replace(" ","")
            
        elif data[i].startswith("Total"): #charge
            info=data[i+2].split(" ",data[i+2].count(" "))
            claim_info['CHARGE']=info[0].replace("$","")
        elif  data[i].startswith("Payment of "): #paid
            claim_info['PAID']= re.findall(" \$\d+\.\d{2} ",data[i])[0].replace("$","").replace(" ","")
        
            
            EOB_CLAIM.save_csv(claim_info)
        else:
            continue

    




