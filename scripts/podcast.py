#!/usr/bin/env python3
import yt_dlp
from datetime import datetime, timezone

CHANNEL_URL = "https://www.youtube.com/@course_edu"

def generate_rss():
    """Simple working RSS generator"""
    try:
        print("🔄 Fetching videos from YouTube...")
        
        ydl_opts = {
            'quiet': False,
            'extract_flat': True,
        }
        
        # KORREKT: yt_dlp verwenden
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(CHANNEL_URL, download=False)
            videos = info.get('entries', [])[:10]
        
        print(f"✅ Found {len(videos)} videos")
        
        # RSS Feed erstellen
        rss = f'''<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
<channel>
    <title>Course Edu Podcast</title>
    <link>https://youtube.com/@course_edu</link>
    <description>Course Edu YouTube videos as podcast</description>
    <language>de</language>
    <lastBuildDate>{datetime.now(timezone.utc).strftime('%a, %d %b %Y %H:%M:%S GMT')}</lastBuildDate>
'''
        
        for video in videos:
            video_id = video.get('id')
            title = video.get('title', 'Unbekannt')
            # XML-sichere Zeichen ersetzen
            safe_title = title.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            
            rss += f'''
    <item>
        <title>{safe_title}</title>
        <enclosure url="https://www.youtube.com/watch?v={video_id}" type="audio/mpeg" length="0"/>
        <link>https://www.youtube.com/watch?v={video_id}</link>
        <guid>https://www.youtube.com/watch?v={video_id}</guid>
        <pubDate>{datetime.now(timezone.utc).strftime('%a, %d %b %Y %H:%M:%S GMT')}</pubDate>
    </item>
'''
        
        rss += '</channel>\n</rss>'
        
        with open('feed.rss', 'w', encoding='utf-8') as f:
            f.write(rss)
        
        print(f"🎉 RSS feed generated with {len(videos)} episodes")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        # Fallback feed
        with open('feed.rss', 'w') as f:
            f.write('''<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
<channel>
    <title>Course Edu Podcast</title>
    <description>Error occurred</description>
</channel>
</rss>''')

if __name__ == "__main__":
    generate_rss()
