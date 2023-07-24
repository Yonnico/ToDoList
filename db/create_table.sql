BEGIN;
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY,
    user_id TEXT,
    task_index INTEGER NOT NULL DEFAULT 1,
    done boolean DEFAULT False,
    title TEXT NOT NULL,
    description TEXT NOT NULL
);
COMMIT;