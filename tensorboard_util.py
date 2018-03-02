import os
import sys
import subprocess  # NEW WAY!

if "win32" in sys.platform:
	tensorboard_logs = './logs/' # windows friendly
else:
	tensorboard_logs = '/tmp/tensorboard_logs/'

global logdir
logdir=tensorboard_logs

def get_last_tensorboard_run_nr():
	try:
		logs=subprocess.check_output(["ls", tensorboard_logs]).split("\n")
	except:
		if not os.path.exists(logdir):
			os.system("mkdir " + tensorboard_logs)
		print("first run!")
		return 0
	# print("logs: ",logs)
	runs=map(lambda x: (not x.startswith("run") and -1) or int(x[-1]) ,logs)
	# print("runs ",runs)
	if runs==9: runs=0 # restart
	return max(runs)+1



def set_tensorboard_run(reset=False,auto_increment=True,run_nr=-1):
	if run_nr < 1 or auto_increment:
		run_nr = get_last_tensorboard_run_nr()
	if run_nr == 0 or reset:
		run_nr=0
		clear_tensorboard()
	print("RUN NUMBER " + str(run_nr))
	global logdir
	last = tensorboard_logs + 'run' + str(run_nr - 1)
	if run_nr>0 and (not os.path.exists(last) or len(os.listdir(last))==0):
		run_nr -= 1  #   previous run was not successful

	logdir = tensorboard_logs + 'run' + str(run_nr)
	if not os.path.exists(logdir):
		os.system("mkdir " + logdir)


def clear_tensorboard():
	os.system("rm -rf %s/*" % tensorboard_logs)  # sync

def nop():
	return tf.constant("nop")
	# pass

def show_tensorboard():
		# add in /usr/local/lib/python2.7/site-packages/tensorflow/tensorboard/dist/index.html :
		# <link rel="stylesheet" type="text/css" href="plottable/plottable.css"> due to BUG in tf 10.0
		print("run: tensorboard --debug --logdir=" + tensorboard_logs+" and navigate to http://0.0.0.0:6006")

def kill_tensorboard():
	os.system("ps -afx | grep tensorboard | grep -v 'grep' | awk '{print $2}'| xargs kill -9")

def current_logdir():
	print("current logdir: "+logdir)
	return logdir

def run_tensorboard(restart=False,show_browser=False):
	if restart: kill_tensorboard()
		#  cd /usr/local/lib/python2.7/dist-packages/tensorflow/tensorboard/ in tf 10.0 due to BUG
		# ,cwd="/usr/local/lib/python2.7/dist-packages/tensorflow/tensorboard"
	try:
		subprocess.Popen(["tensorboard", '--logdir=' + tensorboard_logs])  # async
	except:
		print("tensorboard missing, install if you like")
	# os.system("sleep 5; open http://0.0.0.0:6006")
	if show_browser:
		subprocess.Popen(["open", 'http://0.0.0.0:6006'])  # async

# run_tensorboard()
