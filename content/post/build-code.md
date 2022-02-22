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
type = "sidebar"
layout = "sidebar"
+++

Are you interested in contributing but don't know where to start? Head over documentation or start by following these step-by-step instructions and build `CODE` from scratch.

<!--more-->

Choose your operating system or opt for using Gitpod (hack, build, debug and run entirely using a web-browser) from the list below for straightforward instructions to get you going quickly. If you are a seasoned developer with commit access, or just feeling extraordinarily brave, feel free to follow the general instructions.

{{< build-dropdown >}}<br>

<section id="build-code-gitpod" class="build-code-content">

## Build CODE on Gitpod
On top of our daily LibreOffice core archives, we have also added integration support for Gitpod, a cloud based development environment. Now you can start hacking Collabora Online (COOL) in under ~5 minutes!

**Steps to quick start:**

* Sign-up on [Gitpod.io](http://gitpod.io/) with your GitHub account
* Install the [proper extension](https://www.gitpod.io/docs/browser-extension/) for your browser
* Go to [COOL repo](https://github.com/CollaboraOnline/online)
* Click on the green Gitpod button near the top of the GitHub repo page

![GitPod green button on GitHub](/images/gitpod-button-onGitHub.png)

* Wait for a few minutes, and you will have a full development environment with COOL already cloned & built, ready-to-start/develop

{{< figure src="/images/gitpod-screenshot-COOL.png" title="Gitpod, your development environment for Collabora Online on the cloud">}}

* Don’t forget to fork the main repo ![|226x56](/images/forking.gif)
* And set the remote address in .git/config to point to your fork’s address with this command:

```bash
git remote set-url origin https://github.com/PUT-YOUR-GITHUB-USERNAME-HERE/online.git
```

Happy hacking! : )

_First published on [ Collabora Online Community Roundup #2](https://www.collaboraoffice.com/online/collabora-online-community-roundup-2/)_

</section>

<section id="build-code-opensuse" class="build-code-content">

## Build CODE on openSUSE
The instructions below have been prepared for and tested on openSUSE Leap 15.3. You might need to do small adjustments for other releases.

### Dependencies
We need LibreOffice core, POCO library and several other libraries and tools to build `CODE`. Open a terminal and follow the steps below.

```bash
zypper ar http://download.opensuse.org/repositories/devel:/libraries:/c_c++/openSUSE_Leap_15.3/devel:libraries:c_c++.repo
```
```bash
zypper in poco-devel libcap-progs python3-polib libcap-devel npm libtool cppunit-devel pam-devel python3-lxml
```

### LibreOffice
CODE needs LibreOffice to be built to run. However, it takes a considerable amount of time and brings in
extra complexity. So, we will instead download a daily built archive which contains only the pieces that are absolutely necessary. If you are working only on the online side, without doing any code-level changes on the LibreOffice core, or you just want to quickly get going to do some small fixes, then this will be enough for you. Otherwise, refer to the general instructions.

Now download a daily-built archive of LibreOffice core:
```bash
wget https://github.com/CollaboraOnline/online/releases/download/for-code-assets/core-co-2021-assets.tar.gz
```

Extract the contents of the archive:
```bash
tar xvf core-co-2021-assets.tar.gz
```

Mark the location of the extracted contents before changing directory:
```bash
export LOCOREPATH=$(pwd)
```
### Building CODE
You need to clone it, run autoconf/automake, configure and build using the GNU
make. **Before moving on, [fork the repo](https://github.com/CollaboraOnline/online/fork) if you haven't done that yet.**

Now clone the forked repo:
```bash
git clone https://github.com/YOURUSERNAME/online.git collabora-online
```

Switch to the local clone's directory:
```bash
cd collabora-online
```

Run autogen to generate the configure file:
```bash
./autogen.sh
```

Run the generated configure script with proper parameters:
```bash
./configure --enable-silent-rules --with-lokit-path=${LOCOREPATH}/include \
            --with-lo-path=${LOCOREPATH}/instdir \
            --enable-debug --enable-cypress
```
Note: you can also add `--disable-ssl` instead of changing coolwsd.xml everytime you want to disable ssl.

Start the actual build, which might take from a few minutes to half an hour (or more) depending on how powerful your machine is:
```bash
make -j $(nproc)
```

If you want to run the unit tests, use `make check` instead of the `make`.

Note that the loolforkit program needs the `CAP_SYS_CHROOT` capability,
thus **you will be asked the root password** when running make as it
invokes `sudo` to run `/sbin/setcap`.

Found a problem? [Submit an issue to contribute](https://github.com/CollaboraOnline/online/issues/new)!
</section>

<section id="build-code-fedora" class="build-code-content">

## Build CODE on Fedora
The instructions for Fedora will be here. [Submit an issue to contribute](https://github.com/CollaboraOnline/online/issues/new)!
</section>

<section id="build-code-arch" class="build-code-content">

## Build CODE on Arch

The instructions below have been prepared for and tested on Manjaro 21.2.0. You might need to do small adjustments for Arch and/or other Arch-based distributions.

### Dependencies
We need LibreOffice core, POCO library and several other libraries and tools to build `CODE`.

Open a terminal and follow the steps below:

```bash
sudo pacman -Syu libcap libcap-ng lib32-libcap libpng
```

```bash
sudo pacman -Syu poco
```

### LibreOffice
CODE needs LibreOffice to be built to run. However, it takes a considerable amount of time and brings in extra complexity. So, we will instead download a daily built archive which contains only the pieces that are absolutely necessary. If you are working only on the online side, without doing any code-level changes on the LibreOffice core, or you just want to quickly get going to do some small fixes, then this will be enough for you. Otherwise, refer to the general instructions.

Now download a daily-built archive of LibreOffice core:
```bash
wget https://github.com/CollaboraOnline/online/releases/download/for-code-assets/core-co-2021-assets.tar.gz
```

Extract the contents of the archive:
```bash
tar xvf core-co-2021-assets.tar.gz
```

Mark the location of the extracted contents before changing directory:
```bash
export LOCOREPATH=$(pwd)
```

### Building CODE
You need to clone it, run autoconf/automake, configure and build using the GNU
make. **Before moving on, [fork the repo](https://github.com/CollaboraOnline/online/fork) if you haven't done that yet.**

Now clone the forked repo:
```bash
git clone git@github.com:YOURUSERNAME/online.git collabora-online
```

Switch to the local clone's directory:
```bash
cd collabora-online
```

Run autogen to generate the configure file:
```bash
./autogen.sh
```
(install all missing packages that `./autogen.sh` couldn't find on your system)

Run the generated configure script with proper parameters:
```bash
./configure --enable-silent-rules --with-lokit-path=${LOCOREPATH}/include \
            --with-lo-path=${LOCOREPATH}/instdir \
            --enable-debug --enable-cypress
```
Note: you can also add `--disable-ssl` instead of changing coolwsd.xml everytime you want to disable ssl.

Start the actual build, which might take from a few minutes to half an hour (or more) depending on how powerful your machine is:
```bash
make -j $(nproc)
```

If you want to run the unit tests, use `make check` instead of the `make`.

Note that the loolforkit program needs the `CAP_SYS_CHROOT` capability,
thus **you will be asked the root password** when running make as it
invokes `sudo` to run `/sbin/setcap`.

Found a problem? [Submit an issue to contribute](https://github.com/CollaboraOnline/online/issues/new)!

</section>

<section id="build-code-ubuntu" class="build-code-content">

## Build CODE on Ubuntu
The instructions below have been prepared for and tested on Ubuntu 20.04 LTS. You might need to do small
adjustments for other releases.

### Dependencies
We need LibreOffice core, POCO library and several other libraries and tools to build `CODE`. Open a terminal and follow the steps below.

Lets start by installing the `dialog` package, which will be needed while installaing some
of the other packages:
```bash
sudo apt install -y dialog
```

Now install the rest of the required packages:
```bash
sudo apt install -y libpoco-dev python3-polib libcap-dev npm \
                    libpam-dev wget git build-essential libtool \
                    libcap2-bin python3-lxml libpng-dev libcppunit-dev \
                    pkg-config fontconfig
```

### LibreOffice
CODE needs LibreOffice to be built to run. However, it takes a considerable amount of time and brings in
extra complexity. So, we will instead download a daily built archive which contains only the absolutely necessary pieces. If you are working only on the online side, without doing any code-level changes on the LibreOffice core, or you just want to quickly get going to do some small fixes, then this will be enough for you. Otherwise, refer to the general instructions.

Now download a daily-built archive of LibreOffice core:
```bash
wget https://github.com/CollaboraOnline/online/releases/download/for-code-assets/core-co-2021-assets.tar.gz
```

Extract the contents of the archive:
```bash
tar xvf core-co-2021-assets.tar.gz
```

Mark the location of the extracted contents before changing directory:
```bash
export LOCOREPATH=$(pwd)
```

### Building CODE
You need to clone it, run autoconf/automake, configure and build using the GNU
make. **Before moving on, [fork the repo](https://github.com/CollaboraOnline/online/fork) if you haven't done that yet.**

Now clone the forked repo:
```bash
git clone https://github.com/YOURUSERNAME/online.git collabora-online
```

Switch to the local clone's directory:
```bash
cd collabora-online
```

Run autogen to generate the configure file:
```bash
./autogen.sh
```

Run the generated configure script with proper parameters:
```bash
./configure --enable-silent-rules --with-lokit-path=${LOCOREPATH}/include \
            --with-lo-path=${LOCOREPATH}/instdir \
            --enable-debug --enable-cypress
```
Note: you can also add `--disable-ssl` instead of changing coolwsd.xml everytime you want to disable ssl.

Start the actual build, which might take from a few minutes to half an hour (or more) depending on how powerful your machine is:
```bash
make -j $(nproc)
```

If you want to run the unit tests, use `make check` instead of the `make`.

Note that the loolforkit program needs the `CAP_SYS_CHROOT` capability,
thus **you will be asked the root password** when running make as it
invokes `sudo` to run `/sbin/setcap`.
</section>

<section id="build-code-general" class="build-code-content">

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

Make sure you use and build the following specific core branch: `distro/collabora/co-2021`

#### Option B - Download a Daily-Built Archive of LibreOffice (Quick & Dirty)
Download the daily archive:
```
wget https://github.com/CollaboraOnline/online/releases/download/for-code-assets/core-co-2021-assets.tar.gz
```

Extract the archive:
```
tar xvf core-co-2021-assets.tar.gz
```

You should now have two new directories extracted: `instdir` and `include`. You will use the locations of these directories for the `configure` parameters in the following steps.

### POCO

If you use openSUSE Leap 15.3, you can use:

    zypper ar http://download.opensuse.org/repositories/devel:/libraries:/c_c++/openSUSE_Leap_15.3/devel:libraries:c_c++.repo
    zypper in poco-devel libcap-progs python3-polib libcap-devel npm libtool cppunit-devel pam-devel python3-lxml

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
```bash
git clone git@github.com:CollaboraOnline/online.git collabora-online
```
```bash
cd collabora-online
```
```bash
./autogen.sh
```
```bash
./configure --enable-silent-rules --with-lokit-path=${MASTER}/include \
            --with-lo-path=${MASTER}/instdir \
            --with-poco-includes=<POCOINST>/include --with-poco-libs=<POCOINST>/lib \
            --enable-debug --enable-cypress
```
Note: you can also add `--disable-ssl` instead of changing coolwsd.xml everytime you want to disable ssl.
```bash
make -j `nproc`
```
In the above, `${MASTER}` is the location of the LibreOffice source tree you have built
in the previous steps. `POCOINST` is the location of your custom-built or externally installed POCO library.
If you use POCO from a distro package (not a self-built version), you can omit
the `--with-poco-includes` and `--with-poco-libs` from the above.

If you want to run the unit tests, use `make check` instead of the `make`.

Note that the loolforkit program needs the `CAP_SYS_CHROOT` capability,
thus you will be asked the root password when running make as it
invokes sudo to run `/sbin/setcap`.
</section>

### Running

Now do:

    make run

Among other, the output will contain the links that you can directly follow to
see Writer, Calc, and Impress test documents in your browser.

### Hacking it

When you change a JavaScript file (they are located under the browser/
subdirectory), you need to stop the existing CODE instance and issue `make
run` again, because the files are cached.

Alternatively you can export a variable like:

    export LOOL_SERVE_FROM_FS=1

to avoid the caching, so that you can just Shift+Reload the pages to see the
new content.

{{< edit-button to="/content/post/build-code.md" name="Edit page">}}
