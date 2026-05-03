{{$section := .Get "section"}}

{{ if eq $section "code-needs-lo-wget" }}
CODE needs the engine (formerly "Collabora Office core") to be built to run. Building the engine from source takes a considerable amount of time and brings in extra complexity, so we will instead download a daily-built archive containing the pieces that are absolutely necessary. If you are working only on the online side, without any engine-side changes, or you just want to quickly get going to do some small fixes, this will be enough for you. Otherwise, [refer to the general instructions](/post/build-code/#build-code-n-lo).

The archive ships only the engine's `instdir`; the LOKit headers no longer need to be bundled because they are already in the monorepo at `engine/include`. Run the following from the top of the cloned `online` monorepo so the asset is extracted into the existing `engine/` directory:

```bash
wget https://github.com/CollaboraOnline/online/releases/download/for-code-assets/{{.Get "lotar"}}
tar xvf {{.Get "lotar"}} -C engine
```

Export the location of the engine tree as a variable for the configure step:
```bash
export COCOREPATH=$(pwd)/engine

# Or make it persistent as part of your .bashrc with
echo "export COCOREPATH=$(pwd)/engine" >> ~/.bashrc && source ~/.bashrc
```
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

{{ if eq $section "clone-lo" }}
Collabora Office core lives inside the `online` monorepo under `engine/`, so a separate `core` clone is no longer needed. If you have not cloned the monorepo yet, run the `clone-online` step above first. Then move into the core tree:

```bash
cd engine
git checkout {{.Get "lobranch"}}
```
{{ end }}

{{ if eq $section "clone-online" }}
Collabora Online is hosted on Gerrit as a single monorepo. The LibreOffice core sits under `engine/` inside the same repo, so there is no separate `core` clone any more.

For an anonymous read-only clone (no account needed):
```bash
git clone https://gerrit.collaboraoffice.com/online collabora-online
```

If you have a Gerrit account and plan to push changes for review, clone over SSH instead:
```bash
git clone ssh://YOUR_USERNAME@gerrit.collaboraoffice.com:29418/online collabora-online
```

See the [first contribution guide](https://forum.collaboraonline.com/t/your-first-pull-request/41) for the full Gerrit workflow (SSH key, `commit-msg` hook, pushing to `refs/for/main`).

Switch to the local clone's directory:
```bash
cd collabora-online
```
{{ end }}

{{ if eq $section "build-online" }}
Run autogen to generate the configure file:
```bash
./autogen.sh
```

Run the generated configure script with proper parameters:
```bash
./configure --enable-silent-rules --with-lokit-path=${COCOREPATH}/include \
            --with-lo-path=${COCOREPATH}/instdir \
            --enable-debug --enable-cypress
```
Note: when building from the monorepo with core built in `engine/`, set `COCOREPATH=$(pwd)/engine` from the top of the clone before running configure. You can also add `--disable-ssl` instead of changing coolwsd.xml every time you want to disable ssl.

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
