import ddddocr
import time
import base64
import requests
import pprint


class Website:
    def __init__(self, stu_num, stu_pwd):
        self.stu_pwd = stu_pwd
        self.stu_num = stu_num
        self.cookie = ""
        self.ocr = ddddocr.DdddOcr()

    def get_cookie(self):
        url = "http://172.13.1.32/index.jsp"
        headers = {
            "User-Agent": "Apifox/1.0.0 (https://apifox.com)",
            "Accept": "*/*",
            "Host": "172.13.1.32",
            "Connection": "keep-alive",
        }

        res = requests.get(url, headers=headers)
        self.cookie = (res.headers["Set-Cookie"]).split(";")[0]

    def get_verify_code_pic(self):
        headers = {
            "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "Connection": "keep-alive",
            "Host": "172.13.1.32",
            "Referer": "http://172.13.1.32/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0",
        }

        url = f"http://172.13.1.32/yzm?d={int(time.time() * 1000)}"
        headers["Cookie"] = self.cookie
        res = requests.get(url, headers=headers)
        return res.content

    def get_verify_code(self):
        return self.ocr.classification(self.get_verify_code_pic())

    def login(self):
        headers = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "Connection": "keep-alive",
            "Content-Length": "62",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Host": "172.13.1.32",
            "Origin": "http://172.13.1.32",
            "Referer": "http://172.13.1.32/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0",
            "X-Requested-With": "XMLHttpRequest",
        }
        url = "http://172.13.1.32/login!doLogin.action"

        headers["Cookie"] = self.cookie
        data = {
            "account": self.stu_num,
            "pwd": base64.b64encode(self.stu_pwd.encode()),
            "verifycode": self.get_verify_code(),
        }
        res = requests.post(url, headers=headers, data=data)
        if len(res.text) > 5000:
            raise Exception(f"Login failed with status code: {res.status_code}")

    def get_course_schedule(self, term = "20251", week = "9"):
        headers = {
            "Host":"172.13.1.32",
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:144.0) Gecko/20100101 Firefox/144.0",
            "Accept":"application/json, text/javascript, */*; q=0.01",
            "Accept-Encoding":"gzip, deflate",
            "X-Requested-With":"XMLHttpRequest",
            "Sec-GPC":"1",
            "Connection":"keep-alive",
            "Referer":"http://172.13.1.32/xsgrkbcx!xskbList.action?xnxqdm={}&zc={}".format(term, week),
            "Pragma":"no-cache",
            "Cache-Control":"no-cache"
        }
        headers["Cookie"] = self.cookie
        url = "http://172.13.1.32/xsgrkbcx!getKbRq.action?xnxqdm={}&zc={}".format(term, week)
        try:
            res = requests.get(url, headers=headers)
            return res.json()
        except Exception as e:
            print(f"Error fetching course schedule: {e}")


    def get_course_grades(self, term = "20242"):
        headers = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "Connection": "keep-alive",
            "Content-Length": "62",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Host": "172.13.1.32",
            "Origin": "http://172.13.1.32",
            "Referer": "http://172.13.1.32/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0",
            "X-Requested-With": "XMLHttpRequest",
        }
        headers["Cookie"] = self.cookie
        url = "http://172.13.1.32/xskccjxx!getDataList.action"
        data = {
            "xnxqdm": term,
            "jhlxdm": "",
            "page": "1",
            "rows": "20",
            "sort": "xnxqdm",
            "order": "asc",
        }
        try:
            res = requests.post(url, headers=headers, data=data)
            return res.json()["rows"]
        except Exception as e:
            print(f"Error fetching course grades: {e}")

    def grab_class(self, kcrwdm, kcmc):
        url = "http://172.13.1.32/xsxklist!getAdd.action"
        headers = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "Connection": "keep-alive",
            "Content-Length": "62",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Host": "172.13.1.32",
            "Origin": "http://172.13.1.32",
            "Referer": "http://172.13.1.32/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0",
            "X-Requested-With": "XMLHttpRequest",
        }
        headers["Cookie"] = self.cookie
        data = {
            "kcrwdm": kcrwdm,
            "kcmc": kcmc,
        }
        res = requests.post(url, headers=headers, data=data)

        if len(res.text) > 5000:
            raise Exception("抢课失败")
        return res.content.decode()

    def logout(self):
        pass
        url = "http://172.13.1.32/login!logout.action"
        
        headers = {
            "Accept":"*/*",
            "Accept-Encoding":"gzip, deflate",
            "Accept-Language":"zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "Connection":"keep-alive",
            "Host":"172.13.1.32",
            "Referer":"http://172.13.1.32/login!welcome.action",
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0",
            "X-Requested-With":"XMLHttpRequest"
        }
        headers["Cookie"] = self.cookie

        requests.post(url, headers=headers)