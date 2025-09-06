from urllib.request import urlopen
import csv
import json
import time
csv_url = "https://gitee.com/wiedersehen/basic_function_project/raw/master/weather_district_id.csv"
resp = urlopen(csv_url)
with open("weather_district_id.csv", mode="wb") as f:
    f.write(resp.read())
province_data = {}
with open("weather_district_id.csv", encoding='utf-8') as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        if len(row) >= 12:
            province = row[11]
            district = row[5]
            areaid = row[0]
            
            if province not in province_data:
                province_data[province] = []
            province_data[province].append((district, areaid))
print(f"成功读取了 {len(province_data)} 个省份的数据")
def get_weather(areaid):
    url = f"http://t.weather.itboy.net/api/weather/city/{areaid}"
    response = urlopen(url)
    text = response.read().decode('utf-8')
    print(f"API返回数据前50个字符: {text[:50]}")
    if "success" not in text:
        return None
    dict_weather = json.loads(text)
    temps = []
    if "data" in dict_weather and "forecast" in dict_weather["data"]:
        forecast = dict_weather["data"]["forecast"]
        for day in forecast:
            # 使用条件判断替换try-except
            if "high" in day and "low" in day:
                high_str = day["high"]
                low_str = day["low"]
                
                # 提取数字部分
                high_digits = ''.join(filter(str.isdigit, high_str))
                low_digits = ''.join(filter(str.isdigit, low_str))
                
                # 检查是否成功提取到数字
                if high_digits and low_digits:
                    high = int(high_digits)
                    low = int(low_digits)
                    
                    avg_temp = (high + low) / 2
                    temps.append(avg_temp)
                    print(f"      温度: 高{high}℃ 低{low}℃ 平均{avg_temp}℃")
                else:
                    print(f"      无法提取温度数字")
            else:
                print(f"      无法找到高低温数据")
    return temps
province_temps = {}
for province, districts in province_data.items():
    print(f"正在获取{province}的天气数据...")
    daily_temps = [[] for _ in range(7)]
    sample_districts = districts[:2] if len(districts) > 2 else districts
    valid_data = False
    for district, areaid in sample_districts:
        print(f"  正在获取{district}(ID:{areaid})的天气数据...")
        temps = get_weather(areaid)
        if temps and len(temps) > 0:
            valid_data = True
            for i, temp in enumerate(temps):
                if i < 7:
                    daily_temps[i].append(temp)
        time.sleep(1)
    if valid_data:
        avg_temps = []
        for day_temps in daily_temps:
            if day_temps:
                avg = sum(day_temps) / len(day_temps)
                avg_temps.append(avg)
                print(f"  第{len(avg_temps)}天平均温度: {round(avg, 1)}℃")
            else:
                avg_temps.append(0)
                print(f"  第{len(avg_temps)}天没有温度数据")
        province_temps[province] = avg_temps

print("\n各省未来一周平均温度:")
print("省份", end="")
for i in range(7):
    print(f"\t第{i+1}天", end="")
print()

for province, temps in province_temps.items():
    print(province, end="")
    for temp in temps:
        print(f"\t{round(temp, 1)}℃", end="")
    print()

with open("province_temps.txt", "w", encoding="utf-8") as f:
    f.write("省份")
    for i in range(7):
        f.write(f"\t第{i+1}天")
    f.write("\n")
    
    for province, temps in province_temps.items():
        f.write(province)
        for temp in temps:
            f.write(f"\t{round(temp, 1)}℃")
        f.write("\n")