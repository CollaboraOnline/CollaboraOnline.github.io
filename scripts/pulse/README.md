# Community Pulse - data pipeline

Community Pulse is the live community dashboard at `/post/pulse/`. A nightly
GitHub Actions workflow (`.github/workflows/pulse_fetch.yaml`) runs the
fetchers in this directory, commits the refreshed JSON under `data/pulse/`,
and the site redeploys - the same pattern as `contributors_fetch.yaml`.

## Files

| Script | Output | Source |
|---|---|---|
| `fetch_github.py` | `data/pulse/github.json` | api.github.com (CollaboraOnline/online) |
| `fetch_gerrit.py` | `data/pulse/gerrit.json` | gerrit.collaboraoffice.com REST |
| `fetch_forum.py` | `data/pulse/forum.json` | forum.collaboraonline.com (Discourse JSON) |
| `fetch_weblate.py` | `data/pulse/weblate.json` | hosted.weblate.org API (project collabora-online) |
| `fetch_docker.py` | `data/pulse/docker.json` | hub.docker.com v2 API (collabora/code) |
| `backfill_github_monthly.py` | `data/pulse/github_monthly.json` | GitHub search API (run manually, not in cron) |
| `run_all.py` | runs all fetchers + appends `data/pulse/history.json` | - |

All scripts are Python 3 **stdlib only** (no pip installs in CI) and use the
shared helpers in `pulse_common.py`.

## Data contract

Every `data/pulse/<source>.json` has this envelope:

```json
{
  "source": "<name>",
  "generated_at": "2026-07-28T00:00:00Z",
  "period": { "days": 30, "from": "2026-06-28", "to": "2026-07-28" },
  "metrics": { ... },
  "notes": ["optional caveats, e.g. 'weblate leaderboard needs auth, omitted'"]
}
```

`period` describes the rolling window used by `*_30d` metrics; sources with
no windowed metrics may omit it.

### Exact metric keys

`github.json` (repo `CollaboraOnline/online`):
`stars`, `forks`, `open_issues` (issues only, PRs excluded), `open_prs`,
`issues_opened_30d`, `issues_closed_30d`, `prs_opened_30d`, `prs_merged_30d`,
`commits_30d` (default branch), `active_authors_30d` (unique commit authors
in window), `easy_hacks_open` (open issues labeled `Easy Hack`),
`top_upvoted_open_issues` (top 5, each `{number, title, url, thumbs_up}`).

`gerrit.json` (host `gerrit.collaboraoffice.com`, project `online`):
`merged_30d`, `open_active` (open, not WIP), `open_unreviewed` (open, not
WIP, no reviewer response), `top_authors_30d` (top 5 by merged changes,
each `{name, merged}`).

`forum.json`:
`cool_forum` -> `{topics_30d, posts_30d, active_users_30d, total_topics,
total_posts, top_topics_monthly}` (top 5, each `{title, url, views, posts}`).

`weblate.json` (project `collabora-online` on hosted.weblate.org):
`languages`, `translated_percent` (project-wide, 1 decimal),
`total_strings`, `components`.

`docker.json` (repository `collabora/code`):
`pull_count`, `star_count`.

`history.json` - array of one compact entry per day, sorted by date,
at most one entry per date (re-runs on the same date replace the entry):

```json
{ "date": "2026-07-28",
  "github":  { "issues_opened_30d": 0, "issues_closed_30d": 0, "prs_merged_30d": 0,
               "commits_30d": 0, "open_issues": 0, "stars": 0 },
  "gerrit":  { "merged_30d": 0, "open_unreviewed": 0 },
  "forum":   { "topics_30d": 0, "posts_30d": 0, "active_users_30d": 0 },
  "weblate": { "languages": 0, "translated_percent": 0.0 },
  "docker":  { "pull_count": 0 } }
```

`github_monthly.json` - backfilled trend seed, most recent 24 full months:

```json
{ "source": "github_monthly", "generated_at": "...",
  "months": [ { "month": "2024-08", "issues_opened": 0, "issues_closed": 0,
                "prs_merged": 0 }, ... ] }
```

## Accuracy policy (non-negotiable)

- **Never guess or estimate.** If an API call fails or an endpoint needs
  auth we don't have, set the affected metric to `null` and explain it in
  `notes`. A missing number is acceptable; a wrong number is not.
- Fetchers exit non-zero on total failure. `run_all.py` then keeps the
  previous day's JSON for that source (never overwrites good data with
  nulls) and records the failure in the history entry as `null`s.
- GitHub requests authenticate via `GITHUB_TOKEN`/`GH_TOKEN` env, falling
  back to `gh auth token` locally; unauthenticated is a last resort.
- Counting endpoints must be used in a way that returns exact totals
  (e.g. GitHub search `total_count`, Link-header pagination tricks), not
  truncated page lengths.

## Running locally

```
python3 scripts/pulse/run_all.py           # refresh all sources + history
python3 scripts/pulse/fetch_github.py      # any fetcher runs standalone
python3 scripts/pulse/backfill_github_monthly.py   # one-off trend seed
```
