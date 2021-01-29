+++
authors = [
    "Collabora",
]
title = "Build for Android"
date = "2020-09-30"
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
build the native parts on Windows. Similarly to the normal CODE, you will need
the following projects, cross-compiled to your target platform:

* LibreOffice
* POCO

If you want to build the full app, you need to build for 4 platforms: ARM,
ARM64, x86 and x86-64. For development, just one of them is enough, the build
currently defaults to ARM.

### Build LibreOffice master for Android

Create a file called `autogen.input` in your LibreOffice clone with the
following content:

    --build=x86_64-unknown-linux-gnu
    --with-android-ndk=/home/$USER/Android/Sdk/ndk-bundle
    --with-android-sdk=/home/$USER/Android/Sdk
    --with-distro=LibreOfficeAndroid
    --enable-sal-log

Then run `./autogen.sh && make`

### Build the POCO for Android

    # clone the poco repository in the same folder where LibreOffice core and online folders are placed.
    git clone https://github.com/pocoproject/poco poco-android
    cd poco-android

    # use the 1.10.1 branch
    git checkout -b poco-1.10.1 origin/poco-1.10.1

    # configure
    ./configure --config=Android --no-samples --no-tests --omit=Crypto,NetSSL_OpenSSL,Zip,Data,Data/SQLite,Data/ODBC,Data/MySQL,MongoDB,PDF,CppParser,PageCompiler,JWT

    # make it
    PATH="$PATH":~/Android/Sdk/ndk-bundle/toolchains/llvm/prebuilt/linux-x86_64/bin make -j8 ANDROID_ABI=armeabi-v7a CC=armv7a-linux-androideabi21-clang CXX=armv7a-linux-androideabi21-clang++ SYSLIBS=-static-libstdc++

    # install it to /opt/poco-android
    PATH="$PATH":~/Android/Sdk/ndk-bundle/toolchains/llvm/prebuilt/linux-x86_64/bin make -j8 ANDROID_ABI=armeabi-v7a CC=armv7a-linux-androideabi21-clang CXX=armv7a-linux-androideabi21-clang++ SYSLIBS=-static-libstdc++ install INSTALLDIR=/opt/poco-android

#### (Optional) ARM64 POCO for Android

Build the ARM64 version of POCO if you want to include ARM64 in the APK too:

    # checkout the 1.10.1 in a different location and apply the following patch:
    --- a/build/config/Android
    +++ b/build/config/Android
    @@ -21,6 +21,9 @@ TOOL      = arm-linux-androideabi
     ARCHFLAGS = -march=armv7-a -mfloat-abi=softfp
     LINKFLAGS = -Wl,--fix-cortex-a8
     else
    +ifeq ($(ANDROID_ABI),arm64-v8a)
    +TOOL      = aarch64-linux-android
    +else
     ifeq ($(ANDROID_ABI),x86)
     TOOL      = i686-linux-android
     ARCHFLAGS = -march=i686 -msse3 -mstackrealign -mfpmath=sse
    @@ -29,6 +32,7 @@ $(error Invalid ABI specified in ANDROID_ABI)
     endif
     endif
     endif
    +endif

     #
     # Define Tools

    # configure as above:
    ./configure --config=Android --no-samples --no-tests --omit=Crypto,NetSSL_OpenSSL,Zip,Data,Data/SQLite,Data/ODBC,Data/MySQL,MongoDB,PDF,CppParser,PageCompiler,JWT

    # and make it:
    PATH="$PATH":~/Android/Sdk/ndk-bundle/toolchains/llvm/prebuilt/linux-x86_64/bin make -j8 ANDROID_ABI=arm64-v8a CC=aarch64-linux-android21-clang CXX=aarch64-linux-android21-clang++ SYSLIBS=-static-libstdc++

    # install
    PATH="$PATH":~/Android/Sdk/ndk-bundle/toolchains/llvm/prebuilt/linux-x86_64/bin make -j8 ANDROID_ABI=arm64-v8a CC=aarch64-linux-android21-clang CXX=aarch64-linux-android21-clang++ SYSLIBS=-static-libstdc++ install INSTALLDIR=/opt/poco-android-64bit

#### (Optional) x86 POCO for Android

If you want to add the support for that into the APK too; eg. for Chromebooks:

    # checkout the 1.10.1 in yet another location
    git clone https://github.com/pocoproject/poco poco-android-x86
    cd poco-android-x86
    git checkout -b poco-1.10.1 origin/poco-1.10.1

    # configure
    ./configure --config=Android --no-samples --no-tests --omit=Crypto,NetSSL_OpenSSL,Zip,Data,Data/SQLite,Data/ODBC,Data/MySQL,MongoDB,PDF,CppParser,PageCompiler,JWT

    # build
    PATH="$PATH":~/Android/Sdk/ndk-bundle/toolchains/llvm/prebuilt/linux-x86_64/bin make -j8 ANDROID_ABI=x86 CC=i686-linux-android21-clang CXX=i686-linux-android21-clang++ SYSLIBS=-static-libstdc++

    # install
    PATH="$PATH":~/Android/Sdk/ndk-bundle/toolchains/llvm/prebuilt/linux-x86_64/bin make -j8 ANDROID_ABI=x86 CC=i686-linux-android21-clang CXX=i686-linux-android21-clang++ SYSLIBS=-static-libstdc++ install INSTALLDIR=/opt/poco-android-x86

#### (Optional) x86-64 POCO for Android

If you want to add the support for that into the APK too:

    # checkout the 1.10.1 in yet another location
    git clone https://github.com/pocoproject/poco poco-android-x86-64
    cd poco-android-x86-64
    git checkout -b poco-1.10.1 origin/poco-1.10.1

    # and apply the following patch:
    diff --git a/build/config/Android b/build/config/Android
    index 9227a3352..1abf6df7c 100644
    --- a/build/config/Android
    +++ b/build/config/Android
    @@ -25,10 +25,14 @@ ifeq ($(ANDROID_ABI),x86)
     TOOL      = i686-linux-android
     ARCHFLAGS = -march=i686 -msse3 -mstackrealign -mfpmath=sse
     else
    +ifeq ($(ANDROID_ABI),x86_64)
    +TOOL      = x86_64-linux-android
    +else
     $(error Invalid ABI specified in ANDROID_ABI)
     endif
     endif
     endif
    +endif

     #
     # Define Tools

    # configure
    ./configure --config=Android --no-samples --no-tests --omit=Crypto,NetSSL_OpenSSL,Zip,Data,Data/SQLite,Data/ODBC,Data/MySQL,MongoDB,PDF,CppParser,PageCompiler,JWT

    # build
    PATH="$PATH":~/Android/Sdk/ndk-bundle/toolchains/llvm/prebuilt/linux-x86_64/bin make -j8 ANDROID_ABI=x86_64 CC=x86_64-linux-android21-clang CXX=x86_64-linux-android21-clang++ SYSLIBS=-static-libstdc++

    # install
    PATH="$PATH":~/Android/Sdk/ndk-bundle/toolchains/llvm/prebuilt/linux-x86_64/bin make -j8 ANDROID_ABI=x86_64 CC=x86_64-linux-android21-clang CXX=x86_64-linux-android21-clang++ SYSLIBS=-static-libstdc++ install INSTALLDIR=/opt/poco-android-x86-64

### Configure the online.git

Don't forget to change `--with-lo-builddir` in the following:

    ./autogen.sh
    ./configure --enable-androidapp \
                --with-lo-builddir=/local/libreoffice/master-android \
                --with-poco-includes=/opt/poco-android/include --with-poco-libs=/opt/poco-android/lib \
                --disable-setcap \
                --enable-silent-rules --enable-debug
    make

If you build for more platforms (with the optional bits described above), just
add more values to --with-lo-builddir, --with-poco-includes and
--with-poco-libs, delimited with `:`. The order must be ARM, ARM64, x86,
x86-64.

For example:

    --with-lo-builddir=/local/libreoffice/master-android-release:/local/libreoffice/master-android-release-64bit \
    --with-poco-includes=/opt/poco-android/include:/opt/poco-android-64bit/include \
    --with-poco-libs=/opt/poco-android/lib:/opt/poco-android-64bit/lib \

### Build the actual app using Android Studio

Just open Android Studio, open the `android` subdirectory as a project and
start the build (Buiild -> Make Project).

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
    --with-distro=LibreOfficeAndroid
    --enable-sal-log
