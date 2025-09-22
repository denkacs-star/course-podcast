#!/usr/bin/env python3
import yt_dlp as youtube_dl
from datetime import datetime, timezone
import xml.etree.ElementTree as ET
from xml.dom import minidom

CHANNEL_URL = "https://www.youtube.com/@course_edu"

def get_videos():
    """Get videos from YouTube channel with better error handling"""
    ydl_opts = {
        'quiet': False,  # Debug output anzeigen
        'extract_flat': True,
        'force_json': True,
    }
    
    try:
        print("🔄 Fetching videos from YouTube...")
        with youtube_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(CHANNEL_URL, download=False)
            videos = info.get('entries', [])
            print(f"✅ Found {len(videos)} videos")
            
            # Debug: Erste 3 Videos anzeigen
            for i, video in enumerate(videos[:3]):
                print(f"Video {i+1}: {video.get('title', 'No title')}")
                
            return videos[:20]  # Limit to 20 newest
        
    except Exception as e:
        print(f"❌ Error fetching videos: {e}")
        return []

def generate_rss():
    """Generate proper RSS feed"""
    videos = get_videos()
    
    if not videos:
        print("❌ No videos found, creating empty feed")
        # Fallback: Leeren Feed erstellen
        videos = []

    # RSS Root mit korrekten Namespaces
    rss = ET.Element('rss', {
        'version': '2.0',
        'xmlns:itunes': 'http://www.itunes.com/dtds/podcast-1.0.dtd',
        'xmlns:content': 'http://purl.org/rss/1.0/modules/content/'
    })
    
    channel = ET.SubElement(rss, 'channel')
    
    # Channel info
    ET.SubElement(channel, 'title').text = "Course Edu Podcast"
    ET.SubElement(channel, 'description').text = "Audio podcast from Course Edu YouTube channel"
    ET.SubElement(channel, 'link').text = "https://www.youtube.com/@course_edu"
    ET.SubElement(channel, 'language').text = "de-DE"
    ET.SubElement(channel, 'generator').text = "YouTube to Podcast Converter"
    ET.SubElement(channel, 'lastBuildDate').text = datetime.now(timezone.utc).strftime('%a, %d %b %Y %H:%M:%S GMT')
    
    # Add episodes
    for video in videos:
        video_id = video.get('id')
        title = video.get('title', 'Unknown Title')
        description = video.get('description', '')[:500] or "No description available"
        
        # Upload date verarbeiten
        upload_date = video.get('upload_date', '')
        if upload_date:
            try:
                pub_date = datetime.strptime(upload_date, '%Y%m%d').strftime('%a, %d %b %Y 12:00:00 GMT')
            except:
                pub_date = datetime.now(timezone.utc).strftime('%a, %d %b %Y %H:%M:%S GMT')
        else:
            pub_date = datetime.now(timezone.utc).strftime('%a, %d %b %Y %H:%M:%S GMT')
        
        item = ET.SubElement(channel, 'item')
        ET.SubElement(item, 'title').text = title
        ET.SubElement(item, 'description').text = description
        
        # GUID muss unique sein
        ET.SubElement(item, 'guid', {'isPermaLink': 'true'}).text = f"https://www.youtube.com/watch?v={video_id}"
        
        ET.SubElement(item, 'link').text = f"https://www.youtube.com/watch?v={video_id}"
        ET.SubElement(item, 'pubDate').text = pubDate
        
        # Enclosure - wichtig für Podcast Apps
        # Hier verwenden wir die YouTube URL als Platzhalter
        enclosure = ET.SubElement(item, 'enclosure', {
            'url': f"https://www.youtube.com/watch?v={video_id}",
            'type': 'audio/mpeg',
            'length': '0'
        })
        
        print(f"✅ Added episode: {title}")
    
    # XML speichern
    rough_string = ET.tostring(rss, encoding='utf-8')
    reparsed = minidom.parseString(rough_string)
    pretty_xml = reparsed.toprettyxml(indent="  ", encoding='utf-8')
    
    with open('feed.rss', 'wb') as f:
        f.write(pretty_xml)
    
    print(f"🎉 RSS feed generated with {len(videos)} episodes")

if __name__ == "__main__":
    generate_rss()
