import time
from urllib.parse import quote
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils.frame_switch import switch_left, switch_right

options = webdriver.ChromeOptions()
options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3')
options.add_argument('window-size=1380,900')
driver = webdriver.Chrome(options=options)

driver.implicitly_wait(time_to_wait=3)

search_term = "이백장돈까스"
encoded_term = quote(search_term)
URL = f"https://map.naver.com/v5/search/{encoded_term}"

driver.get(URL)

switch_left(driver)

collected_names = []

while True:
    scroll_container = driver.find_element(By.ID, "_pcmap_list_scroll_container")
    prev_height = driver.execute_script("return arguments[0].scrollHeight", scroll_container)
    
    # Scroll to the bottom of the list
    while True:
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scroll_container)
        time.sleep(0.5)
        new_height = driver.execute_script("return arguments[0].scrollHeight", scroll_container)
        
        if new_height == prev_height:
            break
        prev_height = new_height

    name_elements = driver.find_elements(By.CSS_SELECTOR, "li.UEzoS.rTjJo span.TYaxT")
    current_names = [name.text for name in name_elements]
    
    for name in current_names:
        if name not in collected_names:
            collected_names.append(name)
            
    side_bar_button_elements = driver.find_elements(By.CSS_SELECTOR, "li.UEzoS.rTjJo a.tzwk0")
    side_bar_buttons = [button for button in side_bar_button_elements]
    
    for button in side_bar_buttons:
        button.click()
        
        switch_right(driver)
        
        menu_links = driver.find_elements(By.CSS_SELECTOR, "a.tpj9w._tab-menu")
        for link in menu_links:
            try:
                span = link.find_element(By.CSS_SELECTOR, "span.veBoZ")
                if span.text.strip() == "메뉴":
                    link.click()
                    
                    more_menu_button = driver.find_element(By.CSS_SELECTOR, "a.fvwqf")
                    more_menu_button.click()
                    
                    break
            except Exception as e:
                print("예외 발생:", e)
                continue
        
        time.sleep(1)
        
        switch_left(driver)

    try:
        list_buttons = driver.find_elements(By.CSS_SELECTOR, "div.zRM9F a[target='_self']")
        
        if not list_buttons:
            raise Exception("No list buttons found.")
        
        next_list_button = list_buttons[-1]
        disabled = next_list_button.get_attribute("aria-disabled")
        
        if disabled == "true":
            break
        else:
            next_list_button.click()
            time.sleep(0.5)
    
    except Exception as e:
        print("get error while finding next button:", e)
        break

for idx, name in enumerate(collected_names):
    print(f"{idx+1}. {name}")

driver.quit()