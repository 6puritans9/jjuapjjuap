import requests
from bs4 import BeautifulSoup

def get_weekly_dreamtower_meal(weekly):
  url = "https://dorm.kyonggi.ac.kr:446/Khostel/mall_main.php?viewform=B0001_foodboard_list&board_no=1"

  response = requests.get(url)
  print('응답코드: ', response.status_code)
  response.raise_for_status()

  html = response.content.decode('euc-kr')
  soup = BeautifulSoup(html, 'html.parser')

  # 경기드림타워 기숙사 메뉴 스크래핑
  dream_tower = soup.select('table.boxstyle02 > tbody > tr')
  # 일요일, 토요일 제거
  del dream_tower[0]
  del dream_tower[5]
  today_meal = dream_tower[weekly]
  #날짜 정보 가져오기
  if today_meal.select_one('th > a') != None:
    
    date = today_meal.select_one('th > a').text.strip()
    day = date.split()[1]
    date = date.split()[0]
    lunch_html = today_meal.select_one('td:nth-child(3)')
  if lunch_html == None:
    return False;
  # 점심
  if "미운영" in lunch_html.text.strip():
    return False
  lunch = today_meal.select_one('td:nth-child(3)').text.strip()
  # 저녁
  dinner = today_meal.select_one('td:nth-child(4)').text.strip()

  dream_tower_meal = {
    'lunch':lunch,
    'dinner':dinner,
    'date': date,
    'day': day
  }
  return dream_tower_meal

get_weekly_dreamtower_meal(0)