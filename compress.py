import os
import glob
import fitz
import os
from PIL import Image
 
rootPath = os.getcwd()
def mergeImageToPDF(fileName,count):
    doc = fitz.open()
    for index in range(count):
        imageFile = f"{rootPath}/pdf/{index+1}.jpg"
        imgdoc = fitz.open(imageFile)                 # 打开图片
        pdfbytes = imgdoc.convert_to_pdf()        # 使用图片创建单页的 PDF
        imgpdf = fitz.open("pdf", pdfbytes)
        doc.insert_pdf(imgpdf)                   
    doc.save(fileName)                   # 保存pdf文件
    doc.close()

def getSize(file):
    # 获取文件大小:KB
    size = os.path.getsize(file)
    return size / 1024

def compressImage(fileName, outPath, mb=500, step=10, quality=80):
    """不改变图片尺寸压缩到指定大小
    :param infile: 压缩源文件
    :param outfile: 压缩文件保存地址
    :param mb: 压缩目标，KB
    :param step: 每次调整的压缩比率
    :param quality: 初始压缩比率
    """
    o_size = getSize(fileName)
    if o_size <= mb:
        return fileName
    while o_size > mb:
        imageBlob = Image.open(fileName)
        try:
            imageBlob.save(outPath, quality=quality)
        except Exception:
            return
        if quality - step < 0:
            break
        quality -= step
        o_size = getSize(outPath)
    os.remove(fileName)
    os.rename(outPath,fileName)
    

def compressFile(fileName):
    print(f"压缩pdf:{fileName}")
    doc = fitz.open(fileName)    
    count = doc.pageCount
    for pg in range(count):
        page = doc[pg]
        zoom = int(100)
        rotate = int(0)
        trans = fitz.Matrix(zoom / 100.0, zoom / 100.0).prerotate(rotate)
        pm = page.get_pixmap(matrix=trans, alpha=False)
    
        curFile =f'{rootPath}/pdf/{str(pg+1)}.jpg'
        outFile=f'{rootPath}/pdf/{str(pg+1)}-output.jpg'
        pm.save(curFile)
        compressImage(curFile,outFile)
        
    doc.close()
    os.remove(fileName)
    mergeImageToPDF(fileName,count)

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

# status 是否处理 100M以下的
def dealWithCompress(filePath,status):
  files = os.listdir(filePath)
  for file in files:
    fileName = f"{filePath}/{file}"
    if os.path.isdir(fileName):
        dealWithCompress(fileName,status)
    else:
        ext = fileName[-4:].lower()
        if  ".pdf" != ext:
            continue
        fileSize = getSize(fileName)
        if not status and fileSize < 1000 * 100:
            continue  
        compressFile(fileName)