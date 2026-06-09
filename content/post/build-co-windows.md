+++
authors = [
    "Collabora",
]
title = "Build Collabora Office for Windows"
date = "2026-04-27"
home_pos = "3"
description = "Step-by-step build instructions"
tags = [
    "build",
    "make",
]
images = [
    "beaver/co-windows-copyrighted.png",
]
type = "sidebar"
layout = "sidebar"
showimage = false
+++

On Windows and want to tinker? Build Collabora Office and level up your setup.

<!--more-->
<section id="build-co-windows" class="build-co-linux">

# Build Collabora Office

This is the Collabora Office Windows desktop app (`windows/`).

## Requirements

For starters, the same requirements as for building Collabora Office Classic or
LibreOffice, see
https://wiki.documentfoundation.org/Development/BuildingOnWindows. Make sure to
use Visual Studio 2022 — other Visual Studio versions for building the online
bits have not been tested. In the Visual Studio installer, also install the .NET
desktop development components.

Turn on WSL, the Windows Subsystem for Linux, and install a distro. We use the
default, Ubuntu; others presumably work too. In an administrator Command Prompt:

```
wsl --install Ubuntu
```

In that Ubuntu, install the packages needed later. Most of this is needed just
to run the online configure script, which checks for many things that are
irrelevant for a Windows build of Collabora Office. This is not necessarily a
comprehensive list — you might notice more missing things as you go along.

```
sudo apt install libtool python3-lxml python3-polib g++ pkg-config
sudo apt install libpng-dev libzstd-dev libcppunit-dev libpam-dev
```

Node.js is the more essential one, for building the JavaScript bits (the main
reason we use WSL):

```
sudo apt install nodejs npm
```

## Clone the monorepo

All the source code now lives in a single Gerrit monorepo; the former Collabora Office core is the `engine/` subdirectory of the `online` repo, so there is no separate repository to clone any more. Code review happens on [Gerrit](https://gerrit.collaboraoffice.com/), not GitHub pull requests; see the [first contribution guide](https://forum.collaboraonline.com/t/your-first-pull-request/41) for the full workflow.

For an anonymous read-only clone:
```bash
git clone https://gerrit.collaboraoffice.com/online collabora-office
cd collabora-office
```

If you have a Gerrit account and plan to push changes for review, clone over SSH instead:
```bash
git clone ssh://YOUR_USERNAME@gerrit.collaboraoffice.com:29418/online collabora-office
cd collabora-office
```

## Build the engine

Change to the `engine` subdirectory. The known good configuration is in
`distro-configs/CODAWindows.conf`. Make sure that you include it in your
`autogen.input`. You can tweak it as you like, for example:

`autogen.input`:
```
--host=x86_64-pc-cygwin
--with-distro=CODAWindows
--with-lang=ar ca cs cy da de el en-US en-GB es eu fi fr ga gl he hr hu hy id is it ja kk ko nl pl pt pt-BR ro ru sk sl sq sv tr uk zh-CN zh-TW
--with-external-tar=/cygdrive/c/co/src
```

Note that if you build the Collabora Office project in Visual Studio in the
Debug configuration, you *must* use an engine build with either
`--enable-dbgutil` or `--enable-msvc-debug-runtime`.

The engine build should proceed fairly normally. Note that you will not end up
with a runnable Collabora Office Classic. Attempting to run
`instdir/program/soffice.exe` will just produce the message "no suitable
windowing system found, exiting".

You can attempt to run `make check` but that will probably run into some false
positives.

### Building the engine using WSL and Git Bash

It is possible nowadays to configure Collabora Office Classic or LibreOffice for
Windows in WSL, not Cygwin. The actual build will then use the so-called Git
Bash, though, not WSL. It is unclear why the impression is given that one is
building in WSL. We have not used that for Collabora Office, though.

Ideally, in the future, it would be nice to be able to actually truly build the
engine for Windows using only Visual Studio and WSL, without Git Bash.

## Build Collabora Office

### Configure

In an Ubuntu shell, in the top-level of your clone of the `online` repo, run

```
./autogen.sh
```

then run the configure script, like below. POCO, libpng and zstd are built as
part of the engine and linked from its workdir by the Visual Studio project, so
they no longer need to be built or passed separately (zlib likewise comes from
the engine's unpacked sources).

```
./configure --enable-windowsapp --with-app-name='Collabora Office' --with-lo-builddir=$PWD/engine --with-lo-path=`wslpath -w $PWD/engine/instdir` --with-zlib-includes=$PWD/engine/workdir/UnpackedTarball/zlib --with-info-url=https://example.com/coda/info.html
```

Change the `--with-info-url` as appropriate. That is the web page that will be
shown when clicking the leftmost button in the toolbar.

Note that some paths are Unix-like paths, while `--with-lo-path` is a Windows
path. This is important.

### Build the JavaScript bits

```
cd browser && make
```

### Build the app

Open the `windows/coda/CODA.sln` solution in Visual Studio and build it.

To build Collabora Office from the command line, run this in an `x64 native
Tools Command Prompt` window. To do it from a script you probably want to check
what the PATH in such a command prompt window is, and make sure to use the
relevant PATH entries in a `.cmd` file.

```
msbuild /p:Configuration=Release /p:Platform=x64 windows\coda\CODA.sln
```

To first clean the build, run:

```
msbuild /p:Configuration=Release /p:Platform=x64 /t:Clean windows\coda\CODA.sln
```

You could also run that from a WSL shell, as long as you make sure PATH has what
is needed, and you quote the msbuild command-line parameters as needed.

## Pre-built download

If you just want a **pre-built snapshot for Windows**, you can download it here:
👉 https://www.collaboraoffice.com/downloads/Collabora-Office-Windows-Snapshot/

</section>

{{< edit-button href="https://gerrit.collaboraoffice.com/plugins/gitiles/online/+/refs/heads/main/windows/coda/README.md" name="Edit page" >}}
