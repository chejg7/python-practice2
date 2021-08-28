from bs4 import BeautifulSoup
import urllib.request as req
import urllib.parse as par

keyword = "사회"
encoded = par.quote(keyword) # 한글 -> 특수한 문자

page_num = 1
output_total = ""
while True:
    url = f"https://www.joongang.co.kr/_CP/496?keyword={encoded}&sort%20=&pageItemId=439&page={page_num}"
    code = req.urlopen(url)
    soup = BeautifulSoup(code, "html.parser")
    title = soup.select("h2.headline a")
    if len(title) == 0: # 끝 페이지까지 크롤링 완료했으면?
        break
    for i in title:
        print("제목 :", i.text.strip())
        print("링크 :", i.attrs["href"])
        code_news = req.urlopen(i.attrs["href"])
        soup_news = BeautifulSoup(code_news, "html.parser")
        content = soup_news.select_one("div#article_body")
        result = content.text.strip().replace("     ", " ").replace("   ", "")
        print(result)
        print()
        output_total += result

    page_num += 1
    if page_num == 2:
        break

# 형태소 분석기
print("형태소 분석 중입니다..")
from konlpy.tag import Okt
okt = Okt()
print("명사만 추출합니다..")
nouns = okt.nouns(output_total)

#명사 빈도수 카운트
from collections import Counter
count = Counter(nouns)

#불용어 제거
temp = count.copy()
for i in temp.keys():
    if len(i) == 1:
        del count[i]

# 단어구름 만들기
# 이미지 가져오기
import numpy as np
from PIL import Image
image_list = np.array(Image.open("./image.jpg"))
#이미지 색 뽑아오기
from wordcloud import ImageColorGenerator
image_color = ImageColorGenerator(image_list)

from wordcloud import WordCloud
wordcloud = WordCloud(font_path="./NanumMyeongjoBold.ttf", background_color="white", mask=image_list).generate_from_frequencies(count)

#단어구름 띄우기
import matplotlib.pyplot as plt
plt.figure(figsize=(10,10))
plt.imshow(wordcloud.recolor(color_func=image_color), interpolation="bilinear")
plt.axis('off')
plt.show()