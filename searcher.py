import time

from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from emailer import emailer_datas, emailer_notification


class Searcher:
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self._init_webdriver()

    def _init_webdriver(self):
        """
        Function responsible for the initialization of the webdriver (selenium), giving it a User Agent and turning it
        headless

        :return: nothing
        """

        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=ChromeDriverManager().install())

    def login(self):
        self.driver.get("https://inforestudante.ipc.pt/nonio/security/login.do")
        time.sleep(5)
        self.driver.find_element(By.ID, "username").send_keys(self.email)
        self.driver.find_element(By.ID, "password1").send_keys(self.password)
        time.sleep(2)
        self.driver.find_element(By.ID, "password1").send_keys(Keys.ENTER)
        time.sleep(3)

        if "dashboard" in self.driver.current_url:
            return True
        else:
            return False

    def go_to_inscricoes(self):
        self.driver.get(
            self.driver.find_element(By.CLASS_NAME, "menu_22").
            find_element(By.XPATH, "..").
            get_attribute("href")
        )
        time.sleep(5)

        self.driver.get(
            self.driver.find_element(By.ID, "link_0").
            find_element(By.TAG_NAME, "a").
            get_attribute("href")
        )
        time.sleep(5)

    def availability_date_checker(self):
        datas = list()
        for row in self.driver.find_elements(By.CLASS_NAME, "lightrow"):
            if row.find_element(By.XPATH, "td[5]").text:
                print(f"DATAS DISPONIVEIS: CADEIRA - {row.find_element(By.XPATH, 'td[2]').text}; DATA - {row.find_element(By.XPATH, 'td[5]').text}")
                datas.append({
                    "cadeira": row.find_element(By.XPATH, 'td[2]').text,
                    "data": row.find_element(By.XPATH, 'td[5]').text
                })

        if len(datas) == 0:
            self.driver.get(
                self.driver.find_element(By.CLASS_NAME, "botaodetalhes").
                get_attribute("href")
            )
            time.sleep(5)

            if "ainda não se encontram disponíveis" in self.driver.page_source:
                return False
            else:
                emailer_notification()
                return True

        else:
            emailer_datas(datas)
            return True
