#!/usr/bin/env python
#encoding: utf-8

import logging.handlers
import re

import EOB_CLAIM

PROVIDER_NUMBER_TAG="Provider Number"
NAME_TAG = "PATIENT NAME:"
ID_TAG="SUBSCRIBER#:"
BILL_TAG="Total"
PROVIDER_TAG="PAYMENT OF"

logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='myapp.log',
                filemode='w')


def PARSING_EOB(filePath):

    
    claim_info= EOB_CLAIM.CLAIM_INFO()
    data=""
    with open(filePath, 'rt') as f:
        data = f.readlines()
    f.close()

    for i in range(len(data)):


        if data[i].startswith("PATIENT NAME:"):       # name
            info=data[i].replace("PATIENT NAME: ","")
            info=info.split(" ",info.count(" "))
            claim_info["FIRST"] = info[0]
            if len(info)==2:
                claim_info["LAST"] =info[-1].replace("\n","")
            else:
                if len(info[1])>len(info[-1]):
                    claim_info["LAST"] =info[1].replace("\n","")
                else:
                    claim_info["LAST"] =info[-1].replace("\n","")
            
        elif re.match("Provider Number \d{9} ", data[i]):
            claim_info['TAX']=data[i].replace("Provider Number ","")[:9]
        elif data[i].startswith(ID_TAG):     # id
            member_id = data[i].split(" ", data[i].count(" "))
            claim_info['ID'] = "'"+member_id[1].replace("\n","")
        elif data[i].startswith("REF#:"):
            claim_info['CLAIM']=("'"+data[i].split(" ",data[i].count(' '))[1].replace("\n",""))
        elif data[i]=="Total\n": #paid info
            claim_info['CHARGE'] = data[i+2].replace("$","").replace("\n","")
            claim_info['ALLOW'] = data[i+4].replace("$","").replace("\n","")
            
            if re.match("^\d{1,4}\.\d{2} \$\d{1,4}\.\d{2}\n$",data[i+6]): 
                info = data[i+6].split(" ",data[i+6].count(" "))
                claim_info['DED'] = info[1].replace("$","").replace("\n","")
            elif re.match("^\$\d{1,4}\.\d{2}\n$",data[i+8]) or re.match("^\d{1,4}\.\d{2}\n$",data[i+8]): 
                claim_info['DED'] = data[i+8].replace("$","").replace("\n","")
            elif re.match("^\$\d{1,4}\.\d{2}\n$",data[i+10]) or re.match("^\d{1,4}\.\d{2}\n$",data[i+10]): 
                claim_info['DED'] = data[i+10].replace("$","").replace("\n","")
            else:
                claim_info['DED'] = ""
        elif re.match("\d{1} \d{8} \d{8}",data[i]):
            info=str(data[i][2:10])
            claim_info['DOS']=info[0:2]+"/"+info[2:4]+"/"+info[4:]   
            
                
        elif data[i].startswith("Remittance Tracking Number"):
            claim_info['EOB']="'"+data[i].split(" ",data[i].count(' '))[-1].replace("\n","")

        elif data[i]=="PAYMENT OF\n":
            claim_info['PAID'] = data[i+2].split(' ',data[i+2].count(' '))[0].replace("$","").replace("\n","")
            

            EOB_CLAIM.save_csv(claim_info)

        #elif data[i] == "VIEW ELIGIBILITY, BENEFITS, AND CLAIM DETAILS AND GET PRECERTIFICATION\n":
        elif len( re.findall("VIEW ELIGIBILITY, BENEFITS, AND CLAIM DETAILS AND GET PRECERTIFICATION" ,data[i]))>0:
            EOB_CLAIM.save_csv(claim_info)



            
        else:
            continue
    
    
    