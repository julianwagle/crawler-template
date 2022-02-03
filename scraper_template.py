# Formatted and Linted with Black

from datetime import datetime as dt
from inspect import stack
from itertools import islice
from json import dump, load
from logging import (
    basicConfig as lbc,
    StreamHandler as lsh,
    debug as l0,
    info as l1,
    warning as l2,
    error as l3,
    critical as l4,
)
from os import environ as env, listdir, remove, replace, mkdir
from pathlib import Path
from random import choice, randint, uniform
from re import sub, search, compile
from requests import get as req
from string import ascii_letters as abc
from subprocess import check_call as subp
from sys import exit as xit, executable as xec
from time import sleep
from uuid import uuid4 as uu
from zipfile import ZipFile as zf

from bs4 import BeautifulSoup as bs

from selenium import webdriver as wd
from selenium.webdriver.chrome.service import Service as sv
from selenium.webdriver.common.action_chains import ActionChains as ac
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait as wdw

from selenium_stealth import stealth as shh
    
DIR_ROOT = Path(__file__).resolve(strict=1).parent
DIR_DATA = f"../data/"
DIR_LOGS = f"./logs/"
DIR_HTML = f"../data/html/"
DIR_IMGS = f"../data/imgs/"
CHROME_DRIVER = f"./chromedriver"

class Main:


    # INIT SECTION
    ##############
    def __init__(self):
        self.log_config()
        self.log_clean()
        self.__SETTINGS__()
        self.main()

    def __SETTINGS__(self):
        self.log_start(extra=1)
        # BROWSER CONFIG
        ################
        # Configured for MacOS
        self.CHROME_PATH = "/Users/home/Library/Application Support/Google/Chrome/"
        self.CHROME_PROFILE = "Profile 5"
        # Don't change this. It's the only option for slenium_stealth
        self.USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36"
        # PROJECT SPECIFIC

    def main(self):
        self.log_start(extra=1)
        self.web()


    ###################################
    # GENERAL HELPERS AND UTILS BEGIN #
    ###################################

    # SELENIUM CONFIG
    #################
    def web(self):
        self.log_start()
        self.web_options()
        self.web_driver()
        self.web_action()
        self.web_shh()
        self.web_clear()

    def web_options(self):
        self.log_start()
        self.options = wd.ChromeOptions()

        self.options.add_argument(f"--user-data-dir={self.CHROME_PATH}")
        self.options.add_argument(f"--profile-directory={self.CHROME_PROFILE}")

        self.options.add_argument("--user-agent=%s" % self.USER_AGENT)

        self.options.add_argument("start-maximized")
        self.options.add_experimental_option("excludeSwitches", ["enable-automation"])
        self.options.add_experimental_option("useAutomationExtension", 0)

    def web_driver(self):
        self.log_start()

        self.driver = sv(CHROME_DRIVER)
        self.driver = wd.Chrome(service=self.driver, options=self.options)
        self.driver.set_script_timeout(1000)
        self.driver.implicitly_wait(30)

    def web_action(self):
        self.log_start()
        self.action = ac(self.driver)

    def web_shh(self):
        self.log_start()
        shh(
            driver=self.driver,
            user_agent=self.USER_AGENT,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=1,
            run_on_insecure_origins=0,
        )

    def web_clear(self):
        self.log_start()
        # I think they place a blocked cookie in browser ...
        # sneaky little fuckers. Ruins the proxy rotation
        self.driver.delete_all_cookies()

    # SELENIUM HELPERS
    ##################
    def web_go(self, url, get=0, https=1):
        self.log_start()
        if https:
            self.driver.get(f"https://{url}")
        else:
            self.driver.get(f"{url}")
        if get:
            return self.bs_html()

    def web_scroll(self, count):
        self.log_start()
        for i in range(count):
            l0(f"{stack()[1][3]} status ({i}/{count})")
            html = self.bs_html()
            body = self.bs_element(html, key="body")
            l0("Down keys to be sent.")
            body.send_keys(Keys.PAGE_DOWN)
            self.zzz(mn=0.25 , mx=1)

    def web_type(self, element, txt):
        self.log_start()
        element.click()
        for char in txt:
            self.zzz(mn=0.1, mx=0.2)
            pf = [1] * 59
            pf.append(0)
            pf = choice(pf)
            if pf == 1:
                element.send_keys(char)
            else:
                element.send_keys(choice(abc))
                element.send_keys(Keys.BACK_SPACE)
                element.send_keys(char)

    # BS4 HELPERS
    #############
    def bs_children(self, element):
        self.log_start()
        elements = element.children
        for e in elements:
            if len(str(e)) > 1:
                yield bs(str(e), "html.parser")

    def bs_click(self, html, key, val=0, n=0):
        self.log_start()
        if val:
            element = html.find_all(attrs={key: val})[n]
        else:
            element = html.find_all(key)[n]
        xpath = self.bs_xpath(element)
        wdw(self.driver, 30).until(
            ec.element_to_be_clickable((By.XPATH, xpath))
        ).click()
        self.zzz()

    def bs_element(self, html, key, val=0, n=0):
        self.log_start()
        if val:
            element = html.find_all(attrs={key: val})[n]
        else:
            element = html.find_all(key)[n]
        xpath = self.bs_xpath(element)
        l0(f"grabbed xpath: {xpath}")
        element = self.driver.find_element(By.XPATH, xpath)
        l0(f"found element: {element}")
        return element

    def bs_html(self, pretty=0):
        self.log_start()
        src = self.driver.page_source
        l0("grabbed page src")
        html = bs(src, "html.parser")
        l0("parsed page src")
        if pretty:
            l0("making html pretty")
            return html.prettify()
        l0("html complete")
        return html

    def bs_read(self, page):
        self.log_start()
        f = open(f"{DIR_HTML}/{page}.html", "r")
        html = f.read()
        soup = bs(html, "html.parser")
        self.bs_save(page=page, html=soup)
        return soup

    def bs_save(self, page, html=0):
        self.log_start()
        if html:
            html = html.prettify()
        else:
            html = self.bs_html(pretty=1)
        with open(f"{DIR_HTML}{page}.html", "w") as fout:
            fout.write(html)

    def bs_title(self):
        html = self.bs_html(pretty=1)
        soup = bs(html, "html.parser")
        title = soup.title.string
        title = self.str_clean(str(title))
        return title

    def bs_xpath(self, element):
        self.log_start()
        """
        Generate xpath of soup element
        :param element: bs4 text or node
        :return: xpath as string
        """
        components = []
        child = element if element.name else element.parent
        for parent in child.parents:
            """
            @type parent: bs4.element.Tag
            """
            previous = islice(parent.children, 0, parent.contents.index(child))
            xpath_tag = child.name
            xpath_index = sum(1 for i in previous if i.name == xpath_tag) + 1
            components.append(
                xpath_tag if xpath_index == 1 else "%s[%d]" % (xpath_tag, xpath_index)
            )
            child = parent
        components.reverse()
        return "/%s" % "/".join(components)

    # LOGGING HELPERS
    #################
    def log_config(self):
        t = str(dt.now()).split(".")[0].replace(" ", "@")
        lbc(
            filename=f"{DIR_LOGS}{t}.log",
            encoding="utf-8",
            format="%(asctime)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d@%H:%M:%S",
            level=0,
        )
        lsh().setLevel(0)

    def log_clean(self, store=3):
        self.log_start()
        logs = listdir(DIR_LOGS)
        names = []
        for i in range(len(logs)):
            names.append(str(logs[i]).split(".")[0])
        names.sort(key=lambda date: dt.strptime(date, "%Y-%m-%d@%H:%M:%S"))
        keepers = names[-store:]
        for f in logs:
            name = str(f).split(".")[0]
            if name not in keepers:
                remove(f"{DIR_LOGS}{f}")

    def log_start(self, nap=0, extra=0, n=3):
        if extra:
            look = ">" * 45
        else:
            look = ">" * 15

        name = str(stack()[1][n])
        l0(f"{look} starting {name} ")
        if nap:
            self.zzz()
        return name

    def log_except(self, e):
        look = "!" * 15
        return l3(f"{look} error at {stack()[1][3]}: {e}")

    # JSON HELPERS
    ##############
    def json_dump(self, content, dest):
        self.log_start()
        pth = f"{DIR_ROOT}/{uu()}{uu()}.json"
        with open(pth, "w") as f:
            dump(content, f, indent=4)
        try:
            with open(pth) as f:
                q = load(f)
            replace(pth, dest)
        except:
            remove(pth)

    def json_load(self, pth):
        self.log_start()
        try:
            with open(pth, "r") as json_file:
                data = load(json_file)
        except FileNotFoundError as e:
            self.log_except(e)
            data = {}
            self.json_dump(data, pth)
        return data

    # OTHER
    #######
    # string cleaning hahaha .. get it? like sPring cleaning hahaha!
    def str_clean(self, s, json=0):
        self.log_start()
        s = sub(r"…", "...", s)
        s = sub(r"[`‘’‛⸂⸃⸌⸍⸜⸝]", "'", s)
        s = sub(r"[„“]|(\'\')|(,,)", '"', s)
        s = sub(r"\s+", " ", s).strip()
        if json:
            l0("cleaning json")
            s = s.replace("'", '"')
        return s

    def zzz(self, mn=1, mx=5):
        t = round(uniform(mn, mx), 7)
        if t > 5:
            l0(f"sleeping for {t}")
        sleep(t)


if __name__ == "__main__":
    Main()
