#!/usr/bin/env python3
"""Fetch Community Pulse forum metrics into data/pulse/forum.json.

Source: https://forum.collaboraonline.com - the Collabora Online forum
(a Discourse instance with public JSON endpoints, no auth).
"""

import sys
import time

import pulse_common as pc

COOL_FORUM = 'https://forum.collaboraonline.com'

TOP_TOPICS_LIMIT = 5

# Pause between requests so we stay polite to the Discourse servers.
REQUEST_GAP_SECONDS = 1


def get_json(url):
    time.sleep(REQUEST_GAP_SECONDS)
    return pc.http_get_json(url)


def topic_url(base, topic):
    slug = topic.get('slug')
    if slug:
        return '%s/t/%s/%d' % (base, slug, topic['id'])
    return '%s/t/%d' % (base, topic['id'])


def top_topics(base, list_path, limit=TOP_TOPICS_LIMIT):
    """Return the first topics of a Discourse topic-list endpoint.

    The list keeps the server's own ordering (for top.json that is the
    Discourse "top" score for the period). Each entry carries only fields
    the API returned: title, url, views and posts (posts_count).
    """
    doc = get_json('%s/%s' % (base, list_path))
    topics = doc.get('topic_list', {}).get('topics', [])
    result = []
    for topic in topics[:limit]:
        result.append({
            'title': topic.get('title'),
            'url': topic_url(base, topic),
            'views': topic.get('views'),
            'posts': topic.get('posts_count'),
        })
    return result


def fetch_cool_forum(notes):
    metrics = {
        'topics_30d': None,
        'posts_30d': None,
        'active_users_30d': None,
        'total_topics': None,
        'total_posts': None,
        'top_topics_monthly': None,
    }
    try:
        about = get_json(COOL_FORUM + '/about.json')
        stats = about.get('about', {}).get('stats', {})
        metrics['topics_30d'] = stats.get('topics_30_days')
        metrics['posts_30d'] = stats.get('posts_30_days')
        metrics['active_users_30d'] = stats.get('active_users_30_days')
        metrics['total_topics'] = stats.get('topics_count')
        metrics['total_posts'] = stats.get('posts_count')
    except Exception as err:
        notes.append('cool_forum: /about.json failed (%s); '
                     'stats metrics set to null' % err)
    try:
        metrics['top_topics_monthly'] = top_topics(
            COOL_FORUM, 'top.json?period=monthly')
    except Exception as err:
        notes.append('cool_forum: /top.json?period=monthly failed (%s); '
                     'top_topics_monthly set to null' % err)
    return metrics


def main():
    notes = []
    metrics = {
        'cool_forum': fetch_cool_forum(notes),
    }

    def has_data(value):
        if isinstance(value, dict):
            return any(has_data(v) for v in value.values())
        return value is not None

    if not has_data(metrics):
        print('fetch_forum: every metric failed, not writing forum.json',
              file=sys.stderr)
        for note in notes:
            print('  ' + note, file=sys.stderr)
        return 1

    pc.write_source_json('forum', metrics, period_doc=pc.period(),
                         notes=notes or None)
    return 0


if __name__ == '__main__':
    sys.exit(main())
