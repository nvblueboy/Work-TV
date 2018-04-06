import numpy as np
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm, rcParams

import json, random
import jsonRequests

def multiplyColor(c, a): return tuple((i*a for i in c))


def nearColor(a,  b):
	l = [abs(x-y) for (x,y) in zip(a,b)]
	threshold = .1
	for i in l:
		if i > threshold:
			return False
	return True

def checkColors(l, a):
	for i in l:
		if nearColor(i, a):
			return True
	return False

#Resolution
width = 1920.0
height = 864.0
DPI = float(72)

#Bar Width
bar_width = 0.8

#Base color
base_color = (.280, .592, 1)


plt.rc('font',family='serif')
plt.rc('font',serif='Roboto')

#title font
titleFont = {"fontsize":70, "family":'serif', "weight":"light"}


#axis font
axisFont = {"fontsize":30}



def saveImage(jsonData, outputFile):

	fig = plt.figure(figsize=(width/DPI, height/DPI), dpi=DPI)
	plt.ylim(ymax=10)
	names = sorted([result["name"] for result in jsonData["results"]])
	people = []
	index = 0

	##Iterate through everything and get the names of every account.

	accts = set()
	for result in jsonData["results"]:
		for acct in result["accts"]:
			accts.add(acct["name"])

	accts = list(accts)
	internals = ["1 - SA - Internal", "2 - SA - App Dev"]

	for internal in internals:
		if internal in accts:
			accts.remove(internal)

	internals.sort()

	accts = accts + internals


	colorDict = {"1 - SA - Internal":(.5,.5,.5), "2 - SA - App Dev":(.7,.7,.7)} # Map account to color.
	usedColors = []

	bars = []
	acct_list = []

	for result in jsonData["results"]:
		if len(result["accts"]) > 0:
			resource_name = result["name"]
			people.append(resource_name)
			bottom = 0
			for acct_name in accts:
				for acct in result["accts"]:
					if acct_name == acct["name"]:
						name = acct["name"]

						if name not in colorDict:
							c = base_color
							while (checkColors(usedColors, c)):
								strength = random.random()
								c = multiplyColor(base_color, strength)
							colorDict[name]=c
							usedColors.append(c)

						color = colorDict[name]
						amt = acct["amount"]
						p, = plt.bar(index, (amt), bar_width, bottom=bottom, color=color, label=name)
						if name not in acct_list:
							bars.append(p)
							acct_list.append(name)
			
						bottom = bottom + amt

			index = index + 1

	plt.legend(handles=bars, labels=acct_list, loc=1, fontsize="large")

	low_bar_height = 4.5

	values = list([low_bar_height for i in range(len(people))])

	plt.plot(np.arange(len(people)), values , color=(0,0,0))

	high_bar_height = 9

	values = list([high_bar_height for i in range(len(people))])

	plt.plot(np.arange(len(people)), values , color=(0,0,0))

	plt.title('Hours by account',fontdict=titleFont)
	plt.tick_params(axis='both', which='major', labelsize=17)
	plt.xticks(np.arange(len(people)), people)
	plt.yticks(np.arange(0, 12, 2))
	plt.ylabel('Hours Spent', fontdict = axisFont)


	plt.savefig(outputFile)

def getJsonData():
	url = "https://www.softwareanywhere.com/services/apexrest/TimeSlips"
	response = jsonRequests.getResponse(url)
	if response.status:
		parsed = json.loads(response.raw.decode('string-escape').strip('"'))
		return parsed
	else:
		return False


if __name__ == "__main__":
	jsonData = getJsonData()

	saveImage(jsonData, "testGraph.png")

