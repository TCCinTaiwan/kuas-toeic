# -*- coding: utf-8 -*-
import os
import sys
from flask import Flask, render_template, request
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoAlertPresentException, NoSuchElementException, WebDriverException, UnexpectedAlertPresentException
import re
import json
app = Flask(__name__, static_url_path = "", static_folder = "static") #宣告一個Flask
app.debug = True #開啟Debug模式
error = [
    "未知錯誤!!",
    "無法連線到'Easy test線上學習測驗平台'!!",
    "查無此帳號!!",
    "密碼錯誤!!",
    "找不到選修科目!!",
    "找不到測驗!!!"
]
warning = [
    "帳密相同",
    "上次考試尚未完成"
    "找不到考古題"
]
browser = webdriver.Chrome() #log參數 service_args=["--verbose", "--log-path=/home/ubuntu/workspace/toeic.log"]
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        returnPage = answerToeic(str(request.form['user']), str(request.form['pwd']), str(request.form['test']), int(request.form['number']), int(request.form['score']), int(request.form['elective']), request.form.get('previous') == 'on')
        return returnPage
    else:
        return render_template('login.htm') #靜態登入頁面
def answerToeic(account = '', password = '', test = 'simulation', number = 1, score = 0, elective = 1, previous = True):
    def screenshot():
        browser.maximize_window()
        screenshotNum = 1
        while (os.path.isfile(os.path.join('static', account + '-' + str(screenshotNum) + '.png'))):
            screenshotNum += 1
        browser.save_screenshot(os.path.join('static', account + '-' + str(screenshotNum) + '.png'))
        browser.quit()
        return account + '-' + str(screenshotNum)
    def errorPage(errorCode = 0):
        # print(error[errorCode], file = sys.stderr)
        return render_template('error.htm', screenshot = screenshot(), error = error[errorCode])
    print("使用者帳號：", account, file = sys.stderr)
    print("使用者密碼：", password, file = sys.stderr)
    print("選擇測驗類型：", test, file = sys.stderr)
    print("飆幾大題：", score, file = sys.stderr)
    print('使用考古題：', previous, file = sys.stderr)
    try:
        print('先登出一次', file = sys.stderr)
        browser.get('http://140.127.113.187/logout.asp')
        browser.get('http://140.127.113.187/index.asp?m=false')
        print("登入'Easy test線上學習測驗平台'...", file = sys.stderr)
        browser.find_element_by_name('cust_id').send_keys(account) #帳號
        browser.find_element_by_name('cust_pass').send_keys(password + Keys.RETURN) #密碼
        # 查無此帳號、密碼錯誤、帳號密碼相同會跳提示
        try:
            alertText = browser.switch_to_alert().text
            browser.switch_to_alert().accept()
            if (alertText == "查無此帳號"):
                print("查無此帳號!!", file = sys.stderr)
                return errorPage(errorCode = 2)
            elif (re.match("密碼錯誤次數 : \d，當錯誤次數超過5次時，帳號會被鎖", alertText)):
                print("密碼錯誤", re.match("密碼錯誤次數 : (\d)，當錯誤次數超過5次時，帳號會被鎖", alertText).group(1), "!!", file = sys.stderr)
                return errorPage(errorCode = 3)
            elif (re.match("您的帳號與密碼相同，為提升安全性，建議修改。\n\n如需修改密碼請至系統管理進行變更。", alertText)):
                print("帳密相同!!", file = sys.stderr)
            else:
                print(alertText)
        except WebDriverException:
            pass
        print("登入成功...", file = sys.stderr)
        # 選修
        if (elective > 1):
            browser.get("http://140.127.113.187/Courses/new_toeic/")
            try:
                print("選擇選修科目!!!", file = sys.stderr)
                browser.find_element_by_xpath('//*[@id="choice"]/option[' + str(elective) + ']').click()
            except UnexpectedAlertPresentException:
                browser.switch_to_alert().accept()
                return errorPage(errorCode = 4)
        # 不繼續上次考試
        browser.get("http://140.127.113.187/Courses/new_toeic/" + test + ".asp")
        try:
            browser.switch_to_alert().dismiss()
            # 此試卷有中斷紀錄，接續中斷測驗請點” 確定”\n\n重新測驗一份新試卷請點” 取消”，將會清除之前的中斷測驗紀錄。
            print("放棄上次考試...", file = sys.stderr)
        except NoAlertPresentException:
            pass
        # 選擇要考的
        testName = ''
        toeicLink = browser.find_element_by_xpath('/html/body/table/tbody/tr/td[2]/table/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr[6]//a[' + str(number) +']') # tr[6]原本是tr[8]
        testName = toeicLink.text
        # 使用考古題，必須同名稱
        if (previous  and os.path.isfile("Q&A/" + testName + ".json")):

            print("載入考古題", file = sys.stderr)
            jsonFile = open("Q&A/" + testName + ".json", "r")
            q = json.loads(jsonFile.read())
        else:
            toeicLink.click()
            try:
                browser.switch_to_alert().dismiss()
                # 此試卷有中斷紀錄，接續中斷測驗請點” 確定”\n\n重新測驗一份新試卷請點” 取消”，將會清除之前的中斷測驗紀錄。
                print("放棄上次考試...", file = sys.stderr)
            except NoAlertPresentException:
                pass
            print("進入考試，先飆'" + testName + "'答案...", file = sys.stderr)
            try:
                browser.switch_to_window(browser.window_handles[1])
            except:
                return errorPage(errorCode = 0)
            for i in range(7):
                browser.execute_script("for(var index = 0; index < document.getElementsByTagName('input').length; index++){if (document.getElementsByTagName('input')[index].value == 'A') {document.getElementsByTagName('input')[index].click();} else if (document.getElementsByTagName('input')[index].type == 'image'){document.getElementsByTagName('input')[index].click();}}")
            print("抓答案...", file = sys.stderr)
            correct = {
                'simulation' : 'correct',
                'elective_simulation' : 'elective_correct',
                'make_subjust' : 'make_correct',
                'elective_make_subjust' : 'elective_make_correct',
            }
            browser.get("http://140.127.113.187/Courses/new_toeic/" + correct[test] + ".asp?Q_Type=1")
            browser.execute_script('q={};')
            for i in range(7):
                url = "http://140.127.113.187/Courses/new_toeic/" + correct[test] + str(i + 1) +".asp"
                print("載入" + url, file = sys.stderr)

                browser.execute_script('document.getElementsByTagName("frame")[1].src = "' + url + '";n=' + str(i) +';');
                browser.execute_script('targetDocument=document.getElementsByTagName("frame")[1].contentWindow.document;index_count=((n<1)?10:(n<4)?30:(n<5)?40:(n<6)?12:48);index_2_count=((n==1)?3:4);for(index=' + ('-1' if (test == 'elective_make_subjust' and (i < 2 or i == 4)) else '0') + ';index<index_count' + ('-1' if (test == 'elective_make_subjust' and (i < 2 or i == 4)) else '') + '?-1:0;index++){if(n==5){q_name=targetDocument.getElementsByName("q"+(index+1))[0].parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.innerHTML.match(/([A-Z].[^<]*)</)[1];q_ans=targetDocument.getElementsByName("q"+(index+1))[0].parentElement.parentElement.parentElement.getElementsByTagName("font")[1].parentElement.innerHTML.match(/ \\([A-D]{1}\\) ([a-zA-Z $\\d\'.\\-,]*)/)[1];q[q_name]=q_ans}else{if(n>3){q_name=targetDocument.getElementsByName("q"+(index+1))[0].parentElement.parentElement.parentElement.getElementsByTagName("font")[0].innerHTML;q_ans=targetDocument.getElementsByName("q"+(index+1))[0].parentElement.parentElement.parentElement.getElementsByTagName("font")[1].parentElement.innerHTML.match(/ \\([A-D]{1}\\) ([a-zA-Z $\\d\'.\\-,]*)/)[1];q[q_name]=q_ans}else{for(index_2=0;index_2<index_2_count;index_2++){q_name=targetDocument.getElementsByName("q"+(index+1))[0].parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.getElementsByTagName("audio")[0].src.match(/sound\/(T\d{2}-\d{2}-\d{3}(-\d{2}){0,1}).mp3/)[1];if(targetDocument.getElementsByName("q"+(index+1))[index_2].parentElement.getElementsByTagName("font")[0]!=null){q[q_name]=String.fromCharCode("A".charCodeAt(0)+index_2)}}}}};')
            q = browser.execute_script("return q;")
            browser.get("http://140.127.113.187/Courses/new_toeic/" + test + ".asp")
            toeicLink = browser.find_element_by_xpath('/html/body/table/tbody/tr/td[2]/table/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr[6]//a[' + str(number) +']')
            testName = toeicLink.text
            jsonFile = open("Q&A/" + testName + ".json", "w")
            jsonFile.write(json.dumps(q))
        jsonFile.close()
        toeicLink.click()
        try:
            browser.switch_to_alert().dismiss()
            # 此試卷有中斷紀錄，接續中斷測驗請點” 確定”\n\n重新測驗一份新試卷請點” 取消”，將會清除之前的中斷測驗紀錄。
            print("放棄上次考試...", file = sys.stderr)
        except NoAlertPresentException:
            pass
        print("進入考試'" + testName + "'...", file = sys.stderr)
        browser.switch_to_window(browser.window_handles[1])
        print("切換到考試頁面", file = sys.stderr)
        for i in range(7 - score):
            print("第%d大題，使用考古題。" % (i + 1), file = sys.stderr)
            # print("n=" + str(i) + ";q=" + str(q) + ";index_count=((n<1)?10:(n<4)?30:(n<5)?40:(n<6)?12:48);index_2_count=((n==1)?3:4);for(index=0;index<index_count;index++){if(n<4){q_name=document.getElementsByName('q'+(index+1))[0].parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.getElementsByTagName('a')[" + ('0' if (test == 'elective_make_subjust') else '((n==1)?1:0)') + "].onclick.toString().match(/play_sound\(\\\"(T\d{2}-\d{2}-\d{3}(-\d{2}){0,1}).mp3\\\"/)[1]}else{if(n==5){q_name=document.getElementsByName('q'+(index+1))[0].parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.innerHTML.match(/([A-Z].[^<]*)</)[1]}else{q_name=document.getElementsByName('q'+(index+1))[0].parentElement.parentElement.parentElement.getElementsByTagName('b')[0].innerHTML}}ans=q[q_name];for(index_2=0;index_2<index_2_count;index_2++){if(n<4){if(document.getElementsByName('q'+(index+1))[index_2].value==ans){document.getElementsByName('q'+(index+1))[index_2].click()}}else{if(document.getElementsByName('q'+(index+1))[index_2].parentElement.getElementsByTagName('label')[0].innerHTML.match(/\([A-D]{1}\) ([a-zA-Z $\\d'.\\-,]*)/)[1]==ans){document.getElementsByName('q'+(index+1))[index_2].click()}}}}for(var index=0;index<document.getElementsByTagName('input').length;index++){if(document.getElementsByTagName('input')[index].type=='image'){document.getElementsByTagName('input')[index].click()}};", file = sys.stderr)
            browser.execute_script("n=" + str(i) + ";q=" + str(q) + ";index_count=((n<1)?10:(n<4)?30:(n<5)?40:(n<6)?12:48);index_2_count=((n==1)?3:4);for(index=0;index<index_count;index++){if(n<4){q_name=document.getElementsByName('q'+(index+1))[0].parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.getElementsByTagName('a')[" + ('0' if (test == 'elective_make_subjust') else '((n==1)?1:0)') + "].onclick.toString().match(/play_sound\(\\\"(T\d{2}-\d{2}-\d{3}(-\d{2}){0,1}).mp3\\\"/)[1]}else{if(n==5){q_name=document.getElementsByName('q'+(index+1))[0].parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.innerHTML.match(/([A-Z].[^<]*)</)[1]}else{q_name=document.getElementsByName('q'+(index+1))[0].parentElement.parentElement.parentElement.getElementsByTagName('b')[0].innerHTML}}ans=q[q_name];for(index_2=0;index_2<index_2_count;index_2++){if(n<4){if(document.getElementsByName('q'+(index+1))[index_2].value==ans){document.getElementsByName('q'+(index+1))[index_2].click()}}else{if(document.getElementsByName('q'+(index+1))[index_2].parentElement.getElementsByTagName('label')[0].innerHTML.match(/\([A-D]{1}\) ([a-zA-Z $\\d'.\\-,]*)/)[1]==ans){document.getElementsByName('q'+(index+1))[index_2].click()}}}}for(var index=0;index<document.getElementsByTagName('input').length;index++){if(document.getElementsByTagName('input')[index].type=='image'){document.getElementsByTagName('input')[index].click()}};")
        for i in range(7 - score, 7): # 飆
            print("第%d大題，用猜的。" % (i + 1), file = sys.stderr)
            browser.execute_script("for(var index = 0; index < document.getElementsByTagName('input').length; index++){if (document.getElementsByTagName('input')[index].value == 'A') {document.getElementsByTagName('input')[index].click();} else if (document.getElementsByTagName('input')[index].type == 'image'){document.getElementsByTagName('input')[index].click();}}")
        print("答題成功!!", file = sys.stderr)
        return '<title>Toeic 自動填充題</title>答題成功!!<a href=""><input type="button" value="回選擇頁面" /></a><br/><img  src="' + screenshot() + '.png"/>'
    except:
        return errorPage(errorCode = 0)
if __name__ == '__main__':
    app.run(host = os.getenv('IP', '0.0.0.0'), port = int(os.getenv('PORT', 8080)))