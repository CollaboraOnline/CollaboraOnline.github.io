+++
authors = [
    "Collabora",
]
title = "Build for iOS"
date = "2020-09-30"
description = "Step-by-step build instructions"
tags = [
    "build",
    "make",
]
images = [
    "build-code-ios.jpg",
]
type = "sidebar"
layout = "sidebar"
+++

Are you familiar with iOS development environment and interested to learn more while helping the project?
<!--more-->
# How to build the iOS app:

## 1) Build the LibreOffice core code
### on a Mac ## {#ios-1-build-Lo-mac .extraclass class="requirement-machine"}

First you need to build the LibreOffice core code for iOS. Put in your autogen.input something like this:

```bash
--enable-debug
--enable-dbgutil
--enable-werror
--with-distro=LibreOfficeiOS
```

and build "normally". (Naturally, no unit tests will be run when cross-compiling LibreOffice.) Of course there is no requirement to use those --enable options; as a minimum, just `--with-distro=LibreOfficeiOS` should work.

This will produce a large number of static archives (.a) here and there in instdir and workdir, but no app that can be run as such. (You can see a list of them in workdir/CustomTarget/ios/ios-all-static-libs.list)

## 2) Build COOL Dependencies
### on a Mac ## {#ios-2-build-cool-mac .extraclass class="requirement-machine"}

POCO LIBRARY

2.1) The below instructions are for the so-called basic edition of
POCO 1.10.1. (If there has been a newer release of POCO by the time
you read this, adapt as necessary.) Get the POCO library source code
from https://pocoproject.org/releases/poco-1.10.1/ , the
poco-1.10.1.tar.gz archive.

2.2) Unpack in some suitable location.

2.3) Compile
```bash
./configure --config=iPhone --static --no-tests --no-samples --omit=Data/ODBC,Data/MySQL --prefix=$HOME/poco-ios-arm64
```
```bash
make POCO_TARGET_OSARCH=arm64 -s -j4
```
```bash
make POCO_TARGET_OSARCH=arm64 install
```

This will install the poco static libraries and headers to your $home directory into poco-ios-arm64 directory. You can change the directory to your wishes, but by installing it this way into a directory in `$HOME` it doesn't pollute your root directories, doesn't need root permissions and can be removed easily.

## 3) Clone Online
### on a Mac ## {#ios-3-clone-online-mac .extraclass class="requirement-machine"}
Do a separate clone of the online repo on macOS, but don't do any autogen.sh, configure, or make, or open the Mobile Xcode project there yet. We call this the app folder.

## 4) Clone Online
### on a Linux machine ## {#ios-4-clone-online-linux .extraclass class="requirement-machine"}
Do a separate clone of the online repo, run autogen.sh, and configure it with the --enable-iosapp option:

```bash
./configure --enable-iosapp --with-app-name="My Own Mobile Office Suite"
```

Then run make. That will produce files in loleaflet/dist, nothing else. Copy those to the corresponding folder in the app folder from step 2. This is how I do it:

```bash
make clean && make && tar cf - loleaflet/dist | ssh misan.local 'cd lo/online-ios-device && rm -rf loleaflet/dist && tar xvf -'
```

where `misan.local` is the macOS machine where I build the app, and `~/lo/online-ios-device` is the app folder from step 2.

## 5) Building for iOS
### on a Mac ## {#ios-5-clone-online-mac .extraclass class="requirement-machine"}
Now back to your Mac, and with LibreOffice built from step 1, you must already have GNU autoconf installed on the Mac. Install also GNU automake and libtool. Preferably from sources, to make sure a potential installation of brew or similar will not pollute your environment with unknown stuff.

As GNU libtool will be needed only for a very minimal part of the build (running the `autogen.sh` script, but not anything else), it's safest to install it somewhere that is not in your $PATH. Let's say `/opt/libtool`. (Installing Automake in the default `/usr/local`, which is in `$PATH`, is less risky.)

Run the autogen.sh script in the app folder, with GNU libtool available, for instance:

```bash
PATH=/opt/libtool/bin:$PATH ./autogen.sh
```

5.1) In the app folder from step 2, edit the `ios/Mobile.xcodeproj/project.pbxproj` file in your favourite text editor. Change `LOSRCDIR` and all instances of `../ios-device` to refer the the LibreOffice core source directory from step 1.

5.2) In the app folder, run:

```bash
./configure --enable-iosapp --with-app-name="My Own Mobile Office Suite" --with-lo-builddir=$HOME/lode/dev/LO --with-poco-includes=$HOME/poco-ios-arm64/include --with-poco-libs=$HOME/poco-ios-arm64/lib
```

The configure script puts the app name as the `CFBundleDisplayName` property into the `ios/Mobile/Info.plist` file, and sets up some symbolic links that point to the LibreOffice core source and build directories (which typically will be the same, of course).

5.3) Before opening the Xcode project for the first time
   - seriously consider disabling source code indexing, this
   spawns a vast number of git processes, and consumes huge
   amounts of CPU & memory:

	Xcode -> Preferences, "Source Control", uncheck "Enable Source Control"

5.4) Now you can open the Mobile Xcode project, build it, and run it.


{{< edit-button to="/content/post/build-code-ios.md" name="Edit page">}}
