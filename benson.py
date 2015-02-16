import matplotlib.pyplot as plt
import numpy as np
import pandas as ps
import scipy
from collections import Counter
from dateutil import parser
from itertools import groupby
from operator import itemgetter
from pprint import pprint

#challenge 1
def makeDict(fileName):
	""""read a text file as data frame, then return a dictionary
		fileName: str, name of the text file
		mtaDict: dictionary based on the mta data"""
	
	df = ps.read_csv(fileName, header=False)
	tmp = df.iloc[0:9000,]
	mtaDict = {}
	
	for i in range(0, len(df)):
		key = tuple(df.iloc[i, 0:4])
		l = list(df.iloc[i, 5:])
		if key not in mtaDict:
			mtaDict[key] = [l]
		else:
			mtaDict[key].append(l)
		
	return mtaDict

#challenge 2
def timeSeries(dt):
	"""For each key, list is the point in time and the cumulative
		count of entries.
		dt: dictionary """
	
	for key, series in dt.iteritems():
		for i in range(len(series)):
			series[i][0] =(parser.parse(series[i][1] + 'T' + series[i][2]))
			series[i][1] = series[i][4]
			series[i][2:] = []

	return dt

#challenge 3
def totalDaily(dt):
	"""total daily entries 
		dt: dictionary
		total_daily: dictionary for daily counts"""
		
	total_daily = {}
	
	for key, series in dt.iteritems():
		all_counts ={}
		series.sort(key=itemgetter(0))#sorting by the 1st item in list
		for date, count in groupby(series, lambda x:x[0].date()):
			l=[]
			for i in count:
				l.append(i[1])
			all_counts[date] = l
		
		for key2, series2 in all_counts.iteritems():
			all_counts[key2] = max(series2)-min(series2)
		
		total_daily[key] = all_counts.items()
		
	return total_daily

#challenge 4
def plotDaily(dt):
	"""plot the daily time series for a turnstile, default is set to first one
		dt: dictionary"""
	
	dates, counts = [], []
	
	for key, value in dt.iteritems():
		for date, count in value:
			dates.append(date)
			counts.append(count)
		break
	
	plt.plot(dates, counts, 'o')
	plt.setp(plt.gca().get_xticklabels(), rotation=45)
	plt.margins(0.2)
	plt.ylabel('Counts')
	plt.tight_layout()
	plt.show()

#challenge 5
def combo(dt):
	"""combine turnstiles in the same ControlArea/Unit/Station combo
		dt: dictionary"""
	
	combo_dt = {}
	
	for key, series in dt.iteritems():
		new_key = list(key)
		del new_key[2]
		new_key = tuple(new_key)
		for l in series:
			if new_key not in combo_dt:
				combo_dt[new_key] = [l]
			else:
				combo_dt[new_key].append(l)
	
	combo_dt = addUp(combo_dt)
	
	return combo_dt

#cumulative values from a list
def addUp(dt):
	for keys, values in dt.iteritems():
		c = Counter()
		for dates, counts in values:
			c[dates] += counts
		dt[keys] = c.items()
	
	return dt
	
#challenge 6
def station(dt):
	"""combine everything in each station
		dt: dictionary"""
	
	station_dt = {}
	for keys, values in dt.iteritems():
		new_keys = keys[2]
		for l in values:
			if new_keys not in station_dt:
				station_dt[new_keys] = [l]
			else:
				station_dt[new_keys].append(l)
	
	station_dt = addUp(station_dt)
	
	return station_dt

#challenge 7
def plotStation(dt):
	"""plot the time series for a station, default is the first one"""

	plotDaily(dt)
	
#challenge 8
def weekTotal(dt):
	"""make one list of counts for one week for one station
		default to 1st key"""
	day_counts = Counter()
	day_total = []
	
	for station, time_series in dt.iteritems():
		for dates, counts in time_series:
			weekDay = dates.isoweekday()
			day_counts[weekDay] += counts
		break
	day_total = sorted(day_counts.items())
	return day_total

def plotWeekTotal(dt1, dt2, dt3):
	week1 = weekTotal(dt1)
	week2 = weekTotal(dt2)
	week3 = weekTotal(dt3)

	plt.plot(week1, 'bo')
	plt.plot(week1, color='blue')
	plt.plot(week2, 'go')
	plt.plot(week2, color='green')
	plt.plot(week3, 'o', color='purple')
	plt.plot(week3, color='purple')
	line1, = plt.plot([1,2,3], color='blue', label='week 1')
	line2, = plt.plot([1,2,3], color='green', label='week 2')
	line3, = plt.plot([1,2,3], color='purple', label='week 3')
	
	plt.ylim([2000,18000])
	plt.margins(0.05)
	plt.legend(handles=[line1, line2, line3])
	plt.show()	

#challenge 9
def totalRiderShip(dt):
	"""sum up the total ridership and find out the station with the highest
		traffic value"""
	total_rider = {}
	for keys, values in dt.iteritems():
		total = 0
		for dates, counts in values:
			total += counts
		total_rider[keys] = total
	
	total_rider = sorted(total_rider.items(), key=itemgetter(1))
	return total_rider	

#challenge 10
def plotTotal(dt):
	"""make a single list of total ridership values and plot it with"""
	station, counts = [], []
	for i in range(len(dt)):
		station.append(dt[i][0])
		counts.append(dt[i][1])

	indices = range(len(counts))
	plt.bar(indices, counts)
	plt.show()


def main():
	#challenge 1
	dt1 = makeDict('turnstile_141227.txt')
	dt2 = makeDict('turnstile_150103.txt')
	dt3 = makeDict('turnstile_150110.txt')
	#challenge 2
	dt1 = timeSeries(dt1)
	dt2 = timeSeries(dt2)
	dt3 = timeSeries(dt3)
	#challenge 3
	dt1 = totalDaily(dt1)
	dt2 = totalDaily(dt2)
	dt3 = totalDaily(dt3)
	#challenge 4
	plotDaily(dt1)
	#challenge 5
	dt1=combo(dt1)
	dt2=combo(dt2)
	dt3=combo(dt3)
	#challenge 6
	dt1=station(dt1)
	dt2=station(dt2)
	dt3=station(dt3)
	#challenge 7
	plotStation(dt1)
	#challenge 8
	plotWeekTotal(dt1,dt2,dt3)
	#challenge 9
	dt1=totalRiderShip(dt1)
	#challenge 10
	plotTotal(dt1)
	#pprint (dt1)

if __name__ == '__main__':
	main()