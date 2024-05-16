from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time


def display_paragraphs(browser):
    paragraph_index = 0
    paragraphs = browser.find_elements(By.CSS_SELECTOR, "p")
    while paragraph_index < len(paragraphs):
        print(f"Paragraph {paragraph_index + 1}: {paragraphs[paragraph_index].text}")
        cont = input("Листать дальше? (да/нет): ").strip().lower()
        if cont != 'да':
            break
        paragraph_index += 1


def list_internal_links(browser):
    links = browser.find_elements(By.CSS_SELECTOR, "a[href^='/wiki/']")
    internal_links = []
    for link in links:
        href = link.get_attribute('href')
        text = link.text
        if href and text:
            internal_links.append(link)
    for i, link in enumerate(internal_links, start=1):
        print(f"{i}. {link.text} ({link.get_attribute('href')})")
    return internal_links


def navigate_wikipedia(browser):
    while True:
        print("\nВыберите действие:")
        print("1. Листать параграфы текущей статьи")
        print("2. Перейти на одну из связанных страниц")
        print("3. Выйти из программы")

        choice = input("Введите номер действия: ").strip()

        if choice == '1':
            display_paragraphs(browser)
        elif choice == '2':
            links = list_internal_links(browser)
            choice = int(input("Введите номер статьи для перехода: ").strip())
            if 1 <= choice <= len(links):
                links[choice - 1].click()
                time.sleep(3)
                navigate_wikipedia(browser)
            else:
                print("Неверный выбор. Попробуйте снова.")
        elif choice == '3':
            print("Выход из программы.")
            break
        else:
            print("Неверный выбор. Попробуйте снова.")


def search_wikipedia(query):
    # Открываем браузер Firefox
    browser = webdriver.Firefox()
    try:
        browser.get("https://www.wikipedia.org/")
        search_box = browser.find_element(By.ID, "searchInput")
        search_box.send_keys(query)
        search_box.send_keys(Keys.RETURN)

        time.sleep(3)

        # Проверка на наличие результатов поиска
        if "search" in browser.current_url:
            search_results = browser.find_elements(By.CSS_SELECTOR, ".mw-search-result-heading a")

            if search_results:
                print("Результаты поиска:")
                for i, result in enumerate(search_results, start=1):
                    print(f"{i}. {result.text}")

                choice = int(input("Введите номер статьи, на которую хотите перейти: ").strip())
                if 1 <= choice <= len(search_results):
                    search_results[choice - 1].click()
                    time.sleep(3)
                    navigate_wikipedia(browser)
                else:
                    print("Неверный выбор номера статьи.")
            else:
                print("По вашему запросу ничего не найдено.")
        else:
            # Если мы уже на странице статьи, сразу начинаем навигацию
            navigate_wikipedia(browser)
    finally:
        browser.quit()


if __name__ == "__main__":
    query = input("Что вы хотите найти в Википедии? ")
    search_wikipedia(query)
