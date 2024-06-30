import json
import sys
import time
import urllib.parse

import requests

# --------请提供移通智慧门户的密码，不是教务系统的密码，智慧门户地址：http://ehall.cqyti.com/--------
# --------账号--------
USERNAME = ""
# --------密码--------
PASSWORD = ""

from ytzhmh import ZhiHui
from bs4 import BeautifulSoup


class Ytpj:

    def __init__(self, session):
        self.session: requests.Session = session
        self.gnmkdm = {
            "pj": "N401605"
        }

    def get_xspj_cxXspjIndex(self):
        submit = {
            "_search": False,
            "nd": int(time.time() * 1000),
            "queryModel.showCount": 100,
            "queryModel.currentPage": 1,
            "queryModel.sortName": "kcmc,jzgmc",
            "queryModel.sortOrder": "asc",
            "time": 1

        }
        res = self.session.post("http://192.168.200.87/jwglxt/xspjgl/xspj_cxXspjIndex.html?doType=query&gnmkdm=N401605",
                                data=submit)
        res_json = res.json()

        items = res_json['items']
        return items

    def get_xspj_cxXspjDisplay(self, jxb_id, kch_id, xsdm, jgh_id, tjzt, pjmbmcb_id, sfcjlrjs):
        submit = {
            "jxb_id": jxb_id,
            "kch_id": kch_id,
            "xsdm": xsdm,
            "jgh_id": jgh_id,
            "tjzt": tjzt,
            "pjmbmcb_id": pjmbmcb_id,
            "sfcjlrjs": sfcjlrjs
        }
        res = self.session.post("http://192.168.200.87/jwglxt/xspjgl/xspj_cxXspjDisplay.html?gnmkdm=N401605",
                                data=submit)
        submit2 = {
            "ztpjbl": 100,
            "jszdpjbl": 0,
            "xykzpjbl": 0,
            "jxb_id": jxb_id,
            "kch_id": kch_id,
            "jgh_id": "",
            "xsdm": xsdm,
            # "modelList": [],
            "tjzt": tjzt
        }
        soup = BeautifulSoup(res.content.decode(), 'html.parser')
        jghid1 = soup.find("div", class_="xspj-body").attrs['data-jgh_id']
        submit2['jgh_id'] = jghid1
        # title = str(soup.find("div", class_="col-sm-8").get_text()).strip()
        # print(soup.find("div", class_="col-sm-4"))
        # jsxm = str(soup.find("span", attrs={"id": "jsxm"}).get_text()).strip()
        # print(title)
        # print("教师：{}".format(jsxm))

        panelPjdx = soup.find_all("div", class_="panel-pjdx")
        # 几个评教内容
        for i in range(len(panelPjdx)):
            panelBody = panelPjdx[i].find("div", class_="panel-body")
            xspjList = panelBody.find_all("table", class_="table-xspj")

            pjmbmcb_id = panelPjdx[i].attrs['data-pjmbmcb_id']
            data_pjdxdm = panelPjdx[i].attrs['data-pjdxdm']
            data_fxzgf = panelPjdx[i].attrs['data-fxzgf']
            data_xspfb_id = panelPjdx[i].attrs['data-xspfb_id']
            # submit2['modelList'].append({
            #     "pjmbmcb_id": pjmbmcb_id,
            #     "pjdxdm": data_pjdxdm,
            #     "fxzgf": data_fxzgf,
            #     "py": data_pjdxdm,
            #     "xspfb_id": data_xspfb_id,
            #     "xspjList": []
            # })
            submit2[f'modelList[{i}].pjmbmcb_id'] = pjmbmcb_id
            submit2[f'modelList[{i}].pjdxdm'] = data_pjdxdm
            submit2[f'modelList[{i}].fxzgf'] = data_fxzgf
            submit2[f'modelList[{i}].py'] = ""
            submit2[f'modelList[{i}].xspfb_id'] = data_xspfb_id
            # 按照xspjList循环
            for j in range(len(xspjList)):
                pjzbxm_id = xspjList[j].attrs['data-pjzbxm_id']
                # submit2['modelList'][i]['xspjList'].append({
                #     "pjzbxm_id": pjzbxm_id,
                #     "childXspjList": []
                # })
                submit2[f'modelList[{i}].xspjList[{j}].pjzbxm_id'] = pjzbxm_id
                # 按照childXspjList循环
                childXspjList = xspjList[j].find_all("tr", class_="tr-xspj")
                for k in range(len(childXspjList)):
                    pfdjdmxmb_id_input = childXspjList[k].find("div", class_="input-xspj-1").find("input")  # 评分标签
                    # if k == len(childXspjList) - 1:
                    #     pfdjdmxmb_id_input = childXspjList[k].find("div", class_="input-xspj-2").find("input")  # 评分标签
                    pfdjdmxmb_id = pfdjdmxmb_id_input.attrs['data-pfdjdmxmb_id']
                    pjzbxm_id = childXspjList[k].attrs['data-pjzbxm_id']
                    pfdjdmb_id = childXspjList[k].attrs['data-pfdjdmb_id']
                    zsmbmcb_id = childXspjList[k].attrs['data-zsmbmcb_id']

                    # submit2['modelList'][i]['xspjList'][j]['childXspjList'].append({
                    #     "pfdjdmxmb_id": pfdjdmxmb_id,
                    #     "pjzbxm_id": pjzbxm_id,
                    #     "pfdjdmb_id": pfdjdmb_id,
                    #     "zsmbmcb_id": zsmbmcb_id,
                    # })
                    submit2[f'modelList[{i}].xspjList[{j}].childXspjList[{k}].pfdjdmxmb_id'] = pfdjdmxmb_id
                    submit2[f'modelList[{i}].xspjList[{j}].childXspjList[{k}].pjzbxm_id'] = pjzbxm_id
                    submit2[f'modelList[{i}].xspjList[{j}].childXspjList[{k}].pfdjdmb_id'] = pfdjdmb_id
                    submit2[f'modelList[{i}].xspjList[{j}].childXspjList[{k}].zsmbmcb_id'] = zsmbmcb_id
                    submit2[f'modelList[{i}].xspjList[{j}].childXspjList[{k}].pfdjdmxmb_id'] = pfdjdmxmb_id
        submit3 = {
            "bfzpf": "100",
            "jxb_id": jxb_id,
            "jgh_id": jghid1
        }
        # 不用提交分数 保存自动获取分数
        # res = self.session.post("http://192.168.200.87/jwglxt/xspjgl/xspj_cxSftf.html?gnmkdm=N401605", data=submit3)
        # print(json.dumps(submit2))
        res = self.session.post("http://192.168.200.87/jwglxt/xspjgl/xspj_bcXspj.html?gnmkdm=N401605", data=submit2)
        print(res.content.decode())
        res = self.session.post("http://192.168.200.87/jwglxt/xspjgl/xspj_tjXspj.html?gnmkdm=N401605", data=submit2)
        print(res.content.decode())

    def cz(self, jxb_id, kch_id, xsdm, jgh_id, tjzt, pjmbmcb_id, sfcjlrjs):
        submit = {
            "jxb_id": jxb_id,
            "kch_id": kch_id,
            "xsdm": xsdm,
            "jgh_id": jgh_id,
            "tjzt": tjzt,
            "pjmbmcb_id": pjmbmcb_id,
            "sfcjlrjs": sfcjlrjs
        }
        res = self.session.post("http://192.168.200.87/jwglxt/xspjgl/xspj_cxXspjDisplay.html?gnmkdm=N401605",
                                data=submit)
        submit2 = {
            "ztpjbl": 100,
            "jszdpjbl": 0,
            "xykzpjbl": 0,
            "jxb_id": jxb_id,
            "kch_id": kch_id,
            "jgh_id": "",
            "xsdm": xsdm,
            # "modelList": [],
            "tjzt": tjzt
        }
        soup = BeautifulSoup(res.content.decode(), 'html.parser')
        jghid1 = soup.find("div", class_="xspj-body").attrs['data-jgh_id']
        submit2['jgh_id'] = jghid1
        panelPjdx = soup.find_all("div", class_="panel-pjdx")
        # 几个评教内容
        for i in range(len(panelPjdx)):
            panelBody = panelPjdx[i].find("div", class_="panel-body")
            xspjList = panelBody.find_all("table", class_="table-xspj")

            pjmbmcb_id = panelPjdx[i].attrs['data-pjmbmcb_id']
            data_pjdxdm = panelPjdx[i].attrs['data-pjdxdm']
            data_fxzgf = panelPjdx[i].attrs['data-fxzgf']
            data_xspfb_id = panelPjdx[i].attrs['data-xspfb_id']

            submit2[f'modelList[{i}].pjmbmcb_id'] = pjmbmcb_id
            submit2[f'modelList[{i}].pjdxdm'] = data_pjdxdm
            submit2[f'modelList[{i}].fxzgf'] = data_fxzgf
            submit2[f'modelList[{i}].py'] = ""
            submit2[f'modelList[{i}].xspfb_id'] = data_xspfb_id
            # 按照xspjList循环
            for j in range(len(xspjList)):
                pjzbxm_id = xspjList[j].attrs['data-pjzbxm_id']
                submit2[f'modelList[{i}].xspjList[{j}].pjzbxm_id'] = pjzbxm_id
                # 按照childXspjList循环
                childXspjList = xspjList[j].find_all("tr", class_="tr-xspj")
                for k in range(len(childXspjList)):
                    pfdjdmxmb_id = childXspjList[k].attrs['data-pfdjdmb_id']
                    pjzbxm_id = childXspjList[k].attrs['data-pjzbxm_id']
                    pfdjdmb_id = childXspjList[k].attrs['data-pfdjdmb_id']
                    zsmbmcb_id = childXspjList[k].attrs['data-zsmbmcb_id']

                    submit2[f'modelList[{i}].xspjList[{j}].childXspjList[{k}].pfdjdmxmb_id'] = pfdjdmxmb_id
                    submit2[f'modelList[{i}].xspjList[{j}].childXspjList[{k}].pjzbxm_id'] = pjzbxm_id
                    submit2[f'modelList[{i}].xspjList[{j}].childXspjList[{k}].pfdjdmb_id'] = pfdjdmb_id
                    submit2[f'modelList[{i}].xspjList[{j}].childXspjList[{k}].zsmbmcb_id'] = zsmbmcb_id
                    submit2[f'modelList[{i}].xspjList[{j}].childXspjList[{k}].pfdjdmxmb_id'] = pfdjdmxmb_id
        res = self.session.post("http://192.168.200.87/jwglxt/xspjgl/xspj_bcXspj.html?gnmkdm=N401605", data=submit2)
        print(res.content.decode())

if __name__ == "__main__":
    Z = ZhiHui(USERNAME, PASSWORD)
    flag, cookie = Z.login()
    if not flag:
        print("登录失败", cookie)
        sys.exit(1)
    flag, cookie = Z.get_jiao_wu()
    if not flag:
        print("登录失败", cookie)
        sys.exit(1)
    print("登录成功", Z.username)
    Y = Ytpj(Z.session)
    # 也可以使用教务系统cookie
    # session = requests.session()
    # session.cookies.set("JSESSIONID", "D034E1FC99C5BD8A94615B3429966103")
    # session.cookies.set("route", "318b5fd6fda07444c5707644aa54317d")
    # Y = Ytpj(session)

    # 结束
    a = Y.get_xspj_cxXspjIndex()
    for i, v in enumerate(a):
        title = v['kcmc']
        jsxm = v['jzgmc']
        print("当前进度：{}/{}".format(i + 1, len(a)))
        print("课程：{}".format(title))
        print("教师：{}".format(jsxm))
        if v['tjzt'] == "0":
            pjmbmcb_id = v['pjmbmcb_id']
        else:
            pjmbmcb_id = ""
        Y.get_xspj_cxXspjDisplay(v['jxb_id'], v['kch_id'], v['xsdm'], v['jgh_id'], v['tjzt'],
                                 pjmbmcb_id, v['sfcjlrjs'])
        # 需要重置评价分数 请注释上条语句 取消注释下条语句
        # Y.cz(v['jxb_id'], v['kch_id'], v['xsdm'], v['jgh_id'], v['tjzt'],
        #                          pjmbmcb_id, v['sfcjlrjs'])
        print()
    Z.logout()
