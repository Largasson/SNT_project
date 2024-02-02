import typing
import requests
from flask import current_app
from logging import basicConfig, info, INFO

basicConfig(filename='weather_log.log', level=INFO, format="%(asctime)s %(levelname)s %(message)s")


class Forecast(typing.NamedTuple):
    today: dict
    tomorrow: dict
    weekend: dict


class Conditions(typing.NamedTuple):
    today: str
    tomorrow: str
    weekend: str


# Словарь с переводами состояний погоды
weather_translations = {
    "clear": "ясно",
    "partly-cloudy": "малооблачно",
    "cloudy": "облачно с прояснениями",
    "overcast": "пасмурно",
    "light-rain": "небольшой дождь",
    "rain": "дождь",
    "heavy-rain": "сильный дождь",
    "showers": "ливень",
    "wet-snow": "дождь со снегом",
    "light-snow": "небольшой снег",
    "snow": "снег",
    "snow-showers": "снегопад",
    "hail": "град",
    "thunderstorm": "гроза",
    "thunderstorm-with-rain": "дождь с грозой",
    "thunderstorm-with-hail": "гроза с градом"
}


def translate_weather_condition(condition):
    """ Функция, отвечающая за перевод состояния погоды с английского на русский """
    return weather_translations.get(condition, condition)


def get_weather():
    """ Функция, отвечающая за получение данных с сервиса погоды """
    base_url = current_app.config['WEATHER_URL']
    headers = {
        "X-Yandex-API-Key": current_app.config['WEATHER_API_KEY']
    }

    params = {
        "lat": current_app.config['LATITUDE'],
        "lon": current_app.config['LONGITUDE'],
        "extra": "true",
        "lang": "ru_RU"
    }

    try:
        response = requests.get(base_url, headers=headers, params=params)
        weather_data = response.json()
        try:
            today = weather_data["forecasts"][0]["parts"]["day"]
            tomorrow = weather_data["forecasts"][1]["parts"]["day"]
            weekend = weather_data["forecasts"][2]["parts"]["day"]
            forecasts = Forecast(today, tomorrow, weekend)
            conditions = Conditions(
                translate_weather_condition(today['condition']).capitalize(),
                translate_weather_condition(tomorrow['condition']).capitalize(),
                translate_weather_condition(weekend['condition']).capitalize()
            )
            return forecasts, conditions
        except (KeyError, IndexError, TypeError) as err:
            info(f'Ошибка при обращении к json-файлу сервиса погоды. Ошибка связана с {err}')
            return False
    except requests.RequestException as err:
        info(f'Сетевая ошибка при получении данных о погоде. Код ошибки: - {err}')
        return False


if __name__ == "__main__":
    get_weather()
