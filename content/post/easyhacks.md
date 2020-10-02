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

#### Consistent function declaration

Some of the functions use declaration like:

```
blah: function blah(huh) {
    ...
}
```

Instead, we want it to be:

```
blah: function(huh) {
    ...
}
```

without the repeated function name.

[Continue on GitHub](https://github.com/CollaboraOnline/online/issues/68)

#### More dynamic Style panel in the Notebookbar

Switch the UI to using Notebookbar (in _loolwsd.xml_).

The style panel in notebookbar can be made more dynamic if we apply a style
(show selected) with JS/CSS (of course the remaining things can be kept
untouched, just overlap it with CSS). Style is applied to text almost instantly
but in notebookbar it takes a few seconds to appear.

[Continue on GitHub](https://github.com/CollaboraOnline/online/issues/69)

#### Debugging of postMessage

In debug mode, it would be nice to have incoming and outgoing `postMessage`
contents written into browser console.

Interested one can grep for `console.log2` in the _loleaflet/_ code to find out
how it's done for messages in existing debug mode.

Debug mode is accessible with: `Ctrl + Alt + Shift + d`

[Continue on GitHub](https://github.com/CollaboraOnline/online/issues/70)

#### Indication in the Admin console when the daemon shuts down

While _wsd_ is running, open the Admin console. Now `Ctrl + C` to stop the _wsd_
process. The Admin console should show the user that Online was shut down.
Worse, when the _wsd_ is restarted, the Admin console screen is not updated
accordingly; it keeps showing the stale view from the previous launch.

An error box or the overlay saying that _wsd_ has been shut down should be done
and refresh the page with the new WS connection whenever user clicks on
the overlay. This is similar to when the document becomes inactive.

__How to hack:__

Check what web socket messages we receive when _wsd_ shuts down in the backend
and handle it appropriately in the admin websocket. One can check the
websocket handling for the documents in _src/core/Socket.js_ and do something
similar with the admin websocket. Code for admin websocket is in
_loleaflet/src/admin/_

In debug mode, it would be nice to have incoming and outgoing `postMessage` contents written into browser console.

[Continue on GitHub](https://github.com/CollaboraOnline/online/issues/71)
