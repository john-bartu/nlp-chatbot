# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions
import calendar
import datetime
from typing import Any, Text, Dict, List

import requests
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher


# This is a simple example for a custom action which utters "Hello World!"


class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_hello_world"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text="Hello World!")

        return []


class ActionGetWeather(Action):

    def name(self) -> Text:
        return "action_get_weather"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        api_key = '8620dcbda1718a1bb93adc32dd89e3fe'
        loc = tracker.get_slot('location')
        current = requests.get(
            'http://api.openweathermap.org/data/2.5/weather?q={}&appid={}'.format(loc, api_key)).json()

        country = current['sys']['country']
        city = current['name']
        condition = current['weather'][0]['main']
        temperature_c = round(current['main']['temp'] - 273.15, 2)
        response = """It is currently {} in {} at the moment. The temperature is {}C.""" \
            .format(condition, city, temperature_c)
        dispatcher.utter_message(response)
        return [SlotSet('location', loc)]


class ActionGetRoute(Action):

    def name(self) -> Text:
        return "action_get_route"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        location = tracker.get_slot("location")
        dispatcher.utter_message(text=f"Weather for location: {location}.")

        return []


class ActionGetTodayDayOfWeek(Action):

    def name(self) -> Text:
        return "action_get_today_day_of_week"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        day_of_week_no = datetime.datetime.today().weekday()
        day_of_week = calendar.day_name[day_of_week_no]
        return [SlotSet('day_of_week', day_of_week)]


class ActionScheduleForDay(Action):

    def name(self) -> Text:
        return "action_get_schedule_for_day"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        day_of_week = str(tracker.get_slot('day_of_week')).lower()

        mapper = {
            'monday': 'utter_schedule_monday',
            'tuesday': 'utter_schedule_tuesday',
            'wednesday': 'utter_schedule_wednesday',
            'thursday': 'utter_schedule_no_lectures',
            'friday': 'utter_schedule_friday',
            'saturday': 'utter_schedule_no_lectures',
            'sunday': 'utter_schedule_no_lectures',
        }

        if day_of_week in mapper:
            dispatcher.utter_message(template=mapper[day_of_week])
        else:
            dispatcher.utter_message(template='utter_schedule_unknown_day_of_week')
        return []
#
# def get_route2(loc):
#     source_loc = (50.0576542, 19.9454402)
#     dest_loc = (50.0712524, 19.9386159)
#     route, route_length, route_time = get_route(source_loc, dest_loc)
#     print(f'{route = }')
#     print(f'{route_length = }')
#     print(f'{route_time = }')
#
#
# if __name__ == '__main__':
#     location2 = 'kek'
#     print(location2)
#     get_route2(location2)
#     print('finished')
