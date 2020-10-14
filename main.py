from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import selenium.webdriver.support as EC
import requests, time, random, json, os


def auth(login, password):
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(chrome_options=options)
    wait = WebDriverWait(driver, 15)
    driver.get('http://www.vk.com')
    elem = driver.find_element_by_id('index_email')
    elem.send_keys(login)
    elem = driver.find_element_by_id('index_pass')
    elem.send_keys(password)
    elem.send_keys(Keys.RETURN)
    try:
        # wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'top_profile_img')))
        time.sleep(5)
        driver.get('https://oauth.vk.com/authorize?client_id=2685278&scope=1073741823&redirect_uri=https://api.vk.com/blank.html&display=page&response_type=token&revoke=1')
        driver.find_element_by_class_name('button_indent').click()
        # wait.until(EC.title_contains('OAuth Blank'))
        time.sleep(5)
        token = driver.current_url.split('access_token=')[1].split('&')[0]
        driver.get('https://likest.ru/')
        print(driver.window_handles)
        driver.find_element_by_id('ulogin-button').click()
        time.sleep(1)
        print(driver.window_handles)
        time.sleep(1)
        driver.switch_to_window(driver.window_handles[(-1)])
        try:
            driver.find_element_by_class_name('button_indent').click()
        except Exception as e:
            pass

        time.sleep(1)
        print(driver.window_handles)
        driver.switch_to_window(driver.window_handles[0])
    except Exception as e:
        driver.close()
        raise Exception('Error while login')

    print(token)
    return [driver, token]


def operationController(driver, token, params):
    localRequestsBase = []
    r = requestErrorHandler('friends.getRequests', {'count':1000,  'access_token':token,  'need_viewed':1,  'v':'5.92'})
    for x in r['response']['items']:
        localRequestsBase.append(x)

    wait = WebDriverWait(driver, 15)
    driver.find_element_by_xpath('//*[@id="main-menu"]/li[3]/a').click()
    driver.find_element_by_xpath('//*[@id="block-system-main"]/div/div[2]/div[2]/a').click()
    elem = driver.find_element_by_id('amount')
    elem.clear()
    elem.send_keys(str(params[0]))
    elem = driver.find_element_by_id('reward')
    elem.clear()
    elem.send_keys('2')
    driver.find_element_by_id('edit-submit').click()
    time.sleep(3)
    driver.get('https://likest.ru/orders/friends')
    while True:
        a = 0
        while a < int(params[1]):
            r = requestErrorHandler('friends.getRequests', {'count':1000,  'access_token':token,  'need_viewed':1,  'v':'5.92'})
            for x in r['response']['items']:
                if x not in localRequestsBase:
                    requestErrorHandler('account.ban', {'owner_id':x,  'access_token':token,  'v':'5.92'})
                    a += 1
                    time.sleep(0.5)

            time.sleep(3)

        time.sleep(3)
        driver.find_element_by_class_name('order-action').click()
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="targeting"]/legend/span/a')))
        driver.find_element_by_xpath('//*[@id="targeting"]/legend/span/a').click()
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="limiting"]/legend/span/a')))
        driver.find_element_by_xpath('//*[@id="limiting"]/legend/span/a').click()
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="lim-60"]')))
        elem = driver.find_element_by_xpath('//*[@id="lim-60"]')
        elem.clear()
        elem.send_keys('1')
        elem = driver.find_element_by_xpath('//*[@id="friends-min"]')
        elem.clear()
        elem.send_keys('999')
        driver.find_element_by_xpath('//*[@id="required-mail"]').click()
        driver.find_element_by_xpath('//*[@id="edit-submit"]').click()
        time.sleep(5)
        driver.get('https://likest.ru/orders/friends#ok')
        while True:
            r = requestErrorHandler('friends.getRequests', {'count':1000,  'access_token':token,  'need_viewed':1,  'v':'5.92'})
            for x in r['response']['items']:
                if x not in localRequestsBase:
                    requestErrorHandler('account.ban', {'owner_id':x,  'access_token':token,  'v':'5.92'})
                    time.sleep(0.5)

            element = driver.find_element_by_css_selector('html')
            r = element.get_attribute('innerHTML')
            if '<a href="#" class="ztips" title="">' not in r:
                break
            driver.refresh()
            elem = driver.find_element_by_xpath('//*[@id="logo"]')
            time.sleep(4)

        time.sleep(3)
        driver.find_element_by_class_name('order-action').click()
        elem = driver.find_element_by_xpath('//*[@id="amount"]')
        elem.clear()
        elem.send_keys(str(params[0]))
        driver.find_element_by_xpath('//*[@id="edit-submit"]').click()
        time.sleep(5)
        r = requestErrorHandler('account.getBanned', {'access_token':token,  'count':'200',  'v':'5.92'})
        for x in r['response']['items']:
            requestErrorHandler('account.unban', {'owner_id':x,  'access_token':token,  'v':'5.92'})
            time.sleep(0.5)

        localRequestsBase = []
        r = requestErrorHandler('friends.getRequests', {'count':1000,  'access_token':token,  'need_viewed':1,  'v':'5.92'})
        for x in r['response']['items']:
            localRequestsBase.append(x)

        time.sleep(3)
        driver.find_element_by_class_name('order-action').click()
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="targeting"]/legend/span/a')))
        driver.find_element_by_xpath('//*[@id="targeting"]/legend/span/a').click()
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="limiting"]/legend/span/a')))
        driver.find_element_by_xpath('//*[@id="limiting"]/legend/span/a').click()
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="lim-60"]')))
        elem = driver.find_element_by_xpath('//*[@id="lim-60"]')
        elem.clear()
        elem.send_keys('0')
        elem = driver.find_element_by_xpath('//*[@id="friends-min"]')
        elem.clear()
        elem.send_keys('0')
        driver.find_element_by_xpath('//*[@id="required-mail"]').click()
        driver.find_element_by_xpath('//*[@id="edit-submit"]').click()
        time.sleep(3)


def requestErrorHandler(method, data):
    while True:
        try:
            r = requests.get(f"https://api.vk.com/method/{method}?", params=data)
            if r.status_code != 200:
                raise Exception('HTTP error')
            print('Процесс запущен.')
            return json.loads(r.text)
        except Exception as e:
            print(e)


number = input('Введите номер телефона: ')
password = input('Введите пароль: ')
params = [input('Введите количество подписчиков: '), input('Введите максимальный размер чс: ')]
data = auth(number, password)
operationController(data[0], data[1], params)
