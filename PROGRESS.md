# SOC Platform: Progress Tracker

Project: Django + DRF + Channels SOC alert platform
Repo: https://github.com/frenkiegithua/django-soc-project
Scope rule: every day is SOC or security work. No unrelated domains.

## Plan (7 phases, 100 days)

| Phase | Days | Focus | Status |
|---|---|---|---|
| 1: Foundations | 1-15 | Python refresh, Django basics, request/response, templates, forms | Complete |
| 2: Databases & Auth | 16-30 | Models, relationships, users, permissions, security events DB | In progress |
| 3: REST APIs & Networking | 31-45 | HTTP deeply, REST, DRF, network-aware APIs | Not started |
| 4: SOC Dashboard | 46-65 | Real SOC alert dashboard with analyst features | Not started |
| 5: Security & Hardening | 66-80 | CSRF, XSS, SQL injection, authentication, secure design | Not started |
| 6: Logs & Detection | 81-90 | Event pipelines, log processing, detection rules, alerts | Not started |
| 7: Capstone | 91-100 | Mini SOC platform combining everything | Not started |

## Day Log

| Day | Topic | Commit | Status |
|---|---|---|---|
| 1-5 | Setup, views, templates, forms | early commits | Done |
| 6-7 | Alert model, admin, ModelForm, filtering | early commits | Done |
| 8 | Search, pagination, sorting | early commits | Done |
| 9 | REST API (CRUD, webhook, CSV export) | early commits | Done |
| 10 | Token auth, rate limiting, audit fields | early commits | Done |
| 11 | Incident model, analytics, stats endpoint | early commits | Done |
| 12 | Notifications (email, Slack, webhook) | fd47063 | Done |
| 13 | Authenticated WebSocket dashboard, reconnect with backoff | 005e8d3 | Done |
| 14 | Live Open Incidents counter over WebSocket | 27b87b1 | Done |
| 15 | Incident assignment and "my queue" (?assigned=me) | no dedicated commit | Done (shipped in Day 16 history) |
| 16 | Append-only AuditLog for incident changes | 030230c | Done |
| 17 | Permissions and roles: analyst vs. lead groups | | Next |

## Phase 2 Day Plan (proposed, confirm before use)

- 17: Permissions and roles (analyst vs. lead groups)
- 18: Object-level permissions (only the assignee can resolve an incident)
- 19: Security events schema (normalize alerts into one event model)
- 20: Relationships review and query optimization
- 21: Database integrity (unique and check constraints)
- 22: Audit log hardening and retention
- 23-29: To confirm together when reached
- 30: Phase 2 checkpoint

## Known Gaps

- [ ] API token was pasted into chat several times. Rotate again before any new test. Never paste it into chat or project files.
- [ ] Store the token in an environment variable (`export SOC_TOKEN=...`), not in files.
- [ ] Day 15 has no dedicated commit.
- [ ] Commit author in older commits shows the hostname identity (francis200). Future commits use frenkiegithua.
- [ ] Duplicate Day 14 commit message (fd47063 and 27b87b1).
- [ ] Audit log guard covers model save and delete only. Queryset deletes and raw SQL bypass it. Enforce at the database level in Phase 5.
- [ ] Django login: dashboard uses `LOGIN_URL = '/admin/login/'`. Keep this in settings.

## Working Rules

1. Goal: one sentence, inside the current phase.
2. Design: list models, endpoints, and files. Wait for approval before code.
3. Build: replace whole files. No partial edits.
4. Verify: test with expected output.
5. Record: update this file, commit, push. Run `git grep -n "$SOC_TOKEN" || echo clean` before committing.
6. Check: two knowledge-check questions before the next day.

## Session Handoff Prompt

Paste this file and say:

> Follow this plan. Restate today's day and wait for my go-ahead before writing code. Stay within SOC/security scope.

## Update Log

- 2026-10-19: Day 16 complete. Day 17 is next.
