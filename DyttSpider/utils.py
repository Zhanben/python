import re
import requests
from models import Film

r_url = re.compile(u'/(.*?)"\.html', re.DOTALL)
re_film_id = re.compile(u'<img src="(.*?)" alt', re.DOTALL)
re_image_url = re.compile(u'<img src="(.*?)" alt', re.DOTALL)

r_name_cn = re.compile(u"◎译　　名(.*?)</p>", re.DOTALL)
r_name = re.compile(u"◎片　　名(.*?)</p>", re.DOTALL)
r_year = re.compile(u"◎年　　代(.*?)</p>", re.DOTALL)
r_country = re.compile(u"(产　　地|国　　家)(.*?)</p>", re.DOTALL)
r_category = re.compile(u"◎类　　别(.*?)</p>", re.DOTALL)
r_language = re.compile(u"◎语　　言(.*?)</p>", re.DOTALL)
r_subtitle = re.compile(u"◎字　　幕(.*?)</p>", re.DOTALL)
r_release_date = re.compile(u"◎上映日期(.*?)</p>", re.DOTALL)
r_score = re.compile(u"◎(IMDB评分|豆瓣评分)(.*?)</p>", re.DOTALL | re.IGNORECASE)
r_file_size = re.compile(u"◎文件大小(.*?)</p>", re.DOTALL)
r_movie_duration = re.compile(u"◎片　　长(.*?)</p>", re.DOTALL)
r_director = re.compile(u"◎导　　演(.*?)</p>", re.DOTALL)

r_download_url = re.compile('<td.*?bgcolor="#fdfddf">.*?<a.*?>(.*?)</a>', re.DOTALL)

r_list = (r_name_cn,
          r_name,
          r_year,
          r_country,
          r_category,
          r_language,
          r_subtitle,
          r_release_date,
          r_score,
          r_file_size,
          r_movie_duration,
          r_director)

key_list = ("name_cn",
            "name",
            "year",
            "country",
            "category",
            "language",
            "subtitle",
            "release_date",
            "score",
            "file_size",
            "movie_duration",
            "director")


def do_request(url):
    try:
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.8",
            "Host": "www.dy2018.com",
            "Connection": "keep-alive",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64)"
        }
        resp = requests.get(url, headers=headers, timeout=10)
        resp.encoding = 'gb18030'
        return resp.text
    except requests.exceptions.RequestException as e:
        return ''


def extract_urls(html):
    result = ''
    segments = r_url.findall(html)
    host = "http://www.ygdy8.net"
    for seg in segments:
        result = result + host + seg + '\n'
    return result


def download_image(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36"}
    response = requests.get(url, headers=headers, stream=True)
    image_name = "image/" + url.split('/')[-1]
    if response.status_code == 200:
        with open(image_name, 'wb') as fd:
            for chunk in response.iter_content(128):
                fd.write(chunk)


def film_dict2model(film_moldel, film_dict):
    film_moldel.name_cn = film_dict["name_cn"]
    film_moldel.name = film_dict["name"]
    film_moldel.year = film_dict["year"]
    film_moldel.country = film_dict["country"]
    film_moldel.category = film_dict["category"]
    film_moldel.language = film_dict["language"]
    film_moldel.subtitle = film_dict["subtitle"]
    film_moldel.release_date = film_dict["release_date"]
    film_moldel.score = film_dict["score"]
    film_moldel.file_size = film_dict["file_size"]
    film_moldel.movie_duration = film_dict["movie_duration"]
    film_moldel.director = film_dict["director"]


def extract_details(html, url):
    film = Film()
    film.uid = int(url.split('/')[-1].split('.')[0])
    if html:
        m = re_image_url.search(html)
        if m:
            image_url = m.group(m.lastindex).replace('&nbsp;', '').replace(';', ',').strip()
            image_name = image_url.split('/')[-1]
            download_image(image_url)
            film.image_name = image_name

        m = r_name_cn.search(html)
        if not m:
            film.name_cn = ''
        else:
            film.name_cn = m.group(m.lastindex).replace('&nbsp;', '').replace(';', ',').strip()

        m = r_name.search(html)
        if not m:
            film.name = ''
        else:
            film.name = m.group(m.lastindex).replace('&nbsp;', '').replace(';', ',').strip()

        m = r_year.search(html)
        if not m:
            film.year = ''
        else:
            film.year = m.group(m.lastindex).replace('&nbsp;', '').replace(';', ',').strip()

        m = r_country.search(html)
        if not m:
            film.country = ''
        else:
            film.country = m.group(m.lastindex).replace('&nbsp;', '').replace(';', ',').strip()

        m = r_category.search(html)
        if not m:
            film.category = ''
        else:
            film.category = m.group(m.lastindex).replace('&nbsp;', '').replace(';', ',').strip()

        m = r_language.search(html)
        if not m:
            film.language = ''
        else:
            film.language = m.group(m.lastindex).replace('&nbsp;', '').replace(';', ',').strip()

        m = r_subtitle.search(html)
        if not m:
            film.subtitle = ''
        else:
            film.subtitle = m.group(m.lastindex).replace('&nbsp;', '').replace(';', ',').strip()

        m = r_release_date.search(html)
        if not m:
            film.release_date = ''
        else:
            film.release_date = m.group(m.lastindex).replace('&nbsp;', '').replace(';', ',').strip()

        m = r_score.search(html)
        if not m:
            film.score = ''
        else:
            film.score = m.group(m.lastindex).replace('&nbsp;', '').replace(';', ',').strip()

        m = r_file_size.search(html)
        if not m:
            film.file_size = ''
        else:
            film.file_size = m.group(m.lastindex).replace('&nbsp;', '').replace(';', ',').strip()

        m = r_movie_duration.search(html)
        if not m:
            film.movie_duration = ''
        else:
            film.movie_duration = m.group(m.lastindex).replace('&nbsp;', '').replace(';', ',').strip()

        m = r_director.search(html)
        if not m:
            film.director = ''
        else:
            film.director = m.group(m.lastindex).replace('&nbsp;', '').replace(';', ',').strip()

        urls = r_download_url.findall(html)
        field = ''
        if urls:
            for url in urls:
                field = field + url.strip()
                if urls.index(url) != len(urls) - 1:
                    field = field + ','
        # print field
        film.download_url = field
    return film


def extract_details1(html, url):
    tmp = {}
    film = Film()
    film.uid = int(url.split('/')[-1].split('.')[0])
    if html:
        m = re_image_url.search(html)
        if m:
            image_url = m.group(m.lastindex).replace('&nbsp;', '').replace(';', ',').strip()
            image_name = image_url.split('/')[-1]
            download_image(image_url)
            film.image_name = image_name
        for regex, _key in zip(r_list, key_list):
            tmp[_key] = None
            m = regex.search(html)
            if not m:
                film._key = ''
            else:
                t = m.group(m.lastindex).replace('&nbsp;', '').replace(';', ',').strip()
                tmp[_key] = t
        film_dict2model(film, tmp)

        urls = r_download_url.findall(html)
        field = ''
        if urls:
            for url in urls:
                field = field + url.strip()
                if urls.index(url) != len(urls) - 1:
                    field = field + ','
        film.download_url = field
    return film
