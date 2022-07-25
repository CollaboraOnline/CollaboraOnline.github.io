+++
authors = [
    "Pranam"
]
title = "Pranam's tasks.json"
description = "Pranam's tasks.json"
tags = [
    "snippet",
    "ides",
    "VSCode",
]
+++

```json
{
    "tasks": [
        {
            "type": "shell",
            "label": "build",
            "command": "make -j && notify-send --app-name=Collabora --icon=\"/usr/share/notificationhelper/collabora_logo.png\" \"Build Complete\" && paplay /usr/share/sounds/build_complete.ogg",
            "group": {
                "kind": "build",
                "isDefault": true
            },
            "args": [],
            "options": {
                "cwd": "${workspaceFolder}"
            },
            "presentation": {
                "focus": true
            },
            "problemMatcher": [
                "$gcc"
            ]
        },
        {
            "type": "shell",
            "label": "run",
            "command": "make",
            "args": [
                "-j",
                "run",
                "build-nocheck"
            ],
            "options": {
                "cwd": "${workspaceFolder}"
            },
            "presentation": {
                "focus": true
            },
            "problemMatcher": [
                "$gcc"
            ]
        },
        {
            "type": "shell",
            "label": "g++ build active file",
            "command": "/usr/bin/g++",
            "args": [
                "-g",
                "${file}",
                "-o",
                "${fileDirname}/${fileBasenameNoExtension}"
            ],
            "options": {
                "cwd": "/usr/bin"
            }
        }
    ],
    "version": "2.0.0"
}
```
