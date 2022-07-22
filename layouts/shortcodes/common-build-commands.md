{{$section := .Get "section"}}

{{ if eq $section "code-needs-lo-wget" }}
CODE needs LibreOffice to be built to run. However, it takes a considerable amount of time and brings in
extra complexity. So, we will instead download a daily built archive which contains only the pieces that are absolutely necessary. If you are working only on the online side, without doing any code-level changes on the LibreOffice core, or you just want to quickly get going to do some small fixes, then this will be enough for you. Otherwise, refer to the general instructions.

Now download a daily-built archive of LibreOffice core:
```bash
wget https://github.com/CollaboraOnline/online/releases/download/for-code-assets/core-co-22.05-assets.tar.gz
```

Extract the contents of the archive:
```bash
tar xvf core-co-22.05-assets.tar.gz
```

Export the location of the extracted contents as a variable before changing directory:
```bash
export LOCOREPATH=$(pwd)

# Or make it persistent as part of your .bashrc with
echo "export LOCOREPATH=$(pwd)" >> .bashrc && source .bashrc 
```
{{ end }}

{{ if eq $section "running" }}
### Running & Hacking
Now do:
```bash
make run
```
Among other, the output will contain the links that you can directly follow to
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
```bash
git clone https://github.com/YOURUSERNAME/online.git collabora-online
```

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
./configure --enable-silent-rules --with-lokit-path=${LOCOREPATH}/include \
            --with-lo-path=${LOCOREPATH}/instdir \
            --enable-debug --enable-cypress
```
Note: you can also add `--disable-ssl` instead of changing coolwsd.xml everytime you want to disable ssl.

Start the actual build, which might take from a few minutes to half an hour (or more) depending on how powerful your machine is:
```bash
make -j $(nproc)
```
{{ end }}

{{ if eq $section "run-unit-test" }}
If you want to run the unit tests, use `make check` instead of the `make`.

Note that the coolforkit program needs the `CAP_SYS_CHROOT` capability,
thus **you will be asked the root password** when running make as it
invokes `sudo` to run `/sbin/setcap`.
{{ end }}
