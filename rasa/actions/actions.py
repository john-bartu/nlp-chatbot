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


class ActionRouteForDay(Action):

    def name(self) -> Text:
        return "action_get_route_for_day"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        day_of_week = str(tracker.get_slot('day_of_week')).lower()

        mapper = {
            'monday': 'Only remote lectures today',
            'tuesday': 'Leave [ 16:35 ] -> Bus 703 [ 16:45 - 16:51 ] -> PK [ 16:55 ]\n'
                       'or Leave [ 16:39 ] -> Bus 703 [ 16:48 - 16:54 ] -> PK [ 16:58 ]\n'
                       'or Leave [ 16:42 ] -> Bus 703 [ 16:51 - 16:57 ] -> PK [ 17:01 ]',
            'wednesday': 'Leave [ 14:35 ] -> Bus 703 [14:45 - 14:51] -> PK [14:55]\n'
                         'or Leave [ 14:39 ] -> Bus 703 [ 14:48 - 14:54 ] -> PK [ 14:58 ]\n'
                         'or Leave [ 14:42 ] -> Bus 703 [ 14:51 - 14:57 ] -> PK [ 14:01 ]',
            'thursday': 'No lectures yay!',
            'friday': 'Ouh, yeah. Only remote lectures today!',
            'saturday': 'No lectures yay!',
            'sunday': 'No lectures yay!',
        }

        if day_of_week in mapper:
            dispatcher.utter_message(text=mapper[day_of_week])
        else:
            dispatcher.utter_message(template='utter_schedule_unknown_day_of_week')
        return []


class ActionGetSubjectInfo(Action):

    def name(self) -> Text:
        return "action_get_subject_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        subject = str(tracker.get_slot('subject')).lower()

        mapper = {
            'pjn': 'Przetwarzanie języka naturalnego\n\tdr Radosław Kycia',
            'pm': 'Programowanie mobilne\n\tLecture: dr hab. Joanna Kołodziej, '
                  'prof. PK\n\tLab: mgr inż. Michał Niedzwiecki',
            'ajio': 'Automaty, języki i obliczenia\n\tdr inż. Jerzy Zaczek',
            'sm': 'Seminarium dyplomowe\n\tprof. zw. dr hab. inż. Tadeusz Burczyński',
        }

        if subject in mapper:
            dispatcher.utter_message(text=mapper[subject])
        else:
            dispatcher.utter_message(template='utter_subject_unknown')
        return []
