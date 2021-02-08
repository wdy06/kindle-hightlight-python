from selenium.webdriver import Chrome, ChromeOptions, Remote
from selenium.webdriver.common.keys import Keys
import time
from getpass import getpass
import json


def get_annotations(driver):
    highlight_list = []
    annotations = driver.find_element_by_id("kp-notebook-annotations")
    for highlight in annotations.find_elements_by_id("highlight"):
        highlight_list.append(highlight.text)
    return highlight_list


def main():

    AMAZON_EMAIL = input("your email address:")
    AMAZON_PASSWORD = getpass("your password:")
    BASE_URL = "https://read.amazon.co.jp/kp/notebook"

    options = ChromeOptions()
    # options.add_argument("--headless")
    options.add_experimental_option("prefs", {"intl.accept_languages": "ja"})
    driver = Chrome(options=options, executable_path="xxxxxxx")
    driver.get(BASE_URL)

    # name="signIn" というサインインフォームを埋める。
    # フォームのname属性の値はブラウザーの開発者ツールで確認できる。
    time.sleep(2)
    email_input = driver.find_element_by_name("email")
    email_input.send_keys(AMAZON_EMAIL)  # name="email" という入力ボックスを埋める。
    # email_input.send_keys(Keys.RETURN)
    # time.sleep(2)
    password_input = driver.find_element_by_name("password")
    password_input.send_keys(AMAZON_PASSWORD)  # name="password" という入力ボックスを埋める。
    time.sleep(2)
    # フォームを送信する。
    # logging.info('Signing in...')
    password_input.send_keys(Keys.RETURN)
    while True:
        print("waiting for login...")
        time.sleep(5)
        if driver.title == "Kindle: メモとハイライト":

            notebook_library = driver.find_element_by_id("kp-notebook-library")

            result = []
            for book in notebook_library.find_elements_by_class_name(
                "kp-notebook-library-each-book"
            ):
                book_info = {}
                book.click()
                time.sleep(5)
                #     print(book.id)
                print(book.text)
                book_info["title"] = book.text
                book_info["highlights"] = get_annotations(driver)
                print(book_info)
                result.append(book_info)
                print("----")

            with open("highlights.json", "w") as f:
                json.dump(result, f)
            break


if __name__ == "__main__":
    main()
