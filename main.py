from gc import disable
from operator import ne
import time
from selenium import webdriver
from selenium.webdriver.common.by import By

from utils.frame_switch import switch_left

options = webdriver.ChromeOptions()
options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3')
options.add_argument('window-size=1380,900')
driver = webdriver.Chrome(options=options)

driver.implicitly_wait(time_to_wait=3)
URL = "https://map.naver.com/p/search/%EC%9D%B4%EB%B0%B1%EC%9E%A5%EB%8F%88%EA%B9%8C%EC%8A%A4"
driver.get(URL)

switch_left(driver)

collected_names = []

while True:
    scroll_container = driver.find_element(By.ID, "_pcmap_list_scroll_container")
    prev_height = driver.execute_script("return arguments[0].scrollHeight", scroll_container)

    while True:
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scroll_container)
        time.sleep(1)
        new_height = driver.execute_script("return arguments[0].scrollHeight", scroll_container)
        
        if new_height == prev_height:
            break
        prev_height = new_height

    elements = driver.find_elements(By.CSS_SELECTOR, "li.UEzoS.rTjJo span.TYaxT")
    current_names = [el.text for el in elements]
    
    for name in current_names:
        if name not in collected_names:
            collected_names.append(name)
    
    print(f"현재까지 {len(collected_names)}개의 이름 수집 완료")

    try:
        list_buttons = driver.find_elements(By.CSS_SELECTOR, "div.zRM9F a[target='_self']")
        
        if not list_buttons:
            print("더보기 버튼을 찾을 수 없음.")
            break
        
        next_list_button = list_buttons[-1]
        disabled = next_list_button.get_attribute("aria-disabled")
        print("disabled:", disabled)
        
        if disabled == "true":
            print("마지막 페이지입니다.")
            break
        else:
            next_list_button.click()
            time.sleep(1)
    
    except Exception as e:
        print("get error while finding next button:", e)
        break

for idx, name in enumerate(collected_names):
    print(f"{idx+1}. {name}")

driver.quit()