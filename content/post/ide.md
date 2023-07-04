+++
authors = [
    "Community"
]
title = "IDEs & Text Editors"
date = "2020-10-01"
home_pos = "4"
description = "Development Environment"
tags = [
    "contribute",
    "development",
    "code",
    "environment",

]
images = [
    "easyhacks.jpg",
]
type = "sidebar"
layout = "sidebar"
+++

Tips on how to set your IDE ready for Collabora Online development.

<!--more-->

An integrated development environment (IDE) helps developers to have a better coding experience. Other Preffer a simple text editor. Either way here are some tips on how to get those set it up.

## Collabora Online
Please note this is a very rough page and any contribution is very welcomed. The present tips were gathered with no particular order in mind and by no means represent any official position from Collabora.

### VSCode or VSCodium
#### Easy to grab setup (Pranam)
Thanks [Pranam](https://github.com/lpranam) for making your configurations available:
> I use vs code let me give you config file for vs with which people can debug or whatever they want in vs code without ever leaving it:
* [c_cpp_properties.json]({{< ref "/content/snippets/pranam-c-cpp-properties.md" >}} "Pranam's config")
* [launch.json]({{< ref "/content/snippets/pranam-launch.md" >}} "Pranam's config")
* [tasks.json]({{< ref "/content/snippets/pranam-tasks.md" >}} "Pranam's config")

#### gdb
How to attach VS Code with gdb to the Online server:
```json
{
                "name": "online attach",
                "processId": "${command:pickProcess}",
                "type": "cppdbg",
                "request": "attach",
                "program": "${workspaceFolder}/coolforkit",
                "args": [],
                "stopAtEntry": false,
                "cwd": "${workspaceFolder}",
                "externalConsole": false,
                "MIMode": "gdb",
                "setupCommands": [
                    {
                        "description": "Enable prett-printing for gdb",
                        "text": "-enable-pretty-printing",
                        "ignoreFailures": true
                    }
                ],
                "linux": {
                    "miDebuggerPath": "/usr/bin/gdb"   // < sometimes you need some tricks for permissions
                },
}
```

Source: Anonymous
#### launch.json example
An example of a `launch.json` configuration from [Gokay](https://github.com/gokaysatir)

The file that i use for VS Code server side debugging:
* [launch.json]({{< ref "/content/snippets/gokay-launch.md" >}} "Gokay's config")

Source: [Gokay](https://github.com/gokaysatir)

#### Wastack & C/C++ plugin
I used this for core: https://wastack.wordpress.com/2019/09/28/vs-code-ide-integration-for-libreoffice/ with c++ extension
* For online we need to generate compile_commands.json for that
* compile_commands.json generate
* pip install compiledb
* compiledb make --> creates the file
* I use this config https://marketplace.visualstudio.com/items?itemName=ms-vscode.cpptools this is the extension

source: [Mert](https://github.com/merttumer)

#### WSL
Tip for Windows users: Since I'm using WSL instead of a Linux VM or OS using the windows terminal is significantly better than the standard windows CMD, especially for using panes and other multitasking features. It looks better imo if that matters

source: [NickWingate](https://github.com/NickWingate)

### Vim
#### Find it difficult
Find it hard for COOL development, VS Code is something I'd like to switch to
Source: Anonymous Vim user

#### TDF Vim tips
https://wiki.documentfoundation.org/Development/Vim has some vim tips, navigating a c++ codebase is quite similar for core.git and online.git
Source: [Miklos](https://github.com/vmiklos)

#### Ashod's .vimrc
Thanks [Ash](https://github.com/Ashod) for making your configurations available: [.vimrc]({{< ref "/content/snippets/ash-vimrc.md" >}} "Ashod's .vimrc")
> I use Vim in the terminal (a lot) and I use Vim addon in VSCode. Always customize the colors, behavior of searching, highlighting, etc. for best experience. Also, add shortcuts for common actions (e.g. highlighting multiple words in different colors is very useful when reading logs or complex code with many variables, use F2, F3, etc. to highlight different words in different colors for readability).


### Emacs
#### Henry's init.el
https://github.com/hcvcastro/.emacs.d
> * Custom shortcuts to compile Collabora Online in different folders
> * Custom buffer to fill the configure parameters
> * Custom buffer to query current configure parameters
> * Custom shortcuts to run LO or Collabora Online Development

#### Emacs with LSP
I recommend Emacs wiki and have some kind of Language Server Protocol Support. I use https://emacs-lsp.github.io/lsp-mode/
https://github.com/pedropintosilva/emacs.d

source: [Pedro](https://github.com/pedropintosilva/)

### Kate
#### Plugins
Go to Settings -> Configure Kate... and activate
* [LSP Client](https://docs.kde.org/stable5/en/kate/kate/kate-application-plugin-lspclient.html) which makes it possible to use language server protocol
* [Project Plugin](https://docs.kde.org/stable5/en/kate/kate/kate-application-plugin-projects.html) which allows you to save session, build project, git integration, etc
* [Symbol Viewer](https://docs.kde.org/stable5/en/kate/kate/kate-application-plugin-symbolviewer.html) which will allow you to view and navigate though the symbols of the current file
* You might want to have others also activated: Terminal tool view, external tools, etc

#### Editing
In Settings -> Configure Kate... -> Editing
* Turn on `Auto Brackets`
* Auto completion should be on
* find indentation options here
* You can also activate spell checking here

Also worth to make sure tabs are shown (settings -> Show Tabs)

source: [Pedro](https://github.com/pedropintosilva/)

## Collabora Online for Android
### Android Studio
Android Studio debugger for gdb users gdb commands, and their AS equivalent:

* next: F8
* step: F7
* finish: Shift-F8
* cont: F9

I find it impossible to remember those keystrokes if I don't use them for 2 weeks :)

source: [IRC]({{< ref "/content/post/communicate.md" >}} "Communicate page")


## Additional info
For contributing to core LibreOffice there are excellent resources already available at TDF wiki cafes:
* https://wiki.documentfoundation.org/Development/IDE
* https://wiki.documentfoundation.org/Development/How_to_debug
