# Copyright (C) 2013, Cameron White
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
# 3. Neither the name of the project nor the names of its contributors
#    may be used to endorse or promote products derived from this software
#    without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE PROJECT AND CONTRIBUTORS ``AS IS'' AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE PROJECT OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
# OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
# OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
# SUCH DAMAGE.
class RssTransmissionDaemon(object):

	def __init__(self, db, feed_id, *args, **kargs):

		self.defaults = {
			'username' : None,
			'password' : None,
			'incomplete_dir' : None,
			'download_dir' : None,
			'down_limit' : None,
			'up_limit' : None,
			'cache_size' : None,
			'encryption_usage' : 'preferred',
			'peer_limit' : None,
			'port' : 9091,
			'host' : 127.0.0.1,
		}

		for key in kargs:
			if key in defaults:
				self.defaults[key] = kargs[key]

		feed = db.get_feed(feed_id)
		guids = db.get_parsed_entries_guids(feed_id)

		for entry in feed.entries:
			if not entry.guid in guids:
				for link in entry.links:
					if link['type'] == 'application/x-bittorrent':
						self.add_torrent(link['href'])
				db.set_parsed(feed_id, entry.guid)

	def add_torrent(location):
		command = 'transmission-remote
		command += ' ' + self.defaults['host'] if self.defaults['host']
		command += ' ' + self.defaults['port'] if self.defaults['port']
		command += ' --auth=' + self.defaults['username'] if self.defaults['username']
		command += ':' + self.defaults['password'] if self.defaults['password']
		command += ' --add ' + str(location)
		command += ' --incomplete-dir ' + self.defaults['incomplete_dir'] if self.defaults['incomplete_dir']
		command += ' --download-dir ' + self.defaults['download_dir'] if self.defaults['download_dir']
