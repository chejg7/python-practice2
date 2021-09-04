from bs4 import BeautifulSoup
import urllib.request as req
import urllib.parse as par

keyword = "파이썬"
encoded = par.quote(keyword) # 한글 -> 특수한 문자

page_num = 1
output_list = []
while True:
    url = f"https://www.joongang.co.kr/_CP/496?keyword={encoded}&sort%20=&pageItemId=439&page={page_num}"
    code = req.urlopen(url)
    soup = BeautifulSoup(code, "html.parser")
    title = soup.select("h2.headline a")
    if len(title) == 0: # 끝 페이지까지 크롤링 완료했으면?
        break
    for i in title:
        print("제목 :", i.text.strip())
        output_list.append(i.text)
    page_num += 1
    if page_num == 2:
        break

from konlpy.tag import Okt
okt = Okt()
dataset = []
for title in output_list:
    result = okt.nouns(title)
    result_without_stopwords = []
    for i in result:
        if len(i) != 1: #불용어가 아니라면?
            result_without_stopwords.append(i)
    dataset.append(result_without_stopwords)

import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori

te = TransactionEncoder()
te_ary = te.fit(dataset).transform(dataset)
df = pd.DataFrame(te_ary, columns=te.columns_)
df_apr = apriori(df, use_colnames=True, min_support=0.01)
print(df_apr)
