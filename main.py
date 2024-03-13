import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def get_company_info(url):
    # URLにアクセスしてHTMLを取得
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # ulタグの中から子ページのURLを取得
    ul_tag = soup.find('ul', class_='rnn-group rnn-group--xm rnn-jobOfferList')
    if ul_tag:
        for li_tag in ul_tag.find_all('li'):
            a_tag = li_tag.find('a')
            if a_tag:
                link = urljoin('https://next.rikunabi.com', a_tag['href'])
                # 子ページの会社情報を取得
                get_company_info_details(link)

def get_company_info_details(url):
    # URLにアクセスしてHTMLを取得
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # 会社情報の取得
    company_div = soup.find('div', class_='rn3-companyOfferCompany')
    if company_div:
        company_info_divs = company_div.find_all('div', class_='rn3-companyOfferCompany__info')
        h3_indices = {'社名': -1, '代表者': -1, '企業代表番号': -1}

        for index, info_div in enumerate(company_info_divs):
            h3_tags = info_div.find_all('h3')
            for h3_tag in h3_tags:
                h3_text = h3_tag.text.strip()
                if h3_text in h3_indices:
                    h3_indices[h3_text] = index

        p_tags = company_div.find_all('p')
        if h3_indices['社名'] != -1:
            print(f"社名: {p_tags[h3_indices['社名']].text.strip()}")
        if h3_indices['代表者'] != -1:
            print(f"代表者: {p_tags[h3_indices['代表者']].text.strip()}")
        if h3_indices['企業代表番号'] != -1:
            print(f"企業代表番号: {p_tags[h3_indices['企業代表番号']].text.strip()}")
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

# 次のページのURLを取得する関数
def get_next_page_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    next_page_tag = soup.find('li', class_='rnn-pagination__next')
    if next_page_tag:
        next_page_link = urljoin('https://next.rikunabi.com', next_page_tag.find('a')['href'])
        return next_page_link
    else:
        return None

# 初期URLを指定
initial_url = 'https://next.rikunabi.com/lst'
current_url = initial_url
page_count = 1

# メインの処理ループ
while current_url:
    # 会社情報を取得して出力
    print(f"Page {page_count}")
    get_company_info(current_url)

    # 次のページのURLを取得
    next_page_url = get_next_page_url(current_url)
    if next_page_url:
        current_url = next_page_url
        page_count += 1
    if next_page_url is None:
        print("終了")
        break
