豆瓣电影评论摘要
==============

### 安装

	$ pip install -r requirements.txt

Example:

	$ python summary.py -f example.txt

### 使用

#### 抓取数据

	$ python crawl.py -u <影评列表页url>

比如抓取<爱宠大机密>的影评:

	$ python crawl.py -u "https://movie.douban.com/subject/21817627/reviews"

查看完整命令：

	$ python crawl.py -h

#### 生成摘要

	$ python summary.py -f <filename>

比如 <爱宠大机密> 对应的文件名为 subject_21817627.txt：

	$ python summary.py -f subject_21817627.txt

查看所有已保存的评论文件：

	$ python summary.py -l

查看完整命令：

	$ python summary.py -h
