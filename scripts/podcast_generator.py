#!/usr/bin/env python3
import yt_dlp as youtube_dl
from podgen import Podcast, Episode, Media, Category
from datetime import datetime
import os

# Configuration
CHANNEL_URL = "https://www.youtube.com/@course_edu"
PODCAST_TITLE = "Course Edu Podcast"
PODCAST_DESCRIPTION = "Audio podcast generated from Course Edu YouTube channel"
PODCAST_WEBSITE = "https://denkacs-star.github.io/course-podcast/"
AUTHOR = "Course Edu"

def get_video_info():
    """Extract video information using yt-dlp"""
    ydl_opts = {
        'quiet': True,
        'extract_flat': True,
    }
    
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(CHANNEL_URL, download=False)
            if 'entries' in info:
                return info['entries'][:15]  # Nur die 15 neuesten Videos
            else:
                return [info]
    except Exception as e:
        print(f"Error fetching videos: {e}")
        return []

def create_podcast_feed():
    """Create and update the podcast RSS feed"""
    
    podcast = Podcast(
        name=PODCAST_TITLE,
        description=PODCAST_DESCRIPTION,
        website=PODCAST_WEBSITE,
        explicit=False,
        authors=[AUTHOR],
        language="de",
        category=Category("Education"),  # Korrigierte Kategorie
    )
    
    videos = get_video_info()
    
    print(f"Found {len(videos)} videos")
    
    for video in videos:
        video_id = video.get('id')
        title = video.get('title', 'Unknown Title')
        description = video.get('description', '')[:200] + "..." if video.get('description') else ""
        duration = video.get('duration', 0)
        
        # YouTube URL für Audio
        audio_url = f"https://www.youtube.com/watch?v={video_id}"
        
        # Upload-Datum verarbeiten
        upload_date = video.get('upload_date', '')
        if upload_date:
            try:
                pub_date = datetime.strptime(upload_date, '%Y%m%d')
            except:
                pub_date = datetime.now()
        else:
            pub_date = datetime.now()
        
        try:
            episode = Episode(
                title=title,
                summary=description,
                media=Media(audio_url, duration=duration),
                publication_date=pub_date,
                link=audio_url
            )
            
            podcast.episodes.append(episode)
            print(f"✅ Added episode: {title}")
        except Exception as e:
            print(f"❌ Error adding episode {title}: {e}")
    
    # RSS Feed generieren
    try:
        podcast.rss_file('feed.rss', encoding='UTF-8')
        print(f"✅ Success! Podcast feed generated with {len(podcast.episodes)} episodes")
    except Exception as e:
        print(f"❌ Error generating RSS feed: {e}")

if __name__ == "__main__":
    create_podcast_feed()
