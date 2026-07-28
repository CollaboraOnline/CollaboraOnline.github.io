#!/usr/bin/env python3
"""Run all Community Pulse fetchers and append today's history entry.

Runs the five fetchers as subprocesses, one after the other. A fetcher
that fails does not stop the run: its previous data/pulse/<source>.json
stays in place (the fetchers write nothing on total failure) and the
affected history values become null. After the fetchers, one compact
entry for today is written into data/pulse/history.json, which keeps at
most one entry per date, sorted by date.

Exits non-zero only when every fetcher failed.
"""

import json
import os
import subprocess
import sys

import pulse_common as pc

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

FETCHERS = ['github', 'gerrit', 'forum', 'weblate', 'docker']

HISTORY_PATH = os.path.join(pc.DATA_DIR, 'history.json')

# The metric keys each source contributes to a history entry. Forum
# values live under the cool_forum sub-object of the source metrics.
HISTORY_KEYS = {
    'github': ['issues_opened_30d', 'issues_closed_30d', 'prs_merged_30d',
               'commits_30d', 'open_issues', 'stars'],
    'gerrit': ['merged_30d', 'open_unreviewed'],
    'forum': ['topics_30d', 'posts_30d', 'active_users_30d'],
    'weblate': ['languages', 'translated_percent'],
    'docker': ['pull_count'],
}


def run_fetcher(name):
    """Run one fetcher, echoing its output. Returns True when it succeeded."""
    script = os.path.join(SCRIPT_DIR, 'fetch_%s.py' % name)
    print('--- running fetch_%s.py' % name)
    try:
        proc = subprocess.run([sys.executable, script], capture_output=True,
                              text=True, timeout=1800)
    except (OSError, subprocess.SubprocessError) as err:
        print('fetch_%s.py failed to run: %s' % (name, err), file=sys.stderr)
        return False
    if proc.stdout:
        print(proc.stdout, end='')
    if proc.stderr:
        print(proc.stderr, end='', file=sys.stderr)
    if proc.returncode != 0:
        print('fetch_%s.py exited with code %d; keeping the previous '
              'data/pulse/%s.json' % (name, proc.returncode, name),
              file=sys.stderr)
        # In GitHub Actions this line shows up as a warning annotation on
        # the run, so a partly failed night stays visible while the job
        # itself stays green.
        print('::warning::Community Pulse: fetch_%s.py failed; %s.json '
              'kept from the previous run' % (name, name))
        return False
    return True


def history_entry(date, failed=()):
    """Build today's compact history entry from the source JSON files.

    A source whose fetcher failed this run yields null for every one of
    its keys, even when a previous day's JSON file is still present, so
    the history never records stale values under a fresh date. A source
    file that is missing, or a metric the file does not carry, also
    yields null. The values are copied as-is, never recomputed.
    """
    entry = {'date': date}
    for source, keys in HISTORY_KEYS.items():
        if source in failed:
            entry[source] = {key: None for key in keys}
            continue
        doc = pc.read_source_json(source)
        metrics = doc.get('metrics') if isinstance(doc, dict) else None
        if source == 'forum' and isinstance(metrics, dict):
            metrics = metrics.get('cool_forum')
        if not isinstance(metrics, dict):
            metrics = {}
        entry[source] = {key: metrics.get(key) for key in keys}
    return entry


def append_history(entry):
    """Insert the entry into history.json, replacing any entry for the
    same date, and keep the array sorted by date."""
    history = []
    if os.path.exists(HISTORY_PATH):
        with open(HISTORY_PATH, encoding='utf-8') as fh:
            history = json.load(fh)
    history = [item for item in history if item.get('date') != entry['date']]
    history.append(entry)
    history.sort(key=lambda item: item['date'])
    os.makedirs(pc.DATA_DIR, exist_ok=True)
    with open(HISTORY_PATH, 'w', encoding='utf-8') as fh:
        json.dump(history, fh, indent=1, ensure_ascii=False)
        fh.write('\n')
    print('wrote %s (%d entries)'
          % (os.path.relpath(HISTORY_PATH, pc.REPO_ROOT), len(history)))


def main():
    results = {name: run_fetcher(name) for name in FETCHERS}

    failed = {name for name, ok in results.items() if not ok}
    today = pc.utcnow().strftime('%Y-%m-%d')
    append_history(history_entry(today, failed))

    print('--- run summary (%s)' % today)
    for name in FETCHERS:
        print('  %-8s %s' % (name, 'ok' if results[name] else 'FAILED'))

    if not any(results.values()):
        print('all fetchers failed', file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
