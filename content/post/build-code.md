+++
authors = [
    "Collabora",
]
title = "Build Collabora Online"
date = "2020-10-01"
description = "Step-by-step build instructions"
tags = [
    "build",
    "make",
]
images = [
    "build-code.jpg",
]
+++

Are you interested in contributing but do not know where to start? Head over documentation or start of by following these step-by-step instructions and build `CODE` from scratch:

* [Build CODE]({{< relref "build-code.md" >}} "Explore and clone GitHub repository")
* [Build CODE for Android]({{< relref "build-code-android.md" >}} "Step-by-step setup")
<!--more-->
## Build CODE

### Dependencies

The CODE must be built on Linux, and you need the following:

* LibreOffice
  + you need to build your own tree
* Poco library: http://pocoproject.org/
  + either use a package from your distro, or build it yourself (see below)
* libpng, libcap-progs
  + use the packages from your distro

### LibreOffice

CODE needs LibreOffice to be built to run. However, you have two options to meet this requirement: either by building it locally (Option A - recommended), or by downloading a daily built archive (Option B - quick & dirty) which contains only the absolutely necessary pieces. If you are working only on the online side, without doing any code-level changes on the LibreOffice core, or you just want to quickly get going to do some small fixes, you may prefer the second way.

#### Option A - Build LibreOffice locally (Recommended)
To build LibreOffice, follow the LibreOffice building pages:

https://wiki.documentfoundation.org/Development/BuildingOnLinux

Make sure you use and build the following specific core branch: `distro/collabora/cp-6.4`

#### Option B - Download a Daily-Built Archive of LibreOffice (Quick & Dirty)
Download the daily archive:
```
wget https://github.com/CollaboraOnline/online/releases/download/for-code-assets/core-cp-6.4-assets.tar.gz
```

Extract the archive:
```
tar xvf core-cp-6.4-assets.tar.gz
```

You should now have two new directories extracted: `instdir` and `include`. You will use the locations of these directories for the `configure` parameters in the following steps.

### POCO

If you use openSUSE Leap 15.1, you can use:

    zypper ar http://download.opensuse.org/repositories/devel:/libraries:/c_c++/openSUSE_Leap_15.1/devel:libraries:c_c++.repo
    zypper in poco-devel libcap-progs python3-polib libcap-devel npm

Similar repos exist for other openSUSE and SLE releases.

Collabora provides Poco packages for Debian 8, Debian 9, Ubuntu 16.04 LTS,
and CentOS 7 via the CODE (Collabora Online Development Edition) repositories,
see:

https://www.collaboraoffice.com/code/linux-packages/

Alternatively you can build your own POCO. In that case, ideally use a recent version like
1.10.1 or newer.

### Building CODE

You need to clone it, run autoconf/automake, configure and build using the GNU
make:

    git clone git@github.com:CollaboraOnline/online.git collabora-online
    cd collabora-online
    ./autogen.sh
    ./configure --enable-silent-rules --with-lokit-path=${MASTER}/include \
                --with-lo-path=${MASTER}/instdir \
                --with-poco-includes=<POCOINST>/include --with-poco-libs=<POCOINST>/lib \
                --enable-debug
    make

In the above, ${MASTER} is the location of the LibreOffice source tree you have built
in the previous steps.

If you want to run the unit tests, use `make check` instead of the `make`.

Note that the loolforkit program needs the CAP_SYS_CHROOT capability,
thus you will be asked the root password when running make as it
invokes sudo to run /sbin/setcap.

If you use POCO from a distro package (not a self-built version), you can omit
the --with-poco-includes and and --with-poco-libs from the above.

### Running

Now do:

    make run

Among other, the output will contain the links that you can directly follow to
see Writer, Calc, and Impress test documents in your browser.

### Hacking it

When you change a JavaScript file (they are located under the loleaflet/
subdirectory), you need to stop the existing CODE instance and issue `make
run` again, because the files are cached.

Alternatively you can export a variable like:

    export LOOL_SERVE_FROM_FS=1

to avoid the caching, so that you can just Shift+Reload the pages to see the
new content.
