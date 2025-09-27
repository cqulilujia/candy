
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
from selenium.webdriver.chrome.options import Options


headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"}
url = "https://movie.douban.com/typerank?type_name=%E7%A7%91%E5%B9%BB&type=17&interval_id=100:90&action="

browser = webdriver.Chrome(options=chrome_options)
browser.get(url = url)
browser.implicitly_wait(20)
time.sleep(3)

for i in range(10):
    browser.execute_script(f"window.scrollTo(0, {(i+1)*3000});", )
    time.sleep(3)

content = browser.page_source
with open("douban.txt", "w", encoding="utf-8") as f:
    f.write(content)
browser.quit()

soup = BeautifulSoup(content, "html.parser")
movie_list_divs = soup.find_all("div", class_="movie-list-panel pictext")
movie_list_div = movie_list_divs[0]
movie_list = movie_list_div.find_all("div", class_="movie-list-item")
print(f"找到 {len(movie_list)} 部电影")

all_movies = []

for i in range(min(10, len(movie_list))):
    print(f"\n正在处理第 {i+1} 部电影:")
    
    movie_name = movie_list[i].find("span", class_="movie-name-text").text
    print(f"电影名: {movie_name}")
    
    img_url = movie_list[i].find("img")["data-original"]
    if not os.path.exists(f"movie/{movie_name}"):
        os.makedirs(f"movie/{movie_name}")
    save_image(img_url, f"movie/{movie_name}/poster-preview.png")

    movie_info = {
        "name": movie_name,
        "preview_image": img_url
    }

    movie_url = movie_list[i].find("div", class_="movie-info").find("a")["href"]
    
    browser = webdriver.Chrome(options=chrome_options)
    browser.get(url = movie_url)
    browser.implicitly_wait(20)
    time.sleep(3)
    content = browser.page_source
    soup_movie = BeautifulSoup(content, "html.parser")
    
    actors = []
    actor_links = soup_movie.find_all("a", attrs={"rel": "v:starring"})
    for actor in actor_links:
        actors.append(actor.text)
    movie_info["actors"] = actors
    print(f"演员: {', '.join(actors) if actors else '未知'}")
    
    release_date = soup_movie.find("span", attrs={"property": "v:initialReleaseDate"})
    if release_date:
        movie_info["release_date"] = release_date.text
        print(f"上映日期: {release_date.text}")
    else:
        movie_info["release_date"] = "未知"
        print("上映日期: 未知")
    
    director = soup_movie.find("a", attrs={"rel": "v:directedBy"})
    if director:
        movie_info["director"] = director.text
        print(f"导演: {director.text}")
    else:
        movie_info["director"] = "未知"
        print("导演: 未知")
    
    genres = []
    genre_links = soup_movie.find_all("span", attrs={"property": "v:genre"})
    for genre in genre_links:
        genres.append(genre.text)
    movie_info["genres"] = genres
    print(f"类型: {', '.join(genres) if genres else '未知'}")
    
    rating = soup_movie.find("strong", class_="ll rating_num")
    if rating:
        movie_info["rating"] = rating.text
        print(f"评分: {rating.text}")
    else:
        movie_info["rating"] = "无评分"
        print("评分: 无评分")
    
    poster_link = soup_movie.find("a", class_="nbgnbg")
    if poster_link:
        poster = poster_link["href"]
        browser.quit()

        browser = webdriver.Chrome(options=chrome_options)
        browser.get(url = poster)
        browser.implicitly_wait(20)
        time.sleep(3)
        content = browser.page_source
        poster_soup = BeautifulSoup(content, "html.parser")
        poster_ul = poster_soup.find("ul", class_="poster-col3 clearfix")
        if poster_ul:
            first_li = poster_ul.find("li")
            if first_li:
                first_poster = first_li.find("img")["src"]
                save_image(first_poster, f"movie/{movie_name}/poster-first.png")
                movie_info["high_res_poster"] = first_poster
    
    browser.quit()
    all_movies.append(movie_info)

print(f"\n总共处理了 {len(all_movies)} 部电影")
with open("movie.json", "w", encoding="utf-8") as f:
    json.dump(all_movies, f, ensure_ascii=False, indent=2)
print("电影信息已保存到 movie.json 文件")
