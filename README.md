# GitCommand

## Preamble

I began writing this plugin because I was dissatisfied with the available Sublime Text 2 & `git` integration available at the time.  It met my spartan needs (I still prefer `git` interaction from the command line most often) and I thought it might be useful to others. Since then there has emerged a [very full-featured plugin](https://github.com/kemayo/sublime-text-2-git/wiki) that may be more of what you are looking for.

## So, what is this, then?

GitCommand is a [WindowCommand](http://www.sublimetext.com/docs/2/api_reference.html#sublime.Window) for running simple [git](http://git-scm.com/) commands from within
[Sublime Text 2](http://www.sublimetext.com/2).  Instead of using the Default exec.py implementation which
outputs to the [Build Results](http://sublimetext.info/docs/en/reference/build_systems.html) window, it creates a new scratch file in its own
view and displays the results there.  It will attempt to set a proper language
syntax file when it makes sense, as well.

## Installation

Find your way to your [Sublime Text 2 Packages directory](http://sublimetext.info/docs/en/basic_concepts.html#the-packages-directory), then

```sh
$ git clone git@github.com:krismolendyke/GitCommand.git Git
```

## Usage

You can bring up the Python Console with `ctrl+~` and then run the git command like so

```sh
window.run_command("git")
```

The easier thing to do is bind the git command to a key combination.  Find or create a user keymap file from within Sublime Text 2 menu: `Preferences` &rarr; `Key Bindings - User`.  In that file enter something like this

```json
[
    { "keys": ["ctrl+alt+super+g"], "command": "git" }
]
```

Save that file and now when you press `ctrl+option+command+g` the git command will be run for you.  I dig this binding because it doesn't collide with any others and it's nice and easy for my left hand's pinky, ring and middle fingers to mash `ctrl+option+command` while my right hand taps the `g`.
