# pip install selenium
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def login_chaoxing(username,password,url):
    # 获取当前脚本所在目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # 构造驱动路径（驱动文件在子目录driver中）
    driver_path = os.path.join(current_dir, "driver", "msedgedriver.exe")
    Destination_path = url

    driver = webdriver.Edge(service=Service(driver_path))
    driver.get(Destination_path)
    try:
        #输入账户密码
        user_field = WebDriverWait(driver,30).until(
            EC.presence_of_element_located((By.ID,'phone'))
        )
        pwd_field = driver.find_element(By.ID,'pwd')
        login_btn = driver.find_element(By.ID,'loginBtn')
        user_field.send_keys(username)
        pwd_field.send_keys(password)
        login_btn.click()
        
        #验证登录结果
        # WebDriverWait(driver,15).until(
        #     EC.presence_of_element_located((By.CLASS_NAME,'course-list'))
        # )
        # print("登录成功")
        return driver
    except Exception as e:
        print(f"登录失败：{str(e)}")
        return None
        # driver.quit()

def crawl_and_save(driver,outputfilename,pagenumber):
    if driver:
        script_dir = os.path.dirname(os.path.abspath(__file__))  # 脚本所在目录
        file_path = os.path.join(script_dir, "output",f"{outputfilename}.txt")
        # with open语句会在代码块结束后自动关闭文件
        with open(file_path, "a") as file:
            for _ in range(1,pagenumber+1):  
                try:          
                    # 1. 显示答案按钮检测（优化逻辑）
                    answer_btn_xpath = '//a[@onclick="toAnsweredView()"]'
                    answer_buttons = driver.find_elements(By.XPATH, answer_btn_xpath)
                    if answer_buttons:  # 存在按钮时才点击
                        WebDriverWait(driver, 5).until(
                            EC.element_to_be_clickable((By.XPATH, answer_btn_xpath))
                        ).click()
                        time.sleep(0.5)  # 保守等待答案加载
                    # 2. 题目内容获取（强化容错）
                    question_element = WebDriverWait(driver, 15).until(
                        EC.visibility_of_element_located((By.CLASS_NAME, 'noSplitBx'))
                    )
                    # 3. 写入
                    file.write(f"{question_element.text}\n")

                    # 4. 下一页操作
                    next_btn_xpath = '//a[@onclick="getTheNextQuestion(1)"]'
                    next_button = WebDriverWait(driver, 15).until(
                        EC.presence_of_element_located((By.XPATH, next_btn_xpath))
                    )
                    next_button.click()
                    time.sleep(1)  # 兼容性等待
                except Exception as e:
                    print(f"第{_}题处理失败，错误类型：{type(e).__name__},详情{str(e)}")
                    continue
        input("按回车键退出...") 

if __name__ == "__main__":
    #  https://mooc1.chaoxing.com/exam-ans/exam/test/reVersionTestStartNew?keyboardDisplayRequiresUserAction=1&courseId=200988214&classId=115724606&tId=6677023&id=149823085&p=1&start=0&monitorStatus=0&monitorOp=-1&examsystem=0&qbanksystem=0&qbankbackurl=&remainTimeParam=31378933&relationAnswerLastUpdateTime=1741252221855&enc=f89e725f4077e5748d4ddc87540bbc4b&cpi=43169274&openc=a022a29aebb494f156f06719af13578e&newMooc=true&webSnapshotMonitor=0
    url = input("请输入爬取的学习通题库url")
    user = input("请输入用户名")
    pwd = input("请输入密码")
    outputfilename = input("请输入结果保存的文件名")
    # pagenumber = 342
    pagenumber = int(input("请输入希望爬取的页数"))
    driver = login_chaoxing(user,pwd,url)

    crawl_and_save(driver,outputfilename,pagenumber)
