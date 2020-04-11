from bs4 import BeautifulSoup
import urllib.request
import pandas as pd

'''
1. 전체 코멘트 수로 페이지 수를 계산한다.
2. get_comments로 코멘트를 구한다. 이 과정에서 스포일러, 관람객, 더보기 등을 고려한다.
3. dataframe으로 바꾸고, text로 저장한다.
'''

def get_comments(url):
    comments = []

    response = urllib.request.urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html, 'html.parser')

    lis = soup.find('div', {'class':'score_result'}).findAll('li')

    for li in lis:
        try:
            content = li.findAll('a')[-5]['data-src'] # 더보기를 눌러야 하는 경우, 'data-src'가 있음.
        except:
            content = li.find('p').getText()[30:].strip() # 관람객 + 스포일러 같은 의미없는 Text를 날리기 위해 앞에 30개 정도 Skip.
        score = li.find('em').getText()
        ID = li.findAll('a')[-4].getText().strip()
        date = li.findAll('em')[-2].getText()
        like = li.find('div', {'class':'btn_area'}).findAll('strong')[0].getText()
        dislike = li.find('div', {'class':'btn_area'}).findAll('strong')[1].getText()

        comments.append([content, score, ID, date, like, dislike])

    return comments

# movie_num에 영화 번호를 입력
movie_num = 190588
url = "https://movie.naver.com/movie/bi/mi/pointWriteFormList.nhn?code="+movie_num+"&type=after&isActualPointWriteExecute=false&isMileageSubscriptionAlready=false&isMileageSubscriptionReject=false&page="
response = urllib.request.urlopen(url)
html = response.read()
soup = BeautifulSoup(html, 'html.parser')
total_raw = soup.find('div', {'class' : 'score_total'}).find('em').getText()
total = int(total_raw.replace(',',''))

total_comments = []

for i in range(1, (total+9)//10+1):
    print(i)
    total_comments.extend(get_comments(url+str(i)))

output = {'content':[], 'score':[], 'ID':[], 'date':[], 'like':[], 'dislike':[]}

for c in total_comments:
    for i, k in enumerate(output.keys()):
        output[k].append(c[i])

df = pd.DataFrame(output)
df.to_csv('output.txt',sep='\t', encoding='euc-kr')