"""Shared helpers for the Community Pulse fetchers (stdlib only)."""

import json
import os
import subprocess
import time
import urllib.error
import urllib.request
from datetime import datetime, timedelta, timezone

REPO_ROOT = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(REPO_ROOT, 'data', 'pulse')

WINDOW_DAYS = 30

USER_AGENT = ('COOL-Community-Pulse/1.0 '
              '(+https://collaboraonline.github.io/post/pulse/)')


def utcnow():
    return datetime.now(timezone.utc)


def iso_z(dt):
    return dt.strftime('%Y-%m-%dT%H:%M:%SZ')


def window(days=WINDOW_DAYS):
    """Rolling window ending now; returns (from_date, to_date) as YYYY-MM-DD."""
    to_dt = utcnow()
    from_dt = to_dt - timedelta(days=days)
    return from_dt.strftime('%Y-%m-%d'), to_dt.strftime('%Y-%m-%d')


def period(days=WINDOW_DAYS):
    from_date, to_date = window(days)
    return {'days': days, 'from': from_date, 'to': to_date}


def http_get(url, headers=None, retries=3, timeout=60):
    """GET a URL, return raw bytes. Retries with backoff; raises on failure."""
    request_headers = dict(headers or {})
    request_headers.setdefault('User-Agent', USER_AGENT)
    last_err = None
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers=request_headers)
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return resp.read()
        except (urllib.error.URLError, TimeoutError, OSError) as err:
            last_err = err
            # A 401 or 404 is a definitive answer, so it is raised right
            # away; a 403 is usually a rate limit, so it gets one more
            # try after a pause.
            if isinstance(err, urllib.error.HTTPError) and err.code in (401, 403, 404):
                if err.code == 403 and attempt < retries - 1:
                    time.sleep(30)
                    continue
                raise
            time.sleep(3 * (attempt + 1))
    raise RuntimeError('GET %s failed after %d attempts: %s'
                       % (url, retries, last_err))


def http_get_json(url, headers=None, retries=3, timeout=60):
    body = http_get(url, headers=headers, retries=retries, timeout=timeout)
    # Gerrit prepends an XSSI guard line before the JSON body.
    if body.startswith(b")]}'"):
        body = body.split(b'\n', 1)[1]
    return json.loads(body)


def github_token():
    token = os.environ.get('GITHUB_TOKEN') or os.environ.get('GH_TOKEN')
    if token:
        return token
    try:
        out = subprocess.run(['gh', 'auth', 'token'], capture_output=True,
                             text=True, check=True, timeout=15)
        return out.stdout.strip() or None
    except (OSError, subprocess.SubprocessError):
        return None


def github_headers():
    headers = {'Accept': 'application/vnd.github+json',
               'X-GitHub-Api-Version': '2022-11-28'}
    token = github_token()
    if token:
        headers['Authorization'] = 'Bearer ' + token
    return headers


def write_source_json(name, metrics, period_doc=None, notes=None):
    """Write data/pulse/<name>.json following the envelope contract."""
    os.makedirs(DATA_DIR, exist_ok=True)
    doc = {'source': name, 'generated_at': iso_z(utcnow()), 'metrics': metrics}
    if period_doc:
        doc['period'] = period_doc
    if notes:
        doc['notes'] = notes
    path = os.path.join(DATA_DIR, name + '.json')
    with open(path, 'w', encoding='utf-8') as fh:
        json.dump(doc, fh, indent=2, sort_keys=True, ensure_ascii=False)
        fh.write('\n')
    print('wrote %s' % os.path.relpath(path, REPO_ROOT))
    return path


def read_source_json(name):
    path = os.path.join(DATA_DIR, name + '.json')
    if not os.path.exists(path):
        return None
    with open(path, encoding='utf-8') as fh:
        return json.load(fh)
