#!/usr/bin/env python3
"""Community Pulse fetcher: GitHub metrics for CollaboraOnline/online.

Writes data/pulse/github.json following the envelope contract in README.md.
Python 3 stdlib only. Any metric that cannot be fetched exactly is set to
null with an explanation appended to notes; the script exits non-zero only
when every metric failed (total failure).
"""

import sys
import time
import urllib.parse

import pulse_common

API = 'https://api.github.com'
OWNER_REPO = 'CollaboraOnline/online'

# The authenticated search API allows 30 requests per minute; a short pause
# between search calls keeps a full run well under that.
SEARCH_PAUSE_SECONDS = 2.5


def api_json(path, params=None):
    url = API + path
    if params:
        url += '?' + urllib.parse.urlencode(params)
    return pulse_common.http_get_json(url, headers=pulse_common.github_headers())


def search_issues(query, per_page=1, sort=None, order=None):
    """Run one issue-search call and return the parsed JSON document.

    The search API reports an exact total_count for the query, which is how
    the counting metrics stay exact without paginating result pages.
    """
    params = {'q': query, 'per_page': per_page}
    if sort:
        params['sort'] = sort
    if order:
        params['order'] = order
    doc = api_json('/search/issues', params)
    time.sleep(SEARCH_PAUSE_SECONDS)
    return doc


def search_count(query):
    return search_issues(query)['total_count']


def fetch_commit_stats(default_branch, since_iso):
    """Return (commit_count, unique_author_count) on the default branch.

    Authors are deduplicated by GitHub login when the commit is linked to an
    account, otherwise by the git author name plus email.
    """
    commits = 0
    authors = set()
    page = 1
    while True:
        batch = api_json('/repos/%s/commits' % OWNER_REPO,
                         {'sha': default_branch, 'since': since_iso,
                          'per_page': 100, 'page': page})
        for commit in batch:
            commits += 1
            author = commit.get('author')
            if author and author.get('login'):
                authors.add('login:' + author['login'])
            else:
                git_author = (commit.get('commit') or {}).get('author') or {}
                authors.add('git:%s <%s>' % (git_author.get('name', ''),
                                             git_author.get('email', '')))
        if len(batch) < 100:
            break
        page += 1
    return commits, len(authors)


def main():
    period_doc = pulse_common.period()
    from_date = period_doc['from']
    since_iso = from_date + 'T00:00:00Z'

    metric_keys = ['stars', 'forks', 'open_issues', 'open_prs',
                   'issues_opened_30d', 'issues_closed_30d',
                   'prs_opened_30d', 'prs_merged_30d',
                   'commits_30d', 'active_authors_30d',
                   'easy_hacks_open', 'top_upvoted_open_issues']
    metrics = {key: None for key in metric_keys}
    notes = []

    def fail(what, err):
        notes.append('%s unavailable: %s' % (what, err))
        print('warning: %s failed: %s' % (what, err), file=sys.stderr)

    # Repository document: stars, forks and the actual default branch. The branch
    # normally comes from the repo document itself; the literal is only a fallback
    # for when that request fails, and matches the current default branch.
    default_branch = 'main'
    try:
        repo = api_json('/repos/' + OWNER_REPO)
        metrics['stars'] = repo['stargazers_count']
        metrics['forks'] = repo['forks_count']
        default_branch = repo['default_branch']
    except Exception as err:
        fail('stars/forks (repo document)', err)

    # Exact counts from search total_count. GitHub's own open_issues_count
    # mixes pull requests in, so open issues come from an is:issue search.
    repo_query = 'repo:' + OWNER_REPO
    searches = [
        ('open_issues', '%s is:issue is:open' % repo_query),
        ('open_prs', '%s is:pr is:open' % repo_query),
        ('issues_opened_30d', '%s is:issue created:>=%s' % (repo_query, from_date)),
        ('issues_closed_30d', '%s is:issue closed:>=%s' % (repo_query, from_date)),
        ('prs_opened_30d', '%s is:pr created:>=%s' % (repo_query, from_date)),
        ('prs_merged_30d', '%s is:pr merged:>=%s' % (repo_query, from_date)),
        ('easy_hacks_open', '%s is:issue is:open label:"Easy Hack"' % repo_query),
    ]
    for key, query in searches:
        try:
            metrics[key] = search_count(query)
        except Exception as err:
            fail(key, err)

    # Commit activity on the default branch inside the window.
    try:
        commits, authors = fetch_commit_stats(default_branch, since_iso)
        metrics['commits_30d'] = commits
        metrics['active_authors_30d'] = authors
    except Exception as err:
        fail('commits_30d/active_authors_30d', err)

    # Top five open issues ranked by thumbs-up reactions.
    try:
        doc = search_issues('%s is:issue is:open' % repo_query, per_page=5,
                            sort='reactions-+1', order='desc')
        metrics['top_upvoted_open_issues'] = [
            {'number': item['number'],
             'title': item['title'],
             'url': item['html_url'],
             'thumbs_up': (item.get('reactions') or {}).get('+1', 0)}
            for item in doc['items']]
    except Exception as err:
        fail('top_upvoted_open_issues', err)

    if all(value is None for value in metrics.values()):
        print('error: every GitHub metric failed, not writing github.json',
              file=sys.stderr)
        return 1

    pulse_common.write_source_json('github', metrics, period_doc=period_doc,
                                   notes=notes or None)
    return 0


if __name__ == '__main__':
    sys.exit(main())
