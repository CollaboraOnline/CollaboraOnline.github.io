+++
authors = [
    "Collabora",
]
title = "Build for Android"
date = "2022-07-02"
home_pos = "2"
description = "Step-by-step build instructions"
tags = [
    "build",
    "make",
]
images = [
    "build-code-android.jpg",
]
type = "sidebar"
layout = "sidebar"
showimage = false
showtitle = true
+++

Are you familiar with Android development environment and interested to learn more while helping the project?

# How to build the Android app:

## You will need

### A computer with Linux installed ## {.extraclass class="requirement-machine"}

The development of the Android app has to be done on Linux, it's currently not possible to
build the native parts on Windows

### The Android platform tools including a compatible NDK  ## {.extraclass class="requirement-machine"}

Builds have been tested with Android NDK 23.0.7599858, other NDK versions may or
may not work

### An Android or ChromeOS device or simulator ## {.extraclass class="requirement-machine"}

The Android app can run in a simulator, however some bugs may be present in a
simulator that are not present on a mobile device or vice-versa. If you are able
to, we strongly suggest you build and run for a physical device.

You should [connect this device or simulator to your computer using
adb](https://developer.android.com/tools/adb#Enabling)

## Build LibreOffice for Android

### Clone LibreOffice core

First, use git to clone the LibreOffice core repository from the LibreOffice
gerrit and switch to the Collabora Online branch

{{% common-build-commands section="clone-lo" lobranch="co-24.04" %}}

This is the same core repository as you may already have for building Collabora
Online. If you already have it cloned, you may [use git worktrees to speed up
this step](https://git-scm.com/docs/git-worktree).

### Configure LibreOffice core

Decide what architecture you are going to build for. This will depend on your
android device's ABI. We support building for armeabi-v7a, arm64-v8a, x86 and
x86_64.

If you're not sure what your phone's architecture is, you can either research
online or use adb to get a list of valid architectures

    $ adb shell getprop ro.product.cpu.abilist
    arm64-v8a,armeabi-v7a,armeabi

Create a file called `autogen.input` in your LibreOffice clone with the
following content:

    --build=x86_64-unknown-linux-gnu
    --with-android-ndk=/home/$USER/Android/Sdk/ndk/23.0.7599858
    --with-android-sdk=/home/$USER/Android/Sdk
    --enable-sal-log
    --enable-dbgutil

You also need to add a line specifying which architecture you're building for

#### For arm64-v8a

    --with-distro=CPAndroidAarch64

#### For armeabi-v7a

    --with-distro=CPAndroid

#### For x86_64

    --with-distro=CPAndroidX86_64

#### For x86

    --with-distro=CPAndroidX86

---

For example, if you have a device that supports `arm64-v8a` your autogen.input
should contain this content

    --build=x86_64-unknown-linux-gnu
    --with-android-ndk=/home/$USER/Android/Sdk/ndk-bundle
    --with-android-sdk=/home/$USER/Android/Sdk
    --enable-sal-log
    --with-distro=CPAndroidAarch64
    --enable-dbgutil

Finally, run

    ./autogen.sh

### Build LibreOffice core

Run `make` and wait a while for the build to finish...

    make

## Build Collabora Online

You need a copy of `POCO` and `libzstd` built for Android in order to build the Android app. You can use these scripts to build those

* POCO - use [build-poco-android.sh](https://github.com/CollaboraOnline/online/blob/master/scripts/build-poco-android.sh)
* libzstd - use [build-zstd-android.sh](https://github.com/CollaboraOnline/online/blob/master/scripts/build-zstd-android.sh)

### Configuring the build

Let's set some variables based on what we just built...

    export ABI=arm64-v8a
    export POCO_DIR=/opt/android-poco
    export ZSTD_DIR=/opt/android-zstd
    export LO_BUILDDIR=/opt/libreoffice

...remember to change your ABI to the ABI you're building the app for, POCO\_DIR and ZSTD\_DIR to the output directories of the build scripts, and LO_BUILDDIR to the directory you cloned and built LibreOffice core in.

Now we can use that to configure our Collabora Online build

    ./autogen.sh
    ./configure --enable-androidapp \
                --with-lo-builddir=${LO_BUILDDIR} \
                --with-poco-includes=${POCO_DIR}/install/include \
                --with-poco-libs=${POCO_DIR}/install/${ABI}/lib \
                --with-zstd-includes=${ZSTD_DIR}/lib \
                --with-zstd-libs=${ZSTD_DIR}/install/${ABI}/lib \
                --enable-silent-rules \
                --enable-debug \
                --with-android-abi=${ABI}

### Build Collabora Online

Once again, after configuring the build you can run it with `make`

    make

## Build the android app

### Option 1: Using Android studio

This is the recommended way to build the Android app

- Open Android studio
- Open the `android` subdirectory as a project
- Use `build -> make project` to run the build

### Option 2: Using gradle from the command line

It may be harder to debug the app without using Android Studio. Unless you have
prior experience with debugging Android apps outside Android Studio (or
otherwise aren't able to use Android Studio) we recommend you follow Option 1

    cd android
    ./gradlew build

## Debugging

To debug the native LibreOffice code in Android Studio, you need the debugging
symbols and to setup Android Studio to actually read & use them.

### Add android/obj/local/armeabi-v7a from core.git as a Symbol Directory

In Android Studio, choose Run -> Debug... -> Edit Configurations...

There go to the Android App -> app, choose the Debugger tab, and:

    Debug type: Auto (or Dual)

Symbol Directories: here add the full path, like...

    /local/libreoffice/master-android/android/obj/local/${ABI}

...making sure to substitute `${ABI}` for the ABI you builts for

This path contains the non-stripped version of the liblo-native-code.so, and
the debugger will read the symbols from that one (even if the APK contains
the stripped version). *NB* ensure that this is before any internal source
directories - since the internal source contains stripped native code.

Alternatively you can add the following to your ~/.lldbinit instead:

    settings set target.inline-breakpoint-strategy always
    settings append target.exec-search-paths /local/libreoffice/master-android/android/obj/local/${ABI}

To use pretty printers for types like OUString, add the following to your
~/.lldbinit:

    command script import '/local/libreoffice/master-android/solenv/lldb/libreoffice/LO.py'

From now on, you will be able to debug directly in the Android Studio
debugger.  Happy debugging!

## Cross-compiling with icecream to speed up your build

If you use icecream for parallel building, you can use it for
cross-compilation too.

    # first generate a tarball with the toolchain (once)
    icecc-create-env ~/Android/Sdk/ndk-bundle/toolchains/llvm/prebuilt/linux-x86_64/bin/armv7a-linux-androideabi21-clang ~/Android/Sdk/ndk-bundle/toolchains/llvm/prebuilt/linux-x86_64/bin/armv7a-linux-androideabi21-clang++

And add it and the paths to the compiler as the first things to the
autogen.input:

    CC=icecc [here copy what the output of ./autogen.sh without icecream said for C compiler]
    CXX=icecc [here copy what the output of ./autogen.sh without icecream said for C++ compiler]
    ICECC_VERSION=/path/to/the/tarball/generated/above/955ceb546ceb7a5715bf0223ddd788fe.tar.gz
    --with-parallelism=[amount of cpu threads in your icecream farm]
    --enable-icecream
    [...the original autogen.input...]

So the result will look something like this:

    CC=icecc /home/$USER/Android/Sdk/ndk-bundle/toolchains/llvm/prebuilt/linux-x86_64/bin/clang -mthumb -march=armv7-a -mfloat-abi=softfp -mfpu=neon -Wl,--fix-cortex-a8 -gcc-toolchain /home/$USER/Android/Sdk/ndk-bundle/to>
    CXX=icecc /home/$USER/Android/Sdk/ndk-bundle/toolchains/llvm/prebuilt/linux-x86_64/bin/clang++ -mthumb -march=armv7-a -mfloat-abi=softfp -mfpu=neon -Wl,--fix-cortex-a8 -gcc-toolchain /home/$USER/Android/Sdk/ndk-bundle>
    ICECC_VERSION=/local/libreoffice/android/955ceb546ceb7a5715bf0223ddd788fe.tar.gz
    --with-parallelism=25
    --enable-icecream
    --build=x86_64-unknown-linux-gnu
    --with-android-ndk=/home/$USER/Android/Sdk/ndk-bundle
    --with-android-sdk=/home/$USER/Android/Sdk
    --with-distro=CPAndroid
    --enable-sal-log

{{< edit-button to="/content/post/build-code-android.md" name="Edit page">}}
