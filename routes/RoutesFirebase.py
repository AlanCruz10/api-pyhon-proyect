from enum import Enum
from firebase_admin import db
from connections import firebase_connection

firebase_connection.firebase()


class RoutesFirebase(Enum):
    humidity_one = '/amili/esp32/humidity1'
    humidity_two = '/amili/esp32/humidity2'
    sensor = '/amili/sensor/real-time'
    temperature = '/amili/esp32/temperature'
    light = '/amili/esp32/light'
    water_level = '/amili/esp32/water-level'
    statistics_humidity = "/amili/statistics/humidity"


def humidity_one():
    return db.reference(RoutesFirebase.humidity_one.value)


def humidity_two():
    return db.reference(RoutesFirebase.humidity_two.value)


def sensor():
    return db.reference(RoutesFirebase.sensor.value)


def temperature():
    return db.reference(RoutesFirebase.temperature.value)


def light():
    return db.reference(RoutesFirebase.light.value)


def water_lever():
    return db.reference(RoutesFirebase.water_level.value)


def statistic_humidity():
    return db.reference(RoutesFirebase.statistics_humidity.value)
