from models import FirebaseResponseAfterFive
from entities import User, Parametric, Statistic
from routes import RoutesFirebase
from configurations import configuration_database


class HumidityStatisticsService:

    def __init__(self, humidity_one_percentage, humidity_two_percentage, light, temperature, ):
        self.humidity_one = humidity_one_percentage
        self.humidity_two = humidity_two_percentage
        self.light = light
        self.temperature = temperature
        self.lower_humidity_standard = 80.0
        self.higher_humidity_standard = 90.0
        self.lower_temperature_standard = 20.0
        self.higher_temperature_standard = 25.0
        self.lower_light_standard = 50.0
        self.higher_light_standard = 60.0
        self.higher_moisture_priority = 0.6
        self.lower_moisture_priority = 0.4

    async def humidity_weighted(self):

        humidity1 = list(self.humidity_one[-1])[0]
        humidity2 = list(self.humidity_two[-1])[0]
        temperature = list(self.temperature[-1])[0]
        light = list(self.light[-1])[0]

        date1 = list(self.humidity_one[-1])[-1]

        humidity_one = (self.higher_moisture_priority * float(humidity1)) / 100
        humidity_two = (self.lower_moisture_priority * float(humidity2)) / 100

        if 0 <= humidity_one + humidity_two <= 1:
            humidity_w = (humidity_one + humidity_two) * 100
            status = self.validation_standard(humidity_w, temperature, light)
            user, parameter, statistic, database = configuration_database.create_tables()
            await database.connect()
            product_key = "1234qwer"
            select = user.select().where(user.c.product_key == product_key)
            user_found = await database.fetch_one(query=select)
            if user_found:
                model_user = User.User(**dict(user_found))
                add_parameter = parameter.insert().values(date=date1,
                                                          humidity_above=humidity1,
                                                          humidity_below=humidity2,
                                                          lux=light,
                                                          temperature=temperature,
                                                          status=status,
                                                          user_id=model_user.id)
                id_parameter_added = await database.execute(add_parameter)
                add_statistic = statistic.insert().values(median=humidity_w, parameter_id=id_parameter_added)
                id_statistic_added = await database.execute(add_statistic)
                find_parameter = parameter.select().where(parameter.c.id == id_statistic_added)
                parameter_found = await database.fetch_one(query=find_parameter)
                model_parameter = Parametric.Parametric(**dict(parameter_found))
                update_parameter = parameter.update().where(parameter.c.id == model_parameter.id).values(
                    id=model_parameter.id,
                    date=model_parameter.date,
                    humidity_above=model_parameter.humidity_above,
                    humidity_below=model_parameter.humidity_below,
                    lux=model_parameter.lux,
                    temperature=model_parameter.temperature,
                    status=model_parameter.status,
                    user_id=model_parameter.user_id,
                    statistic_id=id_statistic_added)
                await database.execute(update_parameter)
                parameter_select = parameter.select().where(parameter.c.id == model_parameter.id)
                parameter_entity = await database.fetch_one(query=parameter_select)
                model_parametric = Parametric.Parametric(**dict(parameter_entity))
                user_select = user.select().where(user.c.id == model_parametric.user_id)
                user_entity = await database.fetch_one(query=user_select)
                model_user = User.User(**dict(user_entity))
                statistic_select = statistic.select().where(statistic.c.parameter_id == model_parametric.id)
                statistic_entity = await database.fetch_one(query=statistic_select)
                model_statistic = Statistic.Statistic(**dict(statistic_entity))
                firebase_data_response = dict(
                    FirebaseResponseAfterFive.FirebaseData(id=model_parametric.id,
                                                           date=model_parametric.date,
                                                           humidity_above=model_parametric.humidity_above,
                                                           humidity_below=model_parametric.humidity_below,
                                                           lux=model_parametric.lux,
                                                           temperature=model_parametric.temperature,
                                                           status=model_parametric.status,
                                                           product_key=model_user.product_key,
                                                           median=model_statistic.median))
                RoutesFirebase.statistic_humidity().set(firebase_data_response)
                await database.disconnect()
            else:
                print("User not found")
        else:
            print("Sensor Data Error")

    def validation_standard(self, humidity_w: float | int, temperature: float | int, light: float | int):
        if self.lower_humidity_standard <= humidity_w <= self.higher_humidity_standard and self.lower_temperature_standard <= temperature <= self.higher_temperature_standard and self.lower_light_standard <= light <= self.higher_light_standard:
            return "Healthy"
        elif self.lower_humidity_standard > humidity_w or humidity_w > self.higher_humidity_standard and self.lower_temperature_standard <= temperature <= self.higher_temperature_standard:
            return "Danger"
        elif self.lower_temperature_standard > temperature or temperature > self.higher_temperature_standard and self.lower_humidity_standard <= humidity_w <= self.higher_humidity_standard:
            return "Danger"
        else:
            return "Acceptable"
