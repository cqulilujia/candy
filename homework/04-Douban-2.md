### 作业目标
1. 熟练掌握字符串处理相关函数
2. 掌握requests库使用方法
3. 掌握selenium库使用方法
4. 掌握bs4库使用方法
5. 掌握xpath使用方法

### 基本要求
1. 使用selenium库启动浏览器
   ```python
   # 网址
   "https://movie.douban.com/typerank?type_name=%E7%A7%91%E5%B9%BB&type=17&interval_id=100:90&action="
   ```
2. 爬取所有电影（共2000多部）
3. 爬取电影信息，包括电影名、主演、上映日期等，使用dict变量存储，并保存到本地，以`movie.json`文件为文件名。
4. 保存电影高清海报到本地
5. 解决网站反爬策略带来的爬取失败问题

### 示例代码
```python
import requests
import json
import time
import os
import requests
from bs4 import BeautifulSoup

def save_image(url, file_path):
    response = requests.get(url)
    with open(file_path, 'wb') as f:
        f.write(response.content)

from selenium import webdriver 

headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"}
url = "https://movie.douban.com/typerank?type_name=%E7%A7%91%E5%B9%BB&type=17&interval_id=100:90&action="

# driver = webdriver.Chrome() # 需下载安装Chrome
browser = webdriver.Chrome()
print(2)
browser.get(url = url)
browser.implicitly_wait(20)
time.sleep(3)
browser.execute_script(f"window.scrollTo(0, {3000});", )
time.sleep(3)

content = browser.page_source
# print(content)
with open("douban.txt", "w") as f:
    f.write(content)
browser.quit()

soup = BeautifulSoup(content, "html.parser")
movie_list_divs = soup.find_all("div", class_="movie-list-panel pictext")
movie_list_div = movie_list_divs[0]
# print(movie_list_div)
movie_list = movie_list_div.find_all("div", class_="movie-list-item playable unwatched")
print(len(movie_list))
for i in range(len(movie_list)):
    movie_name = movie_list[i].find("span", class_="movie-name-text").text
    print(movie_name)
    img_url = movie_list[i].find("img")["data-original"]
    if not os.path.exists(f"movie/{movie_name}"):
        os.mkdir(f"movie/{movie_name}")
    print(img_url)
    save_image(img_url, f"movie/{movie_name}/poster-preview.png")

    # 1 点开电影详情界面
    movie_url = movie_list[i].find("div", class_="movie-info").find("a")["href"]
    print(movie_url)
    browser = webdriver.Firefox()
    browser.get(url = movie_url)
    browser.implicitly_wait(20)
    time.sleep(3)
    # time.sleep(3)
    content = browser.page_source
    soup_movie = BeautifulSoup(content, "html.parser")
    poster = soup_movie.find("a", class_="nbgnbg")["href"]
    print(poster)
    browser.quit()

    # 2 在详情界面点击缩略图位置，进入海报界面
    browser = webdriver.Firefox()
    browser.get(url = poster)
    browser.implicitly_wait(20)
    time.sleep(3)
    content = browser.page_source
    # 3 获取第一个海报地址，存到本地
    first_poster = BeautifulSoup(content, "html.parser").find("ul", class_="poster-col3 clearfix").find("li").find("img")["src"]
    print(first_poster)
    save_image(first_poster, f"movie/{movie_name}/poster-first.png")
    browser.quit()

```