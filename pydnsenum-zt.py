import sys
import dns.query
import dns.zone
import dns.resolver

class DnsEnum:
	def __init__(self, domain):
		self.domain = domain

	def start(self):
		self.nameservers = self._getNameservers(self.domain)
		for ns in self.nameservers:
			result = self._doZoneTransfer(ns)
			self._logResult(ns, result)

	def _logResult(self, ns, result):
		if result == None:
			print "[!] Does not support zone transfer: %s" % (ns)
			return

		print "Result from NS: %s" % (ns)
		for r in result:
			print r

	
	def _getNameservers(self, domain):
		answers = dns.resolver.query(domain, 'NS')
		return [ns.to_text() for ns in answers]

	def _doZoneTransfer(self, ns):
		result = []
		try:
			z = dns.zone.from_xfr(dns.query.xfr(ns, self.domain))
			names = z.nodes.keys()
			names.sort()
			for n in names:
				result.append(z[n].to_text(n))
			
			return result
		except:
			return None

if len(sys.argv) != 2:
	print "Usage: %s DOMAIN" % (sys.argv[0])
	exit(-1)

d = DnsEnum(sys.argv[1])
d.start()

