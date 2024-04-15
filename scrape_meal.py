import requests
from bs4 import BeautifulSoup


def parse_meal(lunch, dinner) -> dict:
    lunch_list = []  # 0: 밥, 1: 국, 2/3: 메인 반찬, 4/5: 채소 반찬, 6: 음료
    dinner_list = []
    meal = {"lunch": lunch_list, "dinner": dinner_list}
    for item in lunch.split("\r\n"):
        lunch_list.append(item.strip())
    for item in dinner.split("\r\n"):
        dinner_list.append(item.strip())

    lunch_list[0] = f":rice_ball:{lunch_list[0]}"
    lunch_list[1] = f"      {lunch_list[1]}:k_soup:"
    lunch_list[2] = f":pig:{lunch_list[2]}"
    lunch_list[3] = f"      {lunch_list[3]}"
    lunch_list[4] = f"      {lunch_list[4]}:leafy_green:"
    lunch_list[5] = f"      {lunch_list[5]}"
    lunch_list[6] = f"      {lunch_list[6]}:glass_of_milk:"

    dinner_list[0] = f":rice:{dinner_list[0]}"
    dinner_list[1] = f"      {dinner_list[1]}:k_soup:"
    dinner_list[2] = f":cow:{dinner_list[2]}"
    dinner_list[3] = f"      {dinner_list[3]}"
    dinner_list[4] = f"      {dinner_list[4]}:carrot:"
    dinner_list[5] = f"      {dinner_list[5]}"
    dinner_list[6] = f"      {dinner_list[6]}:bubble_tea:"

    return meal


def get_weekly_dreamtower_meal(weekly):
    url = "https://dorm.kyonggi.ac.kr:446/Khostel/mall_main.php?viewform=B0001_foodboard_list&gyear=2024&gmonth=04&gday=07"

    response = requests.get(url)
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
    meal = parse_meal(lunch, dinner)

    dream_tower_meal = {
        "lunch": meal["lunch"],
        "dinner": meal["dinner"],
        "date": date,
        "day": day,
    }
    return dream_tower_meal


get_weekly_dreamtower_meal(0)
