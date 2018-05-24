from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.core.image import Image
from kivy.properties import StringProperty
from kivy.logger import Logger


import jsonRequests
import time

from BaseApp import RelativeApp

class Server():

	order = ["NA","CS","EU","AP"]

	def __init__(self, name, status):
		self.code = name[0:2].upper()
		self.num = int(name[2:])
		self.status = status
		self.component = ""
		self.name = name

	def __str__(self):
		cm = ""
		if self.component != "":
			cm = ", Linked"
		return self.code + str(self.num) + ": " + self.status + cm

	def __lt__(self, other):
		o = {self.order[i]:i for i in range(len(self.order))}
		if o[self.code] < o[other.code]:
			return True
		elif o[self.code] > o[other.code]:
			return False
		else:
			return self.num < other.num

	def setComponent(self, component):
		self.component = component

	def updateBox(self):
		if self.component == "":
			return
		self.component.name = self.code + str(self.num)
		s = "cross.png"
		if self.status == "OK":
			s = "check.png"
		self.component.source = "./status_icons/"+s

class Event():

	def __init__(self, name, instances, startTime):
		self.name = name
		self.instances = instances
		self.startTime = startTime

class SalesforceStatusApp(RelativeApp):

	updateTime = 300

	oldRunTime = 0

	setupDone = False

	boxes = {}

	statusString = StringProperty()
	affectedServers = StringProperty()

	def __init__(self,**kwargs):
		super(SalesforceStatusApp, self).__init__(**kwargs)

		self.statusString = "Loading server data..."
		self.affectedServers = ""

	def setup(self):
		super(SalesforceStatusApp, self).setup()

	def updateServers(self):
		self.servers = []
		count = 0
		response = jsonRequests.getResponse("https://api.status.salesforce.com/v1/instances/status")
		if response.status:
			jsonData = response.data
			self.servers = []
			for server in jsonData:
				if server["status"] != "OK":
					try:
						s = Server(server["key"],server["status"])
						self.servers.append(s)
					except:
						continue
			if len(self.servers) == 0:
				self.statusString = "All servers operational."
				self.affectedServers = ""
				self.ids.status.pos_hint = {"top":.7}
			else:
				issues = {svr.status.upper() for svr in self.servers}
				self.statusString = "Servers are impacted."
				if "MINOR_INCIDENT_CORE" in issues:
					self.statusString = "Minor incident."
				if "MAJOR_INCIDENT_CORE" in issues:
					self.statusString = "Major incident."
				self.affectedServers = makeServersString([svr.name for svr in self.servers], 8)
				self.ids.status.pos_hint = {"top":.9}
		else:
			Logger.error("Salesforce Status: Couldn't get latest calendar: "+response.message)

	def updateCalendar(self):
		response = jsonRequests.getResponse("https://api.status.salesforce.com/v1/maintenances?startTime="+time.strftime("%Y-%m-%d"))
		if response.status:
			jsonData = response.data
			evts = {}
			for evt in jsonData:
				name = evt["name"]
				timeString = evt["plannedStartTime"]
				start = time.strptime(timeString,"%Y-%m-%dT%H:%M:%S.000Z")
				if timeString+name not in evts:
					evts[timeString+name] = Event(name, set(evt["instanceKeys"]), start)
				else:
					for server in list(evt["instanceKeys"]):
						evts[timeString+name].instances.add(server)
			self.evts = list(evts.values())
			self.evts.sort(key=lambda x: x.startTime)
		else:
			Logger.error("Salesforce status: Couldn't get the latest status: "+response.message)

		for i in range(3):
			e = self.evts[i]
			box = self.ids["evt_"+str(i)]
			box.eventName = time.strftime("%m/%d/%y: ", e.startTime) + e.name
			svrs = []
			for name in e.instances:
				try:
					svrs.append(Server(name, ""))
				except:
					continue
			svrs.sort()
			box.servers = makeServersString([svr.name for svr in svrs], 6)


	def update(self, *args):
		super(SalesforceStatusApp, self).update(*args)

	def updateData(self):
		Logger.info("Salesforce Status: Updating data.")
		self.updateServers()
		self.updateCalendar()


def makeServersString(instances, amount = 10):
	if len(instances) > amount:
		l = instances[:amount]
		extras = len(instances) - amount
		return ", ".join(l) + " + " + str(extras) + " more"
	else:
		return ", ".join(instances)

class EventBox(RelativeLayout):

	eventName = StringProperty()
	servers = StringProperty()

	def __init__(self,**kwargs):
		super(EventBox, self).__init__(**kwargs)
		


if __name__ == "__main__":
	s1 = Server("NA01","OK")
	s2 = Server("NA02","OK")
	s3 = Server("CS02", "OK")
	print(s1)
	print(s2)
	print(s1 < s2)
	print(s2 < s1)

	print(s3<s2)
	print(s2<s3)

	servers = []
	count = 0
	response = jsonRequests.getResponse("https://api.status.salesforce.com/v1/instances/status")
	if response.status:
		jsonData = response.data
		for server in jsonData:
			try:
				s = Server(server["key"],server["status"])
				servers.append(s)
			except:
				continue
		servers.sort()
		for server in servers: print(server)
		print(len(servers))

	print("Getting upcoming events...")

	import requests

	r = requests.get("https://api.status.salesforce.com/v1/maintenances?startTime="+time.strftime("%Y-%m-%d"))
	if r.status_code == 200:
		jsonData = json.loads(r.text)
		evts = {}
		for evt in jsonData:
			name = evt["name"]
			timeString = evt["plannedStartTime"]
			start = time.strptime(timeString,"%Y-%m-%dT%H:%M:%S.000Z")
			if timeString+name not in evts:
				evts[timeString+name] = Event(name, set(evt["instanceKeys"]), start)
			else:
				for server in list(evt["instanceKeys"]):
					evts[timeString+name].instances.add(server)
		evts = list(evts.values())
		evts.sort(key=lambda x: x.startTime)


	instances = ["NA"+str(i) for i in range(20)]

	print(makeServersString(instances, 10))