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
		self.trigger_broker_ip = kwargs.get('broker_ip', '127.0.0.1')
		self.trigger_broker_port = kwargs.get('broker_port', 1883)
		self.trigger_client_id = kwargs.get('client_id', 'kalliope:trigger:mqtt')
		self.trigger_topic = kwargs.get('topic', None)
		if self.trigger_topic is None:
			raise MissingParameterException("Trigger (mqtt) topic is required")


	def run(self):
		logger.debug("[trigger:mqtt] run()")
		self.mqtt = mqtt_client.Client(self.trigger_client_id)
		self.mqtt.connect(self.trigger_broker_ip, self.trigger_broker_port)
		self.mqtt.subscribe(self.trigger_topic)
		self.mqtt.on_message = self.on_mqtt
		self.paused = False
		self.mqtt.loop_forever()

	def on_mqtt(self, client, userdata, message):
		logger.debug("[trigger:mqtt] on_mqtt()")
		payload = message.payload.decode('utf-8')
		if payload == "pause":
			self.pause()
		if payload == "unpause":
			self.unpause()
		if payload is None or payload == "" or payload == "trigger":
			if self.paused is False:
				logger.info("[trigger:mqtt] trigger activated()")
				self.callback()

	def pause(self):
		logger.info("[trigger:mqtt] pause()")
		self.paused = True

	def unpause(self):
		logger.info("[trigger:mqtt] unpause()")
		self.paused = False

