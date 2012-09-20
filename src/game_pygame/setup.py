from distutils.core import setup
import py2exe
import glob
options = {"py2exe":
			{	"compressed":1,
				"optimize":2,
				"bundle_files": 1},
			}
setup(
	options=options,
	windows=["war_fog.py"],
	data_files=[("resource",glob.glob("resource/*"))]
	)