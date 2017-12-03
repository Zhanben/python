#--coding--:utf8--
from utils import *
from concurrent import futures
from models import DbManager, App360


def get_app_detail(soft_id):
    db_item = db.getAppWithSoftId(soft_id)
    if not db_item:
        url = "http://zhushou.360.cn/detail/index/soft_id/" + str(soft_id)
        app_html = do_request(url)
        app_item = extract_details(app_html, soft_id)
        db.saveAppItem(app_object=app_item)


def get_onePage_SoftId(url):
    res_html = do_request(url)
    soft_ids = r_url.findall(res_html)
    if soft_ids:
        return soft_ids
    else:
        return []

if __name__=="__main__":
    # 初始化数据库
    DB_CONNECT_STRING = 'mysql+pymysql://root:hillstone@localhost:3306/app?charset=utf8'
    db = DbManager(Dbstring=DB_CONNECT_STRING)
    db.init_db()
    for url in start_urls:
        for i in range(50):
            one_url = "http://zhushou.360.cn"+url+"?page=%s"%str(i)
            #ids = get_onePage_SoftId(url)
            executor = futures.ThreadPoolExecutor(max_workers=20)
            results = executor.map(get_app_detail, get_onePage_SoftId(one_url))
