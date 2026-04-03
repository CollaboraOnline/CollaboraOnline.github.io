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
<section id="build-co-linux" class="build-co-linux">

# Build Collabora Office

This is the Collabora Office Linux Desktop app built on Qt6 WebEngine.

## Dependencies

### Fedora

Tested on Fedora 43.

```bash
sudo dnf install autoconf automake cppunit-devel fontconfig-devel gcc gcc-c++ \
    git libcap-devel libpng-devel libtool libzstd-devel make npm openssl-devel \
    pam-devel perl-JSON-PP pkgconf-pkg-config poco-devel python3-lxml \
    python3-polib qt6-linguist qt6-qtbase-devel qt6-qtwebengine-devel
```

### Ubuntu

Tested on Ubuntu 24.04 LTS.

```bash
sudo apt install -y autoconf automake build-essential cmake fontconfig git \
    libcap-dev libcppunit-dev libpam0g-dev libpng-dev libssl-dev libtool \
    libzstd-dev npm pkg-config python3-lxml python3-polib qt6-base-dev \
    qt6-tools-dev qt6-tools-dev-tools qt6-webengine-dev
```

#### Poco from source

Ubuntu 24.04 ships Poco 1.11.0, but Collabora Office requires 1.12.0 or newer. Build it from source:

```bash
wget https://github.com/pocoproject/poco/archive/refs/tags/poco-1.14.2-release.tar.gz
tar xzf poco-1.14.2-release.tar.gz
cd poco-poco-1.14.2-release
mkdir cmake-build && cd cmake-build
cmake .. -DCMAKE_INSTALL_PREFIX=/usr/local
make -j $(nproc)
sudo make install
sudo ldconfig
cd ../..
```

### Debian

Tested on Debian 13 (Trixie).

```bash
sudo apt install -y autoconf automake build-essential fontconfig git \
    libcap-dev libcppunit-dev libpam0g-dev libpng-dev libpoco-dev libssl-dev \
    libtool libzstd-dev npm pkg-config python3-lxml python3-polib \
    qt6-base-dev qt6-tools-dev qt6-tools-dev-tools qt6-webengine-dev
```

### Arch Linux

```bash
sudo pacman -Syu autoconf automake base-devel cppunit fontconfig \
    git libcap libpng libtool npm openssl pam perl-json-pp pkgconf poco \
    python-lxml python-polib qt6-base qt6-tools qt6-webengine zstd
```

### openSUSE

Tested on openSUSE Leap 16.0.

```bash
PYVER=$(python3 -c 'import sys; print(f"python{sys.version_info.major}{sys.version_info.minor}")')
sudo zypper install autoconf automake cppunit-devel fontconfig-devel gcc-c++ \
    git libcap-devel libopenssl-devel libpng16-compat-devel libpng16-devel \
    libtool libzstd-devel make npm-default pam-devel pkgconf poco-devel \
    ${PYVER}-lxml ${PYVER}-polib qt6-base-devel qt6-tools-linguist \
    qt6-webenginecore-devel qt6-webenginewidgets-devel
```

### General notes

A C++ compiler with full C++20 support is required, including `std::format` (GCC 13+ or Clang 17+).

Poco >= 1.12.0 is required. Some distros ship an older version -- see the [Ubuntu section](#poco-from-source) for building from source.

## Building

### Collabora Office Core

Collabora Office needs core to be built. For dependency installation, refer to https://wiki.documentfoundation.org/Development/BuildingOnLinux if needed.

```bash
git clone --depth 1 -b main https://gerrit.collaboraoffice.com/core
cd core
```

```bash
./autogen.sh --with-distro=CPLinux-LOKit --without-package-format --with-system-nss
make
```

> For debug builds, add `--enable-dbgutil` to the autogen line.

Once done, set the path for the online build:
```bash
export LOCOREPATH=$(pwd)
```

### Collabora Online

```bash
git clone https://github.com/CollaboraOnline/online.git collabora-online
cd collabora-online
```

```bash
./autogen.sh
./configure --enable-qtapp \
    --with-lo-path=${LOCOREPATH}/instdir \
    --with-lokit-path=${LOCOREPATH}/include \
    --enable-debug
make -j $(nproc)
```

> **Ubuntu:** if you built Poco from source, add `--with-poco-includes=/usr/local/include --with-poco-libs=/usr/local/lib` to configure.

This produces the `coda-qt` executable in `qt/`.

## Running

```bash
./qt/coda-qt                         # start without a document
./qt/coda-qt ../test/data/hello.odt  # open a file
```

## Debug with Chromium DevTools

```bash
export QTWEBENGINE_REMOTE_DEBUGGING=3311
```

Then run `coda-qt` and open [http://localhost:3311](http://localhost:3311)

## Flatpak

Install the runtimes:
```bash
flatpak install org.kde.Sdk//6.10 \
                org.kde.Platform//6.10 \
                org.freedesktop.Sdk.Extension.node20//25.08 \
                io.qt.qtwebengine.BaseApp//6.10
```

Build and export to a local repo:
```bash
flatpak-builder --repo=repo --force-clean --ccache build-dir \
    qt/flatpak/com.collaboraoffice.Office.json
```

Create a `.flatpak` bundle from the repo:
```bash
flatpak build-bundle repo CollaboraOffice.flatpak com.collaboraoffice.Office
```

Or install directly from the repo:
```bash
flatpak --user remote-add --no-gpg-verify --if-not-exists co-local repo
flatpak --user install co-local com.collaboraoffice.Office
```

### Debug symbols

To include debug symbols in the build, add `--keep-build-dirs` and export the debug extension:
```bash
flatpak-builder --repo=repo --force-clean --ccache --keep-build-dirs build-dir \
    qt/flatpak/com.collaboraoffice.Office.json
flatpak build-bundle repo CollaboraOffice.Debug.flatpak \
    com.collaboraoffice.Office.Debug --runtime
```

If you just want a pre-built package instead of compiling, download the
**Collabora Office Linux Flatpak snapshots** here:
👉 https://www.collaboraoffice.com/downloads/Collabora-Office-Linux-Snapshot/

</section>

{{< edit-button to="/content/post/build-co-linux.md" name="Edit page">}}
