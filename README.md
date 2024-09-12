
### 4.安装 talib

```
第一种方法. pip 下安装
（1）https://www.ta-lib.org/下载并解压ta-lib-0.4.0-msvc.zip
（2）解压并将ta_lib放在C盘根目录
（3）https://visualstudio.microsoft.com/zh-hans/downloads/下载并安装Visual Studio Community，安装切记勾选Visual C++功能
（4）Build TA-Lib Library # 构建 TA-Lib 库
    ①在开始菜单中搜索并打开[Native Tools Command Prompt](根据操作系统选择32位或64位)
    ②输入 cd C:\ta-lib\c\make\cdr\win32\msvc
    ③构建库，输入 nmake
（5）安装完成。
第二种方法. Anaconda 下安装
（1）打开Anaconda Prompt终端。
（2）在终端输入命令行conda install -c conda-forge ta-lib 。
（3）此处确认是否继续安装？输入y 继续安装，直到完成
（4）安装完成。
    conda create -n sequoia39 python=3.9
    conda activate sequoia39  
    conda install -c conda-forge ta-lib 
```

a.安装依赖库：

```
#dos切换到本系统的根目录，执行下面命令：
pip install -r requirements.txt
```
b.若想升级项目依赖库至最新版，可以通过下面方法：

先打开requirements.txt，然后修改文件中的“==”为“>=”，接着执行下面命令：

```
pip install -r requirements.txt --upgrade
```
```
uvicorn main:app --reload
```

