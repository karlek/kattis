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
		command_browser = 'xdg-open "https://kth.kattis.com/submissions/%s"' % (ret)
		os.popen(command_browser).read()

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
			self.view.window().run_command('kattis_set')
			return

		# Submit the problem in new thread.
		KattisApiCall(script, problem, filename).start()

### Todo(u): Make a self.window.show_quick_panel call with all problems instead.
# Kattis - Set problem id.
class KattisSetCommand(sublime_plugin.WindowCommand):
	def load_settings(self):
		return sublime.load_settings('Kattis.sublime-settings')

	def run(self, **kwargs):
		# Callback function for show_input_panel.
		def on_done(id):
			self.load_settings().set(self.window.active_view().file_name(), id)
			self.window.active_view().run_command('kattis')

		self.window.show_input_panel("Kattis problem ID:", "", on_done, None, None)

