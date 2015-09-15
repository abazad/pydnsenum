import socket
import struct
import sys

class DnsEnum:
	def __init__(self, ipstart, ipend, verbose=False):
		self.ipstart = ipstart
		self.ipend = ipend
		self.verbose = verbose

	def start(self):
		range = self._getIPRange(self.ipstart, self.ipend)
		for i in range:
			entry = self._checkIP(i)
			self._log(entry)

	# Hat tip: http://stackoverflow.com/questions/17220308/how-to-find-all-ip-addresses-between-2-ip-addresses
	def _getIPRange(self, start, end):
		ipstruct = struct.Struct('>I')
    		start, = ipstruct.unpack(socket.inet_aton(start))
    		end, = ipstruct.unpack(socket.inet_aton(end))
    		return [socket.inet_ntoa(ipstruct.pack(i)) for i in range(start, end+1)]

	def _log(self, entry):
		if entry[0] != None:
			print "Found DNS entry: %s (%s)" % (entry[1], entry[0])
		else:
			if self.verbose:
				print "DNS entry does not exist: %s" % (entry[1])
		
	def _checkIP(self, ip):
		try:
			name = socket.gethostbyaddr(ip)
			return (name[0], ip)
		except:
			return (None, ip)
			

if len(sys.argv) < 2:
	print "Usage: %s START [END] [-v]" % (sys.argv[0])
	exit(-1)

if len(sys.argv) == 4 and sys.argv[3] == "-v":
	d = DnsEnum(sys.argv[1], sys.argv[2], True)
elif len(sys.argv) == 3:
	d = DnsEnum(sys.argv[1], sys.argv[2])
elif len(sys.argv) == 2:
	d = DnsEnum(sys.argv[1], sys.argv[1])

d.start()
