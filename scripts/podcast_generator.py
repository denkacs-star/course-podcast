#!/usr/bin/env python3
from datetime import datetime, timezone

# Einfacher statischer Test-Feed
rss_content = '''<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
<channel>
    <title>Course Edu Podcast</title>
    <link>https://youtube.com/@course_edu</link>
    <description>Test podcast feed</description>
    <item>
        <title>Test Episode 1</title>
        <enclosure url="https://example.com/audio1.mp3" type="audio/mpeg"/>
    </item>
    <item>
        <title>Test Episode 2</title>
        <enclosure url="https://example.com/audio2.mp3" type="audio/mpeg"/>
    </item>
</channel>
</rss>'''

with open('feed.rss', 'w') as f:
    f.write(rss_content)

print("✅ Simple RSS feed generated")
