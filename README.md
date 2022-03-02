## 蓝奏云批量上传

### 使用方法
#### 1、下载扩展 
```
pip install -r package.txt
```
#### 2、从浏览器获取phpdisk_info和ylogin复制到main.py即可，备注(cookie有效期只有三天)
```
Cookie = {
    "phpdisk_info":"",
    "ylogin":""
}
```
#### 3、在main.py的Config中配置指定的文件目录和本地目录，执行即可上传
```
Config = {
    "rootPath":"E:/转移/PPT", # 本地目录
    "rootFolderId":"4877118",  # 目标文件纠结啊
}
```

### 文件描述，按系统目录排序
- compress.py 压缩pdf文件
- dealWithLargeFile.py 处理超过限制size的pdf文件，将他拆分程多个文件
- dealWithOtherFile.py 处理限制上传文件，将他们压缩程zip
- removeFile.py 处理广告文件，批量干掉
- main.py 主程序文件

### 工具文件

- mergeFile.py 合并以上拆分的文件
- renameFile.py 重命名文件 重命名格式为 （【子目录名】-【子子目录名】-【子子目录名】-文件名）依次，中间用横线分割
- getFilePath.py 查找文件，可以获取指定文件夹名字
