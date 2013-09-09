import argparse

parser = argparse.ArgumentParser(
	description='FeedMachine')

parser.add_argument(
	'database', metavar='database',
	help='The location of the database',
	type=str, nargs=1)

# Command Parser
subparsers = parser.add_subparsers(
	title='Commands',
	description='Commands description',
	help='Commands help')

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

# Command Add
parserAdd.add_argument(
	'location', metavar='<location>',
	help='Location of the feed',
	type=str, nargs=1)
# Command Attach
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
# Command Detach
parserDetach.add_argument(
	'scriptId', metavar='<scriptid>',
	help='',
	type=int, nargs=1)

if __name__ == '__main__':
	args = parser.parse_args()
	print(args)
