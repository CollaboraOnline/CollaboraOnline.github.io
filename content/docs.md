+++
title = "Documentation"
description = "CODE Documentation"
date = "2019-02-28"
aliases = ["about-us","about-hugo","contact"]
author = "Hugo Authors"
+++

* [Grab the CODE]({{< relref "#grab-the-code" >}} "Explore and clone GitHub repository")
* [Getting set up]({{< relref "#getting-set-up" >}} "Step-by-step setup")
* [Get involved]({{< relref "#get-involved" >}} "How to contribute")
  * [Your fist commit]({{< relref "#get-involved" >}} "How to contribute")
* [Watch a talk & grab slides]({{< relref "#watch-a-talk--grab-slides" >}} "Step-by-step setup")

The Collabora Online Development Edition is aimed at home users and contains many of the latest and greatest developments. We want as many people as possible to try it out and get back control of their own online documents. We’d also love to get people involved in our efforts to make Online even better. So download Collabora Online Development Edition, enjoy using it at home.

## Grab the CODE
The easiest way to install CODE for a quick tryout is to download it as a virtual appliance from the [Univention App Center](https://www.univention.com/products/univention-app-center/app-catalog/collabora/).This appliance contains the Collabora Online Development Edition, and the additional software you need to get you up and running in minutes. You can choose between two types of integration, CODE + Nextcloud or CODE + ownCloud. Each appliance is available in four formats: KVM, VirtualBox, VMware Workstation and VMware ESXi.

{{< link-button to="https://www.univention.com/products/univention-app-center/app-catalog/collabora/" name="Download virtual appliance">}}

[See more options](https://www.collaboraoffice.com/code/)

## Getting set up
It is highly recommended to set up a reverse proxy in front of CODE, either you run CODE from Docker, or you use native packages. It is easy, and this way CODE can be reached on standard HTTP or HTTPS ports. We provide sample configuration files for Apache2 and Nginx. If you want SSL, we recommend certificates from Let’s Encrypt.

    Setting up Apache 2 reverse proxy
    Setting up Nginx reverse proxy

Now you can give https://collabora.example.com as the WOPI URL in your preferred File Sync and Share solution. See below for specific examples.
For more detailed and pretty instructions on integrating with various partner solutions please see (in alphabetical order):

    Nextcloud Setup Instructions (Apache & Nginx)
    ownCloud

## Get involved
* Checking out the source code to build it yourself is easy:
  + https://github.com/CollaboraOnline/online
* After [building Collabora Online]({{< relref "build-code" >}} "How to build CODE") just do a `make run` and follow the link to tweak things live.
* The API documentation is available here:
  + https://www.collaboraoffice.com/collabora-online-editor-api-reference/
* Send patches via the [GitHub pull requests](https://docs.github.com/en/free-pro-team@latest/github/collaborating-with-issues-and-pull-requests/about-pull-requests)
* To ask questions, use the [Collabora Online forum](https://forum.collaboraonline.com)
* To talk to other developers, please join the IRC [Libera.​Chat/#cool-dev channel](irc://irc.libera.chat/#cool-dev)
  + you can get there directly via a [Webchat](https://web.libera.chat/#cool-dev)
  + you can also join via [Matrix](https://matrix.to/#/#collabora-online:matrix.org)
* And feel free to share your contributions and iterations on twitter by tagging [@CollaboraOffice](https://twitter.com/CollaboraOffice) or [@CollaboraOffice@mastodon.social](https://mastodon.social/@CollaboraOffice) and using the `#cool_dev`

### Your first commit
* First check [How to build CODE]({{< relref "build-code" >}} "How to build CODE")
* Do your modifications and check them
* `git commit` # to commit the stuff
* `git log -p -1` # to check your work
* `git push origin HEAD:feature/name`
* Create a Pull Request via the URL that you are told

## Watch a talk & grab slides

{{< youtube H7HfbZBycRU >}}

| | | |
|-|-|-|
| LibreOffice Conference 2020| [Integrating-OnLine-via-WOPI.pdf](https://speakerdeck.com/kendy/integrating-libreoffice-online-via-wopi) |
| FOSDEM 2020 | [dialog-tunneling.pdf](https://speakerdeck.com/kendy/dialog-tunneling-in-libreoffie-online) |
