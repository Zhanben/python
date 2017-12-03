import re
import requests
from models import App360

r_url = re.compile(u'<a sid="(.*?)" href=', re.DOTALL)

r_name = re.compile(u"<title>(.*?)_360手机助手</title>", re.DOTALL)
r_download_num = re.compile(u'<span class="s-3">下载：(.*?)次</span>', re.DOTALL)
r_score = re.compile(u'<span class="s-1 js-votepanel">(.*?)<em>分</em>', re.DOTALL)
r_author = re.compile(u"<strong>作者：</strong>(.*?)</td>", re.DOTALL)
r_version = re.compile(u"<strong>版本：</strong>(.*?)<!--", re.DOTALL)
r_update_time = re.compile(u"<strong>更新时间：</strong>(.*?)</td>", re.DOTALL)

start_urls = (
    "/list/index/cid/1/",
    "/list/index/cid/11/",
    "/list/index/cid/12/",
    "/list/index/cid/14/",
    "/list/index/cid/15/",
    "/list/index/cid/16/",
    "/list/index/cid/18/",
    "/list/index/cid/17/",
    "/list/index/cid/102228/",
    "/list/index/cid/102230/",
    "/list/index/cid/102231/",
    "/list/index/cid/102232/",
    "/list/index/cid/102139/",
    "/list/index/cid/102233/",
)


def do_request(url):
    try:
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.8",
            #"Connection": "keep-alive",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64)"
        }
        resp = requests.get(url, headers=headers)
        return resp.text
    except requests.exceptions.RequestException as e:
        return None


def extract_SoftIds(html):
    result = []
    soft_ids = r_url.findall(html)
    #print(soft_ids)
    url = ""
    host = "http://zhushou.360.cn/detail/index/soft_id/"
    for sid in soft_ids:
        url = host + sid
        result.append(url)
    return result


def extract_details(html, soft_id):
    app = App360()
    app.soft_id = int(soft_id)
    if html:
        m = r_name.search(html)
        if not m:
            app.name = ''
        else:
            app.name = m.group(m.lastindex).replace('&nbsp;', '').replace(';', ',').strip()
            #print(app.name)

        m = r_download_num.search(html)
        if not m:
            app.download_num = ''
        else:
            app.download_num = m.group(m.lastindex).replace('&nbsp;', '').replace(';', ',').strip()

        m = r_score.search(html)
        if not m:
            app.score = 0
        else:
            app.score = float(m.group(m.lastindex).replace('&nbsp;', '').replace(';', ',').strip())
            #print(app.score)
        m = r_author.search(html)
        if not m:
            app.author = ''
        else:
            app.author = m.group(m.lastindex).replace('&nbsp;', '').replace(';', ',').strip()
            #print(app.author)
        m = r_update_time.search(html)
        if not m:
            app.update_time = ''
        else:
            app.update_time = m.group(m.lastindex).replace('&nbsp;', '').replace(';', ',').strip()
            #print(app.update_time)
        m = r_version.search(html)
        if not m:
            app.version = ''
        else:
            app.version = m.group(m.lastindex).replace('&nbsp;', '').replace(';', ',').strip()
            #print(app.version)

    return app
