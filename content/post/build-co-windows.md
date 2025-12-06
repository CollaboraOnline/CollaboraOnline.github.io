+++
authors = [
    "Collabora",
]
title = "Build Collabora Office for Windows"
date = "2020-12-05"
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
# Build Collabora Office

The steps below are for building the Collabora Office in Windows.

<section id="build-co-windows" class="build-co-linux">

## Windows

### Requirements

For starters, the same requirements as for building LibreOffice, see
https://wiki.documentfoundation.org/Development/BuildingOnWindows as
you will do that as part of building Collabora Office for windows. Make sure to use Visual
Studio 2022. Using other Visual Studio versions for building the
online bits has not been tested.

In Visual Studio 2022, also install the .NET desktop development
components.

### Setup

Turn on WSL, the Windows Subsystem for Linux, and install a distro.
We use the default, Ubuntu, others presumably work, too. In an
administrator Command Prompt:
```
	wsl --install Ubuntu
```
In that Ubuntu, install various things that will be needed later. Most
of this is needed just to run the configure script in online. That
configure script checks for tons of things that are completely
irrelevant for a Windows build of Collabora Office, but oh well. Patches welcome.

This is not necessarily a comprehensive list, you might notice more
missing things as you go along.

	sudo apt install libtool python3-lxml python3-polib g++ pkg-config
	sudo apt install libpng-dev libzstd-dev libcppunit-dev libpam-dev

The following things are more essential, for bulding the JavaScript
stuff. This is the main reason we are using WSL.

	sudo apt install nodejs npm

### Build core

Clone the https://git.libreoffice.org/core repository and check out the distro/collabora/coda-25.04 branch.

The known good configuration is in `distro-configs/CODAWindows.conf`. Make sure that you include
it in your `autogen.input`. You can tweak it as you like, for example:

autogen.input:
```
--host=x86_64-pc-cygwin
--with-distro=CODAWindows
--with-lang=ar ca cs cy da de el en-US en-GB es eu fi fr ga gl he hr hu hy id is it ja kk ko nl pl pt pt-BR ro ru sk sl sq sv tr uk zh-CN zh-TW
--with-external-tar=/cygdrive/c/co/src
```

Note that if you build the Collabora Office project in Visual Studio
in the Debug configuration, you *must* use a core build with either
`--enable-dbgutil` or `--enable-msvc-debug-runtime`.

The core build should proceed fairly normally. Note that you
will not end up with a runnable normal desktop Collabora Office. Attempting
to run instdir/program/soffice.exe will just produce the message "no
suitable windowing system found, exiting".

You can attempt to run `make check` but that will probably run into
some false positives.

#### Building also core using WSL

Apparently it is possible nowadays to build core
for Windows using WSL, not Cygwin. Especialy when/if somebody would
want or need to work on Collabora Office on ARM64 Windows, it is good to manage
without Cygwin, as Cygwin is available only for x64 Windows.

The distro/collabora/coda-25.04 branch was successfully built under WSL following the
instructions on [TDF Wiki](https://wiki.documentfoundation.org/Development/BuildingOnWSLWindows).

Despite allegedly being about building core using *WSL*, the above
uses the so-called Git Bash. Ideally, in the future, it would be nice
to be able to truly build core for Windows using only Visual Studio
and WSL.

### Build direct dependencies of Collabora Office for Windows

Version numbers below are current at the time of writing this. Newer
versions will probably work, too.
For `zlib` and `libpng` we use the unpacked sources in the core build directory, and
the static libraries already built there.

### zstd

Download and unpack the zstd-1.5.7 tarball. Open the Visual Studio
solution zstd-1.5.7/build/VS2010/zstd.sln. Let Visual Studio retarget
the projects. It is enough to build just the libzstd project of the
solution.

Note that you need to manually turn off "Whole Program Optimization"
in the project settings. Having that option on means that the libzstd
archive does not contain normal object files but LLVM bytecode for
link-time code generation, and that won't be useable by the CODA
project.

The static libraries that you are interested end up as
zstd-1.5.7/build/VS2010/bin/x64\_Debug/libzstd\_static.lib and
zstd-1.5.7/build/VS2010/bin/x64\_Release/libzstd\_static.lib .

### Poco

Download and unpack the poco-poco-1.14.2-release.zip archive.

Then build it. Only a subset of it is needed. In a Ubuntu shell
window, run:

    powershell.exe -ExecutionPolicy Bypass -File buildwin.ps1 -action build -config both -linkmode static\_md -platform x64 -components Foundation,Util,JSON,Net,XML

Then move all the headers into one place:

	mkdir -p include/Poco
	cp -a Foundation/include/Poco/* include/Poco
	cp -a Util/include/Poco/* include/Poco
	cp -a JSON/include/Poco/* include/Poco
	cp -a Net/include/Poco/* include/Poco
	cp -a XML/include/Poco/* include/Poco

### Build Collabora Office itself

Clone the https://github.com/CollaboraOnline/online.git repo, and checkout distro/collabora/coda-25.04 branch.

In an Ubuntu shell, run

	./autogen.sh

then run the configure script. Like this to use release build of zstd
and LibreOffice core.

(You will automatically get the Debug libraries of Poco when building
a Debug configuration of the Collabora Office, and the Release libraries
in a Release configuration. There is some slightly questionable
#pragmas in <Poco/Foundation.h> to take care of that.)

	./configure --enable-windowsapp --with-app-name='Collabora Office' --with-lo-builddir=/mnt/c/cygwin64/home/tml/lo/core-gitlab-coda25-coda-release --with-lo-path='C:\cygwin64\home\tml\lo\core-gitlab-coda25-coda-release\instdir' --with-poco-includes=/mnt/c/Users/tml/poco-poco-1.14.2-release/include --with-poco-libs=/mnt/c/Users/tml/poco-poco-1.14.2-release/lib64 --with-zstd-includes=/mnt/c/Users/tml/zstd-1.5.7/lib --with-zstd-libs=/mnt/c/Users/tml/zstd-1.5.7/build/VS2010/bin/x64_Release --with-libpng-includes=/mnt/c/cygwin64/home/tml/lo/core-gitlab-coda25-coda-release/workdir/UnpackedTarball/libpng --with-libpng-libs=/mnt/c/cygwin64/home/tml/lo/core-gitlab-coda25-coda-release/workdir/LinkTarget/StaticLibrary --with-zlib-includes=/mnt/c/cygwin64/home/tml/lo/core-gitlab-coda25-coda-release/workdir/UnpackedTarball/zlib --with-info-url=https://example.com/coda/info.html

Obviously, adapt as necessary to match your username and where you
built LibreOffice, zstd, and Poco. Also change the `--with-info-url` as
appropriate. That is the web page that will be shown when clicking the
leftmost button in the toolbar.

Note, that some paths are Unix-like paths, and the `--with-lo-path` is a Windows path. This is important.

Now you can build the JavaScript bits:
```
	cd browser && make
```
And then finally, open the windows/coda/CODA.sln solution in Visual Studio and build it.

To build Collabora Office from the command line, run this in `x64 native Tools
Command Prompt` window. To do it from a script you probably want to
check what the PATH in such a command prompt window is, and make sure
to use the relevant PATH entries in a .cmd file.

	msbuild /p:Configuration=Release /p:Platform=x64 windows\coda\CODA.sln

To first clean the build, run:

	msbuild /p:Configuration=Release /p:Platform=x64 /t:Clean windows\coda\CODA.sln

You could also run that from a WSL shell, as long as you make sure
PATH has what is needed, and you quote the msbuild command-line
parameters as needed.

</section>
