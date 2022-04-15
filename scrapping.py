import requests
from bs4 import BeautifulSoup

def search_each_period(periods, cookies):
    print('web scrapping start')
    new_sellings = []
    id = 1
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
    }
    session = requests.Session()
    session.headers.update(headers)
    for cookie in cookies:
        c = {cookie['name']: cookie['value']}
        session.cookies.update(c)
    period_max = periods[len(periods) - 1]
    for period in periods:
        page = session.get(f"https://cafe.naver.com/ArticleSearchList.nhn?search.clubid=20486145&search.menuid=214&search.media=0&search.searchdate={period}{period}&search.defaultValue=1&userDisplay=50&search.onSale=1&search.option=3&search.sortBy=date&search.searchBy=0&search.query=%C6%C7%B8%C5%26&search.viewtype=title&search.page=1")
        page_parsed = BeautifulSoup(page.text, "html.parser")
        pagination = page_parsed.find('div', {"class":"prev-next"})
        page_max = int(pagination.select_one('a:last-child').text)
        page_cnt = 1
        while (page_cnt <= page_max):
            page = session.get(f"https://cafe.naver.com/ArticleSearchList.nhn?search.clubid=20486145&search.menuid=214&search.media=0&search.searchdate={period}{period}&search.defaultValue=1&userDisplay=50&search.onSale=1&search.option=3&search.sortBy=date&search.searchBy=0&search.query=%C6%C7%B8%C5%26&search.viewtype=title&search.page={page_cnt}")
            table = page_parsed.find('div', {"class":"article-board result-board m-tcol-c"})
            trs = table.find_all("tr")
            for tr in trs:
                title = ""
                status = ""
                comments = "0"
                date = ""
                views = ""
                likes = ""
                title_td = tr.find("td",{"class": "td_article"})
                if title_td:
                    title_div = title_td.find("div", {"class": "board-list"})
                    title = title_div.find("a",{"class": "article"}).text.strip().replace("\""," ").replace("\'", " ")
                    cmt = title_div.find("a",{"class": "cmt"})
                    if title_div.find("span",{"class": "list-i-selling"}):
                        status = "판매"
                    if title_div.find("span",{"class": "list-i-selling-safe"}):
                        status = "판매(안전)"
                    if title_div.find("span",{"class": "list-i-selling-reservation"}):
                        status = "예약중"
                    if title_div.find("span",{"class": "list-i-sellout"}):
                        status = "완료"
                    if cmt:
                        comments = cmt.text.strip().strip("[""]")
                    date_td = tr.find("td",{"class": "td_date"})
                    if date_td:
                        date = date_td.text.strip()
                    view_td = tr.find("td",{"class": "td_view"})
                    if view_td:
                        views = view_td.text.strip().replace(",","")
                    like_td = tr.find("td",{"class": "td_likes"})
                    if like_td:
                        likes = like_td.text.strip()
                    name_td = tr.find("td",{"class": "td_name"})
                    if name_td:
                        name = name_td.text.strip()
                    new_sellings.append({'id': id,'title': title, 'status': status, 'views': views, 'likes': likes, 'comments': comments, 'name': name, 'date': date})
                    id = id + 1
            page_cnt = page_cnt + 1
        print(f"{period}/{period_max} done")
    print('web scrapping done')
    return new_sellings