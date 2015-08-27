#!/usr/bin/env python
import re, os, os.path, csv, geoip

def getCountry(ip):
	country =geoip.country(ip.strip())
	if len(country) ==0:
		return "N/A"
	return country

def getData(fileName):
	pattern1 = re.compile('[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}')
	pattern2 = re.compile('[ :][0-9][0-9]:[0-9][0-9]:[0-9][0-9]')
	f = open (fileName, "r")
	ip =[]
	times ={}
	locations ={}
	
	for line in f:
		for match in re.findall(pattern1,line):
			if match not in ip :
				x = match.split(".")
				x= map(int,x)
				if x[0]>255 or x[1]>255 or x[2]>255 or x[3]>255:
					continue
				ip.append(match)
				country = getCountry(match)
				if country in locations:
					locations[country]+=1
				else:
					locations[country]=1
					
		time = re.search(pattern2, line)
		if time:
			time = time.group(0)
			hour = time[1:3]
			if hour in times:
				times[hour]+=1
			else:
				times[hour]=1
	f.close()
	return len(ip),times,locations

for f in sorted(os.listdir(os.getcwd())):
	if f.endswith("log"):
		print "Data for: " + f
		distinct,times, locations = getData(f)

		t=sorted(times, key=lambda k: times[k],reverse =True)
		print "Top time intervals:"
		for i in range(min(3,len(t))):
			print ">{0}-{1}: {2} times".format(int(t[i]), int(t[i])+1, times[t[i]])
			
		t=sorted(locations, key=lambda k: locations[k],reverse =True)
		print "Top Countries:"
		for i in range(min(3,len(t))):
			print ">{0}: {1} times".format(t[i], locations[t[i]])
			
		print "Number of unique IPs: {0}".format(distinct)
		print ""
		
print "Done!"