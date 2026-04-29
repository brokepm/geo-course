# Claude Code instructions for this repo

This repo hosts a private podcast feed via GitHub Pages. The owner is using Claude Code to add new episodes, regenerate the feed, and push updates.

## Files in this repo

- `episodes.json` — metadata for all 13 episodes (titles, descriptions, filenames, pub dates)
- `generate_feed.py` — script that produces `feed.xml` from `episodes.json`
- `feed.xml` — the generated RSS feed (do not edit by hand)
- `cover.png` — podcast artwork
- `episodes/` — directory containing all MP3 files
- `README.md` — full setup and usage docs

## Common tasks the user may ask for

### "Add a new episode"
1. Confirm the MP3 filename matches the `filename` field in `episodes.json`
2. If the episode isn't yet in `episodes.json`, ask the user for title, description, and pub date, then add it
3. Run `python generate_feed.py --base-url <BASE_URL>` to regenerate `feed.xml`
4. Run `git add . && git commit -m "Add Module XX" && git push`

### "Regenerate the feed"
Run `python generate_feed.py --base-url <BASE_URL>`. The base URL is in the repo's GitHub Pages settings; check `feed.xml` if unsure — the existing URL is in the `<atom:link>` tag.

### "Update show or episode metadata"
Edit `episodes.json`, then regenerate `feed.xml`, commit, push.

## Hard rules

- Never edit `feed.xml` directly. Always regenerate from `episodes.json`.
- Never delete MP3 files without explicit user confirmation — they're the actual content.
- Always commit and push after regenerating the feed, so subscribers see updates.
- If the user asks to make the repo private, warn them: GitHub Pages requires public repos on the free tier, so making it private will break the feed. They'd need to migrate hosting.
