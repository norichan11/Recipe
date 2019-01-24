from urllib.request import urlopen, Request
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import pandas as pd

df = pd.DataFrame(columns=["Recipe", "Ingredient", "URL", "Class", "Page"])
"""
 存出分項 List 與其 url
"""
print("食譜分類:")
r = Request("https://icook.tw/categories/")
r.add_header("User-Agent", "Mozilla/5.0")
responce = urlopen(r)
html = BeautifulSoup(responce)
#print(html)

menu_list = html.find_all("a", class_="list-title")
#print(menu_list[0])
for i in range(0, len(menu_list)):
    print(menu_list[i]["name"], menu_list[i]["href"])
# output:
#早餐 /categories/147
#早午餐 /categories/210
#下午茶 /categories/206
"""
 存出各分項下食譜List與其食材, url, 分類, 第幾頁(for debug), Image(未完成)
"""
print(" ")
print("分項食譜列表:")
page = 0

for c in range(0, len(menu_list)):  #range(0, 3):  #
    page = 0
    while True:
        page = page + 1
        url1 = "https://icook.tw" + menu_list[c]["href"] + "?page=" + str(page)
        print("正在處理: ", url1)
        try:
            r = Request(url1)
            r.add_header("User-Agent", "Mozilla/5.0")
            responce = urlopen(r)
        except HTTPError:
            print("[!] 到本分類", menu_list[c]["name"], "最後一頁了")
            break

        html = BeautifulSoup(responce)
          #  print(html)

        recipe_item = html.find_all("div", class_="browse-recipe-content")
        #print(recipe_item[0])
        for j in range(0, len(recipe_item)):
            recipe_name = recipe_item[j].find("a", class_="browse-recipe-name")
            #print(recipe_name["title"], recipe_name["href"])
            ingredient = recipe_item[j].find("p", class_="browse-recipe-content-ingredient")
            #print(ingredient.text)

            s = pd.Series([recipe_name["title"], ingredient.text, recipe_name["href"], menu_list[c]["name"], str(page)],
                          index=["Recipe", "Ingredient", "URL", "Class", "Page"])
            df = df.append(s, ignore_index=True)
"""
 存檔
"""
df.to_csv("icook.csv", encoding="utf-8", index=False)