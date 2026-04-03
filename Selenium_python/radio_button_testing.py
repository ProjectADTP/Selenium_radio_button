#Импорт модуля time для работы с задержками
import time
# Импорт необходимых модулей Selenium для работы с Chrome
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
# Импорт webdriver-manager для автоматической установки драйвера Chrome последней версии
from webdriver_manager.chrome import ChromeDriverManager


CONFIG = {
    'base_url': 'https://demoqa.com/radio-button',
    'window_size': (1920, 1080),
}


LOCATORS = {
    'radio_button_yes': [
        (By.XPATH,"//input[@id='yesRadio']"),
        'Yes'
    ],
    'radio_button_impressive': [
        (By.XPATH, "//input[@id='impressiveRadio']"),
        'Impressive'
    ],
    'result':
        (By.XPATH, "//span[@class='text-success']"),
}


def get_options(): # Опции драйвера с отключенными разрешениями и уведомлениями
    options = webdriver.ChromeOptions()
    # Не открывать браузер (режим headless)
    options.add_argument("--headless")
    options.add_experimental_option("excludeSwitches", ['enable-automation'])
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-infobars")
    prefs = {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "profile.password_manager_leak_detection": False,
        "profile.default_content_setting_values.notifications": 2,
        "profile.default_content_setting_values.geolocation": 2,
        "profile.default_content_setting_values.media_stream": 2,
        "translate": {"enabled": False},
    }
    options.add_experimental_option("prefs", prefs)
    return options


def select_radio_button(driver, locator, result):
    # Получение radiobutton по локатору
    radio_button = driver.find_element(*locator[0])
    # Нажатие на radiobutton
    radio_button.click()
    time.sleep(1) #Задержка

    # Проверка состояния radiobutton
    check_selected_state(driver, radio_button, result, locator[1])


def check_selected_state(driver, radio_button, result, excepted_result):
    # Проверка что radiobutton нажат
    assert radio_button.is_selected(), 'Radiobutton не выбран'

    # Проверка вывода сообщения о выбранных элементах
    assert driver.find_element(*result).text == excepted_result, f'Сообщение должно вывести {excepted_result}'


def main(): # Основная программа
    driver = None
    try:
        # Получение web драйвера браузера Chrome
        driver = webdriver.Chrome(
            options=get_options(),
            service=ChromeService(ChromeDriverManager().install())
        )
        # Переход на указанную страницу в браузере
        driver.get(CONFIG.get('base_url'))
        # Установка размера окна браузера в разрешение 1920x1080 (FHD)
        driver.set_window_size(*CONFIG.get('window_size'))
        print("Сайт открыт\n")

        # Нажатие на radiobutton Yes
        select_radio_button(driver, LOCATORS.get('radio_button_yes'), LOCATORS.get('result'))
        print("Radiobutton Yes выбран\n")

        # Нажатие на radiobutton Impressive
        select_radio_button(driver, LOCATORS.get('radio_button_impressive'), LOCATORS.get('result'))
        print("Radiobutton Impressive выбран\n")

        print("Проверка Radiobuttons завершена")

    finally:
        if driver:
            time.sleep(1) #Задержка
            driver.quit() # Закрытие браузера
            print("\nСайт закрыт")
        else:
            print("Драйвер отсутсвует")


if __name__ == '__main__':
    main()