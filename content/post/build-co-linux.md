+++
authors = [
    "Collabora",
]
title = "Build Collabora Office for Linux"
date = "2020-12-01"
home_pos = "2"
description = "Step-by-step build instructions"
tags = [
    "build",
    "make",
]
images = [
    "beaver/co-linux-copyrighted.png",
]
type = "sidebar"
layout = "sidebar"
showimage = false
+++

Linux lover? Build Collabora Office and unleash your inner hacker.

<!--more-->
# Build Collabora Office

This is the Collabora Office Linux app built on Qt6 WebEngine. It’s designed to work the same way as the Collabora Office apps for Windows (windows/) and macOS (macos/).
<section id="build-co-linux" class="build-co-linux">

## Linux

## Build
Use a separate “online” checkout — not the one you use for regular Online builds. Clone the LibreOffice core repository and switch to the `distro/collabora/coda-25.04` branch.  [For general build guidance, see the normal build instruction](/post/build-code/).

It Requires what Collabora Online already requires and the additionally following Qt
libraries: `Qt6Core Qt6Widgets Qt6Gui Qt6WebEngineCore Qt6WebChannel Qt6WebEngineWidgets`.

Run `./autogen.sh`, then configure
```sh
./configure --enable-qtapp --with-lo-path=/path/to/core/instdir --with-lokit-path=/path/to/core/include --enable-debug CXXFLAGS="-O2 -g -fPIC"

```
Adjust the paths to `--with-lo-path` and `--with-lokit-path`.

Then run `make -j$(nproc)` on the **top directory**. This will result in `coda-qt`
executable in this directory.

## Run

Usage: `./qt/coda-qt DOCUMENT [DOCUMENT...]`

e.g.
`./coda-qt ../test/data/hello.odt`

## Debug with Chromium DevTools

```sh
export QTWEBENGINE_REMOTE_DEBUGGING=3311
```

Then run `coda-qt` and open [http://localhost:3311](http://localhost:3311)

## Flatpak

### Building flatpak

There is a flatpak manifest under `flatpak/com.collabora.Office.json`.

Install following dependencies for building the flatpak.

```sh
flatpak install org.kde.Sdk//6.9 \
                org.kde.Platform//6.9 \
                org.freedesktop.Sdk.Extension.node20//24.08 \
                org.freedesktop.Sdk.Extension.openjdk21//24.08 \
                io.qt.qtwebengine.BaseApp//6.9
```

Use flatpak-builder to create a flatpak.

- Build and install user level:
`flatpak-builder build-dir com.collabora.Office.json --install --user --force-clean --ccache`

- Create a bundle from the build-dir:
`flatpak build-bundle .flatpak-builder/cache CODA-Q.bundle com.collabora.Office`

{{< edit-button to="/content/post/build-co-linux.md" name="Edit page">}}
