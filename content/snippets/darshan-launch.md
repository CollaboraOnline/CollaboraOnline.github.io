+++
authors = [
    "Darshan"
]
title = "Darshan's launch.json"
description = "Darshan's launch.json"
tags = [
	"snippet",
	"ides",
    "VSCode",
]
+++

```json
{
    // Use IntelliSense to learn about possible attributes.
    // Hover to view descriptions of existing attributes.
    // For more information, visit: https://go.microsoft.com/fwlink/?linkid=830387
    "version": "0.2.0",
    "configurations": [
        {
            "type": "chrome",
            "request": "launch",
            "name": "Writer",
            "url": "http://localhost:9980/browser/872228b6a8/debug.html?file_path=/${Your-Work-Directory}/test/data/hello-world.odt",
        },
        {
            "type": "chrome",
            "request": "launch",
            "name": "Calc",
            "url": "http://localhost:9980/browser/872228b6a8/debug.html?file_path=/${Your-Work-Directory}/test/data/hello-world.ods",
        },
        {
            "type": "chrome",
            "request": "launch",
            "name": "Impress",
            "url": "http://localhost:9980/browser/872228b6a8/debug.html?file_path=/${Your-Work-Directory}/test/data/hello-world.odp",
        },
        {
            "type": "chrome",
            "request": "launch",
            "name": "Draw",
            "url": "http://localhost:9980/browser/872228b6a8/debug.html?file_path=/${Your-Work-Directory}/test/data/hello-world.odg",
        },
        {
            "type": "chrome",
            "request": "launch",
            "name": "Nextcloud",
            "url": "http://192.168.1.7/apps/files/",
        },
        {
            "name": "kit",
            "type": "cppdbg",
            "request": "attach",
            "program": "/${Your-Work-Directory}/coolforkit",
            "processId": "${command:pickProcess}",
            "MIMode": "gdb",
            "setupCommands": [
                {
                    "description": "Enable pretty-printing for gdb",
                    "text": "-enable-pretty-printing",
                    "ignoreFailures": true
                }
            ]
        },
        {
            "name": "coolwsd attach",
            "type": "cppdbg",
            "request": "attach",
            "program": "/${Your-Work-Directory}/coolwsd",
            "processId": "${command:pickProcess}",
            "MIMode": "gdb",
            "setupCommands": [
                {
                    "description": "Enable pretty-printing for gdb",
                    "text": "-enable-pretty-printing",
                    "ignoreFailures": true
                }
            ]
        },
        {
            "name": "coolwsd launch",
            "type": "cppdbg",
            "request": "launch",
            "program": "/${Your-Work-Directory}/loolwsd",
            "args": ["--o:security.capabilities=\"false\"",
                "--o:sys_template_path=\"/${Your-Work-Directory}/systemplate\"",
                "--o:child_root_path=\"/${Your-Work-Directory}/jails\"",
                "--o:storage.filesystem[@allow]=true",
                "--o:ssl.cert_file_path=\"/${Your-Work-Directory}/etc/cert.pem\"",
                "--o:ssl.key_file_path=\"/${Your-Work-Directory}/etc/key.pem\"",
                "--o:ssl.ca_file_path=\"/${Your-Work-Directory}/etc/ca-chain.cert.pem\"",
                "--o:admin_console.username=admin",
                "--o:admin_console.password=admin",
                "--o:logging.file[@enable]=false",
                "--o:logging.level=error"
                ],
            "cwd": "/${Your-Work-Directory}",
            "stopAtEntry": true,
            "MIMode": "gdb",
            "setupCommands": [
                {
                    "description": "Enable pretty-printing for gdb",
                    "text": "-enable-pretty-printing",
                    "ignoreFailures": true
                }
            ]
        },
    ]
}
```