import socket
import sys

class DnsEnum:
	def __init__(self, domain, file, verbose=False):
		self.domain = domain
		self.file = file
		self.verbose = verbose

	def start(self):
		self._processFile(self.file)

		for s in self.subdomains:
			entry = self._checkDomain(s, self.domain)
			self._log(entry)

	def _log(self, entry):
		if entry[0] != None:
			print "Found DNS entry: %s (%s)" % (entry[1], entry[0])
		else:
			if self.verbose:
				print "DNS entry does not exist: %s" % (entry[1])
		


	def _checkDomain(self, subdomain, domain):
		try:
			check = subdomain + '.' + domain
			ip = socket.gethostbyname(check)
			return (ip, check)
		except:
			return (None, check)
			

	def _processFile(self, file):
		with open(file) as f:
			self.subdomains = [x.strip('\n') for x in f.readlines()]
		

if len(sys.argv) < 3:
	print "Usage: %s DOMAIN FILE [-v]" % (sys.argv[0])
	exit(-1)

if len(sys.argv) == 4 and sys.argv[3] == "-v":
	d = DnsEnum(sys.argv[1], sys.argv[2], True)
else:
	d = DnsEnum(sys.argv[1], sys.argv[2])

d.start()
