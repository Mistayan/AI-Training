# -*- coding: utf-8 -*-
#                           ██╗██████╗ ██╗           
#                           ██║╚════██╗██║           
#                           ██║ █████╔╝██║           
#                      ██   ██║██╔═══╝ ██║           
#                      ╚█████╔╝███████╗███████╗      
#                       ╚════╝ ╚══════╝╚══════╝      
#                       https://jusdeliens.com
#
# Designed with 💖 by Jusdeliens
# Under CC BY-NC-ND 3.0 licence 
# https://creativecommons.org/licenses/by-nc-nd/3.0/ 

import os
os.system("export LANG=en_US.UTF-8")
os.system("pip3 install paho-mqtt")
os.system("pip3 install pillow")

import random
import uuid
from datetime import datetime
import time
import inspect
from paho.mqtt.client import Client
import threading
import io
from PIL import Image
import json

class IRobot:
	def connect(self) -> bool :
		"""
		Connect the client to the broker.
		Should be called once just after the __init__
		"""
		...
	def disconnect(self) -> None :
		"""
		Disconnect the client from the broker.
		"""
		...
	def isConnected(self) -> bool :
		"""
		Returns whether the client is connected to the robot or not.
		"""
		...
	def update(self) -> None :
		"""
		Fetch the last values of robot sensors from server
		And send buffered requests in one shot to limit bandwidth.
		To be call in the main loop at least every 10 msecs.
		"""
		...
	def getRobotId(self) -> str :
		"""
		Returns the unique id of the robot
		"""
		...
	def getBatteryVoltage(self) -> int :
		"""
		Returns the battery voltage in mV.
		"""
		...
	def getFrontLuminosity(self) -> int :
		"""
		Returns the front sensor luminosity from 0 (dark) to 255 (bright)
		"""
		...
	def getFrontLuminosityLevel(self) -> int :
		"""
		Returns the front sensor luminosity from 0 (dark) to 100 (bright)
		"""
		...
	def getBackLuminosity(self) -> int :
		"""
		Returns the back sensor luminosity from 0 (dark) to 255 (bright)
		"""
		...
	def getBackLuminosityLevel(self) -> int :
		"""
		Returns the back sensor luminosity from 0 (dark) to 100 (bright)
		"""
		...
	def getTimestamp(self) -> int :
		"""
		Returns the last timestamp received from Ova,
		i.e. the time elapsed in milliseconds since the boot of the robot
		"""
		...
	def getImageWidth(self) -> int :
		"""
		Returns the width of the last image captured during the last update
		in pixels. 0 If no image captured.
		"""
		...
	def getImageHeight(self) -> int :
		"""
		Returns the height of the last image captured during the last update
		in pixels. 0 If no image captured.
		"""
		...
	def getImageTimestamp(self) -> int :
		"""
		Returns the time elapsed in milliseconds between 
		the last time an image has been captured from the robot 
		and the creating of the robot class.
		"""
		...
	def getImagePixelRGB(self, x:int, y:int) -> tuple[int,int,int] :
		"""
		Returns the RGB code of the pixel at the specified x,y location.
		Returns (0,0,0) if the specified cordinate is invalid.
		"""
		...
	def getImagePixelLuminosity(self, x:int, y:int) -> int :
		"""
		Returns the luminosity from 0 (dark) to 100 (bright) of the pixel at the specified x,y location.
		Returns 0 if the specified cordinate is invalid.
		"""
		...
	def setMotorSpeed(self, left:int, right:int) -> None:
		"""
		Changes the speed of the 2 motors on the robot.
		The requested speeds will be send the next update call 

		# Arguments

		* `left` - The speed from -100 (backward) to 100 (forward) on the left wheel
		* `right` - The speed from -100 (backward) to 100 (forward) on the right wheel
		"""
		...
	def setLedColor(self, r:int, g:int, b:int) -> None:
		"""
		Changes the color of the RGB led on the top of the robot
		The requested color will be send the next update call 

		# Arguments

		* `r` - The red from 0 to 255
		* `g` - The green from 0 to 255
		* `b` - The blue from 0 to 255
		"""
		...
	def playMelody(self, tones:list[tuple[int or str,int]]) -> None:
		"""
		Plays a melody of tone with the buzzer of the robot
		Each tone must be a tuple of two parms in that order :
		(ToneHeight, DurationInMilliseconds) 
		ToneHeight can be either
		- a str for an anglosaxon tone (i.e. A4, D#5, Gb7) 
		- a int for a frequency in Hz (i.e. 440) 
		- a int for a tone index (i.e. 0 for A4, 1 for A#4, 2 for B4 ...) 
		Duration should be an int 
		The requested melody will be send the next update call 
		"""
		...

#region Analytx
class Verbosity:
	NONE = 0
	ERROR = 1
	WARNING = 2
	INFO = 3
	DEBUG = 4
	__fromStringToInt = {'none':0, 'error':1, 'warning':2, 'info':3, 'debug':4}
	__fromIntToString = ['none', 'error', 'warning', 'info', 'debug']
	def fromStringToInt(verbosity):
		if ( verbosity in Verbosity.__fromStringToInt ):
			return Verbosity.__fromStringToInt[verbosity]
		else:
			return 0
	def fromIntToString(verbosity):
		if ( verbosity >= 0 and verbosity < len(Verbosity.__fromIntToString) ):
			return Verbosity.__fromIntToString[verbosity]
		else:
			return "none"
class ILogger:
	def setVerbosity(self, verbosity):
		pass
	def getVerbosity(self):
		pass
	def log(self, verbosity, message, caller, arg):
		pass
class ConsoleLogger(ILogger):
	def __init__(self, verbosity=Verbosity.ERROR):
		self.__verbosity = verbosity
		self.__start = int(1000*time.perf_counter())
	def setVerbosity(self, verbosity):
		self.__verbosity = verbosity
	def getVerbosity(self):
		return self.__verbosity
	def log(self, verbosity, message, caller=None, previousFrame=None):
		if ( verbosity > self.__verbosity ):
			return
		now = datetime.now()
		msEllapsedSinceStart = int(1000*time.perf_counter())-self.__start
		if ( previousFrame == None ):
			previousFrame = inspect.currentframe().f_back
		(filename, line_number, function_name, lines, index) = inspect.getframeinfo(previousFrame)
		print(Verbosity.fromIntToString(verbosity)+'\t'+str(line_number)+':'+str(index)+'\t'+now.strftime("%m/%d/%Y-%H:%M:%S")+'-'+str(msEllapsedSinceStart)+'\t'+message)
		#print(Verbosity.fromIntToString(verbosity)+'\t'+now.strftime("%m/%d/%Y-%H:%M:%S")+'-'+str(msEllapsedSinceStart)+'\t'+filename+'\t'+str(line_number)+':'+str(index)+'\t'+function_name+'\t'+str(caller)+'\t'+message+'\n')
class AnalytX:
	_defaultLogger = ConsoleLogger(Verbosity.WARNING)
	def setVerbosity(verbosity, logger=None):
		if ( logger == None ):
			logger = AnalytX._defaultLogger
		logger.setVerbosity(verbosity)
	def error(message, logger=None, caller=None):
		if ( logger == None ):
			logger = AnalytX._defaultLogger
		logger.log(Verbosity.ERROR, message, caller, inspect.currentframe().f_back)
	def warning(message, logger=None, caller=None):
		if ( logger == None ):
			logger = AnalytX._defaultLogger
		logger.log(Verbosity.WARNING, message, caller, inspect.currentframe().f_back)
	def info(message, logger=None, caller=None):
		if ( logger == None ):
			logger = AnalytX._defaultLogger
		logger.log(Verbosity.INFO, message, caller, inspect.currentframe().f_back)
	def debug(message, logger=None, caller=None):
		if ( logger == None ):
			logger = AnalytX._defaultLogger
		logger.log(Verbosity.DEBUG, message, caller, inspect.currentframe().f_back)
#endregion


#region MusX
class MusX:
	octave = ['C','D','E','F','G','A','B']
	toneLetterToIndex = {'C':-9,'D':-7,'E':-5,'F':-4,'G':-2,'A':0,'B':2}
	def toneToFreq(tone:int or str):
		"""
		tone can be either
		- a str for an anglosaxon tone (i.e. A4, D#5, Gb7) 
		- a int for a frequency in Hz (i.e. 440) 
		- a int for a tone index (i.e. 0 for A4, 1 for A#4, 2 for B4 ...) 
		"""
		toneIndex = None
		if ( type(tone)==str ):
			if ( len(tone)>3):
				AnalytX.warning("⚠️ Incorrect tone. 3 letters max using anglosaxon notation (i.e. A4, D#5, Gb7)")
				return None
			if ( tone[0] not in MusX.toneLetterToIndex ):
				AnalytX.warning("⚠️ Incorrect frequency. Use letters C,D,E,F,G,A or B!")
				return None
			toneIndex = MusX.toneLetterToIndex[tone[0]]
			if ( tone[1] == '#' ):
				toneIndex += 12*(ord(tone[2])-52)+1
			elif ( tone[1] == 'b' ):
				toneIndex += 12*(ord(tone[2])-52)-1
			else:
				toneIndex += 12*(ord(tone[1])-52)
		elif ( type(tone)==int ):
			if ( tone<0 or tone > 8000 ):
				AnalytX.warning("⚠️ Incorrect frequency. Must be between 110Hz and 8000Hz or in index from 0 to 100!")
				return None
			if ( tone < 100 ):
				toneIndex = tone
		else:
			AnalytX.warning("⚠️ Incorrect tone height. Must be between 110Hz and 8000Hz or in index from 0 to 100 or a str using anglosaxon notation")
			return None
		if ( toneIndex != None ):
			tone = int(440 * pow(2, toneIndex / 12.0))
		return tone
#endregion

#region ChromatX
class ChromatX:
	def RGBToHSL(r,g,b): 
		# Make r, g, and b fractions of 1
		r /= 255
		g /= 255
		b /= 255
		# Find greatest and smallest channel values
		cmin = min(r,g,b)
		cmax = max(r,g,b)
		delta = cmax - cmin
		h = 0
		s = 0
		l = 0
		# Calculate hue
		# No difference
		if (delta == 0):
			h = 0
		# Red is max
		elif (cmax == r):
			h = ((g - b) / delta) % 6
		# Green is max
		elif (cmax == g):
			h = (b - r) / delta + 2
		# Blue is max
		else:
			h = (r - g) / delta + 4
		h = int(h * 60)
		# Make negative hues positive behind 360°
		if (h < 0):
			h += 360
		# Calculate lightness
		l = (cmax + cmin) / 2
		# Calculate saturation
		if ( delta == 0 ):
			s = 0 
		else:
			s = delta / (1 - abs(2 * l - 1))
		# Multiply l and s by 100
		s = int(s * 100)
		if ( s > 100 ):
			s = 100
		l = int(l * 100)
		if ( l > 100 ):
			l = 100
		return (h,s,l)
	def HSLToRGB(h,s,l):
		# Must be fractions of 1
		s /= 100.0
		l /= 100.0
		c = (1 - abs(2 * l - 1)) * s
		x = c * (1 - abs((h / 60) % 2 - 1))
		m = l - c/2
		r = 0
		g = 0
		b = 0
		if (0 <= h and h < 60):
			r = c
			g = x
			b = 0
		elif (60 <= h and h < 120):
			r = x
			g = c
			b = 0
		elif (120 <= h and h < 180):
			r = 0
			g = c
			b = x
		elif (180 <= h and h < 240):
			r = 0
			g = x
			b = c
		elif (240 <= h and h < 300):
			r = x
			g = 0
			b = c
		elif (300 <= h and h < 360):
			r = c
			g = 0
			b = x
		r = int((r + m) * 255)
		if ( r > 255 ):
			r = 255
			g = int((g + m) * 255)
		if ( g > 255 ):
			g = 255
			b = int((b + m) * 255)
		if ( b > 255 ):
			b = 255
		return (r,g,b)
#endregion

#region RobotX
class OvaClientMqtt(IRobot):
	"""
	Concrete class to handle input output operation with
	a Jusdeliens Ova robot connected to a mqtt broker
	"""
	melodySizeLimit = 100 # In tone number
	melodyDurationLimit = 10000 # In msecs
	isConnectedTimeout = 10000 # In msecs
	dtTx = 100 # In msecs
	dtPing = 5000 # In msecs
	dtSleepUpdate = 100 # In msecs
	batteryMax = 3900 # In mV
	batteryMin = 3500 # In mV

	def __onChunkImageReceived(self, data:bytes):
		"""Called when rx payload on image topic"""
		payloadLen = len(data)
		if ( payloadLen < 3 ):
			AnalytX.debug("⚠️ Rx image corrupted. Payload len too small")
			return
		imgLen = int.from_bytes(data[0:4],'big', signed=False)
		chunkOfs = int.from_bytes(data[4:8],'big', signed=False)
		chunkLen = int.from_bytes(data[8:12],'big', signed=False)
		AnalytX.debug("📡 Rx image ["+str(chunkOfs)+":"+str(chunkOfs+chunkLen)+"] / "+str(imgLen))
		chunkImg = data[12:]
		if ( chunkOfs == 0 ):
			self.__bufImgOffset = 0
			self.__bufImgExpectedLength = imgLen
		elif ( imgLen != self.__bufImgExpectedLength or self.__bufImgOffset != chunkOfs ):
			AnalytX.debug("⚠️ Rx image corrupted. Expected "+str(self.__bufImgOffset)+"/"+str(self.__bufImgExpectedLength)+" instead of rx "+str(chunkOfs)+"/"+str(imgLen))
			return
		self.__bufImg.append(chunkImg)
		self.__bufImgOffset += chunkLen
		if ( self.__bufImgOffset == self.__bufImgExpectedLength ):
			with self.__bufImgMutex:
				self.__bufImgComplete = self.__bufImg.copy()
				self.__bufImg = []
				self.__rxFromRobot = True
	def __onSensorsReceived(self, data:bytes):
		"""Called when rx payload on sensors topic"""
		newState = {}
		# Parse json payload
		try:
			payloadLen = len(data)
			if ( payloadLen <= 0 ):
				return
			payloadStr = data.decode()
			newState = json.loads(payloadStr)
			AnalytX.debug("📡 Rx state of "+str(payloadLen)+" byte(s): "+payloadStr)
		except:
			AnalytX.debug("⚠️ Rx state failed to parse json")
		with self.__bufRobotStateMutex:
			self.__bufRobotState = newState
			self.__rxFromRobot = True
	def __onPlayerStateReceived(self, data:bytes):
		"""Called when rx payload on player state topic"""
		newState = {}
		# Parse json payload
		try:
			payloadLen = len(data)
			if ( payloadLen <= 0 ):
				return
			payloadStr = data.decode()
			newState = json.loads(payloadStr)
			AnalytX.debug("📡 Rx state of "+str(payloadLen)+" byte(s): "+payloadStr)
		except:
			AnalytX.debug("⚠️ Rx state failed to parse json")
		with self.__bufPlayerStateMutex:
			self.__bufPlayerState = newState
			self.__rxFromPlayer = True
	def __onMessage(client, userdata, message):
		"""Called when rx message from mqtt broker"""
		rxTopic = message.topic
		rxPayload = message.payload
		if ( rxTopic == userdata.__topicImgStream ):
			userdata.__onChunkImageReceived(rxPayload)
		elif ( rxTopic == userdata.__topicRobotState ):
			userdata.__onSensorsReceived(rxPayload)
		elif ( rxTopic == userdata.__topicPlayerState ):
			userdata.__onPlayerStateReceived(rxPayload)
		else:
			AnalytX.debug("📡 Rx "+userdata.__id+" on topic "+rxTopic+": "+str(len(rxPayload))+" byte(s)")
		userdata.__prevRx = datetime.now()
	def __onConnect(client, userdata, flags, rc):
		"""Called after a connection to mqtt broker is requested"""
		if ( rc == 0 ):
			if ( userdata.__isConnectedToBroker == False ):
				userdata.__isConnectedToBroker = True
				AnalytX.info("🟢 Connected "+userdata.__id+" to broker")
				for topic in userdata.__topicsToSubcribe:
					AnalytX.info("⏳ Subscribing "+userdata.__id+" to topic "+topic)
					userdata.__client.subscribe(topic)
				pingRequest = json.dumps({"ping": True})
				userdata.__client.publish(userdata.__topicRobotRequest, pingRequest)
		else:
			AnalytX.error("❌ FAIL to connected "+userdata.__id+" to broker")
	def __onDisconnect(client, userdata, rc):
		"""Called when disconnected from mqtt broker"""
		AnalytX.info("🔴 Disconnected "+userdata.__id+" from broker")
		userdata.__isConnectedToBroker = False
	def __onSubscribe(client, userdata, mid, granted_qos):
		"""Called after suscribed on mqtt topic"""
		AnalytX.info("🔔 Subscribed "+userdata.__id+" to topic "+str(mid))
	def __onUnsubscribe(client, userdata, mid):
		"""Called after unsuscribed from mqtt topic"""
		AnalytX.info("🔔 Unsubscribed "+userdata.__id+" from topic "+str(mid))	

	def _onConnected(self):
		"""Called after the client is connected to the robot"""
		...
	def _onDisconnected(self):
		"""Called after the client is disconnected from the robot"""
		...
	def _onUpdated(self):
		"""Called each time update function is called"""
		...
	def _onRobotChanged(self, robot):
		"""Called each time new state is received from the robot"""
		...
	def _onPlayerChanged(self, player):
		"""Called each time new player state is received from the game"""
		...
	def _onImageReceived(self, img:Image):
		"""Called each time new complete image is received from the robot"""
		...

	def __init__(self,id:str or None=None, arena:str or None=None, username:str or None=None, password:str or None=None, server:str or None=None, port:int=1883, imgOutputPath:str or None="img.jpeg", autoconnect:bool=True, useProxy:bool=True, verbose:int=3):
		"""
		Build a mqtt client to communicate with an ova robot through a mqtt broker

		# Arguments

		* `id` - The unique name of the robot to control (e.g. ovaxxxxxxxxxxxx) as str
		* `arena` - The name of the arena to join as str
		* `username` - The username to join the server as str
		* `password` - The password to join the server as str
		* `server` - The ip address of the server (e.g. 192.168.x.x) or a domain name (e.g. mqtt.jusdeliens.com) as str
		* `port` - The port of the server (e.g. 1883) as an int
		* `autoconnect` - If True, connect to the broker during init. If False, you should call update or connect yourself after init.
		* `useProxy` - If False, send request directly to robot through broker only. If true, sending to server proxy, which then redirect to robot.
		* `verbose` - The level of logs as an int. See Verbosity class for more info.
		"""
		AnalytX.setVerbosity(verbose)
		print("Hi there 👋")
		print("Turn on your Ova to make it sing like a diva 🎤")
		print("Then wait until your hear the congrat jingle 🎵")
		print("You don't have a robot ? Follow the link 👉 https://jusdeliens.com/ova")
		if ( arena == None or username == None or password == None or server == None):
			print("Enter your credentials to connect to your robot")
		while ( id == None or len(id) > 32 or len(id) == 0 ):
			id=input("🤖 robot id (< 32 characters): ")
		while ( server == None or len(server) == 0 ):
			server=input("🌐 server address: ")
			port=int(input("🌐 server port: "))
		if ( arena == None ):
			arena=input("🎲 arena: ")
		if ( username == None ):
			username=input("🧑 username: ")
		if ( password == None ):
			password=input("🔑 password: ")
		self.__startTime = datetime.now()
		
		userLogin=""
		try: userLogin=str(os.getlogin()) 
		except: ...
		macAddr=""
		try: macAddr=str(hex(uuid.getnode())) 
		except: ...

		self.__id : str = "OvaClientMqtt-"+id+"-"+userLogin+"-"+macAddr+"-"+str(random.randint(0,99999))
		self.__arena : str = arena 
		self.__idRobot : str = id 
		self.__wasConnected : bool = False
		self.__reqRobot = {}
		self.__camImgOutputPath = imgOutputPath
		self.__camImg = None
		self.__bufImgComplete = []
		self.__bufImgMutex = threading.Lock()
		self.__bufImg = []
		self.__bufImgOffset = 0
		self.__bufImgExpectedLength = 0
		self.__bufRobotStateMutex = threading.Lock()
		self.__bufRobotState = {}
		self.__robotState = {}
		self.__rxFromRobot: bool = False
		self.__bufPlayerStateMutex = threading.Lock()
		self.__bufPlayerState = []
		self.__rxFromPlayer: bool = False
		self.__playerState = {}
		self.__melodyDuration = 0
		self.__prevImgRx: int = datetime.fromtimestamp(0)
		self.__prevRx: int = datetime.fromtimestamp(0)
		self.__prevTx: int = datetime.fromtimestamp(0)
		self.__prevPing: int = datetime.fromtimestamp(0)
		self.__dtTxToWait: int = OvaClientMqtt.dtTx
		self.__topicImgStream : str  = "optx/clients/stream/"+self.__idRobot
		self.__topicRobotState : str  = "robotx/clients/state/"+self.__idRobot
		self.__topicPlayerState : str  = "ludx/clients/state/"+self.__arena+"/"+self.__idRobot
		self.__topicRobotRequest : str  = ""
		self.__useProxy = useProxy
		if ( useProxy ):
			self.__topicRobotRequest = "ludx/clients/request/"+self.__arena+"/"+self.__idRobot
		else:
			self.__topicRobotRequest = "robotx/clients/request/"+self.__idRobot
		self.__topicsToSubcribe = [self.__topicImgStream, self.__topicRobotState, self.__topicPlayerState]
		self.__client: Client = Client(self.__id, userdata=self)
		self.__isConnectedToBroker: bool = False
		self.__serverAddress: str = server
		self.__username: str  or  None = username
		self.__password: str  or  None = password
		self.__serverPort: int = port
		self.__client.on_message = OvaClientMqtt.__onMessage
		self.__client.on_connect = OvaClientMqtt.__onConnect
		self.__client.on_disconnect = OvaClientMqtt.__onDisconnect
		self.__client.on_subscribe = OvaClientMqtt.__onSubscribe
		self.__client.on_unsubscribe = OvaClientMqtt.__onUnsubscribe
		self.__isLoopStarted = False
		if ( autoconnect ):
			self.connect()

	def connect(self) -> bool :
		if self.__isLoopStarted and self.__isConnectedToBroker:
			return False
		if (self.__username is not None and self.__password is not None):
			self.__client.username_pw_set(self.__username, self.__password)
		try:
			if ( self.__isConnectedToBroker == False ):
				AnalytX.info("⏳ Connecting "+str(self.__id)+" to broker "+self.__serverAddress+":"+str(self.__serverPort)+" ...")
				self.__client._connect_timeout = 5.0
				rc=self.__client.connect(self.__serverAddress, self.__serverPort)
				#OvaClientMqtt.__onConnect(self.__client, self, None, rc) # TODO to remove if using loopstart loopstop
			if ( self.__isLoopStarted == False ):
				AnalytX.info("⏳ Starting mqtt thread loop ...")
				self.__client.loop_start()
				AnalytX.info("🟢 Started mqtt loop")
				self.__isLoopStarted = True
			time.sleep(2)
			return rc == 0
		except:
			return False

	def disconnect(self) -> None :
		if self.__isLoopStarted: 
			AnalytX.info("⏳ Stopping mqtt thread loop ...")
			self.__client.loop_stop(force=True)
			AnalytX.info("🔴 Stopped mqtt thread loop")
			self.__isLoopStarted = False	
		if self.__isConnectedToBroker:
			AnalytX.info("⏳ Disconnecting "+str(self.__id)+" from broker...")
			self.__client.disconnect()

	def isConnected(self) -> bool:
		dtRx = (datetime.now() - self.__prevRx).total_seconds() * 1000
		return self.__isConnectedToBroker and dtRx < OvaClientMqtt.isConnectedTimeout

	def update(self) -> None:
		if ( self.__isConnectedToBroker == False ):
			self.connect()

		try:
			self._onUpdated()
		except: 
			AnalytX.debug("⚠️ Exception during onUpdated call ! Check between the screen and the chair 🫵 😁")
		
		# Rx states and stream
		if ( self.__rxFromRobot ):
			self.__rxFromRobot = False
			# Triggers on connected event
			if ( self.__wasConnected == False ):
				self.__wasConnected = True
				AnalytX.info("🟢 Robot "+str(self.__id)+" connected")
				try:
					self._onConnected()
				except:
					AnalytX.debug("⚠️ Exception during onConnected call ! Check between the screen and the chair 🫵 😁")
			# Swap bug img and sensor states 
			try:
				with self.__bufImgMutex:
					if ( len(self.__bufImgComplete) > 0 ):
						self.__camImg = Image.open(io.BytesIO(b''.join(self.__bufImgComplete)))
						self.__bufImgComplete = []
						self.__prevImgRx = (datetime.now() - self.__startTime).total_seconds() * 1000
						if ( self.__camImgOutputPath != None ):
							try:
								self.__camImg.save(self.__camImgOutputPath)
								AnalytX.debug("📸 Save camera image in "+str(os.getcwd())+"\\"+str(self.__camImgOutputPath))
							except:
								AnalytX.debug("⚠️ Fail to write "+str(self.__camImgOutputPath))
						AnalytX.debug("🖼️ Camera img received: "+str(self.__camImg.width)+"x"+str(self.__camImg.height))
						try:
							self._onImageReceived(self.__camImg)
						except:
							AnalytX.debug("⚠️ Exception during onImageReceived call ! Check between the screen and the chair 🫵 😁")
			except:
				AnalytX.debug("⚠️ Rx image corrupted. Fail to swap buffer.")

			try:
				with self.__bufRobotStateMutex:
					if ( self.__bufRobotState != self.__robotState ):
						AnalytX.debug("🤖 Robot changed: "+str(self.__bufRobotState))
						self.__robotState = self.__bufRobotState
						self.__bufRobotState = {}
						self._onRobotChanged(self.__robotState)
			except:
				AnalytX.debug("⚠️ Rx robot state corrupted. Fail to swap buffer.")
		elif ( self.__wasConnected == True and self.isConnected() == False ):
			self.__wasConnected = False
			AnalytX.info("🔴 Robot "+str(self.__id)+" disconnected")
			try:
				self._onDisconnected()
			except:
				AnalytX.debug("⚠️ Exception during onDisconnected call ! Check between the screen and the chair 🫵 😁")
		if ( self.__rxFromPlayer ):
			self.__rxFromPlayer = False
			try:
				with self.__bufPlayerStateMutex:
					if ( self.__bufPlayerState != self.__playerState ):
						AnalytX.debug("♟️ Player changed: "+str(self.__bufPlayerState))
						self.__playerState = self.__bufPlayerState
						self.__bufPlayerState = {}
						self._onPlayerChanged(self.__playerState)
			except:
				AnalytX.debug("⚠️ Rx player state corrupted. Fail to swap buffer.")
		
		# Tx requests
		dtTx = (datetime.now()-self.__prevTx).total_seconds() * 1000
		if ( len(self.__reqRobot) > 0 and dtTx > self.__dtTxToWait ):
			self.__prevTx = datetime.now()
			payloadStr = json.dumps(self.__reqRobot)
			payloadBytes = str.encode(payloadStr)
			topicsToPub = [self.__topicRobotRequest]
			if ( self.__useProxy == False ):
				topicsToPub.append("ludx/clients/request/"+self.__arena+"/"+self.__idRobot)
			for topic in topicsToPub:
				AnalytX.debug("📡 Tx "+str(self.__id)+" to topic "+str(topic)+": "+str(len(payloadBytes))+" byte(s)")
				self.__client.publish(topic, payloadBytes)
			self.__reqRobot = {}
			if ( self.__melodyDuration > 0 ):
				self.__dtTxToWait = self.__melodyDuration
				time.sleep(self.__melodyDuration/1000.0)
				self.__melodyDuration = 0
			else:
				self.__dtTxToWait = OvaClientMqtt.dtTx

		# Ping
		dtPing = (datetime.now()-self.__prevPing).total_seconds() * 1000
		if ( dtPing > OvaClientMqtt.dtPing ):
			self.__prevPing = datetime.now()
			payloadStr = json.dumps({"ping":True})
			payloadBytes = str.encode(payloadStr)
			topicsToPub = [self.__topicRobotRequest]
			if ( self.__useProxy == False ):
				topicsToPub.append("ludx/clients/request/"+self.__arena+"/"+self.__idRobot)
			for topic in topicsToPub:
				AnalytX.info("📡 Ping "+str(self.__id))
				self.__client.publish(topic, payloadBytes)

		time.sleep(OvaClientMqtt.dtSleepUpdate/1000)

	def getRobotId(self) -> str :
		return self.__idRobot

	def getBatteryVoltage(self) -> int :
		if ( "battery" not in self.__robotState or "voltage" not in self.__robotState["battery"] ):
			return 0
		return self.__robotState["battery"]["voltage"]
	
	def getBatteryLevel(self) -> int :
		voltage = self.getBatteryVoltage()
		if ( voltage > OvaClientMqtt.batteryMax ): return 100
		elif ( voltage < OvaClientMqtt.batteryMin ): return 0
		else:
			return int(100*(voltage-OvaClientMqtt.batteryMin) / (OvaClientMqtt.batteryMax-OvaClientMqtt.batteryMin))

	def getFrontLuminosity(self) -> int :
		if ( "photoFront" not in self.__robotState or "lum" not in self.__robotState["photoFront"] ):
			return 0
		return self.__robotState["photoFront"]["lum"]
	
	def getFrontLuminosityLevel(self) -> int :
		return int(100*self.getFrontLuminosity()/255)

	def getBackLuminosity(self) -> int :
		if ( "photoBack" not in self.__robotState or "lum" not in self.__robotState["photoBack"] ):
			return 0
		return self.__robotState["photoBack"]["lum"]

	def getBackLuminosityLevel(self) -> int :
		return int(100*self.getBackLuminosity()/255)

	def getTimestamp(self) -> int :
		if ( "t" not in self.__robotState ):
			return 0
		return self.__robotState["t"]

	def getImageWidth(self) -> int :
		if ( self.__camImg == None ):
			return 0
		return self.__camImg.width

	def getImageHeight(self) -> int :
		if ( self.__camImg == None ):
			return 0
		return self.__camImg.height

	def getImageTimestamp(self) -> int :
		return self.__prevImgRx

	def getImagePixelRGB(self, x:int,y:int) -> tuple[int,int,int] :
		if ( x < 0 or x >= self.getImageWidth() or y < 0 or y >= self.getImageHeight() ):
			return (0,0,0)
		r,g,b = self.__camImg.getpixel((x, y))
		return (r,g,b)
	def getImagePixelLuminosity(self, x:int,y:int) -> int :
		if ( x < 0 or x >= self.getImageWidth() or y < 0 or y >= self.getImageHeight() ):
			return 0
		r,g,b = self.__camImg.getpixel((x, y))
		h,s,l = ChromatX.RGBToHSL(r,g,b)
		return l

	def setMotorSpeed(self, leftPower:int, rightPower:int):
		if ( leftPower < -100 or rightPower < -100 or leftPower > 100 or rightPower > 100):
			AnalytX.warning("⚠️ Motor speed should be between -100 and +100!")
			return
		self.__reqRobot["motorLeft"] = leftPower
		self.__reqRobot["motorRight"] = rightPower

	def setLedColor(self, r:int, g:int, b:int):
		if ( r < 0 or g < 0 or b < 0 or r > 255 or g > 255 or b > 255 ):
			AnalytX.warning("⚠️ LED RGB should be between 0 and 255!")
			return
		self.__reqRobot["ledR"] = r
		self.__reqRobot["ledG"] = g
		self.__reqRobot["ledB"] = b

	def playMelody(self, tones:list[tuple[int or str,int]]):
		if ( len(tones) <= 0 ):
			AnalytX.warning("⚠️ No tone in melody!")
			return
		if ( len(tones) > OvaClientMqtt.melodySizeLimit ):
			AnalytX.warning("⚠️ Too much tones in melody!")
			return
		duration = 0
		tonesHzMs = []
		for tone in tones:
			if ( len(tone) != 2 ):
				AnalytX.warning("⚠️ Incorrect tone in melody. Should be a tuple of tuples of 2 params : frequency, duration !")
				return
			toneHeight = tone[0]
			toneDuration = tone[1]
			if ( type(toneDuration)!=int or toneDuration < 0 or toneDuration > 10000 ):
				AnalytX.warning("⚠️ Incorrect duration in melody. Should be a positive integer value in ms lesser than 10000 !")
				return
			toneHeight = MusX.toneToFreq(toneHeight)
			if ( toneHeight == None ):
				return
			# freq as index
			tonesHzMs.append((toneHeight,toneDuration))
			duration += toneDuration
		if ( duration > OvaClientMqtt.melodyDurationLimit ):
			AnalytX.warning("⚠️ Melody duration is too long!")
			return
		self.__melodyDuration = duration
		self.__reqRobot["buzzer"] = tonesHzMs

	def prompt(self, jsonReq:str) -> bool:
		try:
			self.__reqRobot = json.loads(jsonReq)
			return True
		except:
			return False

#endregion


