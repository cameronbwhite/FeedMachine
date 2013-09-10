import argparse
from core import *

parser = argparse.ArgumentParser(
	description='FeedMachine')

# database - Positional Argument
parser.add_argument(
	'database', metavar='database',
	help='The location of the database',
	type=str, nargs=1)

# Command - Sub Parser
subparsers = parser.add_subparsers(
	title='Commands',
	description='Commands description',
	help='Commands help',
	dest='command')

# Commands
parserAdd = subparsers.add_parser(
	'add', help='Add a feed to the database')
parserAttach = subparsers.add_parser(
	'attach', help='Attach a script to a feed')
parserDetach = subparsers.add_parser(
	'detach', help='Detach a script to a feed')
parserRemove = subparsers.add_parser(
	'remove', help='Remove a feed from the database')
parserUpdate = subparsers.add_parser(
	'update', help='Update the database')
parserList = subparsers.add_parser(
	'list', help='List stuff')

# Add - Command
parserAdd.add_argument(
	'location', metavar='<location>',
	help='Location of the feed',
	type=str, nargs=1)

# Attach - Command
parserAttach.add_argument(
	'feedId', metavar='<feedid>',
	help='ID of the feed',
	type=int, nargs=1)
parserAttach.add_argument(
	'scriptName', metavar='<scriptname>',
	help='Name of the script',
	type=str, nargs=1)
parserAttach.add_argument(
	'options', metavar='[options]',
	help='',
	type=str, nargs=argparse.REMAINDER)

# Detach - Command
parserDetach.add_argument(
	'scriptId', metavar='<scriptid>',
	help='',
	type=int, nargs=1)

if __name__ == '__main__':
	args = parser.parse_args()
	feedDB = FeedDB(args.database[0])

	if args.command == 'add':
		feedDB.addFeed(args.location[0])
		pass
	elif args.command == 'attach':
		# feedId scriptName **options
		pass
	elif args.command == 'detach':
		# scriptId
		feedDB.removeScriptById(args.scriptId)
		pass
	elif args.command == 'remove':
		# feedId or location
		feedDB.removeFeedById(args.feedId)
		pass
	elif args.command == 'list':
		# "some command string"
		for feed in feedDB.getAllFeeds():
			print('id: {}, title: {}, location: {}'.\
				format(feed.id, feed.data.feed.title, feed.location))

	elif args.command == 'update':
		feedDB.updateAndRunAll()
	else:
		# Throw Error
		pass