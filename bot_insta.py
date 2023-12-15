import os

from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import random

from webdriver_manager.chrome import ChromeDriverManager

from csv_handler import CSVHandler


class InstagramBot:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.users_to_mark = []
        csv = CSVHandler()
        users_to_mark = csv.open_csv('insta_users.csv')
        for user in users_to_mark:
            self.users_to_mark.append(user[0])

        giveaways = csv.open_csv('sorteios.csv')

        self.giveaways = {}
        for giveaway in giveaways:
            url = giveaway[0]
            self.giveaways[url] = [int(giveaway[1].strip()), bool(giveaway[2].strip())]

        options = webdriver.ChromeOptions()
        # options.headless = True

        options.add_argument('--no-sandbox')
        options.add_argument('window-size=1920x1080')
        self.options = options
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

    def login(self):
        driver = self.driver
        driver.get("https://www.instagram.com")
        time.sleep(3)
        campo_usuario = driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div/div/div['
                                                      '1]/section/main/article/div[2]/div[1]/div[2]/form/div/div['
                                                      '1]/div/label/input')
        campo_usuario.click()
        campo_usuario.clear()
        campo_usuario.send_keys(self.username)
        campo_password = driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div/div/div['
                                                       '1]/section/main/article/div[2]/div[1]/div[2]/form/div/div['
                                                       '2]/div/label/input')
        campo_password.click()
        campo_password.clear()
        campo_password.send_keys(self.password)
        campo_password.send_keys(Keys.RETURN)
        time.sleep(10)

        self.make_comments()

    def type_like_human(self, frase, onde_digitar):
        for letra in frase:
            onde_digitar.send_keys(letra)
            time.sleep(random.randint(1, 5) / 30)

    def make_comments(self):
        driver = self.driver
        csv = CSVHandler()

        for url in self.giveaways.keys():

            url_link = url#.split('_')[1]

            if os.path.isfile('done/' + url_link + '.csv'):
                continue

            done = set()
            if os.path.isfile('doing/' + url_link + '.csv'):
                done = csv.open_csv('doing/' + url_link + '.csv')

            driver.get(url)

            users_by_post = []
            amount = self.giveaways[url][0]
            repeat = self.giveaways[url][1]
            users = set()

            if repeat:
                size = len(self.users_to_mark)

                for i in range(1, size):
                    index = random.randint(0, len(self.users_to_mark) - 1)
                    user = self.users_to_mark[index]

                    if len(users) == amount:
                        users_by_post.append(users)
                        users = set()

                    len_before = len(users)
                    users.add(user)
                    len_after = len(users)

                    if len_before == len_after:
                        size += 1

            else:
                for user in self.users_to_mark:
                    if len(users) == amount:
                        users_by_post.append(users)
                        users = set()
                    users.add(user)

            for comment in users_by_post:

                flag = False
                text = ''
                for person in comment:
                    if person in done:
                        flag = True
                    text = text + person + ' '

                if flag:
                    continue

                try:

                    self.driver.find_element(By.CSS_SELECTOR, ".x1qlqyl8").click()
                    comment_field = driver.find_element(By.CSS_SELECTOR,
                                                        ".x1qlqyl8")
                    time.sleep(random.randint(5, 10))
                    self.type_like_human(text, comment_field)
                    time.sleep(random.randint(10, 20))

                    comment_field.send_keys(Keys.RETURN)
                    comment_field.send_keys(Keys.RETURN)


                    done.add(comment)
                    #if not repeat:
                    #    csv.write_csv('doing/', url_link + '.csv', done)
                    time.sleep(60)

                except Exception as e:
                    print(e)
                    time.sleep(5)

            if not repeat:
                csv.write_csv('done/', url_link + '.csv', users_by_post)

    def remove_blocked(self):

        non_blocked = set()
        non_blocked.add('users')
        for user in self.users_to_mark:
            self.driver.get('https://www.instagram.com/' + user)

            blocked = self.driver.find_element_by_xpath('/html/body/div/div[1]/div/div/h2')
            print(blocked.text)
            if 'não está disponível' not in blocked.text:
                non_blocked.add(user)

        csv = CSVHandler()
        csv.write_csv('', 'insta_users.csv', non_blocked)

    def __check_exists_by_xpath(self, xpath):
        try:
            self.driver.find_element(By.XPATH, xpath)
        except NoSuchElementException:
            return False
        return True

    def __check_exists_by_css(self, css_path):
        try:
            self.driver.find_element(By.CSS_SELECTOR, css_path)
        except NoSuchElementException:
            return False
        return True


joaoBot = InstagramBot('user', 'pass')
joaoBot.login()
