import requests
import os
import re  
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('SUPADATA_API_KEY')

def get_transcript(youtube_url, author_name, video_title):
    endpoint = "https://api.supadata.ai/v1/youtube/transcript"
    
    headers = {
        "x-api-key": API_KEY
    }
    
    params = {
        "url": youtube_url,
        "text": "true" 
    }

    print(f"Get the transcript for {author_name} - {video_title}...")
    
    response = requests.get(endpoint, headers=headers, params=params)
    
    if response.status_code == 200:
        data = response.json()
        transcript_text = data.get("content", "")
        
        clean_title = re.sub(r'[\\/*?:"<>|]', "", video_title)
        clean_author = re.sub(r'[\\/*?:"<>|]', "", author_name)
    
        filename = f"{clean_author.replace(' ', '_').lower()}_{clean_title.replace(' ', '_').lower()}.md"
        filepath = os.path.join("research", "youtube-transcripts", filename)
        
        with open(filepath, "w", encoding="utf-8") as file:
            file.write(f"# {author_name} - {video_title}\n\n")
            file.write(f"**Source URL:** {youtube_url}\n\n")
            file.write("---\n\n")
            file.write(transcript_text)
            
        print(f"Success! Saved to: {filepath}")
    else:
        print(f"failed to get the transcript. Error: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    get_transcript(
        youtube_url="https://www.youtube.com/watch?v=gReszNnykpg", 
        author_name="Ahrefs", 
        video_title="The New SEO Playbook for AI Search (Top GEO Ranking Factors)"
    )