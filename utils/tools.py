import os
import json

def getPath(targetPath):
    rootPath = os.getcwd()
    return f"{rootPath}/{targetPath}"

def getHeaders(path=""):
    # fileName = "config/cookie.json"
    fileName = getPath(f"{path}config/cookie.json")
    file = open(fileName,encoding="utf-8")
    data = file.read()
    file.close()
    Cookie = json.loads(data)
    return {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
        "Cookie":f"phpdisk_info={Cookie['phpdisk_info']};ylogin={Cookie['ylogin']}"
    }