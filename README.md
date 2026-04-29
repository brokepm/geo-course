# Geo Intelligence Course — Private Podcast Feed

This repo hosts a private podcast feed using GitHub Pages. It contains:

- 13 audio episodes (~5 hours total)
- An RSS feed that any podcast app can subscribe to
- The cover artwork

## How to subscribe (for listeners)

Send your friends one URL: `https://YOUR-USERNAME.github.io/REPO-NAME/feed.xml`

They subscribe in their podcast app of choice:

**Apple Podcasts (iPhone):** Library tab → three-dot menu (top right) → "Follow a Show by URL" → paste the URL → Follow.

**Apple Podcasts (Mac):** File menu → "Follow a Show by URL..." → paste the URL.

**Pocket Casts:** Profile → Settings → Import & Export → "Add Podcast by URL" → paste.

**Overcast:** Add Podcast (+) → "Add URL" → paste.

The course will appear like any other podcast subscription with all 13 episodes, cover art, and full position retention.

## Setup (one-time, ~30 minutes)

### Prerequisites

- A GitHub account (free, no payment method required)
- Python 3.7+ installed locally
- Git installed locally
- Your 13 MP3 files
- The cover art image (cover.png)

### Step 1: Create a GitHub repository

1. Go to github.com → New repository
2. Name it something like `geo-course` (or whatever you want — this becomes part of your feed URL)
3. **Make it public** (required for free GitHub Pages)
4. Initialize with a README — this just gives you something to start with

### Step 2: Clone the repo locally

```bash
git clone https://github.com/YOUR-USERNAME/geo-course.git
cd geo-course
```

### Step 3: Drop in the starter files

Copy these files into the repo root:
- `episodes.json` (edit the show metadata first — see below)
- `generate_feed.py`
- `cover.png` (your podcast artwork, 1400×1400 minimum)
- `episodes/` directory containing your MP3 files

### Step 4: Edit episodes.json

Open `episodes.json` and replace these placeholders:
- `REPLACE_WITH_YOUR_NAME_OR_INITIALS` — appears as the show author
- `REPLACE_WITH_YOUR_EMAIL` — required by podcast apps; use any email you control
- Adjust episode descriptions if you want
- Update `pub_date` values (one per episode — keep them sequential by date)

### Step 5: Install Python dependency for accurate durations

```bash
pip install mutagen
```

This lets the feed generator read actual MP3 durations. Without it, it defaults to 23 minutes per episode (close enough, but not exact).

### Step 6: Generate the RSS feed

```bash
python generate_feed.py --base-url https://YOUR-USERNAME.github.io/geo-course
```

This produces `feed.xml` in the repo root. Replace `YOUR-USERNAME` and `geo-course` with your actual GitHub username and repo name.

### Step 7: Enable GitHub Pages

1. In your GitHub repo, go to Settings → Pages
2. Under "Source," select **Deploy from a branch**
3. Select branch **main** and folder **/ (root)**
4. Click Save
5. Wait 1-2 minutes for the first deploy

Your URL will be `https://YOUR-USERNAME.github.io/geo-course`.

### Step 8: Commit and push

```bash
git add .
git commit -m "Initial podcast feed"
git push
```

GitHub Pages will deploy automatically. Wait 1-2 minutes.

### Step 9: Test the feed

In your phone's podcast app, follow the subscription instructions at the top of this README using your real URL. Verify:
- The show appears with cover art
- All 13 episodes are listed (or however many you've uploaded)
- An episode plays correctly
- After pausing, position is retained when you reopen the app

### Step 10: Share with your friends

Send them the feed URL plus the subscription instructions from the top of this README.

## Adding new episodes later

When you generate a new MP3:

1. Copy it to `episodes/` with the filename matching `episodes.json` (e.g., `episodes/05-data-layer.mp3`)
2. Regenerate the feed: `python generate_feed.py --base-url https://YOUR-USERNAME.github.io/geo-course`
3. Commit and push:
   ```bash
   git add episodes/05-data-layer.mp3 feed.xml
   git commit -m "Add Module 05"
   git push
   ```
4. Subscribers see the new episode within a few hours (Apple Podcasts caches feeds; Pocket Casts and Overcast refresh more aggressively)

## File size considerations

GitHub has limits:
- Individual files up to 100 MB without warnings
- Files up to 100 MB hard limit on regular Git
- Repo size soft limit of 1 GB, hard limit of 5 GB
- GitHub Pages bandwidth soft limit of 100 GB/month

For 13 MP3s of roughly 23 minutes each at standard podcast quality (128 kbps), you'll have files around 20-25 MB each. Total repo size around 300 MB. You're well within limits.

If any individual MP3 exceeds 100 MB:
1. Re-encode at lower bitrate (96 kbps is fine for speech): `ffmpeg -i input.wav -codec:a libmp3lame -b:a 96k output.mp3`
2. Or use Git LFS (more complex setup, not covered here)

## Privacy notes

The repo is public, which means:
- The repository URL is technically discoverable on GitHub
- The MP3 files themselves are accessible via direct URLs
- The feed URL is the only way someone would actually subscribe and listen
- There's no podcast directory listing, no search engine indexes podcast feeds in this way
- Practically: only people you send the URL to will find this

For a learning course shared with two friends, this is genuinely private enough. If you ever need to revoke access, delete the repo — all URLs immediately stop working.

## Troubleshooting

**Feed doesn't validate / podcast app rejects it:**
Test your feed at https://castfeedvalidator.com/ — paste your feed URL, fix any errors it reports.

**Episodes don't appear:**
Make sure MP3 filenames in `episodes/` exactly match the `filename` field in `episodes.json`.

**Cover art doesn't show:**
Ensure `cover.png` is at least 1400×1400 pixels and located at the repo root.

**Apple Podcasts shows old data:**
Apple caches feeds for hours. Force refresh by pulling down on the episode list. New episodes typically appear within 24 hours.

**Want to update episode descriptions later:**
Edit `episodes.json`, regenerate `feed.xml`, commit and push. Subscribers see updates on next refresh.
