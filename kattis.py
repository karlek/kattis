import sublime, sublime_plugin, os, threading

# Threading to avoid freeze lag when submitting.
class KattisApiCall(threading.Thread):
	def __init__(self, script, problem, filename):
		self.script = script
		self.problem = problem
		self.filename = filename
		threading.Thread.__init__(self)

	def run(self):
		# Run the submit script.
		command_kattis = "python2.7 %s -f -p %s %s" % (self.script, self.problem, self.filename)
		ret = os.popen(command_kattis).read().strip()

		# If the return is not an numerical id it's an error.
		if not ret.isnumeric():
			sublime.error_message(ret)
			return

		# Open the submission in the standard browser.
		open_url("https://open.kattis.com/submissions/%s" % (ret))

def open_url(url):
	command_browser = 'xdg-open "%s"' % (url)
	os.popen(command_browser).read()

# Threading to avoid freeze lag when opening description.
class KattisOpen(threading.Thread):
	def __init__(self, url):
		self.url = url
		threading.Thread.__init__(self)
	def run(self):
		# Open the submission in the standard browser.
		open_url(self.url)

# Kattis - Description
class KattisDescriptionCommand(sublime_plugin.TextCommand):
	def load_settings(self):
		return sublime.load_settings('Kattis.sublime-settings')

	def run(self, edit):
		# Current opened file in viewport.
		filename = self.view.file_name()
		# Problem ID.
		problem  = self.load_settings().get(filename)
		# If problem ID isn't set; query the user.
		if problem is None:
			self.view.window().run_command('kattis_set', {"submit":False})
			return
		KattisOpen("https://open.kattis.com/problems/%s" % (problem)).start()

# Kattis - Statistics
class KattisStatisticsCommand(sublime_plugin.TextCommand):
	def load_settings(self):
		return sublime.load_settings('Kattis.sublime-settings')

	def run(self, edit):
		# Current opened file in viewport.
		filename = self.view.file_name()
		# Problem ID.
		problem  = self.load_settings().get(filename)
		# If problem ID isn't set; query the user.
		if problem is None:
			self.view.window().run_command('kattis_set', {"submit":False})
			return
		KattisOpen("https://open.kattis.com/problems/%s/statistics" % (problem)).start()

# Kattis - Submit
class KattisCommand(sublime_plugin.TextCommand):
	def load_settings(self):
		return sublime.load_settings('Kattis.sublime-settings')

	def run(self, edit):
		# Current opened file in viewport.
		filename = self.view.file_name()
		# Problem ID.
		problem  = self.load_settings().get(filename)
		# Location of submit script.
		script   = sublime.packages_path()+"/kattis/submit.py"

		# If problem ID isn't set; query the user.
		if problem is None:
			self.view.window().run_command('kattis_set', {"submit":True})
			return

		# Submit the problem in new thread.
		KattisApiCall(script, problem, filename).start()

### Todo(u): Make a self.window.show_quick_panel call with all problems instead.
# Kattis - Set problem id.
class KattisSetCommand(sublime_plugin.WindowCommand):
	def load_settings(self):
		return sublime.load_settings('Kattis.sublime-settings')

	def run(self, **kwargs):
		# Callback functions for show_input_panel.
		def on_done(id):
			self.load_settings().set(self.window.active_view().file_name(), id)
		def on_done_submit(id):
			self.load_settings().set(self.window.active_view().file_name(), id)
			self.window.active_view().run_command('kattis')

		filename, _ = os.path.splitext(self.window.active_view().file_name())

		set_func = on_done
		if kwargs["submit"]:
			set_func = on_done_submit
		self.window.show_input_panel("Kattis problem ID:", os.path.basename(filename), set_func, None, None)

