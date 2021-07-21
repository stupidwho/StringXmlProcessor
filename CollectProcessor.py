#!/usr/bin/env python3

import xml.dom.minidom
import csv
import os
from pathlib import Path

aimProjectRootDir = "C:\\Users\\YY\\Projects\\ShoplinePOS-android\\"
csvFileName = "collect.csv"  # 已翻译文件
fieldKeyName = 'name'     # key列的csv列名
ignoreModule = ['sample']

moduleDirPathList = []
for dirpath, dirnames, filenames in os.walk(aimProjectRootDir):
    srcStringsXmlPath = Path(dirpath) / 'src' / 'main' / 'res' / 'values' / 'strings.xml'
    needProcess = True
    if Path(dirpath).name in ignoreModule:
        needProcess = False
    if 'build.gradle' in filenames and srcStringsXmlPath.exists() and needProcess:
        print(dirpath)
        moduleDirPathList.append(dirpath)

languageSet = set()
for moduleDirPath in moduleDirPathList:
    resDirPath = Path(moduleDirPath) / 'src' / 'main' / 'res'
    for itemDir in resDirPath.iterdir():
        if itemDir.name.startswith("values"):
            languageSet.add(itemDir.name)
headerNames = list(languageSet)
headerNames.sort()
headerNames.insert(0, "name")
print(headerNames)
csvWriter = csv.DictWriter(f=open(csvFileName, mode='x', encoding='utf-8', newline='\n'), fieldnames=headerNames)
csvWriter.writeheader()

for moduleDirPath in moduleDirPathList:
    resultList = []
    defaultStringsXmlPath = Path(moduleDirPath) / 'src' / 'main' / 'res' / 'values' / 'strings.xml'
    defaultElementList = xml.dom.minidom.parse(str(defaultStringsXmlPath)).documentElement.getElementsByTagName("string")
    for stringElement in defaultElementList:
        aimStrName = stringElement.getAttribute("name")
        strItemDict = {"name":aimStrName}
        resultList.append(strItemDict)

    for language in languageSet:
        srcStringsXmlPath = Path(moduleDirPath) / 'src' / 'main' / 'res' / language / 'strings.xml'
        if srcStringsXmlPath.exists():
            stringElementList = xml.dom.minidom.parse(str(srcStringsXmlPath)).documentElement.getElementsByTagName("string")
            for stringElement in stringElementList:
                aimStrName = stringElement.getAttribute("name")
                aimStrValue = stringElement.firstChild.data
                for resultItem in resultList:
                    if resultItem["name"] == aimStrName:
                        resultItem[language] = aimStrValue
                        break
    
    csvWriter.writerows(resultList)
print("Collect Finish")
