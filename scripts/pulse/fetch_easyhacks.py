#!/usr/bin/env python3
"""Community Pulse fetcher: open Easy Hack issues in CollaboraOnline/online.

Writes data/pulse/easyhacks.json following the envelope contract in README.md.
Python 3 stdlib only. The issue list comes from the REST issues listing with a
label filter and per_page=100 pagination, so the result is complete and exact
rather than a truncated search sample. On total failure the script writes
nothing and exits non-zero.
"""

import re
import sys
import urllib.parse

import pulse_common

API = 'https://api.github.com'
OWNER_REPO = 'CollaboraOnline/online'
LABEL = 'Easy Hack'

# Conservative mentor extraction. A mentor is recorded only when an issue
# body contains an explicit mentor line, matching phrasings such as
# "Mentor: name", "mentor is @login", "a mentor: name" or "mentors: a, b".
# The pattern requires the word mentor(s) followed by a colon or the word
# "is"/"are", then captures up to the end of that line. Anything less
# explicit (for example "looking for a mentor" or "no mentor yet") does not
# match, and a capture that carries no word characters is discarded, so the
# result is either a clearly stated name/login string or null.
MENTOR_PATTERN = re.compile(
    r'\bmentors?\s*(?::|\bis\b|\bare\b)\s*(?P<name>[^\r\n]+)',
    re.IGNORECASE)


def extract_mentor(body):
    """Return the mentor name/login stated in the issue body, or None."""
    if not body:
        return None
    match = MENTOR_PATTERN.search(body)
    if not match:
        return None
    name = match.group('name').strip().rstrip('.,;')
    # Markdown emphasis around the name ("**Mentor:** @login") leaves
    # stray asterisks or underscores; strip them from both ends.
    name = name.strip('*_ ').strip()
    if not name or not re.search(r'\w', name):
        return None
    return name


def fetch_easy_hack_issues():
    """Return every open Easy Hack issue from the paginated REST listing."""
    issues = []
    page = 1
    while True:
        params = urllib.parse.urlencode({'labels': LABEL, 'state': 'open',
                                         'per_page': 100, 'page': page})
        url = '%s/repos/%s/issues?%s' % (API, OWNER_REPO, params)
        batch = pulse_common.http_get_json(
            url, headers=pulse_common.github_headers())
        for item in batch:
            # The issues listing also carries pull requests; only real
            # issues belong in the board.
            if 'pull_request' in item:
                continue
            issues.append(item)
        if len(batch) < 100:
            break
        page += 1
    return issues


def issue_metrics(item):
    """Build the compact per-issue record from one listing item."""
    labels = [label['name'] for label in item.get('labels') or []
              if label.get('name') and label['name'] != LABEL]
    assignee = (item.get('assignee') or {}).get('login')
    return {
        'number': item['number'],
        'title': item['title'],
        'url': item['html_url'],
        'created_at': item['created_at'][:10],
        'updated_at': item['updated_at'][:10],
        'labels': labels,
        'assignee': assignee,
        'comments': item.get('comments', 0),
        'thumbs_up': (item.get('reactions') or {}).get('+1', 0),
        'mentor': extract_mentor(item.get('body')),
    }


def main():
    try:
        raw_issues = fetch_easy_hack_issues()
    except Exception as err:
        print('error: Easy Hack issue listing failed, not writing '
              'easyhacks.json: %s' % err, file=sys.stderr)
        return 1

    # Sorting on the full timestamp keeps same-day issues in a stable
    # most-recently-updated order even though the record stores dates only.
    raw_issues.sort(key=lambda item: item['updated_at'], reverse=True)
    records = [issue_metrics(item) for item in raw_issues]

    metrics = {'total_open': len(records), 'issues': records}
    pulse_common.write_source_json('easyhacks', metrics)
    return 0


if __name__ == '__main__':
    sys.exit(main())
