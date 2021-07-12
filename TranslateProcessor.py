#!/usr/bin/env python3

import xml.dom.minidom
import csv

stringFileName = "strings.xml" # 提供string的key
csvFileName = "translate.csv"  # 翻译文件，需包含key
fieldKeyName = 'FieldName'     # key列的csv列名
needFieldNames = []

reader = csv.DictReader(open(csvFileName, 'r', encoding='utf-8'))
translateList = []
for csvFieldName in reader.fieldnames:
    needFieldNames.append(csvFieldName)
for translateRow in reader:
    tmpDict = {fieldKeyName : translateRow[fieldKeyName]}
    for fieldName in needFieldNames:
        tmpDict[fieldName] = translateRow[fieldName]
    translateList.append(tmpDict)
for fieldName in needFieldNames:
    if (fieldName == fieldKeyName):
        continue
    dom = xml.dom.minidom.parse(stringFileName)
    root = dom.documentElement
    stringElementList = root.getElementsByTagName("string")
    for stringElement in stringElementList:
        aimStrName = stringElement.getAttribute("name")
        for translateRow in translateList:
            if translateRow[fieldKeyName] == aimStrName:
                stringElement.firstChild.data = translateRow[fieldName]
    doc = xml.dom.minidom.Document()
    doc.appendChild(root)
    saveFileName = "strings-{name}.xml".format(name = fieldName)
    with open(saveFileName, "x", encoding="utf-8") as saveFile:
        doc.writexml(saveFile, encoding="utf-8")
    print(f'{saveFileName} translate finished!!!')
print("all finished!!!")