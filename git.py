import sublime, sublime_plugin
import os
import functools

class GitCommand(sublime_plugin.WindowCommand):
    """
    GitCommand is a WindowCommand for running simple git commands from within
    Sublime Text 2.  Instead of using the Default exec.py implementation which
    outputs to the Build Results window, it creates a new scratch file in its
    own view and displays the results there.  It will attempt to set a proper
    language syntax file when it makes sense too, as well.
    """
    commands = [
        {
            "description": "Log with patch",
            "arguments": ["log", "--stat", "--patch", "--max-count=2"],
            "syntax_file": "Packages/Diff/Diff.tmLanguage"
        },
        {
            "description": "Diff",
            "arguments": ["diff", "--patch-with-stat"],
            "syntax_file": "Packages/Diff/Diff.tmLanguage"
        },
        {
            "description": "Blame",
            "arguments": ["blame"],
            "syntax_file": "based_on_extension"
        },
        {
            "description": "Log",
            "arguments": ["log", "--stat"]
        }
    ]

    # File extension to language syntax file mapping.
    syntaxes = {
        ".js": "Packages/JavaScript/JavaScript.tmLanguage",
        ".py": "Packages/Python/Python.tmLanguage"
    }

    def quick_panel_callback(caller, index):
        if index == -1: return

        self = caller
        active_file = os.path.split(self.window.active_view().file_name())[1]
        active_file_ext = os.path.splitext(active_file)[1]
        working_dir = os.path.dirname(self.window.active_view().file_name())
        selected_command = GitCommand.commands[index]

        cmd = ["git"]
        cmd.extend(selected_command["arguments"])
        cmd.append(active_file)

        args = {
            "cmd": cmd,
            "working_dir": working_dir
        }

        try:
            if "based_on_extension" == selected_command["syntax_file"]:
                args["syntax_file"] = GitCommand.syntaxes[active_file_ext]
            else:
                args["syntax_file"] = selected_command["syntax_file"]
        except:
            pass

        self.window.run_command("exec_to_view", args)

    def run(self):
        quick_panel_items = []
        for command in GitCommand.commands:
            quick_panel_items.append(
                [
                    command["description"],
                    "git %s" % " ".join(command["arguments"])
                ]
            )
        self.window.show_quick_panel(quick_panel_items,
                                     self.quick_panel_callback)

class ExecToViewCommand(sublime_plugin.WindowCommand,
                        __import__("exec").ProcessListener):
    """
    Executes a command and prints its output to a new scratch file in its own
    view within Sublime Text 2.  The majority of this code was swiped from
    exec.py in the Default plugin directory.
    """
    def run(self, cmd = [], file_regex = "", line_regex = "",
            working_dir = "", encoding = "utf-8", env = {}, quiet = True,
            kill = False, syntax_file = "",
            # Catches "path" and "shell"
            **kwargs):

        if kill:
            if self.proc:
                self.proc.kill()
                self.proc = None
                self.append_data(None, "[Cancelled]")
            return

        self.output_view = self.window.new_file()
        self.output_view.set_name(" ".join(cmd))
        if len(syntax_file) > 0: self.output_view.set_syntax_file(syntax_file)
        self.output_view.set_scratch(True)

        # Default the to the current files directory if no working directory was given
        if (working_dir == "" and self.window.active_view()
                        and self.window.active_view().file_name() != ""):
            working_dir = os.path.dirname(self.window.active_view().file_name())

        self.output_view.settings().set("result_file_regex", file_regex)
        self.output_view.settings().set("result_line_regex", line_regex)
        self.output_view.settings().set("result_base_dir", working_dir)

        # Call get_output_panel a second time after assigning the above
        # settings, so that it'll be picked up as a result buffer
        # self.window.get_output_panel("exec")

        self.encoding = encoding
        self.quiet = quiet

        self.proc = None
        if not self.quiet:
            print "Running " + " ".join(cmd)

        # self.window.run_command("show_panel", {"panel": "output.exec"})
        self.window.focus_view(self.output_view)

        merged_env = env.copy()
        if self.window.active_view():
            user_env = self.window.active_view().settings().get('build_env')
            if user_env:
                merged_env.update(user_env)

        # Change to the working dir, rather than spawning the process with it,
        # so that emitted working dir relative path names make sense
        if working_dir != "":
            os.chdir(working_dir)

        err_type = OSError
        if os.name == "nt":
            err_type = WindowsError

        try:
            # Forward kwargs to AsyncProcess
            self.proc = __import__("exec").AsyncProcess(cmd, merged_env, self, **kwargs)
        except err_type as e:
            self.append_data(None, str(e) + "\n")
            if not self.quiet:
                self.append_data(None, "[Finished]")

    def is_enabled(self, kill = False):
        if kill:
            return hasattr(self, 'proc') and self.proc and self.proc.poll()
        else:
            return True

    def append_data(self, proc, data):
        if proc != self.proc:
            # a second call to exec has been made before the first one
            # finished, ignore it instead of intermingling the output.
            if proc:
                proc.kill()
            return

        try:
            str = data.decode(self.encoding)
        except:
            str = "[Decode error - output not " + self.encoding + "]"
            proc = None

        # Normalize newlines, Sublime Text always uses a single \n separator
        # in memory.
        str = str.replace('\r\n', '\n').replace('\r', '\n')

        selection_was_at_end = (len(self.output_view.sel()) == 1
            and self.output_view.sel()[0]
                == sublime.Region(self.output_view.size()))
        self.output_view.set_read_only(False)
        edit = self.output_view.begin_edit()
        self.output_view.insert(edit, self.output_view.size(), str)
        # if selection_was_at_end:
        #     self.output_view.show(self.output_view.size())
        self.output_view.show(0)
        self.output_view.end_edit(edit)
        self.output_view.set_read_only(True)

    def finish(self, proc):
        if not self.quiet:
            self.append_data(proc, "[Finished]")
        if proc != self.proc:
            return

        # Set the selection to the start, so that next_result will work as expected
        edit = self.output_view.begin_edit()
        self.output_view.sel().clear()
        self.output_view.sel().add(sublime.Region(0))
        self.output_view.end_edit(edit)

    def on_data(self, proc, data):
        sublime.set_timeout(functools.partial(self.append_data, proc, data), 0)

    def on_finished(self, proc):
        sublime.set_timeout(functools.partial(self.finish, proc), 0)
