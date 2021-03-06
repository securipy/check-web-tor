#!/usr/bin/python
#-*-coding:utf-8-*-
#- Interhack

#- Check-web-tor
#- Copyright (C) 2015 Interhack 
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License 
# as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version. 
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty 
# of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details. 
# You should have received a copy of the GNU General Public License along with this program. If not, see <http://www.gnu.org/licenses/>



import sys
from contextlib import closing
from optparse import OptionParser
import argparse
import socks  # $ pip install PySocks
from sockshandler import SocksiPyHandler  # see pysocks repository, pip install pysocks
import stem.process  # $ pip install stem
from stem.util import term
import urllib2


__author__ 		= "interhack"
__credits__ 	= "interhack"
__version__ 	= "0.1.1"
__maintainer__ 	= "Securipy"
__email__ 		= "interhack@gmail.com"
__status__ 		= "Development"


class tor(object):
	def __init__(self, ip= 'localhost' ,port=7000, nodes='{ru}', verbose=None):
		self.ip = ip
		self.tor_cmd = 'tor'
		self.port = port
		self.config = dict(SocksPort=str(self.port), ExitNodes=nodes)

		self.verbose = verbose

		self.launch_tor()

	def print_bootstrap_lines(self,line):
		if "Bootstrapped " in line:
			print(term.format(line, term.Color.BLUE))
		else:
			print(line)

	def launch_tor(self):
		print(term.format("Starting Tor:\n", term.Attr.BOLD))
		try:
			if self.verbose == 1 or self.verbose == '1':
				self.tor_process = stem.process.launch_tor_with_config(
					tor_cmd=self.tor_cmd,
					config=self.config,
					init_msg_handler=self.print_bootstrap_lines,
				)
			else:
				self.tor_process = stem.process.launch_tor_with_config(
					tor_cmd=self.tor_cmd,
					config=self.config,
					init_msg_handler='',
				)
		except:
			print("Error starting Tor, check that it does not already started, or is installed")
			sys.exit(0)
		print(term.format("\nOutput created\n", term.Attr.BOLD))

	def quit(self):
		if self.tor_process.poll() is None:
			self.tor_process.terminate()
			self.tor_process.wait()

	def query(self, url):
		opener=urllib2.build_opener(SocksiPyHandler(socks.PROXY_TYPE_SOCKS5, self.ip, self.port))
		try:
			with closing(opener.open(url)) as r:
				return r.read()
			
		except:
			print(" You need specify a correct url(with http/https)")
			self.quit()
			sys.exit(0)

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Designed for easy navigation in the Tor network')
	parser.add_argument('-u', '--url', metavar='url', dest='url', help='Insert url for check ')
	parser.add_argument('-p', '--port', metavar='port', dest='port', help='Port for tor network')
	parser.add_argument('-i', '--ip', metavar='ip', dest='ip', help='Ip for tor network')
	parser.add_argument('-n', '--nodes', metavar='nodes', dest='nodes', help='Output nodes, for tor network')
	parser.add_argument('-v', '--verbose', metavar='verbose', dest='verbose', help='Mode Verbose')
	options = parser.parse_args()

	while options.url == None or options.url == '':
		print("ex: http://ofkztxcohimx34la.onion")
		options.url = raw_input('You need a Url: ')

	if options.ip == None:
		options.ip = 'localhost'
	if options.port == None:
		options.port = 7000
	else:
		try:
			options.port = int(options.port)
		except:
			print("You need a port number")
			sys.exit(0)
	if options.nodes == None:
		options.nodes = '{ru}'

	if options.verbose == None:
		options.verbose = 0
	

	tor_net = tor(ip=options.ip, port=options.port, nodes=options.nodes, verbose=options.verbose)
	print tor_net.query(options.url)
	tor_net.quit()
	