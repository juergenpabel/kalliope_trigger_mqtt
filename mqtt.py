#!/usr/bin/python3

import logging
import time
from threading import Thread
from kalliope import Utils
from paho.mqtt import client as mqtt_client


logging.basicConfig()
logger = logging.getLogger("kalliope")


class Mqtt(Thread):
	def __init__(self, **kwargs):
		super(Mqtt, self).__init__()
		logger.debug("[trigger:mqtt] __init__()")
		self.callback = kwargs.get('callback', None)
		if self.callback is None:
			raise MissingParameterException("Callback function is required")
		self.trigger_topic = kwargs.get('topic', None)
		if self.trigger_topic is None:
			raise MissingParameterException("Trigger (mqtt) topic is required")


	def run(self):
		logger.debug("[trigger:mqtt] run()")
		self.mqtt = mqtt_client.Client('kalliope_trigger_mqtt')
		self.mqtt.connect('127.0.0.1', 1883)
		self.mqtt.subscribe(self.trigger_topic)
		self.mqtt.on_message = self.on_mqtt
		self.paused = False
		self.mqtt.loop_forever()

	def on_mqtt(self, client, userdata, message):
		logger.debug("[trigger:mqtt] on_mqtt()")
		if self.paused is False:
			logger.info("[trigger:mqtt] trigger activated()")
			self.callback()

	def pause(self):
		logger.debug("[trigger:mqtt] pause()")
		self.paused = True

	def unpause(self):
		logger.debug("[trigger:mqtt] unpause()")
		self.paused = False

