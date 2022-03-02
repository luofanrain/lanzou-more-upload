import os
import fitz
import os
import zipfile
 
rootPath = os.getcwd()
def imageToPdf(fileName):
    doc = fitz.open()
    imgdoc = fitz.open(fileName)                 # 打开图片
    pdfbytes = imgdoc.convert_to_pdf()        # 使用图片创建单页的 PDF
    imgpdf = fitz.open("pdf", pdfbytes)
    doc.insert_pdf(imgpdf)   
    pdfName = f"{'.'.join(fileName.split('.')[0:-1])}.pdf"           
    doc.save(pdfName)       
    doc.close()
    os.remove(fileName)

def dealWithToZip(filePath,fileName, targetFileName):
    zipf = zipfile.ZipFile(targetFileName, 'w',zipfile.ZIP_DEFLATED)
    zipf.write(filePath, fileName)
    zipf.close()
    os.remove(filePath)

def dealWithOtherFile(filePath,exts):
  files = os.listdir(filePath)
  for file in files:
    fileName = f"{filePath}/{file}"
    if os.path.isdir(fileName):
        dealWithOtherFile(fileName,exts)
    else:
        fileInfo = fileName.split('.')
        ext = fileInfo[-1].lower()
        print(fileName)
        if not ext in exts:
            fileSize = os.path.getsize(fileName)
            if fileSize > 1024 * 1024 * 100:
                continue
            targetFileName = f"{'.'.join(fileInfo[0:-1])}.zip"
            dealWithToZip(fileName,file,targetFileName)
            pass