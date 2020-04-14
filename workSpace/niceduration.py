

minutesToSeconds = 60
hoursToSeconds = minutesToSeconds * 60
daysToSeconds = 24 * hoursToSeconds

def SecondsToNiceDuration(seconds):
	days = int(seconds / daysToSeconds)
	seconds -= days * daysToSeconds

	hours = int(seconds / hoursToSeconds)
	seconds -= hours * hoursToSeconds

	minutes = int(seconds / minutesToSeconds)
	seconds -= minutes * minutesToSeconds
	
	s = ""

	if days > 0:
		s = s + "%d days " % days
	if hours > 0:
		s = s + "%d hours " % hours
		return s

	if minutes > 0:
		s = s + "%d minutes " % minutes
	if seconds > 0:
		s = s + "%d seconds" % seconds

	return s