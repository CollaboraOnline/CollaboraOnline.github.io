+++
authors = [
    "Collabora",
]
title = "Build Collabora Office for Mac"
date = "2020-12-01"
home_pos = "4"
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

Got a Mac and a curious mind? Build your own Collabora Office and see the magic happen.

<!--more-->
# Build Collabora Office

The steps below are for building the Collabora Office in macOS (macos/).

<section id="build-co-mac" class="build-co-linux">

## Mac

The following instructions depend heavily on using Homebrew, as that makes the
managing the build requirements much easier. It is of course possible to avoid
it, and only depend on eg. self-built POCO, etc.

### Setup

* Node.js
    + Needed for building the JS parts (not needed if you build them on another linux machine)
    + Install nodejs (20.x) by downloading the macOS .pkg from the `Prebuilt installer` tab at https://nodejs.org/en/download. It provides the `npm` and `node` commands that are required to build everything in the `browser/` folder.
* for ./configure
    ```
    brew install libtool
    ```

* install the Python helpers used by the build
    ```
    /opt/homebrew/bin/pip3 install --break-system-packages lxml
    /opt/homebrew/bin/pip3 install --break-system-packages polib
    ```

* Install and/or update the Command Line Tools for Xcode:
    * `xcode-select --install`
    * After that you might need to update them in System Settings > General > Software Updates
        * For some reason for me it lists both 15.3 and 16.0 there. As I have Xcode 16.0, I choose just that one.

### Clone the monorepo

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

### Build the engine

Move into the `engine/` subdirectory of the monorepo and build the `main` branch with the following `autogen.input`.

`autogen.input`:

    # Distro
    --with-distro=CPMacOS-LOKit
    --disable-mergelibs

    # Overrides for the debug builds
    --enable-debug
    #--enable-dbgutil

    --enable-werror
    --enable-symbols
    # If you don't want localizations
    --without-lang

For dependency installation, refer to https://wiki.documentfoundation.org/Development/BuildingOnLinux

### Configure Collabora Online

Run this from the top of the monorepo (one level up from `engine/`):

    ./autogen.sh && ./configure \
    --enable-macosapp \
    --enable-experimental \
    --with-app-name="Collabora Office" \
    --with-app-package-name=com.yourpackage.name \
    --with-vendor="Your Name" \
    --with-lo-path=engine/instdir/your-built-lo.app

POCO, zstd and libpng are built as part of the engine and taken from its
workdir, so they no longer need to be installed (via Homebrew or otherwise) or
passed on the configure line.

Adjust `your-built-lo.app` to match the app bundle name produced by your engine
build.

### Build the JavaScipt bits

Just run `make` from the terminal.

### Build the Desktop Edition

Open the macos/coda/coda.xcodeproj project in Xcode and choose `Build and Run current scheme`.

That's it!

### pre-built macOS

If you just want a pre-built macOS version instead of building locally, please use
the **TestFlight preview build**:  
👉 https://testflight.apple.com/join/sbkwMzMt


</section>

{{< edit-button to="/content/post/build-co-mac.md" name="Edit page">}}
