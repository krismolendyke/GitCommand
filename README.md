# GitCommand

GitCommand is a [WindowCommand](http://www.sublimetext.com/docs/2/api_reference.html#sublime.Window) for running simple [git](http://git-scm.com/) commands from within
[Sublime Text 2](http://www.sublimetext.com/2).  Instead of using the Default exec.py implementation which
outputs to the [Build Results](http://sublimetext.info/docs/en/reference/build_systems.html) window, it creates a new scratch file in its own
view and displays the results there.  It will attempt to set a proper language
syntax file when it makes sense, as well.
