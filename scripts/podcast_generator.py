#!/usr/bin/env python3
import yt_dlp as youtube_dl
from podgen import Podcast, Episode, Media
import os
import json
from datetime import datetime, timedelta
import hashlib

# Configuration
CHANNEL_URL = "https://www.youtube.com/@course_edu"
PODCAST_TITLE = "Course Edu Podcast"
PODCAST_DESCRIPTION = "Audio podcast generated from Course Edu YouTube channel"
PODCAST_WEBSITE = "https://denkacs-star.github.io/course-podcast/"
PODCAST_IMAGE = "https://denkacs-star.github.io/course-podcast/cover.jpg"
AUTHOR = "Course Edu"

def get_video_info():
    """Extract video information using yt-dlp"""
    ydl_opts = {
        'quiet': True,
        'extract_flat': True,
        'force_json': True,
    }
    
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            # Get channel info and videos
            info = ydl.extract_info(CHANNEL_URL, download=False)
            
            if 'entries' in info:
                return info['entries']
            else:
                return [info]
    except Exception as e:
        print(f"Error fetching videos: {e}")
        return []

def generate_audio_url(video_id):
    """Generate direct audio URL (this is a simplified approach)"""
    # Note: In practice, you might need to use a service or different method
    # This is a placeholder for the actual audio extraction
    return f"https://youtube.com/watch?v={video_id}"

def create_podcast_feed():
    """Create and update the podcast RSS feed"""
    
    # Create podcast object
    podcast = Podcast(
        name=PODCAST_TITLE,
        description=PODCAST_DESCRIPTION,
        website=PODCAST_WEBSITE,
        image=PODCAST_IMAGE,
        explicit=False,
        authors=[AUTHOR],
        language="de",
        category="Education",
    )
    
    # Get videos from channel
    videos = get_video_info()
    
    # Sort by upload date (newest first)
    videos.sort(key=lambda x: x.get('upload_date', ''), reverse=True)
    
    # Add episodes (limit to 20 most recent)
    for video in videos[:20]:
        video_id = video.get('id')
        title = video.get('title', 'Unknown Title')
        description = video.get('description', '')[:500] + "..." if len(video.get('description', '')) > 500 else video.get('description', '')
        upload_date = video.get('upload_date', '20230101')
        
        # Convert YYYYMMDD to datetime
        try:
            pub_date = datetime.strptime(upload_date, '%Y%m%d')
        except:
            pub_date = datetime.now()
        
        # Generate audio URL (simplified)
        audio_url = generate_audio_url(video_id)
        
        # Create episode
        episode = Episode(
            title=title,
            summary=description,
            media=Media(
                audio_url,
                size=0,  # Size would need to be determined
                duration=video.get('duration', 0)
            ),
            publication_date=pub_date,
            link=f"https://youtube.com/watch?v={video_id}"
        )
        
        podcast.episodes.append(episode)
    
    # Generate RSS feed
    podcast.rss_file('../feed.rss', encoding='UTF-8')
    print(f"Podcast feed updated with {len(podcast.episodes)} episodes")

if __name__ == "__main__":
    create_podcast_feed()
