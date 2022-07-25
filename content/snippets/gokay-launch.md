+++
authors = [
    "Gokay"
]
title = "Gokay's launch.json"
description = "Gokay's tasks.json"
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
		"name": "(gdb) Attach",
		"type": "cppdbg",
		"request": "attach",
		"program": "${workspaceFolder}/kit/Kit.o",
		"processId": "${command:pickProcess}",
		"MIMode": "gdb",
		"setupCommands": [
			{
				"description": "Enable pretty-printing for gdb",
				"text": "-enable-pretty-printing",
				"ignoreFailures": true
			},
			{
				"description":  "Set Disassembly Flavor to Intel",
				"text": "-gdb-set disassembly-flavor intel",
				"ignoreFailures": true
			}
		]
	},
        {
            "name": "(gdb) Launch",
            "type": "cppdbg",
            "request": "launch",
            "program": "${workspaceFolder}/coolwsd",
            "args": [
                "--o:sys_template_path=/home/gokaysatir/Documents/CollaboraOffice/online2205/systemplate"
                , "--o:security.capabilities=$(CAPABILITIES)"
                , "--o:child_root_path=/home/gokaysatir/Documents/CollaboraOffice/online2205/jails"
                , "--o:storage.filesystem[@allow]=true"
                , "--o:ssl.cert_file_path=/home/gokaysatir/Documents/CollaboraOffice/online2205/etc/cert.pem"
                , "--o:ssl.key_file_path=/home/gokaysatir/Documents/CollaboraOffice/online2205/etc/key.pem"
                , "--o:ssl.ca_file_path=/home/gokaysatir/Documents/CollaboraOffice/online2205/etc/ca-chain.cert.pem"
                , "--o:admin_console.username=admin"
                , "--o:admin_console.password=admin"
                , "--o:logging.file[@enable]=true"
                , "--o:security.capabilities=false"
                , "--o:logging.level=trace"
            ],
            "stopAtEntry": false,
            "cwd": "${workspaceFolder}",
            "environment": [],
            "externalConsole": false,
            "MIMode": "gdb",
            "setupCommands": [
                {
                    "description": "Enable pretty-printing for gdb",
                    "text": "-enable-pretty-printing",
                    "ignoreFailures": true
                }
            ]
        }
    ]
}
```
