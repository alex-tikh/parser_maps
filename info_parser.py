import os
import json
import random
import argparse
import csv
import signal
import glob

from time import sleep

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

from webdriver_manager.firefox import GeckoDriverManager

from soup_parser import SoupContentParser
from utils import json_pattern


class Parser:
    def __init__(self, driver):
        self.driver = driver
        self.soup_parser = SoupContentParser()

    def _write_csv(self, outputs, type_org):
        with open(f"result_output/{type_org}_outputs.csv", "a", newline="") as csvfile:
            headers = outputs[0].keys()
            writer = csv.DictWriter(
                csvfile, delimiter=",", lineterminator="\n", fieldnames=headers
            )

            if csvfile.tell() == 0:
                writer.writeheader()  # file doesn't exist yet, write a header

            writer.writerows(outputs)

    def _driver_wait(self, element_class, delay=10):
        myElem = WebDriverWait(self.driver, delay).until(
            EC.presence_of_element_located((By.CLASS_NAME, element_class))
        )

    def _driver_quit(self):
        driver_pid = self.driver.service.process.pid
        self.driver.quit()
        try:
            os.kill(int(driver_pid), signal.SIGTERM)
            print("Killed browser using process")
        except ProcessLookupError as ex:
            pass

    def parse_data(self, hrefs, type_org):
        self.driver.maximize_window()
        self.driver.get("https://yandex.ru/maps")
        parent_handle = self.driver.window_handles[0]
        org_id = 0
        outputs = []
        if os.path.exists(f"result_output/{type_org}_outputs.csv"):
            os.remove(f"result_output/{type_org}_outputs.csv")

        for organization_url in hrefs:
            try:
                self.driver.execute_script(
                    f'window.open("{organization_url}","org_tab");'
                )
                child_handle = [
                    x for x in self.driver.window_handles if x != parent_handle
                ][0]
                self.driver.switch_to.window(child_handle)
                sleep(1)
                soup = BeautifulSoup(self.driver.page_source, "lxml")
                org_id += 1
                name = self.soup_parser.get_name(soup)
                address = self.soup_parser.get_address(soup)
                website = self.soup_parser.get_website(soup)
                opening_hours = self.soup_parser.get_opening_hours(soup)
                ypage = self.driver.current_url
                rating = self.soup_parser.get_rating(soup)
                social = self.soup_parser.get_social(soup)
                phone = self.soup_parser.get_phone(soup)
                goods, reviews = None, None
                coordinates = self.soup_parser.get_coordinates(soup)
                n_reviews = self.soup_parser.get_review_number(soup)
                stops = self.soup_parser.get_transport_stops(soup)
                tags = self.soup_parser.get_tags(soup)
                output = json_pattern.into_json(
                    org_id,
                    name,
                    address,
                    coordinates,
                    website,
                    opening_hours,
                    ypage,
                    rating,
                    n_reviews,
                    phone,
                    social,
                    stops,
                    tags,
                )
                outputs.append(output)

                if len(outputs) % 100 == 0:
                    self._write_csv(outputs, type_org)
                    outputs = []
                    self._driver_quit()
                    sleep(random.uniform(2.2, 2.4))
                    headOption = webdriver.FirefoxOptions()
                    headOption.headless = True
                    driver_path = GeckoDriverManager(path="drivers", version="0.32.2").install()
                    self.driver = webdriver.Firefox(
                        executable_path=driver_path, options=headOption
                    )
                    self.driver.maximize_window()
                    self.driver.get("https://yandex.ru/maps")
                    parent_handle = self.driver.window_handles[0]
                print(f"Данные добавлены, id - {org_id}")

                self.driver.switch_to.window(parent_handle)
                sleep(random.uniform(0.2, 0.4))

            except Exception as e:
                print("except", e)
                self._driver_quit()
                sleep(random.uniform(2.2, 2.4))
                headOption = webdriver.FirefoxOptions()
                headOption.headless = True
                driver_path = GeckoDriverManager(path="drivers", version="0.32.2").install()
                self.driver = webdriver.Firefox(
                    executable_path=driver_path, options=headOption
                )
                self.driver.maximize_window()
                self.driver.get("https://yandex.ru/maps")
                parent_handle = self.driver.window_handles[0]

        if len(outputs) > 0:
            self._write_csv(outputs, type_org)
        print("Данные сохранены")
        self._driver_quit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("type_org", help="organization type")
    args = parser.parse_args()
    type_org = args.type_org

    all_hrefs = []
    files = glob.glob(f"links/{type_org}/*.json")
    for file in files:
        with open(file, "r", encoding="utf-8") as f:
            hrefs = json.load(f)["1"]
            all_hrefs += hrefs
    all_hrefs = list(set(all_hrefs))
    print("all_hrefs", len(all_hrefs))

    headOption = webdriver.FirefoxOptions()
    headOption.headless = True
    driver_path = GeckoDriverManager(path="drivers", version="0.32.2").install()
    driver = webdriver.Firefox(executable_path=driver_path, options=headOption)
    parser = Parser(driver)
    parser.parse_data(all_hrefs, type_org)
