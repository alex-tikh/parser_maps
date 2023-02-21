from bs4 import BeautifulSoup
from selenium.common.exceptions import (
    NoSuchElementException,
    MoveTargetOutOfBoundsException,
)
from selenium.webdriver import ActionChains

import json


class SoupContentParser:
    def get_name(self, soup_content):
        try:
            name = soup_content.find(
                "h1", {"class": "orgpage-header-view__header"}
            ).getText()
            return name
        except Exception:
            pass
        try:
            name = soup_content.find(
                "h1", {"class": "card-title-view__title"}
            ).getText()
            return name
        except Exception:
            return ""

    def get_phone(self, soup_content):
        try:
            content = soup_content.find("script", {"class": "state-view"}).contents[0]
            content_dict = json.loads(content)
            phones = []
            for dict_phone in content_dict["stack"][0]["results"]["items"][0]["phones"]:
                try:
                    phones.append(
                        dict_phone["number"].replace(" ", "")
                        + " {"
                        + dict_phone["info"]
                        + "}"
                    )
                except Exception:
                    try:
                        phones.append(dict_phone["number"].replace(" ", ""))
                    except Exception:
                        pass

            return ", ".join(phones)
        except Exception:
            return ""

    def get_coordinates(self, soup_content):
        try:
            content = soup_content.find("script", {"class": "state-view"}).contents[0]
            content_dict = json.loads(content)
            coordinates = content_dict["stack"][0]["results"]["items"][0]["coordinates"]
            return coordinates
        except Exception:
            return []

    def get_social(self, soup_content):
        try:
            socials = []
            for data in soup_content.find_all(
                "a", {"class": "button _view_secondary-gray _ui _size_medium _link"}
            ):
                social = data["href"]
                socials.append(social)
            return ", ".join(socials)
        except Exception:
            return ""

    def get_address(self, soup_content):
        try:
            address = soup_content.find(
                "a", {"class": "business-contacts-view__address-link"}
            ).getText()
            return address
        except Exception:
            return ""

    def get_website(self, soup_content):
        try:
            website = soup_content.find(
                "span", {"class": "business-urls-view__text"}
            ).getText()
            return website
        except Exception:
            return ""

    def get_opening_hours(self, soup_content):
        opening_hours = []
        try:
            for data in soup_content.find_all("meta", {"itemprop": "openingHours"}):
                opening_hours.append(data.get("content"))
            return opening_hours
        except Exception:
            return ""

    def get_goods(self, soup_content):
        dishes = []
        prices = []
        try:
            for dish_s in soup_content.find_all(
                "div", {"class": "related-item-photo-view__title"}
            ):
                dishes.append(dish_s.getText())

            for price_s in soup_content.find_all(
                "span", {"class": "related-product-view__price"}
            ):
                prices.append(price_s.getText())

            for dish_l in soup_content.find_all(
                "div", {"class": "related-item-list-view__title"}
            ):
                dishes.append(dish_l.getText())

            for price_l in soup_content.find_all(
                "div", {"class": "related-item-list-view__price"}
            ):
                prices.append(price_l.getText())

        except NoSuchElementException:
            try:
                for dish_l in soup_content.find_all(
                    "div", {"class": "related-item-list-view__title"}
                ):
                    dishes.append(dish_l.getText())

                for price_l in soup_content.find_all(
                    "div", {"class": "related-item-list-view__price"}
                ):
                    prices.append(price_l.getText())
            except Exception:
                pass
        except Exception:
            return ""

        return dict(zip(dishes, prices))

    def get_rating(self, soup_content):
        rating = ""
        try:
            for data in soup_content.find_all(
                "span", {"class": "business-summary-rating-badge-view__rating-text"}
            ):
                rating += data.getText()
            return rating
        except Exception:
            return ""

    def get_review_number(self, soup_content):
        try:
            n_reviews = soup_content.find(
                "div", {"class": "business-header-rating-view__text"}
            ).getText()
            return n_reviews
        except Exception:
            pass
        try:
            n_reviews = soup_content.find(
                "div", {"class": "business-header-rating-view__text _clickable"}
            ).getText()
            return n_reviews
        except Exception:
            return ""

    def get_reviews(self, soup_content, driver):
        reviews = []
        slider = driver.find_element_by_class_name(name="scroll__scrollbar-thumb")
        try:
            reviews_count = int(
                soup_content.find_all("div", {"class": "tabs-select-view__counter"})[
                    -1
                ].text
            )
        except ValueError:
            reviews_count = 0
        except AttributeError:
            reviews_count = 0
        except Exception:
            return ""

        if reviews_count > 150:
            find_range = range(100)
        else:
            find_range = range(30)

        for i in find_range:
            try:
                ActionChains(driver).click_and_hold(slider).move_by_offset(
                    0, 50
                ).release().perform()

            except MoveTargetOutOfBoundsException:
                break

        try:
            soup_content = BeautifulSoup(driver.page_source, "lxml")
            for data in soup_content.find_all(
                "div", {"class": "business-review-view__body-text _collapsed"}
            ):
                reviews.append(data.getText())

            return reviews
        except Exception:
            return ""

    def get_transport_stops(self, soup_content):
        content = soup_content.find("script", {"class": "state-view"}).contents[0]
        content_dict = json.loads(content)
        try:
            res = ""
            for metro_dict in content_dict["stack"][0]["results"]["items"][0]["metro"]:
                res += (
                    "метро "
                    + metro_dict["name"]
                    + " ("
                    + metro_dict["distance"]
                    + ")\n"
                )

            for stop_dict in content_dict["stack"][0]["results"]["items"][0]["stops"]:
                res += (
                    "остановка "
                    + stop_dict["name"]
                    + " ("
                    + stop_dict["distance"]
                    + ")\n"
                )
            return res
        except Exception:
            pass

        try:
            res = ""
            for metro_dict in content_dict["stack"][0]["stops"]["data"]["searchResult"][
                "metro"
            ]:
                res += (
                    "метро "
                    + metro_dict["name"]
                    + " ("
                    + metro_dict["distance"]
                    + ")\n"
                )

            for stop_dict in content_dict["stack"][0]["stops"]["data"]["searchResult"][
                "stops"
            ]:
                res += (
                    "остановка "
                    + stop_dict["name"]
                    + " ("
                    + stop_dict["distance"]
                    + ")\n"
                )

            return res
        except Exception:
            return ""

    def get_tags(self, soup_content):
        try:
            tags = []
            for data in soup_content.find_all(
                    "a", {"class": "orgpage-categories-info-view__link"}
            ):
                tags.append(data["aria-label"])

            return ", ".join(tags)
        except Exception:
            return ""

    def get_city(self, soup_content):
        try:
            data = soup_content.find_all(
                "a", {"class": "breadcrumbs-view__breadcrumb _outline"}
            )[1]

            return data["aria-label"]
        except Exception:
            return ""

    def get_category(self, soup_content):
        try:
            data = soup_content.find_all(
                "a", {"class": "breadcrumbs-view__breadcrumb _outline"}
            )[2]

            return data["aria-label"]
        except Exception:
            return ""
