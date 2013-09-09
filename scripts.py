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
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class Runnable(object):
    @staticmethod
    def run(feed_data, parsed_entries_guids, **options):
        raise NotImplementedError

class transmissionDaemonScript(Runnable):

	_default_options = {
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
		'host' : '127.0.0.1',
	}

	@staticmethod
	def run(feed_data, parsed_entries_guids, options):

		for key in options:
			if not key in _default_options:
				raise KeyError

		for key in _default_options:
			if not key in options:
				options[key] = _default_options[key]

		for entry in feed_data.entries:
			if not entry.guid in parsed_entries_guids:
				for link in entry.links:
					if link['type'] == 'application/x-bittorrent':
						os.system(create_command(link['href'], options))

	@staticmethod
	def create_command(location, options):
		command = 'transmission-remote'
		if options['host']:
			command += ' ' + str(options['host'])
		if options['port']:
			command += ' ' + str(options['port'])
		if options['username']:
			command += ' --auth=' + str(options['username'])
		if options['password']:
			command += ':' + str(options['password'])
		if location:
			command += ' --add ' + str(location)
		if options['incomplete-dir']:
			command += ' --incomplete-dir ' + str(options['incomplete_dir'])
		if options['download_dir']:
			command += ' --download-dir ' + str(options['download_dir']) 
		return command
