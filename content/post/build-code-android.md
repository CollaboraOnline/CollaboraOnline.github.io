+++
authors = [
    "Collabora",
]
title = "Build for Android"
date = "2022-07-02"
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
+++

Are you familiar with Android development environment and interested to learn more while helping the project?
<!--more-->

Head over documentation or start of by following these step-by-step instructions and build `CODE` from scratch:

* [Build CODE]({{< relref "build-code.md" >}} "Explore and clone GitHub repository")
* [Build CODE for Android]({{< relref "build-code-android.md" >}} "Step-by-step setup")

## Build CODE for Android
The development of the Android app has to be done on Linux, it's currently not possible to
build the native parts on Windows. Builds have been tested with Android NDK r20b, newer NDKs may or may not work.
Similarly to the normal CODE, you will need the following projects, cross-compiled to your target platform:

* LibreOffice (LOKit)
* POCO - use [build-poco-android.sh](https://github.com/CollaboraOnline/online/blob/master/scripts/build-poco-android.sh)
* libzstd - use [build-zstd-android.sh](https://github.com/CollaboraOnline/online/blob/master/scripts/build-zstd-android.sh)

If you want to build the full app, you need to build for 4 platforms: ARM,
ARM64, x86 and x86-64. For development, just one of them is enough, the build
currently defaults to ARM.

### Build LibreOffice master for Android

Create a file called `autogen.input` in your LibreOffice clone with the
following content:

    --build=x86_64-unknown-linux-gnu
    --with-android-ndk=/home/$USER/Android/Sdk/ndk-bundle
    --with-android-sdk=/home/$USER/Android/Sdk
    --with-distro=CPAndroid
    --enable-sal-log

Then run `./autogen.sh && make`

### Configure the online.git

Don't forget to change `--with-lo-builddir` and/or path for POCO and libzstd in the following:

    ./autogen.sh
    ./configure --enable-androidapp \
                --with-lo-builddir=/opt/libreoffice/master-android \
                --with-poco-includes=/opt/android-poco/install/include \
                --with-poco-libs=/opt/android-poco/install/armeabi-v7a/lib \
                --with-zstd-includes=/opt/android-zstd/lib \
                --with-zstd-libs=/opt/android-zstd/install/armeabi-v7a/lib \
                --disable-setcap \
                --enable-silent-rules \
                --enable-debug
    make
If you build for more platforms, just add more values to
--with-lo-builddir, --with-poco-includes, --with-poco-libs,
--with-zstd-includes and --with-zstd-libs delimited with `:`.
The order must be ARM, ARM64, x86, x86-64.

For example:

                --with-lo-builddir=/opt/libreoffice/core_android_armeabi-v7a:/opt/libreoffice/core_android_arm64-v8a:/opt/libreoffice/core_android_x86:/opt/libreoffice/core_android_x86-64 \
                --with-poco-includes=/opt/android-poco/install/include:/opt/android-poco/install/include:/opt/android-poco/install/include:/opt/android-poco/install/include \
                --with-poco-libs=/opt/android-poco/install/armeabi-v7a/lib:/opt/android-poco/install/arm64-v8a/lib:/opt/android-poco/install/x86/lib:/opt/android-poco/install/x86_64/lib \
                --with-zstd-includes=/opt/android-zstd/lib:/opt/android-zstd/lib:/opt/android-zstd/lib:/opt/android-zstd/lib \
                --with-zstd-libs=/opt/android-zstd/install/armeabi-v7a/lib:/opt/android-zstd/install/arm64-v8a/lib:/opt/android-zstd/install/x86/lib:/opt/android-zstd/install/x86_64/lib \


### Build the actual app using Android Studio

Just open Android Studio, open the `android` subdirectory as a project and
start the build (Build -> Make Project).

Alternatively you can build from the command line:

    cd android
    ./gradlew build

### Debugging

To debug the native LibreOffice code in Android Studio, you need the debugging
symbols and to setup Android Studio to actually read & use them.

#### Build debugging symbols for the modules you are interested in

Add something like the following to autogen.input:

    --enable-symbols="vcl/ desktop/ sal/ svx/ framework/ sfx2/ tools/ cppu/ cppuhelper/ filter/ comphelper/ Library_sw Library_swd Library_swui"

clean the appropriate modules, like

    make vcl.clean desktop.clean sal.clean svx.clean framework.clean sfx2.clean tools.clean cppu.clean cppuhelper.clean filter.clean comphelper.clean sw.clean

and rebuild using 'make'.

#### Add android/obj/local/armeabi-v7a from core.git as a Symbol Directory

In Android Studio, choose Run -> Debug... -> Edit Configurations...

There go to the Android App -> app, choose the Debugger tab, and:

    Debug type: Auto (or Dual)

Symbol Directories: here add the full path, like

    /local/libreoffice/master-android/android/obj/local/armeabi-v7a

This path contains the non-stripped version of the liblo-native-code.so, and
the debugger will read the symbols from that one (even if the APK contains
the stripped version). *NB* ensure that this is before any internal source
directories - since the internal source contains stripped native code.

Alternatively you can add the following to your ~/.lldbinit instead:

    settings set target.inline-breakpoint-strategy always
    settings append target.exec-search-paths /local/libreoffice/master-android/android/obj/local/armeabi-v7a

To use pretty printers for types like OUString, add the following to your
~/.lldbinit:

    command script import '/local/libreoffice/master-android/solenv/lldb/libreoffice/LO.py'

From now on, you will be able to debug directly in the Android Studio
debugger.  Happy debugging!

### Tip: How to speed up your core.git build

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
