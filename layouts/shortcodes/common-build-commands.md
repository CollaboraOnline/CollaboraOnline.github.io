{{$section := .Get "section"}}
{{$clonedir := .Get "clonedir" | default "collabora-online"}}

{{ if eq $section "build-engine" }}
CODE needs the engine (formerly "Collabora Office core") to be built before online can be configured and built. The online build compiles its C++ parts with the engine's build system and links against libraries built in the engine tree, so it needs a complete engine build under `engine/`, not just a set of installed binaries.

The engine has many more build dependencies than online. Install the packages your distribution needs to build LibreOffice; the engine's `README.md` and https://wiki.documentfoundation.org/Development/BuildingOnLinux list them.

From the top of the cloned `online` monorepo, configure and build the engine with the developer variant of the LOKit distro configuration:

```bash
cd engine
./autogen.sh --with-distro=CPLinux-LOKit-Dev
make -j $(nproc)
cd ..
```

The first build takes at least an hour or two, possibly more depending on your machine and your internet connection. Later builds only rebuild what changed. The `CPLinux-LOKit-Dev` configuration turns off packaging, translations and merged libraries and turns on debugging utilities. For an optimized engine without the debug checks, use `--with-distro=CPLinux-LOKit --without-package-format` instead.

{{ end }}

{{ if eq $section "running" }}
### Running & Hacking
Now do:
```bash
make run
```
The output will contain the links that you can directly follow to
see Writer, Calc, and Impress test documents in your browser.

#### Hacking it
When you change a JavaScript file (they are located under the browser/
subdirectory), you need to stop the existing CODE instance and issue ```make run``` again, because the files are cached.
Alternatively you can export a variable like:
```bash
export COOL_SERVE_FROM_FS=1
```
to avoid the caching, so that you can just Shift+Reload the pages to see the
new content.
{{ end }}

{{ if eq $section "clone-online" }}
Collabora Online is hosted on Gerrit as a single monorepo: all the source code lives in one repository, with the former Collabora Office core under `engine/`.

For an anonymous read-only clone (no account needed):
```bash
git clone https://gerrit.collaboraoffice.com/online {{$clonedir}}
```

If you have a Gerrit account and plan to push changes for review, clone over SSH instead:
```bash
git clone ssh://YOUR_USERNAME@gerrit.collaboraoffice.com:29418/online {{$clonedir}}
```

See the [first contribution guide](https://forum.collaboraonline.com/t/your-first-pull-request/41) for the full Gerrit workflow (SSH key, `commit-msg` hook, pushing to `refs/for/main`).

Switch to the local clone's directory:
```bash
cd {{$clonedir}}
```
{{ end }}

{{ if eq $section "build-online" }}
Run autogen to generate the configure file:
```bash
./autogen.sh
```

Run the generated configure script. The engine is in `engine/`, where configure looks by default, so no paths need to be passed:
```bash
./configure --enable-debug --enable-cypress
```
You can add `--disable-ssl` instead of changing coolwsd.xml every time you want to disable ssl.

Start the actual build, which might take from a few minutes to half an hour (or more) depending on how powerful your machine is:
```bash
make -j $(nproc)
```
{{ end }}

{{ if eq $section "run-unit-test" }}
If you want to run the unit tests, use `make check` instead of `make`.

Note that the coolforkit program needs the `CAP_SYS_CHROOT` capability,
thus **you will be asked the root password** when running make as it
invokes `sudo` to run `/sbin/setcap`.
{{ end }}
