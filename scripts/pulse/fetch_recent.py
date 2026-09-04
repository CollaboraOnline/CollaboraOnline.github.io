#!/usr/bin/env python3
"""Fetch the most recently merged changes on Gerrit for the homepage.

Writes data/pulse/recent.json. Only the submit time, subject, owner display
name and change number, since this file is served publicly.
"""

import sys
import urllib.parse

import pulse_common as pc

BASE = 'https://gerrit.collaboraoffice.com'
PROJECT = 'online'
COUNT = 8


def owner_display_name(owner):
    """Human-readable owner name from DETAILED_ACCOUNTS info, never an email."""
    return (owner.get('name')
            or owner.get('display_name')
            or owner.get('username')
            or 'account %s' % owner.get('_account_id'))


def submitted_iso(change):
    """Gerrit timestamps look like '2026-09-04 10:22:27.000000000' in UTC."""
    raw = change.get('submitted') or change.get('updated')
    if not raw:
        return None
    return raw.split('.')[0].replace(' ', 'T') + 'Z'


def main():
    query = 'project:%s status:merged' % PROJECT
    url = ('%s/changes/?q=%s&n=%d&o=DETAILED_ACCOUNTS'
           % (BASE, urllib.parse.quote(query), COUNT))

    try:
        changes = pc.http_get_json(url)
    except Exception as err:
        print('fetch_recent: Gerrit query failed, not writing output: %s' % err,
              file=sys.stderr)
        return 1

    entries = []
    for change in changes:
        when = submitted_iso(change)
        if not when:
            continue
        entries.append({
            'number': change.get('_number'),
            'subject': change.get('subject'),
            'owner': owner_display_name(change.get('owner') or {}),
            'submitted': when,
            'url': '%s/c/%s/+/%s' % (BASE, PROJECT, change.get('_number')),
        })

    if not entries:
        print('fetch_recent: no merged changes came back, not writing output',
              file=sys.stderr)
        return 1

    # Gerrit orders by update time, so the newest merge is not first.
    entries.sort(key=lambda item: item['submitted'], reverse=True)

    pc.write_source_json('recent', {'changes': entries}, notes=[
        "Covers the Gerrit project 'online' only.",
        'Timestamps are submit times in UTC, as reported by Gerrit.',
    ])
    return 0


if __name__ == '__main__':
    sys.exit(main())
