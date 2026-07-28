#!/usr/bin/env python3
"""Community Pulse backfill: monthly GitHub trend seed for CollaboraOnline/online.

Writes data/pulse/github_monthly.json covering the most recent 24 full
calendar months (ending with the last completed month). For each month it
records issues_opened, issues_closed and prs_merged, each taken from the
exact total_count of a GitHub search over a precise first-day..last-day
date range.

Python 3 stdlib only. A month whose searches fail gets null values and an
entry in notes; the script exits non-zero only when every month failed.
This is a one-off seed script, not part of the nightly cron.
"""

import calendar
import json
import os
import sys
import time
import urllib.error
import urllib.parse

import pulse_common

API = 'https://api.github.com'
OWNER_REPO = 'CollaboraOnline/online'
MONTHS_BACK = 24

# The authenticated search API allows 30 requests per minute. Three
# searches per month over 24 months is 72 calls, so a pause between calls
# keeps the whole run just above the two-second floor that limit implies.
SEARCH_PAUSE_SECONDS = 2.2

# When a search still comes back rate-limited (HTTP 403), wait this long
# before trying that call again.
RATE_LIMIT_WAIT_SECONDS = 65
RATE_LIMIT_RETRIES = 3


def recent_full_months(count):
    """Return the last `count` completed calendar months as (year, month)
    tuples in chronological order. The current month is still in progress,
    so the list ends with the previous month."""
    now = pulse_common.utcnow()
    year, month = now.year, now.month
    months = []
    for _ in range(count):
        month -= 1
        if month == 0:
            year -= 1
            month = 12
        months.append((year, month))
    months.reverse()
    return months


def month_range(year, month):
    """Return (first_day, last_day) of the month as YYYY-MM-DD strings."""
    last = calendar.monthrange(year, month)[1]
    return ('%04d-%02d-01' % (year, month),
            '%04d-%02d-%02d' % (year, month, last))


def search_count(query):
    """Return the exact total_count for an issue-search query.

    Retries after a pause when GitHub answers 403, which is how the search
    API reports that the per-minute rate limit was hit.
    """
    url = (API + '/search/issues?'
           + urllib.parse.urlencode({'q': query, 'per_page': 1}))
    for attempt in range(RATE_LIMIT_RETRIES + 1):
        try:
            doc = pulse_common.http_get_json(
                url, headers=pulse_common.github_headers(), retries=1)
            time.sleep(SEARCH_PAUSE_SECONDS)
            return doc['total_count']
        except urllib.error.HTTPError as err:
            if err.code == 403 and attempt < RATE_LIMIT_RETRIES:
                print('rate limited, waiting %ds: %s'
                      % (RATE_LIMIT_WAIT_SECONDS, query), file=sys.stderr)
                time.sleep(RATE_LIMIT_WAIT_SECONDS)
                continue
            raise


def main():
    months = recent_full_months(MONTHS_BACK)
    repo_query = 'repo:' + OWNER_REPO
    rows = []
    notes = []

    for year, month in months:
        label = '%04d-%02d' % (year, month)
        first_day, last_day = month_range(year, month)
        date_range = '%s..%s' % (first_day, last_day)
        row = {'month': label, 'issues_opened': None,
               'issues_closed': None, 'prs_merged': None}
        queries = [
            ('issues_opened', '%s is:issue created:%s' % (repo_query, date_range)),
            ('issues_closed', '%s is:issue closed:%s' % (repo_query, date_range)),
            ('prs_merged', '%s is:pr merged:%s' % (repo_query, date_range)),
        ]
        for key, query in queries:
            try:
                row[key] = search_count(query)
            except Exception as err:
                notes.append('%s %s unavailable: %s' % (label, key, err))
                print('warning: %s %s failed: %s' % (label, key, err),
                      file=sys.stderr)
        rows.append(row)
        print('%s issues_opened=%s issues_closed=%s prs_merged=%s'
              % (label, row['issues_opened'], row['issues_closed'],
                 row['prs_merged']))

    if all(row[key] is None
           for row in rows
           for key in ('issues_opened', 'issues_closed', 'prs_merged')):
        print('error: every month failed, not writing github_monthly.json',
              file=sys.stderr)
        return 1

    doc = {'source': 'github_monthly',
           'generated_at': pulse_common.iso_z(pulse_common.utcnow()),
           'months': rows}
    if notes:
        doc['notes'] = notes
    os.makedirs(pulse_common.DATA_DIR, exist_ok=True)
    path = os.path.join(pulse_common.DATA_DIR, 'github_monthly.json')
    with open(path, 'w', encoding='utf-8') as fh:
        json.dump(doc, fh, indent=2, sort_keys=True, ensure_ascii=False)
        fh.write('\n')
    print('wrote %s' % os.path.relpath(path, pulse_common.REPO_ROOT))
    return 0


if __name__ == '__main__':
    sys.exit(main())
