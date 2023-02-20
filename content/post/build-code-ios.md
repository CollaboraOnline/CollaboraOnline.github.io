+++
authors = [
    "Collabora",
]
title = "Build for iOS"
date = "2020-10-03"
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

1.1) First you need to build the LibreOffice core code for iOS. Put in your autogen.input something like this:

```bash
# Comment out for production builds
--enable-debug
--enable-dbgutil

# Standard build options
--enable-werror
--enable-symbols
--with-myspell-dicts
--with-distro=LibreOfficeiOS
```

and build "normally". (Naturally, no unit tests will be run when cross-compiling LibreOffice.) Of course there is no requirement to use those --enable options; as a minimum, just `--with-distro=LibreOfficeiOS` should work.

This will produce a large number of static archives (.a) here and there in instdir and workdir, but no app that can be run as such. (You can see a list of them in workdir/CustomTarget/ios/ios-all-static-libs.list)

## 2) Build COOL Dependencies
### on a Mac ## {#ios-2-build-cool-mac .extraclass class="requirement-machine"}

MACPORTS PACKAGES

2.1.1) Install [MacPorts](https://github.com/macports/macports-base/releases).
Note: make sure that /opt/local/bin/port is at the end of your PATH.

2.1.2) Install the following MacPorts modules:
```bash
sudo /opt/local/bin/port install npm9 -x11
sudo /opt/local/bin/port install pkgconfig -x11
sudo /opt/local/bin/port install cairo -x11
sudo /opt/local/bin/port install pango -x11
```

2.1.3) Install the following Python modules:
```bash
/usr/bin/pip3 install polib
/usr/bin/pip3 install lxml
```

POCO LIBRARY

2.2.1) The below instructions are for the so-called basic edition of
poco 1.10.1. (If there has been a newer release of poco by the time
you read this, adapt as necessary.) Get the poco library source code
from https://pocoproject.org/releases/poco-1.10.1/, the
poco-1.10.1.tar.gz archive.

2.2.2) Unpack in some suitable location.

2.2.3) Compile. Note: in the second command, force path to load /usr/bin/python3
and set the minimum iOS version to match the LibreOffice build:
```bash
./configure --config=iPhone --static --no-tests --no-samples --omit=Data/ODBC,Data/MySQL --prefix=$HOME/poco-ios-arm64
```
```bash
PATH="/usr/bin:$PATH" make POCO_TARGET_OSARCH=arm64 IPHONE_SDK_VERSION_MIN=14.5 -s -j4
```
```bash
make POCO_TARGET_OSARCH=arm64 install
```

This will install the poco static libraries and headers to your $HOME directory into poco-ios-arm64 directory. You can change the directory to your wishes, but by installing it this way into a directory in `$HOME` it doesn't pollute your root directories, doesn't need root permissions and can be removed easily.

ZSTD LIBRARY

2.3.1) The below instructions are for the so-called basic edition of
zstd 1.5.2. (If there has been a newer release of zstd by the time
you read this, adapt as necessary.) Get the zstd library source code
from https://github.com/facebook/zstd/releases/tag/v1.5.2, the
zstd-1.5.2.tar.gz archive.

2.3.2) Unpack in some suitable location.

2.3.3) Compile. Note: in the first command, force SDK to iOS and set the
minimum iOS version to match the LibreOffice build:
```bash
CC="/usr/bin/clang -arch arm64 -isysroot /Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS16.2.sdk -target arm64-apple-ios14.5" make
```
```bash
make DESTDIR=$HOME/zstd-ios-arm64 install
```
Important: the following command deletes any shared libraries that may have
been installed in the previous command. This is important because recent
versions of Xcode will link to a dynamic library if it exists in the same
folder as a static library and our iOS app will not run if it is linked to
any non-system dynamic libraries:
```bash
find "$HOME/zstd-ios-arm64" -name "*.dylib*" -exec rm {} \;
```

This will install the zstd static libraries and headers to your $HOME directory into zstd-ios-arm64 directory. You can change the directory to your wishes, but by installing it this way into a directory in `$HOME` it doesn't pollute your root directories, doesn't need root permissions and can be removed easily.

## 3) Clone Online
### on a Mac ## {#ios-3-clone-online-mac .extraclass class="requirement-machine"}
Do a separate clone of the online repo on macOS, but don't do any autogen.sh, configure, or make, or open the Mobile Xcode project there yet. We call this the app folder.

## 4) Clone Online
### on a Linux machine ## {#ios-4-clone-online-linux .extraclass class="requirement-machine"}
Do a separate clone of the online repo, run autogen.sh, and configure it with the --enable-iosapp option:

```bash
./autogen.sh
./configure --enable-iosapp --with-app-name="My Own Mobile Office Suite" --with-vendor=MyOwnApp
```

Then run make. That will produce files in browser/dist, nothing else. Copy those to the corresponding folder in the app folder from step 2. This is how I do it:

```bash
make clean && make && tar cf - browser/dist | ssh misan.local 'cd lo/online-ios-device && rm -rf browser/dist && tar xvf -'
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

5.1) In the app folder, set LOSRCDIR to the absolute path of the LibreOffice build built in step 1 and then run:

```bash
./configure --enable-iosapp --with-app-name="My Own Mobile Office Suite" --with-vendor=MyOwnApp --with-poco-includes=$HOME/poco-ios-arm64/include --with-poco-libs=$HOME/poco-ios-arm64/lib --with-zstd-libs=$HOME/zstd-ios-arm64/usr/local/lib --with-zstd-includes=$HOME/zstd-ios-arm64/usr/local/include --with-lo-builddir=$LOSRCDIR
make
```

Note: if you did step 4 and cloned Online on a Linux machine, make is unnecessary. If you run make, you can ignore any errors and continue on to the steps below.

The configure script puts the app name as the `CFBundleDisplayName` property into the `ios/Mobile/Info.plist` file, and sets up some symbolic links that point to the LibreOffice core source and build directories (which typically will be the same, of course).

5.2) Before opening the Xcode project for the first time
   - seriously consider disabling source code indexing, this
   spawns a vast number of git processes, and consumes huge
   amounts of CPU & memory:

	Xcode -> Preferences, "Source Control", uncheck "Enable Source Control"

5.3) Now you can open the Mobile Xcode project, build it, and run it. Note:
building for "My Mac (Designed for iPad)" on Mac Silicon will run, but it
is unstable. Also, you can't run in an emulator since LibreOffice for iOS is
built for arm64 only. So, effectively, you can only test the build on a real
iOS device.

{{< edit-button to="/content/post/build-code-ios.md" name="Edit page">}}
