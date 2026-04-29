#!/usr/bin/env python3
"""
Generate a podcast RSS feed (feed.xml) from episodes.json.

Usage:
    python generate_feed.py --base-url https://yourusername.github.io/geo-course

The base URL is where your podcast files are hosted publicly.
For GitHub Pages: https://USERNAME.github.io/REPO-NAME
For Backblaze B2:  https://f000.backblazeb2.com/file/BUCKETNAME

The script reads episodes.json, looks up each MP3 file's size and duration,
and produces a feed.xml suitable for any podcast app.
"""

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from email.utils import format_datetime
from pathlib import Path
from xml.sax.saxutils import escape

try:
    import mutagen
    HAS_MUTAGEN = True
except ImportError:
    HAS_MUTAGEN = False


def get_audio_duration(filepath):
    """Return audio duration as HH:MM:SS string. Falls back to 00:23:00 if mutagen unavailable."""
    if not HAS_MUTAGEN:
        return "00:23:00"
    if not os.path.exists(filepath):
        return "00:23:00"
    try:
        audio = mutagen.File(filepath)
        total_seconds = int(audio.info.length)
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    except Exception as e:
        print(f"  Warning: could not read duration for {filepath}: {e}", file=sys.stderr)
        return "00:23:00"


def get_file_size(filepath):
    """Return file size in bytes, or 0 if file doesn't exist yet."""
    if os.path.exists(filepath):
        return os.path.getsize(filepath)
    return 0


def format_pubdate(date_str):
    """Convert YYYY-MM-DD to RFC 2822 format required by RSS."""
    dt = datetime.strptime(date_str, "%Y-%m-%d").replace(tzinfo=timezone.utc)
    return format_datetime(dt)


def generate_feed(config_path, base_url, episodes_dir):
    """Generate RSS XML and return as string."""
    with open(config_path, "r") as f:
        config = json.load(f)

    show = config["show"]
    episodes = config["episodes"]

    base_url = base_url.rstrip("/")

    # Header / channel metadata
    parts = []
    parts.append('<?xml version="1.0" encoding="UTF-8"?>')
    parts.append(
        '<rss version="2.0" '
        'xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd" '
        'xmlns:content="http://purl.org/rss/1.0/modules/content/" '
        'xmlns:atom="http://www.w3.org/2005/Atom">'
    )
    parts.append("  <channel>")
    parts.append(f"    <title>{escape(show['title'])}</title>")
    parts.append(f'    <atom:link href="{base_url}/feed.xml" rel="self" type="application/rss+xml"/>')
    parts.append(f"    <link>{base_url}</link>")
    parts.append(f"    <language>{escape(show['language'])}</language>")
    parts.append(f"    <description>{escape(show['description'])}</description>")
    parts.append(f"    <itunes:author>{escape(show['author'])}</itunes:author>")
    parts.append(f"    <itunes:summary>{escape(show['description'])}</itunes:summary>")
    parts.append(f"    <itunes:subtitle>{escape(show['subtitle'])}</itunes:subtitle>")
    parts.append(f"    <itunes:explicit>{'yes' if show['explicit'] else 'no'}</itunes:explicit>")
    parts.append(f"    <itunes:category text=\"{escape(show['category'])}\"/>")
    parts.append("    <itunes:owner>")
    parts.append(f"      <itunes:name>{escape(show['author'])}</itunes:name>")
    parts.append(f"      <itunes:email>{escape(show['email'])}</itunes:email>")
    parts.append("    </itunes:owner>")
    parts.append(f'    <itunes:image href="{base_url}/{show["image_filename"]}"/>')
    parts.append(f"    <image>")
    parts.append(f"      <url>{base_url}/{show['image_filename']}</url>")
    parts.append(f"      <title>{escape(show['title'])}</title>")
    parts.append(f"      <link>{base_url}</link>")
    parts.append(f"    </image>")

    # Episodes (newest first per RSS convention)
    for ep in sorted(episodes, key=lambda e: e["number"], reverse=True):
        mp3_path = Path(episodes_dir) / ep["filename"]
        size = get_file_size(mp3_path)
        duration = get_audio_duration(mp3_path)
        ep_url = f"{base_url}/episodes/{ep['filename']}"
        guid = f"{base_url}/episodes/{ep['slug']}"

        parts.append("    <item>")
        parts.append(f"      <title>{escape(ep['title'])}</title>")
        parts.append(f"      <description>{escape(ep['description'])}</description>")
        parts.append(f"      <itunes:summary>{escape(ep['description'])}</itunes:summary>")
        parts.append(f'      <enclosure url="{ep_url}" length="{size}" type="audio/mp4"/>')
        parts.append(f"      <guid isPermaLink=\"false\">{guid}</guid>")
        parts.append(f"      <pubDate>{format_pubdate(ep['pub_date'])}</pubDate>")
        parts.append(f"      <itunes:duration>{duration}</itunes:duration>")
        parts.append(f"      <itunes:episode>{ep['number']}</itunes:episode>")
        parts.append(f"      <itunes:episodeType>full</itunes:episodeType>")
        parts.append(f"      <itunes:explicit>no</itunes:explicit>")
        parts.append("    </item>")

    parts.append("  </channel>")
    parts.append("</rss>")
    return "\n".join(parts)


def main():
    parser = argparse.ArgumentParser(description="Generate podcast RSS feed")
    parser.add_argument(
        "--base-url",
        required=True,
        help="Public base URL where files are hosted (e.g. https://username.github.io/geo-course)",
    )
    parser.add_argument(
        "--config",
        default="episodes.json",
        help="Path to episodes config (default: episodes.json)",
    )
    parser.add_argument(
        "--episodes-dir",
        default="episodes",
        help="Path to directory containing MP3 files (default: episodes)",
    )
    parser.add_argument(
        "--output",
        default="feed.xml",
        help="Output path for feed.xml (default: feed.xml)",
    )
    args = parser.parse_args()

    if not HAS_MUTAGEN:
        print("Note: mutagen not installed. Episode durations will default to 00:23:00.")
        print("      Install with: pip install mutagen")
        print()

    feed_xml = generate_feed(args.config, args.base_url, args.episodes_dir)
    with open(args.output, "w") as f:
        f.write(feed_xml)
    print(f"Wrote {args.output}")
    print(f"Feed URL will be: {args.base_url.rstrip('/')}/feed.xml")


if __name__ == "__main__":
    main()
