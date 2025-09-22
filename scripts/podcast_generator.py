#!/usr/bin/env python3
import yt_dlp as youtube_dl
from datetime import datetime, timezone

def generate_rss():
    """Simple working RSS generator"""
    ydl_opts = {'quiet': False, 'extract_flat': True}
    
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info("https://www.youtube.com/@course_edu", download=False)
        videos = info.get('entries', [])[:10]
    
    rss = f'''<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
<channel>
    <title>Course Edu Podcast</title>
    <link>https://www.youtube.com/@course_edu</link>
    <description>Course Edu YouTube videos as podcast</description>
    <language>de</language>
'''
    
    for video in videos:
        video_id = video.get('id')
        title = video.get('title', 'Video').replace('&', '&amp;')
        
        rss += f'''
    <item>
        <title>{title}</title>
        <enclosure url="https://www.youtube.com/watch?v={video_id}" type="audio/mpeg"/>
        <link>https://www.youtube.com/watch?v={video_id}</link>
        <guid>https://www.youtube.com/watch?v={video_id}</guid>
    </item>
'''
    
    rss += '</channel>\n</rss>'
    
    with open('feed.rss', 'w', encoding='utf-8') as f:
        f.write(rss)
    
    print(f"Generated feed with {len(videos)} episodes")

if __name__ == "__main__":
    generate_rss()
