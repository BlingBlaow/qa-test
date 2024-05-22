import requests
import pytest
from test_data import reserse_geocoding_data

# Строка User-Agent
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"

# Устанавливаем базовые URL для API Nominatim
BASE_URL_REVERSE = "https://nominatim.openstreetmap.org/reverse"


class TestReverseNominatimGeocoding:

    @pytest.mark.parametrize(
        "lat, lon, expected_address_fragment", reserse_geocoding_data
    )
    def test_reverse_geocoding(self, lat, lon, expected_address_fragment):
        params = {"lat": lat, "lon": lon, "format": "json"}
        headers = {"User-Agent": USER_AGENT}

        # Выполняем GET-запрос к API Nominatim для поиска адреса
        response = requests.get(BASE_URL_REVERSE, params=params, headers=headers)

        # Преобразуем ответ в JSON формат
        data = response.json()

        # Проверяем статус код ответа
        assert response.status_code == 200

        # Проверяем что в ответе есть поле address
        assert "address" in data, "Данные не найдены"

        # Извлекаем страну из результата
        address = data["address"]
        assert "country" in address, "Поле 'country' не найдено в 'address'"

        # Извлекаем Страну и координаты из результата
        country = address["country"]
        lat = data["lat"]
        lon = data["lon"]

        # Выводим результат
        print(f"Name: {country}, Latitude: {lat}, Longitude: {lon}")

        # Преобразуем в строку данные для удобства проверки
        values = [v for k, v in address.items()]
        address_str = " ,".join(values)

        # Проверям что предполагаемый адрес содержится в строке адреса
        assert (
            expected_address_fragment in address_str
        ), f"Данный адрес не найден для {lat}, {lon}"


if __name__ == "__main__":
    pytest.main()  # Запуск тестов с использованием pytest
