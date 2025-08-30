### 作业目标
1. 熟练掌握字符串处理相关函数
2. 掌握requests库使用方法
3. 掌握selenium库使用方法

### 基本要求
1. 使用selenium库启动浏览器
   ```python
   # 网址
   "https://movie.douban.com/typerank?type_name=%E7%A7%91%E5%B9%BB&type=17&interval_id=100:90&action="
   ```
2. 爬取页面所有电影信息，包括电影名、主演、上映日期等，使用dict变量存储，并保存到本地，以`movie.json`文件为文件名。

### 示例代码
```python
import json
import os
import requests
from selenium import webdriver 

headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"}
url = "https://movie.douban.com/typerank?type_name=%E7%A7%91%E5%B9%BB&type=17&interval_id=100:90&action="

# 需下载安装Chrome浏览器
browser = webdriver.Chrome()
browser.get(url = url)
browser.implicitly_wait(20)
time.sleep(3)
content = browser.page_source
with open("douban.txt", "w") as f:
    f.write(content)
browser.quit()
```