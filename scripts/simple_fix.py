#!/usr/bin/env python3
import yt_dlp as youtube_dl
from datetime import datetime, timezone

CHANNEL_URL = "https://www.youtube.com/@course_edu"

def generate_basic_rss():
    """Generate a very basic but working RSS feed"""
    ydl_opts = {'quiet': False, 'extract_flat': True}
    
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(CHANNEL_URL, download=False)
        videos = info.get('entries', [])[:10]
    
    rss_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd">
<channel>
    <title>Course Edu Podcast</title>
    <description>Audio versions of Course Edu YouTube videos</description>
    <link>https://www.youtube.com/@course_edu</link>
    <language>de</language>
    <lastBuildDate>{datetime.now(timezone.utc).strftime('%a, %d %b %Y %H:%M:%S GMT')}</lastBuildDate>
    <generator>YouTube to Podcast Converter</generator>
'''
    
    for video in videos:
        video_id = video.get('id')
        title = video.get('title', 'Unknown').replace('&', '&amp;')
        
        rss_content += f'''
    <item>
        <title>{title}</title>
        <description>Audio version of YouTube video</description>
        <link>https://www.youtube.com/watch?v={video_id}</link>
        <enclosure url="https://www.youtube.com/watch?v={video_id}" type="audio/mpeg" length="0"/>
        <guid>https://www.youtube.com/watch?v={video_id}</guid>
        <pubDate>{datetime.now(timezone.utc).strftime('%a, %d %b %Y %H:%M:%S GMT')}</pubDate>
    </item>
'''
    
    rss_content += '</channel>\n</rss>'
    
    with open('feed.rss', 'w', encoding='utf-8') as f:
        f.write(rss_content)
    
    print(f"✅ Generated RSS with {len(videos)} episodes")

if __name__ == "__main__":
    generate_basic_rss()
