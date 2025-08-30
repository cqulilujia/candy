### 作业目标
1. 掌握文件读取功能
2. 掌握requests库使用方法

### 基本要求
1. 读取本地的`weather_district_id.csv`文件，获取所有地区的`id`，用于获取天气信息。
   ```python
   # csv文件地址
   https://gitee.com/wiedersehen/basic_function_project/blob/master/weather_district_id.csv
   ```
2. 根据地区`id`，通过爬虫获取每个地区未来七天的最高温度。
3. 计算每个省未来七天所有城市的平均最高温度，并依次打印，打印格式如下：
   ```
   省份1：
   第1天：x1摄氏度
   第2天：x2摄氏度
   ···
   第7天：x7摄氏度
   -------------------
   省份2：
   第1天：y1摄氏度
   第2天：y2摄氏度
   ···
   第7天：y7摄氏度
   -------------------
   ···
   ```
### 示例代码
```python
import requests
import json

def get_wether():
    url = 'http://t.weather.itboy.net/api/weather/city/101021500'
    response = requests.get(url)
    text = response.text # string
    dict_weather = json.loads(text)
    forecast = dict_weather["data"]["forecast"]
    tomorrow_weather = forecast[1]
    print(f'最高温度：{tomorrow_weather['high']}，最低温度：{tomorrow_weather['low']}，天气：{tomorrow_weather['type']}')
```