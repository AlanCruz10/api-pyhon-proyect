import asyncio
from routes import RoutesFirebase
import datetime
from utilities import format_date_time
from models import FirebaseResponse
from services import HumidityStatisticsService

humidity_one_data_array = []
humidity_two_data_array = []
temperature_data_array = []
light_data_array = []
water_level_array = []
product_key_array = []
first_time = []
last_print_time = datetime.datetime.min


def clear_arrays():
    humidity_one_data_array.clear()
    humidity_two_data_array.clear()
    temperature_data_array.clear()
    light_data_array.clear()
    water_level_array.clear()


async def main():
    global last_print_time
    while True:
        format_time = format_date_time.format_date_now()
        product_key = RoutesFirebase.product_key().get()
        humidity_one = RoutesFirebase.humidity_one().get()
        humidity_two = RoutesFirebase.humidity_two().get()
        light = RoutesFirebase.light().get()
        temperature = RoutesFirebase.temperature().get()
        water_level = RoutesFirebase.water_lever().get()

        product_key_concat = str(product_key), format_time
        humidity_one_concat = str(humidity_one), format_time
        humidity_two_concat = str(humidity_two), format_time
        light_concat = str(light), format_time
        temperature_concat = str(temperature), format_time
        water_level_concat = str(water_level), format_time

        product_key_array.append(product_key_concat)
        humidity_one_data_array.append(humidity_one_concat)
        humidity_two_data_array.append(humidity_two_concat)
        light_data_array.append(light_concat)
        temperature_data_array.append(temperature_concat)
        water_level_array.append(water_level_concat)

        product_key_parameter = str(product_key)
        humidity_below = float(humidity_two)
        humidity_above = float(humidity_one)
        lux = float(light)
        temperature_parameter = float(temperature)
        water_level_parameter = float(water_level)

        parametric = dict(FirebaseResponse.FirebaseResponse(date=format_time,
                                                            humidity_above=humidity_above,
                                                            humidity_below=humidity_below,
                                                            lux=lux,
                                                            temperature=temperature_parameter,
                                                            status="sensor",
                                                            product_key=product_key_parameter))
        RoutesFirebase.sensor().set(parametric)
        for humidity_one_data, humidity_two_data in zip(humidity_one_data_array, humidity_two_data_array):
            humidity_one_data_list = list(humidity_one_data)
            humidity_two_data_list = list(humidity_two_data)
            date_time_one = humidity_one_data_list[-1]
            date_time_one_object = datetime.datetime.strptime(date_time_one, '%d-%m-%Y %H:%M:%S')
            if len(first_time) == 0:
                first_time.append(date_time_one_object)
            else:
                time_difference = date_time_one_object - first_time[0]
                if time_difference.total_seconds() >= 60 and (
                        date_time_one_object - last_print_time).total_seconds() >= 60:
                    last_print_time = date_time_one_object
                    first_time.clear()
                    humidity_statistics_service = HumidityStatisticsService.HumidityStatisticsService(
                        humidity_one_data_array, humidity_two_data_array, light_data_array, temperature_data_array, product_key_array)
                    await humidity_statistics_service.humidity_weighted()
                    clear_arrays()

        await asyncio.sleep(1)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
