# GitCommand

GitCommand is a WindowCommand for running simple git commands from within
Sublime Text 2.  Instead of using the Default exec.py implementation which
outputs to the Build Results window, it creates a new scratch file in its own
view and displays the results there.  It will attempt to set a proper language
syntax file when it makes sense too, as well.
