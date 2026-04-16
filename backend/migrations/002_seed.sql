-- 002_seed.sql
-- Initial seed data for community showcase

-- Tags
INSERT OR IGNORE INTO tags (id, name, slug) VALUES
    ('tag_productivity', 'Productivity', 'productivity'),
    ('tag_utility', 'Utility', 'utility'),
    ('tag_social', 'Social', 'social'),
    ('tag_media', 'Media', 'media'),
    ('tag_automation', 'Automation', 'automation'),
    ('tag_health', 'Health', 'health'),
    ('tag_developer', 'Developer', 'developer'),
    ('tag_finance', 'Finance', 'finance'),
    ('tag_education', 'Education', 'education'),
    ('tag_fun', 'Fun', 'fun');

-- System user for seed shortcuts
INSERT OR IGNORE INTO users (id, email, display_name, avatar_url, auth_provider, provider_user_id, role)
VALUES ('system_user', 'system@shortcutai.app', 'ShortcutAI', '', 'system', 'system', 'admin');

-- Sample shortcuts
INSERT OR IGNORE INTO shortcuts (id, author_id, title, slug, summary, description, status, visibility, risk_level)
VALUES
    ('sc_morning', 'system_user', 'Morning Briefing', 'morning-briefing',
     'Get weather, calendar events, and news headlines in one tap.',
     'A daily morning routine shortcut that fetches the current weather forecast, shows your upcoming calendar events for the day, and reads top news headlines. Perfect for starting your day informed.',
     'published', 'public', 'low'),

    ('sc_pdf', 'system_user', 'Save Web Page as PDF', 'save-webpage-pdf',
     'Convert any web page to a PDF and save it to Files.',
     'Takes the current Safari page URL, converts it to a clean PDF document, and saves it to your iCloud Drive or local Files app. Useful for archiving articles and receipts.',
     'published', 'public', 'low'),

    ('sc_water', 'system_user', 'Water Reminder', 'water-reminder',
     'Reminds you to drink water every hour during the day.',
     'Sets up recurring notifications throughout the day to remind you to stay hydrated. Tracks your daily water intake and shows a summary at the end of the day.',
     'published', 'public', 'low'),

    ('sc_meeting', 'system_user', 'Meeting Notes', 'meeting-notes',
     'Start a timer, record notes, and save to a file when done.',
     'Starts a meeting timer, provides a text input for notes during the meeting, and when you stop, saves the notes with timestamp and duration to a markdown file in your Files app.',
     'published', 'public', 'low'),

    ('sc_resize', 'system_user', 'Batch Resize Photos', 'batch-resize-photos',
     'Select multiple photos and resize them to a chosen dimension.',
     'Lets you select multiple photos from your library, choose a target resolution (1080p, 720p, or custom), and resizes all of them at once. Saves the resized images to a new album.',
     'published', 'public', 'medium'),

    ('sc_wifi', 'system_user', 'Share Wi-Fi Password', 'share-wifi-password',
     'Generate a QR code for your current Wi-Fi network.',
     'Reads your current Wi-Fi network name, asks for the password, generates a QR code that others can scan to connect automatically. No need to spell out passwords.',
     'published', 'public', 'medium'),

    ('sc_expense', 'system_user', 'Quick Expense Log', 'quick-expense-log',
     'Log expenses with amount, category, and notes to a spreadsheet.',
     'A fast expense tracker that asks for amount, category (food, transport, shopping, etc.), and optional notes. Appends to a CSV file in iCloud Drive for later review.',
     'published', 'public', 'low'),

    ('sc_pomodoro', 'system_user', 'Pomodoro Timer', 'pomodoro-timer',
     'A 25-minute focus timer with break reminders.',
     'Classic Pomodoro technique: 25 minutes of focused work, then a 5-minute break. After 4 cycles, take a longer 15-minute break. Plays a sound when each phase ends.',
     'published', 'public', 'low'),

    ('sc_clipboard', 'system_user', 'Clipboard Manager', 'clipboard-manager',
     'Save and recall clipboard history from a menu.',
     'Saves your clipboard contents to a local list. When triggered, shows a menu of recent items you can paste back. Supports text and URLs.',
     'published', 'public', 'medium'),

    ('sc_translate', 'system_user', 'Quick Translate', 'quick-translate',
     'Translate selected text or clipboard to your chosen language.',
     'Takes text from your clipboard or share sheet, detects the source language, and translates it to your preferred target language using the built-in translation API.',
     'published', 'public', 'low'),

    ('sc_workout', 'system_user', 'Workout Logger', 'workout-logger',
     'Log exercises with sets, reps, and weight to Health.',
     'A gym companion that lets you pick an exercise, enter sets/reps/weight, and logs it. Tracks your workout history and can show progress over time.',
     'published', 'public', 'low'),

    ('sc_wallpaper', 'system_user', 'Daily Wallpaper', 'daily-wallpaper',
     'Set a new wallpaper from Unsplash every day.',
     'Fetches a random high-quality photo from Unsplash based on your chosen category (nature, architecture, abstract, etc.) and sets it as your wallpaper automatically.',
     'published', 'public', 'low');

-- Shortcut versions (placeholder — no actual files)
INSERT OR IGNORE INTO shortcut_versions (id, shortcut_id, version_number, source_type, signing_status)
VALUES
    ('ver_morning', 'sc_morning', 1, 'generated', 'pending'),
    ('ver_pdf', 'sc_pdf', 1, 'generated', 'pending'),
    ('ver_water', 'sc_water', 1, 'generated', 'pending'),
    ('ver_meeting', 'sc_meeting', 1, 'generated', 'pending'),
    ('ver_resize', 'sc_resize', 1, 'generated', 'pending'),
    ('ver_wifi', 'sc_wifi', 1, 'generated', 'pending'),
    ('ver_expense', 'sc_expense', 1, 'generated', 'pending'),
    ('ver_pomodoro', 'sc_pomodoro', 1, 'generated', 'pending'),
    ('ver_clipboard', 'sc_clipboard', 1, 'generated', 'pending'),
    ('ver_translate', 'sc_translate', 1, 'generated', 'pending'),
    ('ver_workout', 'sc_workout', 1, 'generated', 'pending'),
    ('ver_wallpaper', 'sc_wallpaper', 1, 'generated', 'pending');

-- Update current_version_id
UPDATE shortcuts SET current_version_id = 'ver_morning' WHERE id = 'sc_morning';
UPDATE shortcuts SET current_version_id = 'ver_pdf' WHERE id = 'sc_pdf';
UPDATE shortcuts SET current_version_id = 'ver_water' WHERE id = 'sc_water';
UPDATE shortcuts SET current_version_id = 'ver_meeting' WHERE id = 'sc_meeting';
UPDATE shortcuts SET current_version_id = 'ver_resize' WHERE id = 'sc_resize';
UPDATE shortcuts SET current_version_id = 'ver_wifi' WHERE id = 'sc_wifi';
UPDATE shortcuts SET current_version_id = 'ver_expense' WHERE id = 'sc_expense';
UPDATE shortcuts SET current_version_id = 'ver_pomodoro' WHERE id = 'sc_pomodoro';
UPDATE shortcuts SET current_version_id = 'ver_clipboard' WHERE id = 'sc_clipboard';
UPDATE shortcuts SET current_version_id = 'ver_translate' WHERE id = 'sc_translate';
UPDATE shortcuts SET current_version_id = 'ver_workout' WHERE id = 'sc_workout';
UPDATE shortcuts SET current_version_id = 'ver_wallpaper' WHERE id = 'sc_wallpaper';

-- Community posts
INSERT OR IGNORE INTO community_posts (id, shortcut_id, category, featured, rank_score)
VALUES
    ('cp_morning', 'sc_morning', 'productivity', 1, 95.0),
    ('cp_pdf', 'sc_pdf', 'utility', 1, 90.0),
    ('cp_water', 'sc_water', 'health', 0, 85.0),
    ('cp_meeting', 'sc_meeting', 'productivity', 1, 88.0),
    ('cp_resize', 'sc_resize', 'media', 0, 82.0),
    ('cp_wifi', 'sc_wifi', 'utility', 1, 92.0),
    ('cp_expense', 'sc_expense', 'finance', 0, 80.0),
    ('cp_pomodoro', 'sc_pomodoro', 'productivity', 0, 87.0),
    ('cp_clipboard', 'sc_clipboard', 'utility', 0, 78.0),
    ('cp_translate', 'sc_translate', 'utility', 0, 83.0),
    ('cp_workout', 'sc_workout', 'health', 0, 76.0),
    ('cp_wallpaper', 'sc_wallpaper', 'fun', 0, 74.0);

-- Tag associations
INSERT OR IGNORE INTO shortcut_tags (shortcut_id, tag_id) VALUES
    ('sc_morning', 'tag_productivity'),
    ('sc_morning', 'tag_automation'),
    ('sc_pdf', 'tag_utility'),
    ('sc_pdf', 'tag_productivity'),
    ('sc_water', 'tag_health'),
    ('sc_meeting', 'tag_productivity'),
    ('sc_resize', 'tag_media'),
    ('sc_resize', 'tag_utility'),
    ('sc_wifi', 'tag_utility'),
    ('sc_wifi', 'tag_social'),
    ('sc_expense', 'tag_finance'),
    ('sc_expense', 'tag_productivity'),
    ('sc_pomodoro', 'tag_productivity'),
    ('sc_clipboard', 'tag_utility'),
    ('sc_clipboard', 'tag_developer'),
    ('sc_translate', 'tag_utility'),
    ('sc_translate', 'tag_education'),
    ('sc_workout', 'tag_health'),
    ('sc_wallpaper', 'tag_fun'),
    ('sc_wallpaper', 'tag_media');

-- Set some download/like counts for realism
UPDATE shortcuts SET download_count = 1247, like_count = 89, favorite_count = 45 WHERE id = 'sc_morning';
UPDATE shortcuts SET download_count = 2103, like_count = 156, favorite_count = 78 WHERE id = 'sc_pdf';
UPDATE shortcuts SET download_count = 876, like_count = 67, favorite_count = 34 WHERE id = 'sc_water';
UPDATE shortcuts SET download_count = 654, like_count = 48, favorite_count = 22 WHERE id = 'sc_meeting';
UPDATE shortcuts SET download_count = 1532, like_count = 112, favorite_count = 55 WHERE id = 'sc_resize';
UPDATE shortcuts SET download_count = 3210, like_count = 234, favorite_count = 120 WHERE id = 'sc_wifi';
UPDATE shortcuts SET download_count = 445, like_count = 31, favorite_count = 15 WHERE id = 'sc_expense';
UPDATE shortcuts SET download_count = 987, like_count = 76, favorite_count = 38 WHERE id = 'sc_pomodoro';
UPDATE shortcuts SET download_count = 321, like_count = 23, favorite_count = 11 WHERE id = 'sc_clipboard';
UPDATE shortcuts SET download_count = 1876, like_count = 134, favorite_count = 67 WHERE id = 'sc_translate';
UPDATE shortcuts SET download_count = 234, like_count = 18, favorite_count = 9 WHERE id = 'sc_workout';
UPDATE shortcuts SET download_count = 567, like_count = 42, favorite_count = 21 WHERE id = 'sc_wallpaper';
