import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# 与えられたURLから会社情報を取得する関数を定義します
def get_company_info(url):
    # URLにアクセスしてHTMLを取得します
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # ulタグの中から子ページのURLを取得します
    ul_tag = soup.find('ul', class_='rnn-group rnn-group--xm rnn-jobOfferList')
    if ul_tag:
        for li_tag in ul_tag.find_all('li'):
            a_tag = li_tag.find('a')
            if a_tag:
                # 子ページのURLを絶対URLに変換します
                link = urljoin('https://next.rikunabi.com', a_tag['href'])
                # 子ページの会社情報を取得します
                get_company_info_details(link)

# 会社情報を取得して詳細を出力する関数を定義します
def get_company_info_details(url):
    # URLにアクセスしてHTMLを取得します
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # 会社情報の取得
    company_div = soup.find('div', class_='rn3-companyOfferCompany')
    if company_div:
        # company_div内のすべてのh3タグとpタグを取得して出力します
        for tag in company_div.find_all(['h3', 'p']):
            print(tag.text.strip())
        print('-------------------')
    else:
        # 'rn3-companyOfferCompany'がない場合は、'rn3-companyOfferTabMenu__navItem'からURLを取得
        li_tags = soup.find_all('li', class_='rn3-companyOfferTabMenu__navItem')
        for li_tag in li_tags:
            span_tag = li_tag.find('span')
            if span_tag and span_tag.text.strip() == '求人情報':
                a_tag = li_tag.find('a')
                if a_tag:
                    link = urljoin('https://next.rikunabi.com', a_tag['href'])
                    get_company_info_details(link)


# 次のページのURLを取得する関数を定義します
def get_next_page_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    next_page_tag = soup.find('li', class_='rnn-pagination__next')
    if next_page_tag:
        next_page_link = urljoin('https://next.rikunabi.com', next_page_tag.find('a')['href'])
        return next_page_link
    else:
        return None

# 初期URLを指定します
initial_url = 'https://next.rikunabi.com/lst'
current_url = initial_url
page_count = 1

# メインの処理ループです
while current_url:
    # 会社情報を取得して出力します
    print(f"Page {page_count}")
    get_company_info(current_url)

    # 次のページのURLを取得します
    next_page_url = get_next_page_url(current_url)
    if next_page_url:
        current_url = next_page_url
        page_count += 1
    if next_page_url is None:
        print("終了")
        break
