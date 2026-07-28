#!/usr/bin/env python3
"""Fetch translation metrics for the collabora-online project on hosted.weblate.org.

Writes data/pulse/weblate.json with: languages, translated_percent,
total_strings, components.

Uses three API requests on a clean run (a retried request adds more), because the unauthenticated rate limit on
hosted.weblate.org is low (100 requests per day):

  1. /api/projects/collabora-online/statistics/  -> translated_percent, total
  2. /api/projects/collabora-online/components/?page_size=1  -> count
  3. /api/projects/collabora-online/languages/  -> one entry per language

All three endpoints work without authentication. An optional WEBLATE_TOKEN
environment variable is sent as an Authorization header when present, which
raises the rate limit.
"""

import os
import sys

import pulse_common as pc

API_BASE = 'https://hosted.weblate.org/api/projects/collabora-online/'


def weblate_headers():
    headers = {'Accept': 'application/json'}
    token = os.environ.get('WEBLATE_TOKEN')
    if token:
        headers['Authorization'] = 'Token ' + token
    return headers


def get_json(path):
    return pc.http_get_json(API_BASE + path, headers=weblate_headers())


def language_count(doc):
    # The languages endpoint returns a plain JSON array with one entry per
    # language; newer Weblate versions may return the usual paginated
    # envelope with a "count" field instead. Accept both shapes.
    if isinstance(doc, list):
        return len(doc)
    if isinstance(doc, dict) and isinstance(doc.get('count'), int):
        return doc['count']
    raise ValueError('unexpected languages payload shape: %s' % type(doc).__name__)


def main():
    metrics = {
        'languages': None,
        'translated_percent': None,
        'total_strings': None,
        'components': None,
    }
    notes = []
    failures = 0

    # Project-wide statistics: translated_percent and the total number of
    # strings (summed over every language and component pair). Weblate
    # already reports translated_percent rounded to one decimal.
    try:
        stats = get_json('statistics/')
        metrics['translated_percent'] = round(float(stats['translated_percent']), 1)
        metrics['total_strings'] = int(stats['total'])
    except Exception as err:
        failures += 1
        notes.append('statistics endpoint failed, translated_percent and '
                     'total_strings unavailable: %s' % err)

    # Component count comes from the paginated envelope; page_size=1 keeps
    # the response small while "count" still holds the exact total.
    try:
        components = get_json('components/?page_size=1')
        metrics['components'] = int(components['count'])
    except Exception as err:
        failures += 1
        notes.append('components endpoint failed, components unavailable: %s' % err)

    try:
        languages = get_json('languages/')
        metrics['languages'] = language_count(languages)
    except Exception as err:
        failures += 1
        notes.append('languages endpoint failed, languages unavailable: %s' % err)

    if failures == 3:
        print('fetch_weblate: all requests failed', file=sys.stderr)
        for note in notes:
            print('  ' + note, file=sys.stderr)
        return 1

    # No windowed (*_30d) metrics here, so the envelope carries no period.
    pc.write_source_json('weblate', metrics, notes=notes or None)
    return 0


if __name__ == '__main__':
    sys.exit(main())
