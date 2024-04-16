import requests
import random
from bs4 import BeautifulSoup
from enum import Enum

CONSTANTS = {
    "INDENT": "      ",
    "EMOJIS": {
        "RICE": [":rice_ball:", ":rice:", ":ramen:", ":curry:", ":spaghetti:"],
        "SOUP": [":k_soup:"],
        "MAIN": [":pig:", ":cow:", ":chicken:", ":fried_shrimp:", ":poultry_leg:"],
        "VEGE": [":leafy_green:", ":carrot:", ":potato:", ":mushroom:"],
        "DRINK": [
            ":glass_of_milk:",
            ":bubble_tea:",
            ":beverage_box:",
        ],
    },
}


class Dish(Enum):
    RICE = (0,)
    SOUP = (1,)
    MAIN = (2, 3)
    VEGE = (4, 5)
    DRINK = (6,)


def get_emoji(idx):
    name = ""
    for element in Dish:
        if idx in element.value:
            name = element.name

    r = random.randint(0, 9)
    emojis = CONSTANTS["EMOJIS"][name]
    return emojis[r % len(emojis)]


def parse(lunch, dinner):
    lunch_list = [item.strip() for item in lunch.split("\r\n")]
    dinner_list = [item.strip() for item in dinner.split("\r\n")]
    meal_list = [lunch_list, dinner_list]

    for meal in meal_list:
        for idx, item in enumerate(meal):
            emoji = get_emoji(idx)

            if not idx in (0, 2):
                item = CONSTANTS["INDENT"] + item

            if idx == 3 or idx == 5:
                meal[idx] = item
            elif idx in Dish.RICE.value:
                meal[idx] = emoji + item
            elif idx in Dish.MAIN.value:
                meal[idx] = emoji + item
            elif idx in Dish.VEGE.value:
                meal[idx] = item + emoji
            else:
                meal[idx] = item + emoji

    return {"lunch": meal_list[0], "dinner": meal_list[1]}


def concat(parsed):
    lunch_result = ""
    dinner_result = ""

    for element in parsed["lunch"]:
        lunch_result += f"{element}\n"
    for element in parsed["dinner"]:
        dinner_result += f"{element}\n"

    return {"lunch": lunch_result, "dinner": dinner_result}


def get_weekly_dreamtower_meal(weekly):
    URL = "https://dorm.kyonggi.ac.kr:446/Khostel/mall_main.php?viewform=B0001_foodboard_list&board_no=1"

    response = requests.get(URL)
    print("응답코드: ", response.status_code)
    response.raise_for_status()

    html = response.content.decode("euc-kr")
    soup = BeautifulSoup(html, "html.parser")

    # 경기드림타워 기숙사 메뉴 스크래핑
    dream_tower = soup.select("table.boxstyle02 > tbody > tr")
    # 일요일, 토요일 제거
    del dream_tower[0]
    del dream_tower[5]
    today_meal = dream_tower[weekly]
    # 날짜 정보 가져오기
    if today_meal.select_one("th > a") != None:

        date = today_meal.select_one("th > a").text.strip()
        day = date.split()[1]
        date = date.split()[0]
        lunch_html = today_meal.select_one("td:nth-child(3)")
    if lunch_html == None:
        return False
    # 점심
    if "미운영" in lunch_html.text.strip():
        return False
    lunch = today_meal.select_one("td:nth-child(3)").text.strip()
    # 저녁
    dinner = today_meal.select_one("td:nth-child(4)").text.strip()
    meal_parsed = parse(lunch, dinner)
    meal_concat = concat(meal_parsed)

    dream_tower_meal = {
        "lunch": meal_concat["lunch"],
        "dinner": meal_concat["dinner"],
        "date": date,
        "day": day,
    }
    return dream_tower_meal
