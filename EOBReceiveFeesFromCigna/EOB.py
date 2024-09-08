

#!/usr/bin/env python
#encoding: utf-8

import os
import re
import shutil

import requests

# import EOB_AETNA
# import EOB_AVAILITY
import EOB_CIGNA_IN
import EOB_CIGNA_OUT

#import EOB_UHC
 

CIGNA_ALIEN_CODE='"056/'
CIGNA_ALIEN_FLAG_2='!"#$'
AETNA_EOB_FLAG="Aetna"
CIGNA_IN_EOB_FLAG="Cigna"
CIGNA_OUT_EOB_FLAG="Cigna Health"
UHC_EOB_FLAG="UNITEDHEALTHCARE"
OPTUM_EOB_TAG="Optum Pay"
AVAILITY_EOB_FLAG="Check Summary"
UMR_EOB_FLAG="UMR USNAS"
WRITTEN = False
FAILURE_LIST=[]
SUCCESS_LIST=[]

def PARSING_EOB(filePath):
    
    data=""
    with open(filePath, 'rt') as f:
        data = f.readlines()
    f.close()
    pattern=0
    
    for i in range(len(data)):
        if data[i].find( CIGNA_ALIEN_CODE )!=-1:

            pattern=0
            break
        elif data[i].startswith (CIGNA_OUT_EOB_FLAG):

            EOB_CIGNA_OUT.PARSING_EOB(filePath)

            pattern=2
            break
        elif data[i].find(CIGNA_IN_EOB_FLAG)!=-1:

            EOB_CIGNA_IN.PARSING_EOB(filePath)

            pattern=7
            break
        elif data[i].find(CIGNA_ALIEN_FLAG_2)!=-1:

            pattern=0
            break
        else:
            if i>100:
                pattern=0
                break
    if pattern==0:
        print( filePath )



def download_driver(path):
    '''下载文件'''
    # if os.path.exists(path+r"\pdftotxt.exe"):
    if os.path.exists("pdftotxt.exe"):
        return
    file = requests.get(
        "https://drive.google.com/u/1/uc?id=1OQdtDbh4xt670mZnFkhVBxIyptRhUvYK&export=download&confirm=t&uuid=4bf668fe-d6d9-4949-93f4-682fb588cafa&at=ACjLJWngZP7pzu4G-cxYx1vc7YcW:1672623412064")
    with open("pdftotxt.exe", 'wb') as _file:  # save the downloaded chromeDriver.zip
        _file.write(file.content)
    shutil.move(os.getcwd() + r"/pdftotxt.exe", path + r"/pdftotxt.exe")

    print("\nSTART......")


def running(path):
    #download_driver(path)
    if os.path.exists(os.getcwd() + r"\EOB.csv"):
        os.remove(os.getcwd() + r"\EOB.csv")

    scaning(path)
    # os.remove(path+r"/pdftotxt.exe")
    for item in FAILURE_LIST:
        print(item)


def scaning(path):
    global SUCCESS_LIST
    global FAILURE_LIST
    # UHC_MERGE = PdfFileWriter()
    for filename in os.listdir(path):

        fp = os.path.join(path, filename)

        if os.path.isdir(fp):
            scaning(fp)
            continue

        # os.path.splitext() method in Python is used to split the path name into a pair root and ext. Here,
        # ext stands for extension and has the extension portion of the specified path while root is everything
        # except ext part.
        if os.path.splitext(fp)[-1].lower() != ".pdf":
            continue
        if re.search(r" ", filename):
            os.rename(fp, fp.replace(" ", ""))
            fp = fp.replace(" ", "")

        txtFp = fp.replace(".pdf", ".txt").replace(".PDF", ".txt")
        # os.system(path+"\\pdftotxt.exe"+" "+fp+" "+txtFp)

        os.system("pdftotxt.exe" + " " + fp + " " + txtFp)


        if os.path.exists(txtFp):


            PARSING_EOB(txtFp)


            SUCCESS_LIST.append(fp)
            os.remove(txtFp)
        else:

            FAILURE_LIST.append(fp)


