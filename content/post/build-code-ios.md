+++
authors = [
    "Collabora",
]
title = "Build for iOS"
date = "2023-09-01"
home_pos = "3"
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
showimage = false
+++

Are you familiar with iOS development environment and interested to learn more while helping the project?
<!--more-->
# How to build the iOS app:

## You will need

### A developer program enrollment ## {#ios-1-build-Lo-mac .extraclass class="requirement-machine"}

You will need an Apple ID that is a member of the Apple Developer program, as Collabora iOS relies on Fonts and iCloud capabilities, which are only available to accounts in the developer platform

If you don't have an account in the developer program, you can enroll [on Apple's developer program website](https://developer.apple.com/programs/enroll/). If you are developing Collabora iOS for work your employer may be able to [add you to a development team](https://developer.apple.com/help/account/manage-your-team/invite-team-members/)

### A Mac ## {#ios-1-build-Lo-mac .extraclass class="requirement-machine"}
You will need a Mac with [Xcode](https://apps.apple.com/gb/app/xcode/id497799835) installed

### An iOS or iPadOS device ## {#ios-1-build-Lo-mac .extraclass class="requirement-machine"}

**Collabora Office cannot run in a simulator** because the LibreOfficeKit bits are built for an `iOS` target, but the simulator is `iOS-simulator`. Therefore, you'll need a real device to run this.

Building for `My Mac (Designed for iPad)` on Mac Silicon will run, but it is unstable. In particular, sometimes bugs are present on Mac that are not present on a mobile device or vice-versa. We strongly suggest you build and run for a physical iOS or iPadOS device.


## 1) Build the LibreOfficeKit code for iOS
### on a Mac ## {#ios-1-build-Lo-mac .extraclass class="requirement-machine"}

1.1) First you need to build the LibreOfficeKit code (LibreOffice core) for iOS. For the build dependencies, it is the best to install [LODE, the LibreOffice Development Environment](https://wiki.documentfoundation.org/Development/lode) and add its `bin` directory to the `PATH`. Then get LibreOffice core source code and put in your autogen.input something like this:

```bash
# Comment out for production builds
--enable-debug
--enable-dbgutil

# Standard build options
--enable-werror
--enable-symbols
--with-myspell-dicts
--with-distro=LibreOfficeiOS
--with-lang=ar bg ca cs da de el en-US en-GB eo es eu fi fr gl he hr hu id is it ja ko lo nb nl oc pl pt pt-BR sq ru sk sl sv tr uk vi zh-CN zh-TW
```

and build "normally". (Naturally, no unit tests will be run when cross-compiling LibreOffice.) Of course there is no requirement to use those --enable options; as a minimum, just `--with-distro=LibreOfficeiOS` should work.

This will produce a large number of static archives (.a) here and there in instdir and workdir, but no app that can be run as such. (You can see a list of them in workdir/CustomTarget/ios/ios-all-static-libs.list)

## 2) Build COOL Dependencies
### on a Mac ## {#ios-2-build-cool-mac .extraclass class="requirement-machine"}

PYTHON MODULES, NODEJS, and HOMEBREW

2.1.1) Install the following Python modules:
```bash
/usr/bin/pip3 install polib
/usr/bin/pip3 install lxml
```

2.1.2) Install nodejs from https://nodejs.org/en/download (macOS pkg). This package provides `npm` and `node` commands that are required to build everything in `browser/` folder.

2.1.3) Install Homebrew from https://github.com/Homebrew/brew/releases/latest (macOS pkg) and add /opt/homebrew/bin and /opt/homebrew/sbin to the end of your PATH.

2.1.4) Install the following Homebrew modules:
```bash
brew install pkg-config
brew install pixman
brew install cairo
brew install pango
brew install giflib
```
These modules are required to build `canvas` node module. On Intel based Macs the build system pulls a binary from GitHub, therefore building from source is only required on M1/M2 Macs.

POCO LIBRARY

2.2.1) The below instructions are for the so-called basic edition of
poco 1.10.1. (If there has been a newer release of poco by the time
you read this, adapt as necessary.) Get the poco library source code
from https://pocoproject.org/releases/poco-1.10.1/ , the
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
from https://github.com/facebook/zstd/releases/tag/v1.5.2/ , the
zstd-1.5.2.tar.gz archive.

Alternatively you can use the helper script to build libzstd for iOS: https://github.com/CollaboraOnline/online/blob/master/scripts/build-zstd-ios.sh

2.3.2) Unpack in some suitable location.

2.3.3) Compile. Note: in the first command, force SDK to iOS and set the
minimum iOS version to match the LibreOffice build:
```bash
CC="/usr/bin/clang -arch arm64 -isysroot /Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS.sdk -target arm64-apple-ios14.5" make
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

## 3) Build the iOS app
### on a Mac ## {#ios-3-clone-online-mac .extraclass class="requirement-machine"}
3.1) Do a separate clone of the online repo on macOS.

Run autogen.sh, and configure it with the --enable-iosapp option:

```bash
./autogen.sh
./configure \
--enable-iosapp \
--with-app-name="My Own Mobile Office Suite" \
--enable-experimental \
--with-vendor="MyOwnApp" \
--with-poco-includes=$HOME/poco-ios-arm64/include \
--with-poco-libs=$HOME/poco-ios-arm64/lib \
--with-zstd-includes=$HOME/zstd-ios-arm64/usr/local/include \
--with-zstd-libs=$HOME/zstd-ios-arm64/usr/local/lib \
--with-lo-builddir=/path/to/libreoffice/core
```

Then run:

```bash
(cd browser && make)
```

The configure script puts the app name as the `CFBundleDisplayName` property into the `ios/Mobile/Info.plist` file, and sets up some symbolic links that point to the LibreOffice core source and build directories (which typically will be the same, of course).

3.2) Before opening the Xcode project for the first time
   - seriously consider disabling source code indexing, this
   spawns a vast number of git processes, and consumes huge
   amounts of CPU & memory:

	Xcode -> Preferences, "Source Control", uncheck "Enable Source Control"

3.3) Now you can open the Mobile Xcode project. Important: you will still need to do some configuration before you can run the iOS app. Xcode is very restrictive and requires the following:
   - Xcode must be signed into an Apple ID that is a member of the Apple Developer Program
   - In the Xcode project's Signing & Capabilities panel, you must change the Bundle Identifier to a unique bundle ID. To obtain a unique bundle ID, login to your Apple Developer account at https://developer.apple.com and create a unique bundle ID in the Certificates, Identifiers & Profiles page. Be sure to check the Fonts and iCloud options in the Capabilities section. A screen snapshot of a sample unique build ID configuration is here: https://collaboraonline.github.io/images/build-code-ios-bundle-ID-config.png

3.4) Now you can open the Mobile Xcode project, build it, and run it. Note:
building for "My Mac (Designed for iPad)" on Mac Silicon will run, but it
is unstable. Also, you can't run in an emulator since LibreOffice for iOS is
built for arm64 only. So, effectively, you can only test the build on a real
iOS device.

{{< edit-button to="/content/post/build-code-ios.md" name="Edit page">}}
