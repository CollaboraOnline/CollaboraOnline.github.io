+++
authors = [
    "Collabora",
]
title = "FAQ"
date = "2020-09-30"
description = "Frequently Asked Questions"
tags = [
    "contribute",
    "report",
		"test",
]
images = [
    "faq.jpg",
]
+++

Perhaps your question is one that we have been asked before; have a read, and let us know if not.

<!--more-->

## What is Collabora Online anyway? {#whatisit}

Collabora Online is a feature rich online collaboration office suite
with great support for all major document, spreadsheet and
presentation file formats. It is based on LibreOffice and used in
combination with software for managing, sharing, files.

It can be installed on a server that you host yourself, or by a
company of your choice. It is excellent for users and organizations
looking for an office solution in the cloud that protects their
privacy and allows them to keep full control of their sensitive data.

### Who created Collabora Online? {#creators}

Collabora Online is mainly written by Collabora. Collabora's 20+
committers provided 95%+ of the commits in the last year. Checkout
our [2020 infographic](https://www.collaboraoffice.com/community-news/updated-libreoffice-growth-infographic-2020/)
or the [git repository](https://github.com/CollaboraOnline/online)

We built on top of a huge volume of work from both LibreOffice [credits](https://www.libreoffice.org/about-us/credits/),
however the Online functionality was created primarily by Collabora (as [announced in 2015](https://people.gnome.org/~michael/blog/2015-03-25-libreoffice-icewarp.html)) – or for a [detailed story](https://people.gnome.org/~michael/blog/2015-12-15-code.html).

The first integration for ownCloud (and later for Nextcloud) was built
on top of Documents plugin (based on work of Frank Karlitschek and
Victor Dubiniuk) that was renamed to RichDocuments, with a docker
image from Lukas Reschke. Currently we have many more integrations
written by either Collabora or by Collabora Partners.

### Who contributed to the Mobile work? {#mobile-story}

Our mobile app is built on top of our Online / web work. For the story
of those behind that [see here](https://www.collaboraoffice.com/collabora-office-for-android-ios-credits/)
in particular thanks to Adfinis for their investment!

Of note, was the [TDF tender](https://blog.documentfoundation.org/blog/2014/09/04/tender-for-base-framework-for-an-android-version-of-libreoffice-with-basic-editing-capabilities-201409-01/) to build a base framework for editing. This built
on the work Smoose/SUSE/Collabora re-using the Mozilla Java/Fennec renderer for an
Android viewer. You can read the reports
[1](https://www.collaboraoffice.com/wp-content/uploads/2020/09/TDF0002-report-M1.pdf),
[2](https://www.collaboraoffice.com/wp-content/uploads/2020/09/TDF0002-report-M2.pdf)
that list the commits, all of which were to the LibreOffice core; at that time
Online barely existed. It is safe to say that a negligable amount of TDF
donor funded code is present in Online.

### What about translators work? {#translators}

Great point! Many translators have made important contributions. While Online
represents only one hundredth of the strings that LibreOffice has, it re-uses
many translations from the core too. We try to extract translators names to
[credit their hard work]({{< relref "translate.md#Credits" >}}), which is much
appreciated.
Of course we prepared the vital [translation environment](https://collaboraonline.github.io/post/translate/)
and are already merging changes.

## Why is Collabora Online its own project? {#own-project}

Back in 2015 Collabora started the online development on TDF's
infrastructure as a source-only project: a place to collaborate around
development, with own-branded products versions derived from that.

Gradually pressure built to change this, and there were very long discussions
around some [serious problems](https://lwn.net/Articles/825602/) with the
new board, staff, wider community in 2020. During these discussions it became
clear that we could provide the stability and confidence
[needed to invest](#investment) longer term in improving the software most
simply by moving Collabora Online to its own project.

We believe that doing this also removes the need for a number of
unpleasant compromises and inter-company conflicts that put strain
on TDF. It also follows the well known pattern of many other successful
FOSS companies: RedHat/Fedora, openSUSE, Samba+, ownCloud, Nextcloud,
RocketChat, Mattermost, BigBlueButton, and others beyond number.

More details are in the
[announcement E-mail](https://www.mail-archive.com/board-discuss@documentfoundation.org/msg04727.html).

### Is this the first separate project based on this code?

It seems not; this turns out to be reasonably common. Checkout
[OSSIIs](https://github.com/OSSII/oxool-community) [version](https://www.ossii.com.tw/product/online).
Or [Zimbra Docs](https://www.zimbra.com/email-server-software/zimbra-docs/)
(with no contributions back), and there are other examples.
Clearly having a team of engineers with wide experience, who contribute
to the code behind the version you choose is important.

### Will you still contribute to the LibreOffice core? {#libo-contrib}

Emphatically yes. We expect that as our business grows over time there
will continue to be a net increase in the amount of work: fixes, rendering
improvements, performance wins, features etc. that we can contribute back
to the LibreOffice core vs. the status quo. We continue to have significant
numbers of Collabora Office customers who want bug fixes and improvements
which we contribute back. We try to merge all of our work into core's master
branch for the next LibreOffice version, and we use daily comparison
tooling to check this delta stays small.

Against that — LibreOffice is its own project, with its own processes
and gets to choose what it includes from whichever contributors it
includes in the normal way.

For our part — we intend to keep working hard to improve LibreOffice
core in all the normal ways: code, sponsorship, mentoring, evangelizing
and serving in lots of capacities as before while we are welcome as
collaborators. This move is focused only on protecting the Online piece
and we hope the choices TDF makes will complement that.

### Do we need investment? {#investment}

Let us first state clearly that volunteers have always contributed to FOSS projects, and do so in many different ways. This is important and LibreOffice is no
exception. So obviously we would love you to get involved and e.g. help out improving
the code with us.

Professional developers bring the ability to contribute huge amounts of feature/function work, mentoring, and the depth of focus
necessary to tackle the hardest issues: improving interoperability,
performance, memory consumption, latency, move with changes in os and other software libraries — as well as building new UX
infrastructure and adding product polish — we're far from done.

Donations have also been a helpful revenue stream for TDF, however the
size of our investment need is sufficiently large that TDF's
donation cash-flow cannot meet it.

If you'd like a detailed explanation of some of the problems see: [vendor neutral
marketing](https://people.gnome.org/~michael/data/vendor-neutral-marketing.html)
complete with pictures.

### Does investment mean Venture Capital? {#VC}

No, Collabora is a FOSS company whose mission is to accelerate the adoption of FOSS across all industries, we have no plans to dilute our mission.
We do this by generating revenues around consultancy and product support. This allows us to hire full time engineers to invest on the FOSS codebases that we support.


### Did you try to work things out with TDF? {#TDF}

Indeed, from [2013](https://people.gnome.org/~michael/data/2013-09-25-economics.pdf)
it has been clear that we need to work to build the ecoystem around
LibreOffice. Many papers have been written since, presented, long
blogs, lengthy conversations through many conferences, board meetings.
Discussions in the community and board over a long period have done
nothing to build confidence.

Against that there have been some positives, a visionary Marketing
plan from Italo for example; but against much resistance.

### Why is branding & visibility important? {#visibility}

In large part for marketing. By investing in OSS, you can get your
brand widely known, that's really important when someone wants support
or services, or a custom version of the product.

	"No one expects it to be easy to make money in free
	software. While making money with free software is a
	challenge, the challenge is not necessarily greater than with
	proprietary software. In fact you make money in free software
	exactly the same way you do it in proprietary software: by
	building a great product, marketing it with skill and
	imagination, looking after your customers, and thereby
	building a brand that stands for quality and customer
	service." — Bob Young (founder of RedHat)

FOSS companies have very few assets: our code is all public, but we
can build brands that reflect the time & excellence we put into our
software, and use these to create a distinction that commands a price.

Unfortunately, investing in a brand you do not own, and leading people
to an environment where end-users / casual purchasers are extremely
unlikely to discover that the work was done by you — makes things
very difficult.

### Which brand to choose? {#brand-choice}

Customers have been confused in the past by branding, seeing
LibreOffice/TDF as the authentic source for Online. The use and
licensing of that brand has also been a cause for concern.

We all know well the annoyance or injustice of using a misleading
brand, or one that doesn't acknowledge those doing the work. The
LibreOffice users who call it OpenOffice by mistake, and of course
for years the GNU/Linux campaign to try to get fair representation
of the GNU project's work.

In more recent times we have several examples
[1](https://github.com/owncloud/richdocuments/issues/277),
[2](https://github.com/nextcloud/richdocuments/issues/639),
[3](https://github.com/learnweb/moodle-mod_collabora/issues/16)
of attempts to change the branding on code written by others.


## A Free / Open Source project {#floss}

We are committed to becoming a best-of-breed Free / Open Source
project. We start from a great place with the LibreOffice
heritage of license and general ethos, and we plan to build on
that, to make CODE a fun project to develop on. Clearly we
respect and recognize the contribution of all the developers of
LibreOffice and will honor that in equivalent access.

### Can I re-compile and re-distribute CODE? {#code-compile}

Yes, you'll need to follow the
[build instructions]({{< relref "build-code.md" >}}), as well
as the [license](https://www.mozilla.org/en-US/MPL/2.0/) and for now
if you're modifying it significantly
you will need to use your own brand name to make it clear that you are
standing behind that, and to avoid creating confusion around its origin.
That is easy to do using various configure options.

If you contribute significantly back to CODE we would love to work
with you to credit, help and promote your contribution, we look
forward to working with you. We will work to more explicitly open
up our (small) pieces of proprietary theming / branding / CSS over
time.

### Do you use a CLA ?

No. We use an in-bound == outbound licensing model, that gives the
same rights and responsibilities to all participants. Following
the LibreOffice ethos.

### Why use Transifex ?

Good question - we're investigating a move to a hosted Weblate
solution right now; this was a quick and easy way to bootstrap
the project.

### How do I get commit access? {#commit-access}

Please poke us on IRC with your TDF commit credentials, and your
GitHub name, and we'll get you setup. We want TDF committership
to transfer to Collabora Online, and we welcome and honor
all who wish to to contribute.

### How do I get a say in the project? {#say}

We love to work with sharp people, to write FOSS, and to listen to
them. We will try to attract and energise a community of do-ers, and
include them into our decision making over time.

We will try to keep commercial rivalry out in the marketplace
where it belongs, and keep the project focused on developing new
feature / function.

We also have a Partner Council that includes those partners and
customers who through their sales &amp; evangelism efforts have
contributed significantly to development, and we expect to expand this
over time.

### Is there the forum for questions and discussions?

You are welcome on the [Collabora Online forum](https://forum.collaboraonline.com/)!


{{< css.inline >}}
<style>
.canon { background: white; width: 100%; height: auto;}
</style>
{{< /css.inline >}}
