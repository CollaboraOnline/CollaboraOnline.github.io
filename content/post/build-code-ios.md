+++
authors = [
    "Collabora",
]
title = "Build for iOS"
date = "2023-09-01"
home_pos = "6"
description = "Step-by-step build instructions"
tags = [
    "build",
    "make",
]
images = [
    "beaver/build-code-ios-copyrighted.png",
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

**Collabora Office cannot run in a simulator** because the engine is built for an `iOS` target, but the simulator is `iOS-simulator`. Therefore, you'll need a real device to run this.

Building for `My Mac (Designed for iPad)` on Mac Silicon will run, but it is unstable. In particular, sometimes bugs are present on Mac that are not present on a mobile device or vice-versa. We strongly suggest you build and run for a physical iOS or iPadOS device.


## 1) Build the engine for iOS
### on a Mac ## {#ios-1-build-Lo-mac .extraclass class="requirement-machine"}

1.1) Apart from Xcode, building the engine needs the usual autotools and pkg-config, which you can install with [Homebrew](https://brew.sh/):

```bash
brew install autoconf automake libtool pkg-config
```

All the source code now lives in a single Gerrit monorepo; the former Collabora Office core is the `engine/` subdirectory of the `online` repo, so there is no separate repository to clone any more. Code review happens on [Gerrit](https://gerrit.collaboraoffice.com/), not GitHub pull requests; see the [first contribution guide](https://forum.collaboraonline.com/t/your-first-pull-request/41) for the full workflow.

For an anonymous read-only clone:

```bash
git clone https://gerrit.collaboraoffice.com/online collabora-office
```

If you have a Gerrit account and plan to push changes for review, clone over SSH instead:

```bash
git clone ssh://YOUR_USERNAME@gerrit.collaboraoffice.com:29418/online collabora-office
```

Then move into `collabora-office/engine` and put in your autogen.input something like this:

```bash
# Comment out for production builds
--enable-debug
--enable-dbgutil

# Standard build options
--enable-werror
--enable-symbols
--with-myspell-dicts
--with-distro=CPiOS
--with-lang=ar bg ca cs da de el en-US en-GB eo es eu fi fr gl he hr hu id is it ja ko lo nb nl oc pl pt pt-BR sq ru sk sl sv tr uk vi zh-CN zh-TW
```

and build "normally". (Naturally, no unit tests will be run when cross-compiling.) Of course there is no requirement to use those --enable options; as a minimum, just `--with-distro=CPiOS` should work.

This will produce a large number of static archives (.a) here and there in instdir and workdir, but no app that can be run as such. (You can see a list of them in workdir/CustomTarget/ios/ios-all-static-libs.list)

## 2) Build COOL Dependencies
### on a Mac ## {#ios-2-build-cool-mac .extraclass class="requirement-machine"}

PYTHON MODULES, NODEJS, and HOMEBREW

2.1.1) Install the following Python modules:
```bash
/usr/bin/pip3 install polib
/usr/bin/pip3 install lxml
```

2.1.2) Install nodejs (20.x) by downloading the macOS .pkg from the `Prebuilt installer` tab at https://nodejs.org/en/download. It provides the `npm` and `node` commands that are required to build everything in the `browser/` folder.

2.1.3) Install Homebrew from https://github.com/Homebrew/brew/releases/latest (macOS pkg) and add /opt/homebrew/bin and /opt/homebrew/sbin to the end of your PATH.

2.1.4) Install pkg-config via Homebrew:
```bash
brew install pkg-config
```

POCO and zstd are built as part of the engine and taken
from its workdir, so they no longer need to be built separately for iOS.

## 3) Build the iOS app
### on a Mac ## {#ios-3-clone-online-mac .extraclass class="requirement-machine"}
3.1) Step back to the top of the `collabora-office` clone (one level up from `engine/`) - the same monorepo you used in step 1 contains the online sources.

Run autogen.sh, and configure it with the --enable-iosapp option:

```bash
./autogen.sh
./configure \
--enable-iosapp \
--with-app-name="My Own Mobile Office Suite" \
--enable-experimental \
--with-vendor="MyOwnApp" \
--with-lo-builddir=$(pwd)/engine
```

Then run:

```bash
(cd browser && make)
```

The configure script puts the app name as the `CFBundleDisplayName` property into the `ios/Mobile/Info.plist` file, and sets up some symbolic links that point to the engine source and build directories (which typically will be the same, of course).

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
is unstable. Also, you can't run in an emulator since the engine for iOS is
built for arm64 only. So, effectively, you can only test the build on a real
iOS device.

{{< edit-button to="/content/post/build-code-ios.md" name="Edit page">}}
