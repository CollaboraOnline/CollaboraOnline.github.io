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

#### Consistent function declaration

Some of the functions use declaration like:

    blah: function blah(huh) {
        ...
    }

Instead, we want it to be:

    blah: function(huh) {
        ...
    }

without the repeated function name.

#### More dynamic Style panel in the Notebookbar

Switch the UI to using Notebookbar (in loolwsd.xml).

The style panel in notebookbar can de bone more more dynamic if we apply style
(show selected) with JS/CSS (of cousrse the remaining things can be kept
untouched just overlap it with CSS). Style is applied to text almost instantly
but in notebookbar it takes a few seconds to appear.

#### Debugging of postMessage

In debug mode, it would be nice to have incoming and outgoing `postMessage`
contents written into browser console.

Interested one can grep for "`console.log2`" in the loleaflet/ code to find out
how it's done for messages in existing debug mode.

Debug mode is accessible with: Ctrl + Alt + Shift + d

#### Indication in the Admin console when the daemon shuts down

While wsd is running, open the Admin console. Now Ctrl + C to stop the wsd
process. The Admin console should show the user that Online was shut down.
Worse, when the wsd is restarted, the Admin console screen is not updated
accordingly; it keeps showing the stale view from the previous launch.

An error box or the overlay saying that wsd has been shut down should be done
and refresh the page with the new WS connection whenever user clicks on
the overlay. This is similar to when the document becomes inactive.

How to hack:

Check what web socket messages we receive when wsd shuts down in the backend
and handle it appropriately in the admin websocket. One can check the
websocket handling for the documents in src/core/Socket.js and do something
similar with the admin websocket. Code for admin websocket is in
loleaflet/src/admin/

In debug mode, it would be nice to have incoming and outgoing postMessage contents written into browser console.
