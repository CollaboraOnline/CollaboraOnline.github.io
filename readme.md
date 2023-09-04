**Table of Contents**

- [Work and push to the master branch](#work-and-push-to-the-master-branch)
  - [Directory](#directory)
  - [See how it looks without server](#see-how-it-looks-without-server)
  - [Generate and Run local a server](#generate-and-Run-local-a-server)
- [Deploy to master](#deploy-to-master)

# Work and push to the master branch

The branch with the name `master` hosts all source files used in the creation of the website via hugo. In turn, `gh-pages` branch is then only used to host the generated result (`public` folder)

## Directory
* Posts (buildit, easyhacks, translate, filebugs) are written in markdown and are located in `content/post/*.md`
* Images `content/images/`
* We can also have different authors, and since then everything will be public we can maybe use different authors according to the person who wrote them. `content/authors/` then each post and page has an attribute name `authors` (we can have multiple per content)
* Docs page (Documentation): `content/docs.md`
## See how it looks without server

If you just want to check how the website looks and do not want to run local server
* You can, after all it's a static website
* just download master branch as a .zip
* Unzip it and open it
* There is an `index.html`, you can open with your web browser, it will work
Caveats: since you are not runing a local server when you click a link it will not find dinamycally the `.html` of that directoy. Thus it will show you a non found page. Example:
* You clicked `Build instructions`
* It showed something like:

```
index of file:///home/pedrosilva/collaboraonline-page/public/post/buildit/

Name
index.html
```

To circunvent this you can either click that index.html under `Name` or you can simply type it at the end of that page address like so:
`file:///home/pedrosilva/collaboraonline-page/public/post/buildit/index.html`

Note: ideally we would have this in one folder inside of CollaboraOffice.com so everyone with Basic Auth could check it

## Generate and Run local a server
1. Install Hugo: https://gohugo.io/getting-started/installing/
* Official packages for Debian and Ubuntu: `sudo apt-get install hugo`
* Official packages for Fedora, Red Hat and CentOS `sudo dnf install hugo`
* Community packages for Arch Linux and its derivatives (such as Manjaro): `sudo pacman -Syu hugo`
* For openSUSE
	* Official for Tumbleweed: `sudo zypper install hugo` [view in store](https://software.opensuse.org/download/package?package=hugo&project=openSUSE%3AFactory)
	* Experimental for Leap 15.4/15.5 packages [view in store](https://software.opensuse.org/download/package?package=hugo&project=devel%3Alanguages%3Ago)
		* `# For 15.4`
		* `sudo zypper addrepo https://download.opensuse.org/repositories/devel:languages:go/15.4/devel:languages:go.repo`
		* `# For 15.5:`
		* `sudo zypper addrepo https://download.opensuse.org/repositories/devel:languages:go/15.4/devel:languages:go.repo`
		* `sudo zypper refresh`
		* `zypper install hugo`
* with homebrew for [linux](https://docs.brew.sh/Homebrew-on-Linux); [macOS](https://brew.sh/): `brew install hugo`
note: https://github.com/gohugoio/hugo/releases
2. Repository and branches
* Choose a local folder
* Clone it `git clone https://github.com/CollaboraOnline/CollaboraOnline.github.io.git .`
* `git worktree add -B gh-pages public origin/gh-pages` : Creates a local public folder and be able to manage both branches within the same working tree, allowing to have a mixed of branches checked out at the same time. With this we can generate the site into that public folder.
3. Generate live static website and run server (while watching files etc so it does not need to refresh it will do it automatically)

run `hugo server` in the root of your master branch local copy (you can also disable cash by enabling full re-renders on changes with `hugo server --disableFastRender`).

# Deploy to master:
* There is already a GH action for that (it generates automatically)
when we want to manually publish the generated static website with URL https://collaboraonline.github.io/ (resulting from the changes in `master` branch) we can run `./deploy.sh`
* the script checks for git status and will not proceed if the dir is not clean
* removed any old generated version you might have locally (so anything inside of `public`)
* runs `hugo` to generate the website into the `public` folder
* pushes the contents of `public` folder to gh-pages branch

* gh-pages: The master branch will store the public website files once they are all built.
* master: main branch to store all of the source files and contribute to.
