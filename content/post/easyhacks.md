+++
authors = [
    "Kendy",
]
title = "Easy Hacks"
date = "2020-09-30"
description = "Easy Hacks"
tags = [
    "contribute",
    "development",
    "code",
    "Leaflet",
    "JS",
    "CSS",

]
categories = [
    "themes",
    "syntax",
]
series = ["Themes Guide"]
aliases = ["migrate-from-jekyl"]
images = [
    "easyhacks.jpg",
]
+++

Check out the starting points for new developers on the project — usually with
code pointers helping you to locate the area to hack on easily.
<!--more-->

First, you need to do a build of Collabora Online though, visit
the [How to build CODE]({{< relref "build-code" >}} "How to build CODE") page.

### List of Easy Hacks

Below is a non-exhaustive list of the Easy Hacks. To view the complete list of the current Easy Hacks, you may check [the corresponding issues on GitHub.](https://github.com/CollaboraOnline/online/issues?q=is%3Aissue+is%3Aopen+label%3A%22Easy+Hack%22)

{{< get-easy-hacks >}}

{{< link-button to="https://github.com/CollaboraOnline/online/issues?q=is%3Aissue+is%3Aopen+label%3A%22Easy+Hack%22" name="View all">}}

__How to hack:__

Check what web socket messages we receive when _wsd_ shuts down in the backend
and handle it appropriately in the admin websocket. One can check the
websocket handling for the documents in _src/core/Socket.js_ and do something
similar with the admin websocket. Code for admin websocket is in
_loleaflet/src/admin/_

In debug mode, it would be nice to have incoming and outgoing `postMessage` contents written into browser console.
