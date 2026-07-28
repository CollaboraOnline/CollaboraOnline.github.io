#!/usr/bin/env python3
"""Fetch review metrics from gerrit.collaboraoffice.com for Community Pulse.

Writes data/pulse/gerrit.json. All queries are scoped to the Gerrit project
'online' (the CollaboraOnline monorepo); the other projects hosted on the
same Gerrit are not part of the public dashboard.

The open and unreviewed definitions follow the weekly report script
gerrit-unreviewed-stats.sh: a change is open-active when it is open and not
work-in-progress, and it is unreviewed when in addition no reviewer has
voted Code-Review at +1 or higher, or at -1 or lower.
"""

import sys
import urllib.parse
from collections import Counter

import pulse_common as pc

BASE = 'https://gerrit.collaboraoffice.com'
PROJECT = 'online'
PAGE_SIZE = 500
TOP_AUTHORS = 5


def fetch_all_changes(query, extra=''):
    """Fetch every change matching the query, following Gerrit pagination.

    Gerrit returns at most n results per request and marks the last element
    of a truncated page with _more_changes; the S parameter skips the
    results already seen.
    """
    changes = []
    start = 0
    while True:
        url = ('%s/changes/?q=%s&n=%d&S=%d%s'
               % (BASE, urllib.parse.quote(query), PAGE_SIZE, start, extra))
        page = pc.http_get_json(url)
        changes.extend(page)
        if not (page and page[-1].get('_more_changes')):
            return changes
        # The server may return fewer results per page than requested, so
        # the next offset comes from the page that actually arrived.
        start += len(page)


def owner_display_name(owner):
    """Human-readable owner name from DETAILED_ACCOUNTS info, never an email."""
    return (owner.get('name')
            or owner.get('display_name')
            or owner.get('username')
            or 'account %s' % owner.get('_account_id'))


def main():
    period_doc = pc.period()
    notes = [
        "All metrics cover the Gerrit project 'online' (the CollaboraOnline "
        'monorepo) only; other projects on gerrit.collaboraoffice.com are '
        'excluded.',
        'merged_30d counts changes by submit time (mergedafter:), so it is '
        'exactly the set of changes merged inside the window.',
    ]
    metrics = {}
    failed_queries = 0

    open_active_query = 'project:%s status:open -is:wip' % PROJECT
    unreviewed_query = (open_active_query
                        + ' -label:Code-Review>=1 -label:Code-Review<=-1')
    merged_query = ('project:%s status:merged mergedafter:%s'
                    % (PROJECT, period_doc['from']))

    try:
        merged = fetch_all_changes(merged_query, extra='&o=DETAILED_ACCOUNTS')
        metrics['merged_30d'] = len(merged)
        counts = Counter()
        names = {}
        for change in merged:
            owner = change.get('owner') or {}
            account_id = owner.get('_account_id')
            if account_id is None:
                continue
            counts[account_id] += 1
            names[account_id] = owner_display_name(owner)
        top = sorted(counts.items(),
                     key=lambda item: (-item[1], names[item[0]]))
        metrics['top_authors_30d'] = [
            {'name': names[account_id], 'merged': merged_count}
            for account_id, merged_count in top[:TOP_AUTHORS]]
    except Exception as err:
        metrics['merged_30d'] = None
        metrics['top_authors_30d'] = None
        notes.append('merged-changes query failed, merged_30d and '
                     'top_authors_30d omitted: %s' % err)
        failed_queries += 1

    try:
        metrics['open_active'] = len(fetch_all_changes(open_active_query))
    except Exception as err:
        metrics['open_active'] = None
        notes.append('open-changes query failed, open_active omitted: %s'
                     % err)
        failed_queries += 1

    try:
        metrics['open_unreviewed'] = len(fetch_all_changes(unreviewed_query))
    except Exception as err:
        metrics['open_unreviewed'] = None
        notes.append('unreviewed-changes query failed, open_unreviewed '
                     'omitted: %s' % err)
        failed_queries += 1

    if failed_queries == 3:
        print('fetch_gerrit: all Gerrit queries failed, not writing output',
              file=sys.stderr)
        for note in notes:
            print('fetch_gerrit: %s' % note, file=sys.stderr)
        return 1

    pc.write_source_json('gerrit', metrics, period_doc=period_doc,
                         notes=notes)
    return 0


if __name__ == '__main__':
    sys.exit(main())
