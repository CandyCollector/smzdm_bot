"""
什么值得买自动签到脚本
使用github actions 定时执行
@author : stark
"""
import requests,os
from sys import argv

import config
from utils.serverchan_push import push_to_wechat

class SMZDM_Bot(object):
    def __init__(self):
        self.session = requests.Session()
        # 添加 headers
        self.session.headers = config.DEFAULT_HEADERS

    def __json_check(self, msg):
        """
        对请求 盖乐世社区 返回的数据进行进行检查
        1.判断是否 json 形式
        """
        try:
            result = msg.json()
            print(result)
            return True
        except Exception as e:
            print(f'Error : {e}')            
            return False

    def load_cookie_str(self, cookies):
        """
        起一个什么值得买的，带cookie的session
        cookie 为浏览器复制来的字符串
        :param cookie: 登录过的社区网站 cookie
        """
        self.session.headers['Cookie'] = cookies    

    def checkin(self):
        """
        签到函数
        """
        url = 'https://zhiyou.smzdm.com/user/checkin/jsonp_checkin'
        msg = self.session.get(url)
        if self.__json_check(msg):
            return msg.json()
        return msg.content




if __name__ == '__main__':
    sb = SMZDM_Bot()
    # sb.load_cookie_str(config.TEST_COOKIE)
    cookies = os.environ["__ckguid=CaQ3r5p5lOwcEpOt8Nxnhr5; __jsluid_s=d0a6e15e031b7f31765f7b7095bb65f2; sajssdk_2015_cross_new_user=1; device_id=30858716851632173183818944e5e5ae8b3d6acc2f2d0d9fd659258b7f; _ga=GA1.1.1345917478.1632173185; homepage_sug=a; r_sort_type=score; _zdmA.vid=*; zdm_qd={"referrer":"https://github.com/CandyCollector/smzdm_bot"}; footer_floating_layer=0; ad_date=21; ad_json_feed={}; Hm_lvt_9b7ac3d38f30fe89ff0b8a0546904e58=1632173802; sensorsdata2015jssdkcross={"distinct_id":"17c051a526f506-06ba652118d96f-57341f44-1327104-17c051a5270635","first_id":"","props":{"$latest_traffic_source_type":"引荐流量","$latest_search_keyword":"未取到值","$latest_referrer":"https://github.com/CandyCollector/smzdm_bot"},"$device_id":"17c051a526f506-06ba652118d96f-57341f44-1327104-17c051a5270635"}; sess=AT-z6eGsBZvkuNOzHbYMK09GW/FnKOA6Gsl61fB3qyNfGO84ZHRNlszrbFLZK5VcSLL5GK5t4CaI+bV5hEY5HFfTyx+1JTIKzMGIQQgOE2rhCj5t6troUuSYHyd; user=user:2414843384|2414843384; smzdm_id=2414843384; _ga_09SRZM2FDD=GS1.1.1632173184.1.1.1632173906.0; _zdmA.uid=ZDMA.iO4M7UXOn.1632173907.2419200; userId=user:2414843384|2414843384; Hm_lpvt_9b7ac3d38f30fe89ff0b8a0546904e58=1632173907; bannerCounter=[{"number":1,"surplus":1},{"number":0,"surplus":1},{"number":1,"surplus":1},{"number":0,"surplus":1},{"number":1,"surplus":1},{"number":0,"surplus":1}]; amvid=fb715e738c79c4a069c0812578eefdbe; _zdmA.time=1632173936388.0.https://www.smzdm.com/"]
    sb.load_cookie_str(cookies)
    res = sb.checkin()
    print(res)
    SERVERCHAN_SECRETKEY = os.environ["SERVERCHAN_SECRETKEY"]
    print('sc_key: ', SERVERCHAN_SECRETKEY)
    if isinstance(SERVERCHAN_SECRETKEY,str) and len(SERVERCHAN_SECRETKEY)>0:
        print('检测到 SCKEY， 准备推送')
        push_to_wechat(text = '什么值得买每日签到',
                        desp = str(res),
                        secretKey = SERVERCHAN_SECRETKEY)
    print('代码完毕')
