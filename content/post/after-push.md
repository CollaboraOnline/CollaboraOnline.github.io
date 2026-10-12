+++
authors = [
    "Collabora",
]
title = "After you push to Gerrit"
date = "2026-10-12"
hide_from_home = true
description = "Reviewers, CI, and how to update your change after your first push"
type = "post"
tags = [
    "contribute",
    "development",
    "code",
    "gerrit",
]
showimage = false
showtitle = true
+++

You have pushed your first change to Gerrit. This page explains what happens next: how to get a
review, what the automatic build and test run (CI) checks, and how to update your change until it
is merged.
<!--more-->

## Checklist

1. [Open your change](#find-your-change-and-add-a-reviewer) at the URL the push printed.
2. [Wait for CI](#what-ci-does) (about 2 hours), or [read the failure](#when-ci-fails).
3. [Add a reviewer](#find-your-change-and-add-a-reviewer): the issue's mentor, or Darshan if you
   are not sure.
4. [Fix review comments](#update-your-change) by amending the same commit and pushing again.

Pushing several commits? See [Push several commits in a chain](#push-several-commits-in-a-chain).

## Find your change and add a reviewer

- The push prints the URL of your change on [gerrit.collaboraoffice.com](https://gerrit.collaboraoffice.com/).
- Open it and add a reviewer, ideally after CI is green:
  - If you work on a GitHub issue that has a mentor, or you already know who will review your
    change, add that person.
  - If you are not sure, add Darshan (Gerrit user `Darshan-upadhyay1110`).
- You cannot submit the change yourself. A reviewer gives Code-Review +2 (approval to merge), and
  the change is submitted once it also has Verified +1 from CI.

## What CI does

- Every new patchset (each push of an amended commit) starts one CI run of about ten jobs. They
  cover Linux builds with two compilers, the Cypress browser tests, and builds of the desktop and
  mobile apps.
- The result comes back as the Verified label: +1 when all jobs pass, -1 if any job fails.
- Jenkins posts a comment with a link to the build. Anyone can open it and read the console
  output.
- A run takes roughly 1.5 to 2 hours. It takes longer when the queue is busy.

## Update your change

Amend the same commit, keep the `Change-Id` line (Gerrit uses it to match your new commit to the
same change), and push again. Gerrit adds a new patchset to the same change.

```bash
git commit --amend
git push origin HEAD:refs/for/main
```

- The commands on this page assume `origin` is your SSH clone from Gerrit (see
  [where to get the code]({{< relref "faq.md#where-can-i-get-code" >}})). If your Gerrit remote
  has another name, use that name instead.
- Do not open a new change for fixes. Update the existing one.
- A new patchset cancels the automatic run that is still going for the old one, so you do not
  need to wait.
- If CI failed because `main` was broken and has since been fixed, rebase onto the current `main`
  and push again.

## Push several commits in a chain

Each commit becomes its own change, and each one would start a full CI run. The tip (the newest
commit, at the top of the chain) carries every commit below it, so one build at the tip is enough.
Push everything below the tip as work in progress, then push the tip as ready:

```bash
git push origin HEAD~1:refs/for/main%wip
git push origin HEAD:refs/for/main
```

- If none of the lower commits changed since your last push, the first command fails with
  "no new changes". That is harmless. Run the second command anyway.
- If a lower commit did change, the first command puts its change back into work in progress.
- Later patchsets of the tip start their own builds.
- When the series is ready to merge, take the lower changes out of work in progress in the Gerrit
  web page. That starts no builds.
- A single commit just takes the plain push.

## Work in progress and CI

- Work in progress (WIP) marks a change as a draft that is not ready for review. Set or clear it
  with the button on the change page, or push with `%wip` as shown above.
- A change marked work in progress, or private, gets no CI run.
- Marking it ready for review later also starts no run. Your next real update after that, such as
  a fix or a rebase onto a newer `main`, gets a build.

## When CI fails

- Open the failing job from the link in the Jenkins comment and read the console output.
- A real problem in your change fails again on every run.
- Some failures are not caused by your change: network or download errors, a build machine that
  disconnects, or timeouts. One known case is a Cypress job that is killed with no failing test.
  Its log shows `>>>>>> Information about the killed process group:`.
- You cannot rerun a build yourself. If a failure is not yours, comment on the change or
  [ask in chat](#where-to-ask), and a reviewer will rerun it.
- Do not push a patchset with no real change just to get a new run.
- To check a Cypress test locally, build first, then run it from the top of your clone. The target
  is `check-desktop`, `check-mobile` or `check-multi`, matching the test's folder under
  `cypress_test/integration_tests/`. The spec path is relative to that folder:

```bash
make -j $(nproc)
make -C cypress_test check-desktop spec=calc/foo_spec.js
```

## Where to ask

- Chat with the developers in the [#cool-dev Matrix room](https://app.element.io/?updated=1.11.111#/room/#cool-dev:matrix.org).
- Ask on the [Collabora Online forum](https://forum.collaboraonline.com/).
- If nobody has commented on your change after a few working days, ask about it in the Matrix room
  or on the forum.
- See [Get in touch]({{< relref "communicate.md#get-in-touch" >}}) for the other channels.
- Read the forum guide [Your first pull request](https://forum.collaboraonline.com/t/your-first-pull-request/41)
  for setting up your Gerrit account and pushing your first change.

{{< edit-button to="/content/post/after-push.md" name="Edit page">}}
