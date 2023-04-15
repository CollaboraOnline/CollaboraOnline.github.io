+++
authors = [
    "Collabora",
]
title = "Build Collabora Online"
date = "2020-12-01"
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
# Build CODE
Build **C**ollabora **O**nline **D**evelopment **E**dition. Choose your operating system or opt for using Gitpod (hack, build, debug and run entirely using a web-browser) from the list below for straightforward instructions to get you going quickly. If you are a seasoned developer with commit access, or just feeling extraordinarily brave, feel free to follow the general instructions.

{{< build-dropdown >}}<br>

<section id="build-code-gitpod" class="build-code-content">

## Gitpod {#build-code-on-gitpod}
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

{{% common-build-commands section="running" %}}

If you are using VS Code as your IDE and want to run code in your local VS Code with local ports, follow these steps:
1. Open Gitpod and navigate to the top left option.
2. Select `Gitpod: Open in VS Code`.
3. Install the following extensions in your VS Code: `Gitpod`, `Remote - SSH`, `Remote - SSH: Editing Configuration Files`, and `Remote Explorer`.
4. Configure your SSH key in VS Code.
5. Once everything is set up, type make run. This will allow you to access the hosted port on your local machine.

    
If you are not using the VS Code desktop and instead just your web browser, to open and test Collabora Online:
1. Make sure your web browser is not blocking any tabs from opening;
2. Check that you have the VCN tab opened (if not, open it up from the left side Remote explorer > 6080)
3. In the terminal where make is running: scroll and copy the the URL ending with: hello-world.odt
4. In a new terminal execute the following:
   firefox  [paste copied URL here]
</section>

---

<section id="build-code-opensuse" class="build-code-content">

## openSUSE {#build-code-on-opensuse}
The instructions below have been prepared for and tested on openSUSE Leap 15.3. You might need to do small adjustments for other releases.

### Dependencies
We need LibreOffice core, POCO library and several other libraries and tools to build `CODE`. Open a terminal and follow the steps below.

```bash
# For Leap 15.3
zypper ar http://download.opensuse.org/repositories/devel:/libraries:/c_c++/15.3/devel:libraries:c_c++.repo

# For Leap 15.4
zypper ar http://download.opensuse.org/repositories/devel:/libraries:/c_c++/15.4/devel:libraries:c_c++.repo
```
If this is fresh instalation it might be worth install devel-basis pattern: Minimal set of tools for compiling and linking applications.
It will bring in things like git, gcc, etc.
```bash
sudo zypper install -t pattern devel_basis
```
Now go ahead and install the following packages
```bash
zypper in poco-devel libcap-progs python3-polib libcap-devel npm libtool cppunit-devel pam-devel python3-lxml chromium

# If you are using Leap 15.4 please install this aditional compatability library
zypper in libpng16-compat-devel
```

### LibreOffice
{{% common-build-commands section="code-needs-lo-wget" %}}

### Building CODE
You need to clone it, run autoconf/automake, configure and build using the GNU
make. **Before moving on, [fork the repo](https://github.com/CollaboraOnline/online/fork) if you haven't done that yet.**

Now clone the forked repo:
{{% common-build-commands section="clone-online" %}}

{{% common-build-commands section="build-online" %}}

{{% common-build-commands section="run-unit-tests" %}}

{{% common-build-commands section="running" %}}

</section>

---

<section id="build-code-fedora" class="build-code-content">

## Fedora {#build-code-on-fedora}

The instructions below have been prepared for and tested on Fedora 37. You might need to do small adjustments for Fedora-based distributions.

### Dependencies
We need LibreOffice core, POCO library and several other libraries and tools to build `CODE`.

Open a terminal and follow the steps below:

```bash
sudo dnf install poco-devel gcc gcc-c++ python3-polib \
                 libtool libstdc++-devel libpng libpng-devel \
                 cppunit-devel nodejs-devel chromium \
                 libzstd-devel libcap-devel pam-devel
```

### LibreOffice
{{% common-build-commands section="code-needs-lo-wget" %}}

### Building CODE
You need to clone it, run autoconf/automake, configure and build using the GNU
make. **Before moving on, [fork the repo](https://github.com/CollaboraOnline/online/fork) if you haven't done that yet.**

Now clone the forked repo:
{{% common-build-commands section="clone-online" %}}

{{% common-build-commands section="build-online" %}}

{{% common-build-commands section="run-unit-tests" %}}

{{% common-build-commands section="running" %}}

</section>

---

<section id="build-code-arch" class="build-code-content">

## Arch {#build-code-on-arch}

The instructions below have been prepared for and tested on Manjaro 21.2.3. You might need to do small adjustments for Arch and/or other Arch-based distributions.

### Dependencies
We need LibreOffice core, POCO library and several other libraries and tools to build `CODE`.

Open a terminal and follow the steps below:
```bash
sudo pacman -Syu libcap libcap-ng lib32-libcap libpng poco cppunit nodejs npm chromium python-lxml
```

Additionally you will need to install python-polib. You can do this using pip (as below) *or* using [the python-polib AUR package](https://aur.archlinux.org/packages/python-polib)
```bash
sudo pacman -Syu python-pip
sudo pip install polib
```

### LibreOffice
{{% common-build-commands section="code-needs-lo-wget" %}}

### Building CODE
You need to clone it, run autoconf/automake, configure and build using the GNU
make. **Before moving on, [fork the repo](https://github.com/CollaboraOnline/online/fork) if you haven't done that yet.**

Now clone the forked repo:
{{% common-build-commands section="clone-online" %}}

{{% common-build-commands section="build-online" %}}

{{% common-build-commands section="run-unit-tests" %}}

{{% common-build-commands section="running" %}}

</section>

---

<section id="build-code-debian" class="build-code-content">

## Debian {#build-code-on-debian}
The instructions below have been prepared for and tested on Debian GNU/Linux 11 (bullseye). You might need to do small
adjustments for other releases.


*Note: Sometimes Debian comes without sudo preinstalled. If you do not have sudo, you will need to run `apt install -y sudo` as root. It is not good enough to only run the commands which require sudo below as root, as sudo is also run during `make`*

### Dependencies
We need LibreOffice core, POCO library and several other libraries and tools to build `CODE`. Open a terminal and follow the steps below.

Lets start by installing the `dialog` package, which will be needed while installing some
of the other packages:
```bash
sudo apt install -y dialog
```

Now install the rest of the required packages:
```bash
sudo apt install -y libpoco-dev python3-polib libcap-dev npm \
                    libpam-dev wget git build-essential libtool \
                    libcap2-bin python3-lxml libpng-dev libcppunit-dev \
                    pkg-config fontconfig chromium
```

### LibreOffice
{{% common-build-commands section="code-needs-lo-wget" %}}

### Building CODE
You need to clone it, run autoconf/automake, configure and build using the GNU
make. **Before moving on, [fork the repo](https://github.com/CollaboraOnline/online/fork) if you haven't done that yet.**

Now clone the forked repo:
{{% common-build-commands section="clone-online" %}}

{{% common-build-commands section="build-online" %}}

{{% common-build-commands section="run-unit-tests" %}}

{{% common-build-commands section="running" %}}

</section>

---

<section id="build-code-ubuntu" class="build-code-content">

## Ubuntu {#build-code-on-ubuntu}
The instructions below have been prepared for and tested on Ubuntu 20.04 LTS. You might need to do small
adjustments for other releases.

### Dependencies
We need LibreOffice core, POCO library and several other libraries and tools to build `CODE`. Open a terminal and follow the steps below.

Lets start by installing the `dialog` package, which will be needed while installing some
of the other packages:
```bash
sudo apt install -y dialog
```

Now install the rest of the required packages:
```bash
sudo apt install -y libpoco-dev python3-polib libcap-dev npm \
                    libpam-dev libzstd-dev wget git build-essential libtool \
                    libcap2-bin python3-lxml libpng-dev libcppunit-dev \
                    pkg-config fontconfig snapd chromium-browser
```

*Note: Chomium is needed and used in cpress tests. Ubuntu has no chromium deb packages in its repositories, only a dummy pacakge that points to the respective snap. Probably best to make sure you have snapd installed and install chromium-browser which in turn will install the snap package.*

### LibreOffice
{{% common-build-commands section="code-needs-lo-wget" %}}

### Building CODE
You need to clone it, run autoconf/automake, configure and build using the GNU
make. **Before moving on, [fork the repo](https://github.com/CollaboraOnline/online/fork) if you haven't done that yet.**

Now clone the forked repo:
{{% common-build-commands section="clone-online" %}}

{{% common-build-commands section="build-online" %}}

{{% common-build-commands section="run-unit-tests" %}}

{{% common-build-commands section="running" %}}

</section>

---

<section id="build-code-general" class="build-code-content">

## Build CODE & LO {#build-code-n-lo}

### Dependencies

The CODE must be built on Linux, and you need the following:

* LibreOffice
  + you need to build your own tree
* Poco library: http://pocoproject.org/
  + either use a package from your distro, or build it yourself (see below)
* libpng, libcap-progs, libtool, automake, autoconf, pkg-config, sudo, pam
  + use the packages from your distro

You may also want to have the following optional dependencies:

* Chromium
  + Needed for running cypress tests
* The lxml and polib libraries for python
  + Needed for building javascript
  + These can both be installed via pip or your distro's packages
* Cppunit
  + Needed for unit tests
* Node.js
  + Needed for building the JS parts (not needed if you build them on another linux machine)

### LibreOffice

CODE needs LibreOffice to be built to run. However, you have two options to meet this requirement: either by building it locally (Option A - recommended), or by downloading a daily built archive (Option B - quick & dirty) which contains only the absolutely necessary pieces. If you are working only on the online side, without doing any code-level changes on the LibreOffice core, or you just want to quickly get going to do some small fixes, you may prefer the second way.

#### Option A - Build LibreOffice locally (Recommended)
To build LibreOffice, follow the LibreOffice building pages:

https://wiki.documentfoundation.org/Development/BuildingOnLinux

Make sure you use and build the following specific core branch: `distro/collabora/co-23.05`

#### Option B - Download a Daily-Built Archive of LibreOffice (Quick & Dirty)
Download the daily archive:
```
wget https://github.com/CollaboraOnline/online/releases/download/for-code-assets/core-co-23.05-assets.tar.gz
```

Extract the archive:
```
tar xvf core-co-23.05-assets.tar.gz
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
{{% common-build-commands section="clone-online" %}}
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

{{% common-build-commands section="run-unit-test" %}}

{{% common-build-commands section="running" %}}
</section>

{{< edit-button to="/content/post/build-code.md" name="Edit page">}}
