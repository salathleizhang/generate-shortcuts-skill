-- 001_init.sql
-- Initial schema for Cloudflare D1

CREATE TABLE IF NOT EXISTS users (
    id TEXT PRIMARY KEY,
    email TEXT UNIQUE,
    display_name TEXT NOT NULL DEFAULT '',
    avatar_url TEXT NOT NULL DEFAULT '',
    auth_provider TEXT NOT NULL,          -- google, github, apple
    provider_user_id TEXT NOT NULL,
    role TEXT NOT NULL DEFAULT 'user',    -- user, admin
    created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now')),
    updated_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now'))
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_users_provider
    ON users (auth_provider, provider_user_id);

CREATE TABLE IF NOT EXISTS shortcuts (
    id TEXT PRIMARY KEY,
    author_id TEXT,
    title TEXT NOT NULL DEFAULT '',
    slug TEXT UNIQUE,
    summary TEXT NOT NULL DEFAULT '',
    description TEXT NOT NULL DEFAULT '',
    status TEXT NOT NULL DEFAULT 'draft',
    -- draft, private, pending_signing, signed, pending_review, published, unlisted, hidden, deleted
    current_version_id TEXT,
    visibility TEXT NOT NULL DEFAULT 'private',  -- private, unlisted, public
    risk_level TEXT NOT NULL DEFAULT 'low',       -- low, medium, high
    download_count INTEGER NOT NULL DEFAULT 0,
    like_count INTEGER NOT NULL DEFAULT 0,
    favorite_count INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now')),
    updated_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now')),
    published_at TEXT,
    FOREIGN KEY (author_id) REFERENCES users(id)
);

CREATE INDEX IF NOT EXISTS idx_shortcuts_author ON shortcuts (author_id);
CREATE INDEX IF NOT EXISTS idx_shortcuts_status ON shortcuts (status);
CREATE INDEX IF NOT EXISTS idx_shortcuts_slug ON shortcuts (slug);

CREATE TABLE IF NOT EXISTS shortcut_versions (
    id TEXT PRIMARY KEY,
    shortcut_id TEXT NOT NULL,
    version_number INTEGER NOT NULL DEFAULT 1,
    source_type TEXT NOT NULL DEFAULT 'generated',   -- generated, uploaded
    unsigned_r2_key TEXT,
    signed_r2_key TEXT,
    preview_r2_key TEXT,
    plist_hash TEXT,
    signed_hash TEXT,
    signing_status TEXT NOT NULL DEFAULT 'pending',  -- pending, signed, failed
    created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now')),
    created_by TEXT,
    FOREIGN KEY (shortcut_id) REFERENCES shortcuts(id),
    FOREIGN KEY (created_by) REFERENCES users(id)
);

CREATE INDEX IF NOT EXISTS idx_versions_shortcut ON shortcut_versions (shortcut_id);

CREATE TABLE IF NOT EXISTS signing_jobs (
    id TEXT PRIMARY KEY,
    shortcut_id TEXT NOT NULL,
    version_id TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'queued',
    -- queued, running, succeeded, failed, retrying, cancelled
    input_r2_key TEXT NOT NULL,
    output_r2_key TEXT,
    attempt_count INTEGER NOT NULL DEFAULT 0,
    last_error TEXT,
    locked_by TEXT,
    locked_at TEXT,
    created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now')),
    updated_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now')),
    finished_at TEXT
);

CREATE INDEX IF NOT EXISTS idx_signing_jobs_status ON signing_jobs (status);
CREATE INDEX IF NOT EXISTS idx_signing_jobs_shortcut ON signing_jobs (shortcut_id);

CREATE TABLE IF NOT EXISTS community_posts (
    id TEXT PRIMARY KEY,
    shortcut_id TEXT NOT NULL UNIQUE,
    category TEXT NOT NULL DEFAULT 'general',
    featured INTEGER NOT NULL DEFAULT 0,
    rank_score REAL NOT NULL DEFAULT 0,
    published_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now')),
    hidden_at TEXT,
    FOREIGN KEY (shortcut_id) REFERENCES shortcuts(id)
);

CREATE INDEX IF NOT EXISTS idx_community_category ON community_posts (category);
CREATE INDEX IF NOT EXISTS idx_community_rank ON community_posts (rank_score DESC);

CREATE TABLE IF NOT EXISTS tags (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    slug TEXT NOT NULL UNIQUE,
    created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now'))
);

CREATE TABLE IF NOT EXISTS shortcut_tags (
    shortcut_id TEXT NOT NULL,
    tag_id TEXT NOT NULL,
    PRIMARY KEY (shortcut_id, tag_id),
    FOREIGN KEY (shortcut_id) REFERENCES shortcuts(id),
    FOREIGN KEY (tag_id) REFERENCES tags(id)
);

CREATE TABLE IF NOT EXISTS reports (
    id TEXT PRIMARY KEY,
    shortcut_id TEXT NOT NULL,
    reporter_id TEXT,
    reason TEXT NOT NULL,
    detail TEXT NOT NULL DEFAULT '',
    status TEXT NOT NULL DEFAULT 'pending',  -- pending, reviewing, resolved, dismissed
    created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now')),
    resolved_at TEXT,
    FOREIGN KEY (shortcut_id) REFERENCES shortcuts(id),
    FOREIGN KEY (reporter_id) REFERENCES users(id)
);

CREATE INDEX IF NOT EXISTS idx_reports_status ON reports (status);
CREATE INDEX IF NOT EXISTS idx_reports_shortcut ON reports (shortcut_id);
