import os

import pytest
from bs4 import BeautifulSoup

from soup_parser import SoupContentParser


@pytest.fixture(scope="session")
def soup():
    with open(os.path.dirname(__file__)+'/test_file.html', 'r') as f:
        soup = BeautifulSoup(f.read(), 'lxml')
    return soup


@pytest.fixture(scope="session")
def soup_parser():
    soup_parser = SoupContentParser()
    return soup_parser


def test_soup_get_name(soup, soup_parser):
    name = soup_parser.get_name(soup)
    assert name == "Aroma"


def test_soup_get_address(soup, soup_parser):
    address = soup_parser.get_address(soup)
    assert address == "Ленинградский просп., 39, стр. 80, Москва"


def test_soup_get_website(soup, soup_parser):
    website = soup_parser.get_website(soup)
    assert website == "aromamoscow.com"


def test_soup_get_opening_hours(soup, soup_parser):
    opening_hours = soup_parser.get_opening_hours(soup)
    assert opening_hours == [
        'Mo 08:00-23:00',
        'Tu 08:00-23:00',
        'We 08:00-23:00',
        'Th 08:00-23:00',
        'Fr 08:00-23:00',
        'Sa 08:00-23:00',
        'Su 08:00-23:00'
    ]


def test_soup_get_rating(soup, soup_parser):
    rating = soup_parser.get_rating(soup)
    assert rating == "4,1"


def test_soup_get_phone(soup, soup_parser):
    phone = soup_parser.get_phone(soup)
    assert phone == (
        "+7(926)988-09-23 {Номер ресторана}, "
        "+7(918)607-95-20 {Менеджер-  Мария }, "
        "+7(916)215-99-97 {Управляющий ресторана- Богдан}"
    )


def test_soup_get_review_number(soup, soup_parser):
    review_number = soup_parser.get_review_number(soup)
    assert review_number == "96 отзывов"


def test_soup_get_transport_stops(soup, soup_parser):
    transport_stops = soup_parser.get_transport_stops(soup)
    assert transport_stops == (
        "метро Аэропорт (630\xa0м)\nметро ЦСКА (1,58\xa0км)\n"
        "метро Петровский парк (1,63\xa0км)\n"
        "остановка Улица Константина Симонова (224\xa0м)\n"
        "остановка Метро Аэропорт (южный вестибюль) (660\xa0м)\n"
        "остановка Улица Серёгина (690\xa0м)\n"
        "остановка Старый Зыковский проезд (830\xa0м)\n"
        "остановка Путевой дворец (930\xa0м)\n"
    )


def test_soup_get_coordinates(soup, soup_parser):
    coordinates = soup_parser.get_coordinates(soup)
    assert coordinates == [37.536931, 55.796567]


def test_soup_get_tags(soup, soup_parser):
    tags = soup_parser.get_tags(soup)
    assert tags == "Кафе, доставка еды и обедов, кофейня"
