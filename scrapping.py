import requests
from bs4 import BeautifulSoup
from time import sleep

def set_cookies(cookies):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
    }
    session = requests.Session()
    session.headers.update(headers)
    for cookie in cookies:
        c = {cookie['name']: cookie['value']}
        session.cookies.update(c)
    return session

def get_article_ids(period, session):
    article_ids = []
    page_cnt = 1
    while True:
        sellings = session.get(f"https://cafe.naver.com/ArticleSearchList.nhn?search.clubid=20486145&search.menuid=214&search.media=0&search.searchdate={period}{period}&userDisplay=50&search.sortBy=date&search.searchBy=0&search.option=0&search.query=%C6%C7%B8%C5%26&search.viewtype=title&search.page={page_cnt}")
        sellings_parsed = BeautifulSoup(sellings.text, "html.parser")
        nodata = sellings_parsed.find('div',{'class': 'nodata'})
        if nodata:
            break
        table = sellings_parsed.find('div', {"class":"article-board result-board m-tcol-c"})
        trs = table.find_all("tr")
        for tr in trs:
            article_number = tr.find('div',{'class':'inner_number'})
            if article_number:
                article_ids.append(article_number.text)
        page_cnt = page_cnt + 1
    return article_ids

def get_pdp_soup(driver, article_id):
    driver.get(f"https://cafe.naver.com/chocammall?iframe_url_utf8=%2FArticleRead.nhn%253Fclubid%3D20486145%2526page%3D1%2526menuid%3D214%2526boardtype%3DL%2526articleid%3D{article_id}%2526referrerAllArticles%3Dfalse")
    sleep(0.1)
    driver.switch_to.frame('cafe_main')
    while True:
        pdp_soup = BeautifulSoup(driver.page_source, 'html.parser')
        section = pdp_soup.find('div', {'class': 'section'})
        if section:
            break
        sleep(0.1)

    return pdp_soup

def convert_soup_to_dict(pdp_soup):
    pdp_dict = {}
    pdp_soup.find('div', {'class': 'section'}).find('div',{'class': 'LayerArticle'}).decompose()
    title = pdp_soup.find('h3')
    if title:
        pdp_dict['title'] = title.text.strip()
    cost = pdp_soup.find('strong', {'class':'cost'})
    if cost:
        pdp_dict['cost'] = cost.text.strip()
    detail_list = pdp_soup.find('div', {'class': 'section'}).find_all('dl', {'class':'detail_list'})
    details = []
    for detail_item in detail_list:
        detail_title = detail_item.find('dt')
        if detail_title:
            detail_title = detail_title.text.strip()
        detail_content = detail_item.find('dd')
        if detail_content:
            detail_content = detail_content.text.strip().replace('  ', '').replace('\n', '')
        details.append({f'{detail_title}': f'{detail_content}'})
    pdp_dict['details'] = details
    nickname = pdp_soup.find('div', {'class':'nick_box'})
    if nickname:
        pdp_dict['nickname'] = nickname.text.strip()
    status = pdp_soup.find('p', {'class': 'ProductName'}).find('em')
    if status:
        pdp_dict['status'] = status.text.strip()
    date = pdp_soup.find('span', {'class':'date'})
    if date:
        pdp_dict['date'] = date.text.strip()
    views = pdp_soup.find('span', {'class':'count'})
    if views:
        pdp_dict['views'] = views.text.replace('조회', '').strip()
    main = pdp_soup.find('div', {'class':'se-main-container'})
    if main:
        pdp_dict['main'] = main.text.strip().replace('\n', '').replace('\u200b', '').replace('"', ' ')
    else:
        pdp_dict['main'] = "body 크롤링 실패"
    pdp_dict['comments_cnt'] = pdp_soup.find('strong', {'class':'num'}).text.strip()
    comments = pdp_soup.find('ul', {'class':'comment_list'})
    if comments:
        pdp_dict['comments'] = comments.text.strip().replace('  ', '').replace('\n', '').replace('답글쓰기', '').replace('"', ' ')
    else:
        pdp_dict['comments'] = ''
    likes = pdp_soup.find('div',{'class':'like_article'}).find('em', {'class': "u_cnt _count"})
    if likes:
        pdp_dict['likes'] = likes.text
    return pdp_dict

def get_pdp_dicts(driver, article_ids):
    pdp_dicts = []
    for article_id in article_ids:
        pdp_soup = get_pdp_soup(driver, article_id)
        pdp_dict = convert_soup_to_dict(pdp_soup)
        pdp_dicts.append(pdp_dict)
    return pdp_dicts