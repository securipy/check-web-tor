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

	def print_bootstrap_lines(self,line):
		if "Bootstrapped " in line:
			print(term.format(line, term.Color.BLUE))
		else:
			print(line)

	def launch_tor(self):
		print(term.format("Starting Tor:\n", term.Attr.BOLD))
		try:
			if self.verbose == 1:
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
			print("Error al levantar tor comprueba que no este iniciado ya, o no este instalado")
			sys.exit(0)
		print(term.format("\Output created\n", term.Attr.BOLD))

	def quit(self):
		if self.tor_process.poll() is None:
			self.tor_process.terminate()
			self.tor_process.wait()

	def query(self, url):
		self.launch_tor();opener=urllib2.build_opener(SocksiPyHandler(socks.PROXY_TYPE_SOCKS5, self.ip, self.port))
		try:
			with closing(opener.open(url)) as r:
				return r.read()
			
		except:
			print(" You need specify a correct url(with http/https)")
			self.quit()
			sys.exit(0)

if __name__ == '__main__':
	print("ex: http://ofkztxcohimx34la.onion")
	url = raw_input("Url: ")
	oculto = tor()
	print oculto.query(url)
	oculto.quit()
	