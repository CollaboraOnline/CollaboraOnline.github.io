#!/usr/bin/env python3
"""Fetch Docker Hub metrics for the collabora/code repository.

Writes data/pulse/docker.json with: pull_count, star_count.

A single unauthenticated request to the Docker Hub v2 repository endpoint
returns both numbers.
"""

import sys

import pulse_common as pc

REPO_URL = 'https://hub.docker.com/v2/repositories/collabora/code/'


def main():
    metrics = {'pull_count': None, 'star_count': None}
    notes = []

    try:
        repo = pc.http_get_json(REPO_URL, headers={'Accept': 'application/json'})
    except Exception as err:
        print('fetch_docker: GET %s failed: %s' % (REPO_URL, err), file=sys.stderr)
        return 1

    for key in ('pull_count', 'star_count'):
        value = repo.get(key)
        if isinstance(value, int):
            metrics[key] = value
        else:
            notes.append('%s missing from Docker Hub response, set to null' % key)

    if metrics['pull_count'] is None and metrics['star_count'] is None:
        print('fetch_docker: response carried neither pull_count nor star_count',
              file=sys.stderr)
        return 1

    # Totals only, no windowed metrics, so the envelope carries no period.
    pc.write_source_json('docker', metrics, notes=notes or None)
    return 0


if __name__ == '__main__':
    sys.exit(main())
