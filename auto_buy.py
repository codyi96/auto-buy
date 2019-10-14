import os
import platform
import time
import datetime
from selenium import webdriver


def get_driver():
    os_type = platform.system()
    root_dir = os.path.dirname(os.path.abspath(__file__))
    drivers_dir = os.path.join(root_dir, 'drivers')
    if os_type == 'Darwin':
        return os.path.join(drivers_dir, 'chromedriver_mac64')
    elif os_type == 'Windows':
        return os.path.join(drivers_dir, 'chromedriver_win32.exe')
    elif os_type == 'Linux':
        return os.path.join(drivers_dir, 'chromedriver_linux64')
    else:
        return None


def login(chrome, url, store):
    chrome.get(url)
    chrome.implicitly_wait(10)
    time.sleep(2)
    # 淘宝
    if store == '1':
        chrome.find_element_by_link_text('亲，请登录').click()
    # 天猫
    elif store == '2':
        chrome.find_element_by_link_text('请登录').click()
    time.sleep(30)


def buy(chrome, store, buy_time):
    # 淘宝
    if store == '1':
        # "立即购买"的css_selector
        btn_buy = '#J_juValid > div.tb-btn-buy > a'
        # "立即下单"的css_selector
        btn_order = '#submitOrder_1 > div.wrapper > a'
    # 天猫
    elif store == '2':
        btn_buy = '#J_LinkBuy'
        btn_order = '#submitOrder_1 > div > a'

    while True:
        # 现在时间大于预设时间则开售抢购
        if datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f') > buy_time:
            try:
                # 找到"立即购买" 点击
                if chrome.find_element_by_css_selector(btn_buy):
                    chrome.find_element_by_css_selector(btn_buy).click()
                    break
                time.sleep(0.1)
            except:
                time.sleep(0.3)

    while True:
        try:
            # 找到"立即下单" 点击
            if chrome.find_element_by_css_selector(btn_order):
                chrome.find_element_by_css_selector(btn_order).click()
                # 下单成功，跳转至支付页面
                print('购买成功')
                break
        except:
            time.sleep(0.5)


if __name__ == "__main__":
    driver_location = get_driver()
    if driver_location is None:
        print('不支持的系统类型！')
        exit(-1)
    chrome = webdriver.Chrome(driver_location)
    # chrome.maximize_window()
    url = input('请输入商品链接：')
    store = input('请输入商城序号:\n1. 淘宝\n2. 天猫\n')
    buy_time = input('请输入抢购时间:\neg. 2019-10-15 00:00:00\n')
    print('请登录...')
    login(chrome, url, store)
    buy(chrome, store, buy_time)
