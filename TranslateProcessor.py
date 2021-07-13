#!/usr/bin/env python3

import xml.dom.minidom
import csv
import os
from pathlib import Path

aimProjectRootDir = "C:\\Users\\YY\\Projects\\ShoplinePOS-android\\"
csvFileName = "translate.csv"  # 翻译文件，需包含key
fieldKeyName = 'FieldName'     # key列的csv列名
needFieldNames = ['th-rTH','vi-rVN']
ignoreModule = ['sample']

# 获取所有翻译内容
reader = csv.DictReader(open(csvFileName, 'r', encoding='utf-8'))
translateList = []
for translateRow in reader:
    tmpDict = {fieldKeyName : translateRow[fieldKeyName]}
    for fieldName in needFieldNames:
        tmpDict[fieldName] = translateRow[fieldName]
    translateList.append(tmpDict)

# 找到各个module并更新
moduleDirPathList = []
for dirpath, dirnames, filenames in os.walk(aimProjectRootDir):
    srcStringsXmlPath = Path(dirpath) / 'src' / 'main' / 'res' / 'values' / 'strings.xml'
    needProcess = True
    if Path(dirpath).name in ignoreModule:
        needProcess = False
    if 'build.gradle' in filenames and srcStringsXmlPath.exists() and needProcess:
        print(dirpath)
        moduleDirPathList.append(dirpath)

# 更新strings.xml
for moduleDirPath in moduleDirPathList:
    srcStringsXmlPath = Path(moduleDirPath) / 'src' / 'main' / 'res' / 'values' / 'strings.xml'
    for fieldName in needFieldNames:
        if (fieldName == fieldKeyName):
            continue
        dom = xml.dom.minidom.parse(str(srcStringsXmlPath))
        root = dom.documentElement
        stringElementList = root.getElementsByTagName("string")
        for stringElement in stringElementList:
            aimStrName = stringElement.getAttribute("name")
            for translateRow in translateList:
                if translateRow[fieldKeyName] == aimStrName:
                    stringElement.firstChild.data = translateRow[fieldName]
        doc = xml.dom.minidom.Document()
        doc.appendChild(root)
        saveDirPath = Path(moduleDirPath) / 'src' / 'main' / 'res' / "values-{name}".format(name = fieldName)
        if not saveDirPath.exists():
            saveDirPath.mkdir(parents = True)
        saveFilePath = Path(saveDirPath) / 'strings.xml'
        saveWritter = open(saveFilePath, mode='w', encoding='utf-8') if saveFilePath.exists() else open(saveFilePath, mode='x', encoding='utf-8')
        saveWritter.write('<?xml version="1.0" encoding="utf-8"?>\n')
        root.writexml(saveWritter)
        print(f'{saveFilePath} translate finished!!!')