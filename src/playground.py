import random
# import markdown
import optparse

def path():
	description = "a tool"
	p = optparse.OptionParser(description=description,
								prog="tool",
								version="tool 0.0",
								usage= "%prog [starting d][action]")
	p.add_option('--pattern','-p',
				help="oh fuck!",default="22")
	p.add_option("--list",'-l',action="store_true",
				help='lists',default=False)
	options, arguments = p.parse_args()
	print options
	print arguments

if __name__ == '__main__':
	path()