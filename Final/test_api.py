import requests
import allure


key = 
base_url = "https://kinopoiskapiunofficial.tech"
_headers = {"x-api-key": key}

@allure.title("Поиск фильма")
@allure.description("Поиск фильма по его id")
def test_movie_information():
    headers = _headers
    with allure.step("Указать путь"):
        url = f"{base_url}/api/v2.2/films/301"
    with allure.step("Открыть страницу"):
        response = requests.get(url, headers=headers)
    with allure.step("Проверить статус кода"):
        assert response.status_code == 200
    with allure.step("Проверить название фильма"):
        assert response.json()['nameRu'] == 'Матрица'


@allure.title("Информация о сезонах сериала")
@allure.description("количество сезонов в сериале")
def test_season():
    headers = _headers
    with allure.step("Указать путь"):
        url = f"{base_url}/api/v2.2/films/404900/seasons"
    with allure.step("Открыть страницу"):
        response = requests.get(url, headers=headers)
    with allure.step("Проверить статус кода"):
        assert response.status_code == 200
    with allure.step("Проверить количесво сезонов"):
        assert response.json()['total'] == 5


@allure.title("Факты и ошибки в фильме")
def test_facts():
    headers = _headers
    with allure.step("Указать путь"):
        url = f"{base_url}/api/v2.2/films/301/facts"
    with allure.step("Открыть страницу с фактами и ошибками в фильме"):
        response = requests.get(url, headers=headers)
    with allure.step("Проверить статус кода"):
        assert response.status_code == 200
    with allure.step("Проверить количество фактов и ошибок в фильме"):
        assert response.json()['total'] == 67


@allure.title("Поиск несуществуещего фильма")
@allure.description("Ввести id несуществующего фильма")
def test_non_existent_film():
    headers = _headers
    with allure.step("Указать путь"):
        url = f"{base_url}/api/v2.2/films/901453"
    with allure.step("Открыть страницу"):
        response = requests.get(url, headers=headers)
    with allure.step("Проверить статус кода"):    
        assert response.status_code == 404


@allure.title("Изменить метод")
@allure.description("Измениить метод Get на Post")
def test_change_method():
    headers = _headers
    with allure.step("Указать путь"):  
        url = f"{base_url}/api/v2.2/films/301"
    with allure.step("Изменить метод"):  
        response = requests.post(url, headers=headers)
    with allure.step("Проверить статус кода"):      
        assert response.status_code == 500    


@allure.title("Поиск без ключа")
def test_request_without_key():
    headers = {"x-api-key":""}
    with allure.step("Указать путь"):  
        url = f"{base_url}/api/v2.2/films/301"
    with allure.step("открыть страницу не указывая ключ"):  
        response = requests.get(url, headers=headers)
    with allure.step("Проверить статус кода"):     
        assert response.status_code == 401
