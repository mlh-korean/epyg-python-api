from selenium import webdriver
import time

driver = webdriver.Chrome()

def init_sign_in():
    user_id = "xx_pulp"
    user_passwd = "qwerty888!"
    ig_id_name = "username"
    ig_pw_name = "password"
    ig_si_btn_css = ".sqdOP.L3NKy.y3zKF     "
    si_url = "https://instagram.com/accounts/login/"

    driver.get(si_url)
    time.sleep(2)

    ig_id_form = driver.find_element_by_name(ig_id_name)
    ig_id_form.send_keys(user_id)
    time.sleep(1)

    ig_pw_form = driver.find_element_by_name(ig_pw_name)
    ig_pw_form.send_keys(user_passwd)
    time.sleep(1)

    ig_si_btn = driver.find_element_by_css_selector(ig_si_btn_css)
    ig_si_btn.click()
    time.sleep(5)

def image_crawler(tag):
    target_url = "https://www.instagram.com/explore/tags/"+tag
    driver.get(target_url)
    print('url ' + target_url)
    time.sleep(2)

    images = driver.find_elements_by_css_selector(".FFVAD")
    idx = 0
    imageUrl = []
    for image in images:
        imageUrl.append(image.get_attribute("src"))
        idx += 1

    return imageUrl[9:13]

#
# init_sign_in()
# my_list = image_crawler("timessquare")