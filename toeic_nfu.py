from flask import Flask, render_template, request
from selenium import webdriver
import os
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoAlertPresentException,NoSuchElementException
import sys
app = Flask(__name__, static_url_path = "", static_folder = "static")
app.debug = True
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        print("使用者帳號： %s" % request.form['user'], file = sys.stderr)
        print("使用者密碼： %s" % request.form['pwd'], file = sys.stderr)
        print("選擇測驗類型： %s" % request.form['test'], file = sys.stderr)
        print("飆幾大題： %s" % request.form['score'], file = sys.stderr)
        returnString = answerToeic(request.form['user'], request.form['pwd'], request.form['test'], int(request.form['number']), int(request.form['score']), int(request.form['elective']))
        return returnString
    else:
        return render_template('login.html')
def answerToeic(account, password, test, number = 1, score = 0, elective = 1):
    browser = webdriver.Chrome()
    print("連線到'Easy test線上學習測驗平台'...", file = sys.stderr)
    browser.get('http://140.127.113.187/index.asp?m=false')
    assert "Easy test線上學習測驗平台" in browser.title
    print("登入'Easy test線上學習測驗平台'...", file = sys.stderr)
    browser.find_element_by_name('cust_id').send_keys(account)
    browser.find_element_by_name('cust_pass').send_keys(str(password) + Keys.RETURN)
    try:
        browser.switch_to_alert().accept()
        print("帳密相同", file = sys.stderr)
    except NoAlertPresentException:
        pass
    try:
        browser.find_element_by_name('cust_id')
        browser.maximize_window()
        screenshotNum = 1
        while (os.path.isfile('static/' + account + '-' + str(screenshotNum) + '.png')):
            screenshotNum += 1
        browser.save_screenshot('static/' + account + '-' + str(screenshotNum) + '.png')
        browser.quit()
        print("登入失敗!!!", file = sys.stderr)
        return "<title>Toeic 自動填充題</title>登入失敗<a href=''><input type='button' value='重試' /></a><br/><img  src='" + account + "-" + str(screenshotNum) + ".png'/>"
    except NoSuchElementException:
        browser.get("http://140.127.113.187/Courses/new_toeic/")
        print("選擇選修科目!!!", file = sys.stderr)
        try:
            browser.find_element_by_xpath('//*[@id="choice"]/option[' + str(elective) + ']').click()
        except NoSuchElementException:
            browser.maximize_window()
            screenshotNum = 1
            while (os.path.isfile('static/' + account + '-' + str(screenshotNum) + '.png')):
                screenshotNum += 1
            browser.save_screenshot('static/' + account + '-' + str(screenshotNum) + '.png')
            browser.quit()
            print("找不到選修科目!!!", file = sys.stderr)
            return "<title>Toeic 自動填充題</title>找不到選修科目<a href=''><input type='button' value='重試' /></a><br/><img  src='" + account + "-" + str(screenshotNum) + ".png'/>"
    browser.get("http://140.127.113.187/Courses/new_toeic/" + test + ".asp")
    try:
        browser.switch_to_alert().accept()
        print("繼續上次考試...", file = sys.stderr)
    except:
        pass
    try:
        toeicLink = browser.find_element_by_xpath('/html/body/table/tbody/tr/td[2]/table/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr[8]//a[' + str(number) +']')
        testName = toeicLink.text
    except NoSuchElementException:
        browser.maximize_window()
        screenshotNum = 1
        while (os.path.isfile('static/' + account + '-' + str(screenshotNum) + '.png')):
            screenshotNum += 1
        browser.save_screenshot('static/' + account + '-' + str(screenshotNum) + '.png')
        browser.quit()
        print("找不到測驗!!!", file = sys.stderr)
        return "<title>Toeic 自動填充題</title>找不到測驗<a href=''><input type='button' value='重試' /></a><br/><img  src='" + account + "-" + str(screenshotNum) + ".png'/>"
    print("連線到虎尾'Easy test線上學習測驗平台'...", file = sys.stderr)
    # browser.get('http://140.127.113.187/index.asp?m=false')
    browser.get('http://140.130.28.17/index.asp?m=false')
    assert "Easy test線上學習測驗平台" in browser.title
    print("登入虎尾'Easy test線上學習測驗平台'...", file = sys.stderr)
    # browser.find_element_by_name('cust_id').send_keys(account)
    browser.find_element_by_name('cust_id').send_keys('40132134')
    # browser.find_element_by_name('cust_pass').send_keys(str(password) + Keys.RETURN)
    browser.find_element_by_name('cust_pass').send_keys('40132134' + Keys.RETURN)
    try:
        browser.switch_to_alert().accept()
        print("帳密相同", file = sys.stderr)
    except NoAlertPresentException:
        pass
    try:
        browser.find_element_by_name('cust_id')
        browser.maximize_window()
        screenshotNum = 1
        while (os.path.isfile('static/' + account + '-' + str(screenshotNum) + '.png')):
            screenshotNum += 1
        browser.save_screenshot('static/' + account + '-' + str(screenshotNum) + '.png')
        browser.quit()
        print("登入失敗!!!", file = sys.stderr)
        return "<title>Toeic 自動填充題</title>登入失敗<a href=''><input type='button' value='重試' /></a><br/><img  src='" + account + "-" + str(screenshotNum) + ".png'/>"
    except NoSuchElementException:
        # browser.get("http://140.127.113.187/Courses/new_toeic/")
        # print("選擇選修科目!!!", file = sys.stderr)
        # try:
        #     browser.find_element_by_xpath('//*[@id="choice"]/option[' + str(elective) + ']').click()
        # except NoSuchElementException:
        #     browser.maximize_window()
        #     screenshotNum = 1
        #     while (os.path.isfile('static/' + account + '-' + str(screenshotNum) + '.png')):
        #         screenshotNum += 1
        #     browser.save_screenshot('static/' + account + '-' + str(screenshotNum) + '.png')
        #     browser.quit()
        #     print("找不到選修科目!!!", file = sys.stderr)
        #     return "<title>Toeic 自動填充題</title>找不到選修科目<a href=''><input type='button' value='重試' /></a><br/><img  src='" + account + "-" + str(screenshotNum) + ".png'/>"
        # browser.get("http://140.127.113.187/Courses/new_toeic/" + test + ".asp")
        browser.get("http://140.130.28.17/Courses/new_toeic/" + test + ".asp")
        try:
            browser.switch_to_alert().accept()
            print("繼續上次考試...", file = sys.stderr)
        except NoAlertPresentException:
            try:
                # toeicLink = browser.find_element_by_xpath('/html/body/table/tbody/tr/td[2]/table/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr[8]//a[' + str(number) +']')
                toeicLink = browser.find_element_by_xpath('/html/body/table/tbody/tr/td[2]/table/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr[8]//a[contains(text(), "' + testName + '")]')
            except NoSuchElementException:
                browser.maximize_window()
                screenshotNum = 1
                while (os.path.isfile('static/' + account + '-' + str(screenshotNum) + '.png')):
                    screenshotNum += 1
                browser.save_screenshot('static/' + account + '-' + str(screenshotNum) + '.png')
                browser.quit()
                print("找不到測驗!!!", file = sys.stderr)
                return "<title>Toeic 自動填充題</title>找不到測驗<a href=''><input type='button' value='重試' /></a><br/><img  src='" + account + "-" + str(screenshotNum) + ".png'/>"
            toeicLink.click()
            print("進入考試(抓題前先飆答案)'" + toeicLink.text + "'...", file = sys.stderr)
    browser.switch_to_window(browser.window_handles[1])
    for i in range(7):
        # browser.execute_script("for(var index = 0; index < document.getElementsByTagName('input').length; index++){if (document.getElementsByTagName('input')[index].value == 'A') {document.getElementsByTagName('input')[index].click();} else if (document.getElementsByTagName('input')[index].type == 'image'){document.getElementsByTagName('input')[index].click();}}")
        while (browser.execute_script("return document.getElementsByName('mainFrame')[0].contentWindow.document.all.length;") < 200):
            pass
        browser.execute_script("for(var index = 0; index < document.getElementsByName('mainFrame')[0].contentWindow.document.getElementsByTagName('input').length; index++){if (document.getElementsByName('mainFrame')[0].contentWindow.document.getElementsByTagName('input')[index].value == 'A') {document.getElementsByName('mainFrame')[0].contentWindow.document.getElementsByTagName('input')[index].click();} else if (document.getElementsByName('mainFrame')[0].contentWindow.document.getElementsByTagName('input')[index].type == 'image'){document.getElementsByName('mainFrame')[0].contentWindow.document.getElementsByTagName('input')[index].click();}}")
    print("抓答案...", file = sys.stderr)
    correct = {
        'simulation' : 'correct',
        'elective_simulation' : 'elective_correct',
        'make_subjust' : 'make_correct',
        'elective_make_subjust' : 'elective_make_correct',
    }
    # browser.get("http://140.127.113.187/Courses/new_toeic/" + correct[test] + ".asp?Q_Type=1")
    browser.get("http://140.130.28.17/Courses/new_toeic/" + correct[test] + ".asp?Q_Type=1")
    browser.execute_script('q={};')
    for i in range(7):
        url = "http://140.130.28.17/Courses/new_toeic/" + correct[test] + str(i + 1) +".asp"
        url = "http://140.130.28.17/Courses/new_toeic/" + correct[test] + str(i + 1) +".asp"
        browser.execute_script('document.getElementsByTagName("frame")[1].src = "' + url + '";n=' + str(i) +';');
        browser.execute_script('targetDocument=document.getElementsByTagName("frame")[1].contentWindow.document;index_count=((n<1)?10:(n<4)?30:(n<5)?40:(n<6)?12:48);index_2_count=((n==1)?3:4);for(index=' + ('-1' if (test == 'elective_make_subjust' and (i < 2 or i == 4)) else '0') + ';index<index_count' + ('-1' if (test == 'elective_make_subjust' and (i < 2 or i == 4)) else '') + '?-1:0;index++){if(n==5){q_name=targetDocument.getElementsByName("q"+(index+1))[0].parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.innerHTML.match(/([A-Z].[^<]*)</)[1];q_ans=targetDocument.getElementsByName("q"+(index+1))[0].parentElement.parentElement.parentElement.getElementsByTagName("font")[1].parentElement.innerHTML.match(/ \\([A-D]{1}\\) ([a-zA-Z $\\d\'.\\-,]*)/)[1];q[q_name]=q_ans}else{if(n>3){q_name=targetDocument.getElementsByName("q"+(index+1))[0].parentElement.parentElement.parentElement.getElementsByTagName("font")[0].innerHTML;q_ans=targetDocument.getElementsByName("q"+(index+1))[0].parentElement.parentElement.parentElement.getElementsByTagName("font")[1].parentElement.innerHTML.match(/ \\([A-D]{1}\\) ([a-zA-Z $\\d\'.\\-,]*)/)[1];q[q_name]=q_ans}else{for(index_2=0;index_2<index_2_count;index_2++){q_name=targetDocument.getElementsByName("q"+(index+1))[0].parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.getElementsByTagName("a")[0].href.match(/play_sound\\(\\"(T\\d{2}-\\d{2}-\\d{3}(-\\d{2}){0,1}).mp3\\"/)[1];if(targetDocument.getElementsByName("q"+(index+1))[index_2].parentElement.getElementsByTagName("font")[0]!=null){q[q_name]=String.fromCharCode("A".charCodeAt(0)+index_2)}}}}};')
    q = str(browser.execute_script("return q;"))
    browser.get("http://140.127.113.187/Courses/new_toeic/" + test + ".asp")
    toeicLink = browser.find_element_by_xpath('/html/body/table/tbody/tr/td[2]/table/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr[8]//a[' + str(number) +']')
    testName = toeicLink.text
    jsonFile = open(testName + ".json", "w")
    jsonFile.write(q)
    jsonFile.close()
    print("進入考試'" + toeicLink.text + "'...", file = sys.stderr)
    toeicLink.click()
    browser.switch_to_window(browser.window_handles[2])
    for i in range(7 - score):
        browser.execute_script("n=" + str(i) + ";q=" + q + ";index_count=((n<1)?10:(n<4)?30:(n<5)?40:(n<6)?12:48);index_2_count=((n==1)?3:4);for(index=0;index<index_count;index++){if(n<4){q_name=document.getElementsByName('q'+(index+1))[0].parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.getElementsByTagName('a')[" + ('0' if (test == 'elective_make_subjust') else '((n==1)?1:0)') + "].onclick.toString().match(/play_sound\(\\\"(T\d{2}-\d{2}-\d{3}(-\d{2}){0,1}).mp3\\\"/)[1]}else{if(n==5){q_name=document.getElementsByName('q'+(index+1))[0].parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.innerHTML.match(/([A-Z].[^<]*)</)[1]}else{q_name=document.getElementsByName('q'+(index+1))[0].parentElement.parentElement.parentElement.getElementsByTagName('font')[0].innerHTML}}ans=q[q_name];for(index_2=0;index_2<index_2_count;index_2++){if(n<4){if(document.getElementsByName('q'+(index+1))[index_2].value==ans){document.getElementsByName('q'+(index+1))[index_2].click()}}else{if(document.getElementsByName('q'+(index+1))[index_2].parentElement.getElementsByTagName('label')[0].innerHTML.match(/\([A-D]{1}\) ([a-zA-Z $\\d'.\\-,]*)/)[1]==ans){document.getElementsByName('q'+(index+1))[index_2].click()}}}}for(var index=0;index<document.getElementsByTagName('input').length;index++){if(document.getElementsByTagName('input')[index].type=='image'){document.getElementsByTagName('input')[index].click()}};")
    for i in range(7 - score, 7):
        browser.execute_script("for(var index = 0; index < document.getElementsByTagName('input').length; index++){if (document.getElementsByTagName('input')[index].value == 'A') {document.getElementsByTagName('input')[index].click();} else if (document.getElementsByTagName('input')[index].type == 'image'){document.getElementsByTagName('input')[index].click();}}")
    browser.maximize_window()
    screenshotNum = 1
    while (os.path.isfile('static/' + account + '-' + str(screenshotNum) + '.png')):
        screenshotNum += 1
    browser.save_screenshot('static/' + account + '-' + str(screenshotNum) + '.png')
    returnString = '<title>Toeic 自動填充題</title>答題成功!!<a href=""><input type="button" value="回選擇頁面" /></a><br/><img  src="' + account + '-' + str(screenshotNum) + '.png"/>'
    print(returnString.replace("<br/>", "\n"), file = sys.stderr)
    browser.quit()
    return returnString 
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80)
