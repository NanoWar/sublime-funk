import sublime, sublime_plugin
import os
import subprocess
import signal

# Consts
THIS_PLUGIN_NAME = 'sublime-funk'
THIS_PLUGIN_DEBUG = True

# Initialize plugin
def FunkInit():
	global Funk_DIR, Funk_SYNTAX_FILE, Funk_SNIP_DIR, Funk_HELP_DIR
	Funk_DIR = os.path.join(sublime.packages_path(), THIS_PLUGIN_NAME)
	Funk_SYNTAX_FILE = 'Packages/' + THIS_PLUGIN_NAME + '/' + THIS_PLUGIN_NAME + '.tmLanguage'
	Funk_SNIP_DIR = 'Packages/' + THIS_PLUGIN_NAME + '/' + 'snippets'
	Funk_HELP_DIR = Funk_DIR + '/' + 'helps'



# Debug print
def dbgprint(s):
	if THIS_PLUGIN_DEBUG:
		print ("# FunkAsm:",s)
		sublime.status_message(s)



# Command handler class
class FunkDoCmdCommand(sublime_plugin.WindowCommand):
	# Command handler
	def run(self, cmd):

		# New example files
		if cmd=="NewFunkProgram":
			v=self.window.new_file()
			v.set_syntax_file(Funk_SYNTAX_FILE)
			v.run_command("insert_snippet", {"name": Funk_SNIP_DIR+'/new_funk_program.sublime-snippet'})
			dbgprint("New Funk program created")
		elif cmd=="NewFunkApp":
			v=self.window.new_file()
			v.set_syntax_file(Funk_SYNTAX_FILE)
			v.run_command("insert_snippet", {"name": Funk_SNIP_DIR+'/new_funk_app.sublime-snippet'})
			dbgprint("New Funk app created")
		elif cmd=="NewFunkConfig":
			v=self.window.new_file()
			v.set_syntax_file(Funk_SYNTAX_FILE)
			v.run_command("insert_snippet", {"name": Funk_SNIP_DIR+'/new_funk_config.sublime-snippet'})
			dbgprint("New Funk config created")
		elif cmd=="NewTI83pProgram":
			v=self.window.new_file()
			v.set_syntax_file(Funk_SYNTAX_FILE)
			v.run_command("insert_snippet", {"name": Funk_SNIP_DIR+'/new_ti83p_program.sublime-snippet'})
			dbgprint("New TI83P program created")

		# Build scripts
		elif cmd=="BuildFunk":
			self.window.run_command("build")
			dbgprint("Funk build script started")
		elif cmd=="BuildFunkApp":
			self.window.run_command("build", {"variant": "Build Funk App"})
			dbgprint("Funk App build script started")
		elif cmd=="BuildSpasmTI83p":
			self.window.run_command("build", {"variant": "Build Spasm TI83p"})
			dbgprint("SPASM TI83+ build script started")
		elif cmd=="BuildSpasmTI83pApp":
			self.window.run_command("build", {"variant": "Build Spasm TI83p APP"})
			dbgprint("SPASM TI83+ App build script started")

	# Disable not implemented items
	def is_enabled(self, cmd):
		return True
		if cmd not in ["BuildTasm"]:
			return True



# Helps
class FunkHelpCommand(sublime_plugin.WindowCommand):
	def run(self, indx):
		n=self.help_list()
		self.window.run_command("open_file", {"file": "${packages}/"+THIS_PLUGIN_NAME+"/helps/"+n[indx]})

	# Scan helps folder for files (10 max)
	def help_list(self):
		lst=os.listdir(Funk_HELP_DIR)
		lst.sort()
		return lst[:15]

	# Show help
	def is_visible(self, indx):
		n=self.help_list()
		if indx<len(n):
			return True
		return False

	# Show help names
	def description(self, indx):
		n=self.help_list()
		if indx<len(n):
			return n[indx]
		return ""



# Quick help - F1
class FunkQuickHelpCommand(sublime_plugin.WindowCommand):
	# Init: read items from file
	def __init__(self, *args, **kwargs):
		self.help=[]
		with open(Funk_DIR+'/'+THIS_PLUGIN_NAME+'.quickhelp','rt') as f:
			self.help = [line.strip() for line in f]

		super(FunkQuickHelpCommand,self).__init__(*args, **kwargs)

	# Show help
	def run(self):
		self.window.show_quick_panel(self.help, None, sublime.MONOSPACE_FONT)


wabbitemu_process = None

# Command handler class
class FunkEmulateCommand(sublime_plugin.WindowCommand):
	# Command handler
	def run(self):
		global wabbitemu_process
		dbgprint("Looking for emulator")
		project_dir = os.path.abspath(os.path.dirname(self.window.project_file_name()))
		wabbitemu = project_dir + "/wabbitemu.exe"

		program = None
		for entry in os.listdir(project_dir):
			if entry.endswith(".8xk") or entry.endswith(".8xp"):
				program = entry
				dbgprint("Found program " + entry)

		if program and os.path.isfile(wabbitemu):
			dbgprint("Found wabbitemu in project dir")
			process = subprocess.Popen([wabbitemu, "-F", project_dir + "/" + program])

			# if wabbitemu_process and wabbitemu_process.poll() == None:
			# 	dbgprint("Using existing emulator")
			# 	process.kill()
			# else:
			# 	dbgprint("Starting new emulator")
			# 	wabbitemu_process = process

			if wabbitemu_process:
				dbgprint("Killing existing emulator")
				wabbitemu_process.kill()
			dbgprint("Starting new emulator")
			wabbitemu_process = process

# Autocompletion class
class FunkAutocomplete(sublime_plugin.EventListener):
	# Generate completion list from all opened tabs
	def on_query_completions(self, view, prefix, locations):
		# Check if option is enabled
		if view.settings().get("use_global_completion") != True:
			return []

		# List of all views (our one is always first)
		views = [view] + [v for v in sublime.active_window().views() if v.id() != view.id()]
		compl=[]
		for v in views:
			if v.id() == view.id():
				# For our view use cursor location
				words = v.extract_completions(prefix,locations[0])
			else:
				words = v.extract_completions(prefix)
			# Add only unique words
			for w in words:
				if w not in compl:
					compl.append(w)

		return [(el, el) for el in compl]



# Define plugin_loaded() function for ST3 because it's have another plugin lifecycle
# (cannot call sublime.packages_path() at importing time). For ST2 fust call FunkInit().
if int(sublime.version())>=3000:
	def plugin_loaded():
		FunkInit()
else:
	FunkInit()

dbgprint("FunkAsm plugin started")
