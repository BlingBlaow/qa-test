import pytest
import requests
from test_data import forward_geocoding_data

# Строка User-Agent
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"

# Устанавливаем базовые URL для API Nominatim
BASE_URL_SEARCH = "https://nominatim.openstreetmap.org/search"

class TestSearchNominatimGeocoding:

    @pytest.mark.parametrize(
        "address, expected_lat, expected_lon", forward_geocoding_data
    )
    def test_forward_geocoding(self, address, expected_lat, expected_lon):
        # Параметры запроса для прямого геокодирования
        params = {
            "q": address,  # Адрес для поиска
            "format": "json",  # Формат ответа - JSON
        }
        # Заголовок User-Agent
        headers = {"User-Agent": USER_AGENT}
        # Выполняем GET-запрос к API Nominatim для поиска адреса
        response = requests.get(BASE_URL_SEARCH, params=params, headers=headers)

        # Проверяем статус код ответа
        assert (
            response.status_code == 200
        ), f"Не удалось получить данные для {address}. Статус код: {response.status_code}"

        # Преобразуем ответ в JSON формат
        data = response.json()

        # Проверяем, что результат не пустой
        assert len(data) > 0, "Результаты для данного адреса не найдены."

        # Берем первый результат из ответа
        result = data[0]

        # Извлекаем имя и координаты из результата
        name = result["name"]
        lat = result["lat"]
        lon = result["lon"]

        # Выводим результат
        print(f"Name: {name}, Latitude: {lat}, Longitude: {lon}")

        # Проверяем, что полученные координаты соответствуют ожидаемым (с точностью до 2 знаков после запятой)
        assert (
            abs(float(lat) - float(expected_lat)) < 1e-2
        ), f"Несоответствие широты для {address}"
        assert (
            abs(float(lon) - float(expected_lon)) < 1e-2
        ), f"Несоответствие долготы для {address}"


if __name__ == "__main__":
    pytest.main()  # Запуск тестов с использованием pytest
