from selenium.webdriver.chrome.webdriver import WebDriver
import allure
import pytest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


@pytest.fixture
#Фикстура открывает браузер и переходит на страницу калькулятора.
def driver():
    driver = webdriver.Chrome()
    driver.get("https://www.kinopoisk.ru/")
    driver.maximize_window()
    WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.CSS_SELECTOR, "[alt='Кинопоиск']")))
    yield driver
    driver.quit()

@allure.title("Тестирование поля ввода")
@allure.description("Ввести пробелы в поле поиска")
def test_spaces(driver):
    with allure.step("Ввод пробелов в поле поиска"):
        driver.find_element(By.CSS_SELECTOR, "input[type='text']").send_keys("  ")
    with allure.step("Инициируем поиск"):
        driver.find_element(By.CSS_SELECTOR, "[data-tid='f49ca51f']").click()
        element = driver.find_element(By.CSS_SELECTOR, "span.search_results_topText")
    with allure.step("Проверка отсутствия результатов поиска"):
        assert element.text == 'поиск: • результаты: 0'

@allure.title("Проверка поиска фильма на английском языке")
@allure.description("Ввести английское название фильма ('Matrix'), инициировать поиск и проверить результат.")
def test_text_in_English(driver):
    with allure.step("Ввод английского названия фильма"):
        driver.find_element(By.CSS_SELECTOR, "input[type='text']").send_keys("Matrix")
    with allure.step("Инициируем поиск"):
        driver.find_element(By.CSS_SELECTOR, "[data-tid='f49ca51f']").click()
    with allure.step("Выбор первого результата поиска"):
        driver.find_element(By.CSS_SELECTOR, "[title='/images/sm_film/301.jpg']").click()
    with allure.step("Проверка названия фильма"):
        movie = driver.find_element(By.CSS_SELECTOR, "h1[itemprop='name']")
    assert movie.text == "Матрица (1999)"


@allure.title("Проверка входа в фильм через Enter")
@allure.description("Ввести название фильма ('Матрица'), отправить Enter и проверить попадание на правильную страницу.")
def test_button_enter(driver):
    with allure.step("Ввод названия фильма"):
        driver.find_element(By.CSS_SELECTOR, "input[type='text']").send_keys("Матрица")
    with allure.step("Отправляем запрос нажав Enter"):
        driver.find_element(By.CSS_SELECTOR, "[data-tid='f49ca51f']").send_keys(Keys.ENTER)
    with allure.step("Выбор первого результата поиска"):
        driver.find_element(By.CSS_SELECTOR, "[title='/images/sm_film/301.jpg']").click()
    with allure.step("Проверка названия фильма"):
        movie = driver.find_element(By.CSS_SELECTOR, "h1[itemprop='name']")
        assert movie.text == "Матрица (1999)"


@allure.title("Просмотр ТВ-каналов без авторизации")
@allure.description("Зайти на страницу каналов и попытаться перейти на 'Первый канал'.")
def test_watching_TV_without_authorization(driver):
    with allure.step("Переход на страницу телеканалов"):
        driver.get("https://hd.kinopoisk.ru/channels")
    with allure.step("Ожидание появления канала 'Первый канал'"):    
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".styles_channel-title__pw7kb[title='Первый канал']")))
    with allure.step("Переход на канал"):
        driver.find_element(By.CSS_SELECTOR, ".styles_channel-title__pw7kb[title='Первый канал']").click()
    with allure.step("Проверка видимости логотипа"):    
        element = driver.find_element(By.CSS_SELECTOR, "[href='https://ya.ru']")
        assert element.is_displayed()


@allure.title("Возврат на главную страницу")
@allure.description("Из раздела кинофильмов вернуться на главную страницу Кинопоиска.")
def test_return_to_main_page(driver):
    with allure.step("Переход на раздел кинотеатров"):
        driver.get("https://www.kinopoisk.ru/lists/movies/movies-in-cinema/")
    with allure.step("Ожидание загрузки страницы"):    
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-test-id='my-tickets-button']")))
    with allure.step("Навигация на главную страницу"):    
        driver.find_element(By.CSS_SELECTOR, "[alt='Кинопоиск']").click()
    with allure.step("Проверка отображения главной страницы"):
        element = driver.find_element(By.CSS_SELECTOR, "[href='/lists/categories/movies/1/']")
        assert element.is_displayed()


@allure.title("Адаптация интерфейса при изменении размера окна")
@allure.description("Уменьшить окно браузера и проверить доступность основных элементов интерфейса.")
def test_interface_adaptability(driver):
    with allure.step("Уменьшить окно браузера до 800x600 пикселей"):
        driver.set_window_size(800,600)
    with allure.step("Проверить видимость логотипа"):
        element = driver.find_element(By.CSS_SELECTOR, "[alt='Кинопоиск']")
        assert element.is_displayed()