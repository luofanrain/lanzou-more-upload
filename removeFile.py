
import os


def removeFile(filePath):
  files = os.listdir(filePath)
  for file in files:
    fileName = f"{filePath}/{file}"
    if os.path.isdir(fileName):
      removeFile(fileName)
    else:
      if "长期更新" in fileName or "公众号" in fileName:
        os.remove(fileName)