import json
import random
import string
import requests

from time import sleep
from random import randint
from dateutil import parser
from datetime import datetime, timedelta

from app_logger import get_logger
from text_reader import TextReader
from proxy_manager import ProxyManager
from postcode_generator import PostcodeGenerator

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service as ChromeService


class Selenium():
    def __init__(self, data):
        self.data = data
        self.logger = get_logger(__name__)
        self.url = 'http://localhost:3001/v1.0/browser_profiles/17628173/start?automation=1'
        self.response = requests.request("GET", self.url)
        self.port = json.loads(self.response.content)['automation']['port']
        self.postcode_generator = PostcodeGenerator()
        self.proxy_manager = ProxyManager(TextReader().get_proxies())

    @staticmethod
    def set_extension(ip, port, login, password):
        background_text = """function startProxy() {
        var config = {
            mode: "fixed_servers",
            rules: {
            singleProxy: {
                scheme: "http",
                host: 	"%s",		// Proxy IP or URL: type -> string
                port: 	%s		// Proxy port : type -> int
            },
            bypassList: ["localhost"]
            }
        };
        chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});
        }
        function callbackFn(details) {
            return {
                authCredentials: {
                    username: "%s",
                    password: "%s"
                }
            };
        }
        chrome.webRequest.onAuthRequired.addListener(
                    callbackFn,
                    {urls: ["<all_urls>"]},
                    ['blocking']
        );
        startProxy();
                """ % (ip, port, login, password)

        manifest_text = """{
        "name": "Chrome Proxy Extension",
        "version": "1.0",
        "description": "Proxy auto connect for ChromeDriver Option",
        "manifest_version": 2,
        "permissions": [
            "proxy",
            "tabs",
            "unlimitedStorage",
            "storage",
            "<all_urls>",
            "webRequest",
            "webRequestBlocking"
        ],
        "background": {
            "scripts": ["background.js"]
        },
        "minimum_chrome_version":"22.0.0"
        }
        """
        with open('./proxy/background.js', 'w') as f:
            f.write(background_text)
        with open('./proxy/manifest.json', 'w') as f:
            f.write(manifest_text)

    def create_account(self):
        for acc in self.data:
            try:
                while 1:
                    options = webdriver.ChromeOptions()
                    options.debugger_address = f'127.0.0.1:{self.port}'
                    proxy = self.proxy_manager.get_proxy()
                    self.set_extension(proxy[0].split(':')[0], proxy[0].split(':')[1], proxy[1], proxy[2])
                    options.add_argument('load-extension=./proxy')
                    driver = webdriver.Chrome(service=ChromeService(executable_path='./chromedriver'), options=options)

                    # getting ip
                    driver.get('https://api.ipify.org/')
                    json_file = open('./ip.json')
                    ips_json = json.load(json_file)
                    ip_address = driver.find_element(By.TAG_NAME, "body").text
                    now = datetime.now()

                    if ip_address not in ips_json.keys():
                        ips_json[ip_address] = str(now - timedelta(days=2))

                    if (now - parser.parse(ips_json[ip_address])).days > 0:
                        ips_json[ip_address] = str(now)
                        print(ips_json)
                        json_file = open("./ip.json", "w")
                        json_file.write(json.dumps(ips_json))

                        driver.get("some url")
                        sleep(3)

                        driver.switch_to.frame(0)

                        country_select = Select(
                            driver.find_element(By.ID, 'country_residence'))
                        country_select.select_by_value("197")

                        # confirm country button
                        try:
                            sleep(1)
                            driver.find_element(By.CLASS_NAME, 'ConfirmButton').click()
                        except:
                            pass

                        # gender
                        gender_select = Select(driver.find_element(By.ID, 'title'))

                        if acc[6] == 'F':
                            gender_select.select_by_value("7")
                        else:
                            gender_select.select_by_value("4")

                        # name
                        f_name_input = driver.find_element(By.XPATH,
                                                            '/html/body/div[1]/div/div[1]/div[2]/div/div[2]/div/div[2]/div[4]/div[4]/div[1]/div/input')
                        f_name_input.send_keys(acc[0])
                        s_name_input = driver.find_element(By.XPATH,
                                                            '/html/body/div[1]/div/div[1]/div[2]/div/div[2]/div/div[2]/div[4]/div[4]/div[2]/div/input')
                        s_name_input.send_keys(acc[1])

                        # birth selection
                        day_select = Select(driver.find_element(By.XPATH,
                                                            '/html/body/div[1]/div/div[1]/div[2]/div/div[2]/div/div[2]/div[4]/div[5]/div/div[1]/select'))
                        day_select.select_by_value(acc[4][2:4])
                        month_select = Select(driver.find_element(By.XPATH,
                                                            '/html/body/div[1]/div/div[1]/div[2]/div/div[2]/div/div[2]/div[4]/div[5]/div/div[2]/select'))
                        month_select.select_by_value(acc[4][0:2])
                        year_select = Select(driver.find_element(By.XPATH,
                                                            '/html/body/div[1]/div/div[1]/div[2]/div/div[2]/div/div[2]/div[4]/div[5]/div/div[3]/select'))
                        year_select.select_by_value(acc[4][4:])

                        # email
                        email_input = driver.find_element(By.XPATH,
                                                            '/html/body/div[1]/div/div[1]/div[2]/div/div[2]/div/div[2]/div[5]/div[2]/div/input')
                        email_input.send_keys(acc[5])

                        # phone
                        phone_input = driver.find_element(By.XPATH,
                                                            '/html/body/div[1]/div/div[1]/div[2]/div/div[2]/div/div[2]/div[5]/div[3]/div/input')
                        phone_input.send_keys(self.generate_numbers())

                        sleep(1)
                        # newsletter radio button
                        driver.find_element(By.XPATH,
                                                    '/html/body/div[1]/div/div[1]/div[2]/div/div[2]/div/div[2]/div[6]/div[3]/div/div[2]/label/span').click()

                        # address
                        house_address_input = driver.find_element(By.XPATH,
                                                            '/html/body/div[1]/div/div[1]/div[2]/div/div[2]/div/div[2]/div[7]/div[2]/div/input')
                        house_address_input.send_keys(acc[2])
                        postcode_input = driver.find_element(By.XPATH,
                                                            '/html/body/div[1]/div/div[1]/div[2]/div/div[2]/div/div[2]/div[7]/div[4]/div/input')
                        postcode_input.send_keys(self.postcode_generator.generate_postcode())

                        # login/password
                        login_input = driver.find_element(By.XPATH,
                                                            '/html/body/div[1]/div/div[1]/div[2]/div/div[2]/div/div[2]/div[8]/div[2]/div/input')
                        login_input.send_keys(acc[5].split('@')[0])
                        password = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(10))
                        pass_input = driver.find_element(By.XPATH,
                                                            '/html/body/div[1]/div/div[1]/div[2]/div/div[2]/div/div[2]/div[8]/div[3]/div[1]/input')

                        pass_input.send_keys(password)
                        sleep(1)

                        # policy radio button
                        driver.find_element(By.XPATH, '/html/body/div[1]/div/div[1]/div[2]/div/div[2]/div/div[2]/div[10]/div/div/label').click()

                        # submit button
                        driver.find_element(By.XPATH, '/html/body/div[1]/div/div[1]/div[2]/div/div[2]/div/div[2]/div[11]/button').click()

                        with open("created_accounts.txt", "a") as file_object:
                            file_object.write(f"{acc[5].split('@')[0]}:{password}\n")

                        driver.quit()
                        # proxy reset request
                        requests.request("GET", proxy[4])
                    else:
                        driver.quit()
                        self.proxy_manager.next_proxy()
                        # proxy reset request
                        requests.request("GET", proxy[4])
            except Exception as ex:
                print(str(ex))
                self.logger.error(str(ex))
                with open("errored_accounts.txt", "a") as file_object:
                    file_object.write(f"{acc}\n")
                self.proxy_manager.next_proxy()
        url_stop = 'http://localhost:3001/v1.0/browser_profiles/17628173/stop'
        requests.request("GET", url_stop)

    @staticmethod
    def generate_numbers() -> str:
        region_codes = ['020', '024', '029', '0113', '0114', '0131', '0141', '0151', '0161', '01642', '01223', '01257',
                        '01382', '01386', '01935', '01865', '01772', '01792', '01204', '015396', '016977', '016064']
        region_ind = randint(0, len(region_codes) - 1)
        random_num = str(randint(10000000, 99999999))[:11-len(region_codes[region_ind])]
        return '+44' + region_codes[region_ind] + random_num


if __name__ == '__main__':
    accounts_data = TextReader().get_accounts()
    sel_obj = Selenium(accounts_data)
    sel_obj.create_account()
