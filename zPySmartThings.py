#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @FileName: zPySmartThings.py
# @Author: Zachary Priddy
# @Date:   2016-02-10 21:20:56
# @Last Modified by:   Zachary Priddy
# @Last Modified time: 2016-02-10 21:57:55
#
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy
# of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.


import sys
import requests
import pprint
import json
import math
import zPySmartThings_settings as settings

icons = {
  'chanceflurries': '&#xe036',
  'chancerain': '&#xe009',
  'chancesleet': '&#xe003',
  'chancesnow': '&#xe036',
  'chancetstorms': '&#xe025',
  'clear': '&#xe028',
  'cloudy': '&#xe000',
  'flurries': '&#xe036',
  'fog': '&#xe01b',
  'hazy': '&#xe01b',
  'mostlycloudy': '&#xe001',
  'mostlysunny': '&#xe001',
  'partlycloudy': '&#xe001',
  'partlysunny': '&#xe001',
  'sleet': '&#xe003',
  'rain': '&#xe009',
  'snow': '&#xe036',
  'sunny': '&#xe028',
  'tstorms': '&#xe025'
}

class SmartThings(object):
  def __init__(self, verbose=True):
    self.verbose = verbose
    self.std = {}
    self.endpointd = {}
    self.deviceds = {}

  def load_settings(self):
    """Load the JSON Settings file. 
    
    See the documentation, but briefly you can
    get it from here:
    https://iotdb.org/playground/oauthorize
    """

    self.std = settings.settings

  def request_endpoints(self):
    """Get the endpoints exposed by the SmartThings App
    
    The first command you need to call
    """

    endpoints_url = self.std["api"]
    endpoints_paramd = {
      "access_token": self.std["access_token"]
    }

    endpoints_response = requests.get(url=endpoints_url, params=endpoints_paramd)
    print endpoints_response
    self.endpointd = endpoints_response.json()[0]


  def request_devices(self, device_type, device_id=None):
    """List the devices"""

    devices_url = "%s/%s" % ( self.std["url"], device_type )
    devices_paramd = {
      "deviceId":device_id,
    }
    devices_headerd = {
      "Authorization": "Bearer %s" % self.std["access_token"],
      "deviceId":device_id
    }

    devices_response = requests.get(url=devices_url, params=devices_paramd, headers=devices_headerd, json=devices_paramd)
    #print devices_response.headers
    self.deviceds = devices_response.json()



    return self.deviceds

  def command_devices(self, device_type, device_id, command):

    devices_url = "%s/%s" % ( self.std["url"], device_type )
    devices_paramd = {
      "deviceId":device_id,
      "command":command
    }
    devices_headerd = {
      "Authorization": "Bearer %s" % self.std["access_token"],
      "deviceId":device_id
    }
    devices_response = requests.post(url=devices_url, params=devices_paramd, headers=devices_headerd, json=devices_paramd)
    self.deviceds = devices_response.json()

    return self.deviceds

  def command_switch(self, device_id, command):
    if(command == "t"):
      currentState = self.request_devices("switch", device_id)['switch']
      if(currentState == 'on'):
        command = 'off'
      else:
        command = 'on'

    devices_url = "%s/%s" % ( self.std["url"], "switch" )
    devices_paramd = {
      "deviceId":device_id,
      "command":command
    }
    devices_headerd = {
      "Authorization": "Bearer %s" % self.std["access_token"],
    }
    devices_response = requests.post(url=devices_url, params=devices_paramd, headers=devices_headerd, json=devices_paramd)
    self.deviceds = devices_response.json()

    return command

  def command_dimmer(self, device_id, command):
    if(command == "t"):
      self.deviceds = self.command_switch(device_id,"t")
    else:
      devices_url = "https://graph.api.smartthings.com%s/%s" % ( self.endpointd["url"], "dimmer" )
      devices_paramd = {
        "deviceId":device_id,
        "command": "setLevel"

      }
      devices_headerd = {
        "Authorization": "Bearer %s" % self.std["access_token"],
      }
      devices_response = requests.post(url=devices_url, params=devices_paramd, headers=devices_headerd, json=devices_paramd)

      devices_url = "%s/%s" % ( self.std["url"], "dimmerLevel" )
      devices_paramd = {
        "deviceId":device_id,
        "command": command

      }
      devices_headerd = {
        "Authorization": "Bearer %s" % self.std["access_token"],
      }
      devices_response = requests.post(url=devices_url, params=devices_paramd, headers=devices_headerd, json=devices_paramd)

      self.deviceds = devices_response.json()

    return self.deviceds

  def set_color(self,deviceId,color):
    devices_url = "%s/%s" % ( self.std["url"], "color" )
    devices_paramd = rgbToHsl(color)
    devices_paramd['deviceId'] = deviceId
    devices_headerd = {
      "Authorization": "Bearer %s" % self.std["access_token"],
    }

    devices_response = requests.post(url=devices_url, params=devices_paramd, headers=devices_headerd, json=devices_paramd)

    return self.deviceds

  def set_color_hsla(self,deviceId,hue,sat,color):
    devices_url = "%s/%s" % ( self.std["url"], "color" )
    devices_paramd = {}
    devices_paramd['hex'] = color
    devices_paramd['hue'] = hue
    devices_paramd['sat'] = sat
    devices_paramd['deviceId'] = deviceId
    devices_headerd = {
      "Authorization": "Bearer %s" % self.std["access_token"],
    }

    devices_response = requests.post(url=devices_url, params=devices_paramd, headers=devices_headerd, json=devices_paramd)

    return self.deviceds
    


  def command_mode(self, mode_id):
    devices_url = "%s/%s" % ( self.std["url"], "mode" )
    devices_paramd = {
      "mode":mode_id
    }
    devices_headerd = {
      "Authorization": "Bearer %s" % self.std["access_token"],
    }

    devices_response = requests.post(url=devices_url, params=devices_paramd, headers=devices_headerd, json=devices_paramd)
    devices_response = requests.post(url=devices_url, params=devices_paramd, headers=devices_headerd, json=devices_paramd)
    self.deviceds = devices_response.json()

    return self.deviceds

  def get_mode(self):
    devices_url = "%s/%s" % ( self.std["url"], "mode" )
    devices_paramd = {

    }
    devices_headerd = {
      "Authorization": "Bearer %s" % self.std["access_token"],
    }

    devices_response = requests.get(url=devices_url, params=devices_paramd, headers=devices_headerd, json=devices_paramd)
    self.deviceds = devices_response.json()
    return self.deviceds


  def get_weather(self):
    devices_url = "%s/%s" % ( self.std["url"], "weather" )
    devices_paramd = {
      
    }
    devices_headerd = {
      "Authorization": "Bearer %s" % self.std["access_token"],
    }

    devices_response = requests.get(url=devices_url, params=devices_paramd, headers=devices_headerd, json=devices_paramd)
    self.weather = devices_response.json()

    weatherInfo = {}
    weatherInfo['location'] = self.weather['current_observation']['display_location']['full']
    weatherInfo['sky'] = self.weather['current_observation']['weather']
    weatherInfo['wind'] = self.weather['current_observation']['wind_mph']
    weatherInfo['temperature'] = self.weather['current_observation']['temp_f']
    weatherInfo['humidity'] = self.weather['current_observation']['relative_humidity']

    devices_url = "%s/%s" % ( self.std["url"], "weather" )
    devices_paramd = {
      'feature': 'forecast'
      
    }
    devices_headerd = {
      "Authorization": "Bearer %s" % self.std["access_token"],
    }

    devices_response = requests.get(url=devices_url, params=devices_paramd, headers=devices_headerd, json=devices_paramd)
    self.weather = devices_response.json()

    weatherInfo['low'] = self.weather["forecast"]["simpleforecast"]["forecastday"][0]["low"]["fahrenheit"]
    weatherInfo['high'] = self.weather["forecast"]["simpleforecast"]["forecastday"][0]["high"]["fahrenheit"]
    weatherInfo['icon'] = icons[self.weather["forecast"]["simpleforecast"]["forecastday"][0]["icon"]]
    weatherInfo['precip'] =  self.weather["forecast"]["simpleforecast"]["forecastday"][0]["pop"]
    weatherInfo['tomorrow_temp_low'] =  self.weather["forecast"]["simpleforecast"]["forecastday"][1]["low"]["fahrenheit"]
    weatherInfo['tomorrow_temp_high'] =  self.weather["forecast"]["simpleforecast"]["forecastday"][1]["high"]["fahrenheit"]
    weatherInfo['tomorrow_icon'] =  icons[self.weather["forecast"]["simpleforecast"]["forecastday"][1]["icon"]]
    weatherInfo['tomorrow_precip'] =  self.weather["forecast"]["simpleforecast"]["forecastday"][1]["pop"]

    return weatherInfo

  def getAllDevices(self):
    allDevices = {}
    allDevices["switch"] = self.request_devices("switch")
    allDevices["contact"] = self.request_devices("contact")
    allDevices["lock"] = self.request_devices("lock")
    allDevices["mode"] = self.request_devices("mode")
    allDevices["power"] = self.request_devices("power")
    allDevices["presence"] = self.request_devices("presence")
    allDevices["dimmer"] = self.request_devices("dimmer")
    allDevices["temperature"] = self.request_devices("temperature")
    allDevices["humidity"] = self.request_devices("humidity")
    allDevices["weather"] = self.request_devices("weather")
    allDevices["motion"] = self.request_devices("motion")
    allDevices["color"] = self.request_devices("color")

    return allDevices

  def updateSwitch(self):
    switches = {}
    switches = self.request_devices("switch")

    return switches

  def updateColor(self):
    colors = {}
    colors = self.request_devices("color")
    #print colors

    return colors

  def updatePower(self):
    power = {}
    power = self.request_devices("power")

    return power

  def updateHumidity(self):
    humidity = {}
    humidity = self.request_devices("humidity")

    return humidity

  def updateContact(self):
    contacts = {}
    contacts = self.request_devices("contact")

    return contacts

  def updatePresence(self):
    presence = {}
    presence = self.request_devices("presence")

    return presence

  def updateMotion(self):
    motion = {}
    motion = self.request_devices("motion")

    return motion


  def updateMode(self):
    mode = {}
    mode = self.request_devices("mode")

    return mode

  def updateDimmer(self):
    dimmer = {}
    dimmer = self.request_devices("dimmer")

    return dimmer

  def updateWeather(self):
    weather = {}
    weather = self.request_devices("weather")

    return weather

  def updateTemp(self):
    temperature = {}
    temperature = self.request_devices("temperature")

    return temperature