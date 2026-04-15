import os
import re
from dotenv import load_dotenv
from apify_client import ApifyClient

load_dotenv()
APIFY_TOKEN = os.getenv('APIFY_API_TOKEN')
if not APIFY_TOKEN:
    print("ERROR: APIFY_API_TOKEN tidak ditemukan di file .env!")
    exit()
client = ApifyClient(APIFY_TOKEN)

def scrape_linkedin_posts(linkedin_url, author_name):
    print(f"Memulai misi scraping LinkedIn untuk: {author_name}...")

    run_input = {
        "urls": [linkedin_url],
        "limitPerSource": 5 
    }

    try:
        print("On Process")
        run = client.actor("supreme_coder/linkedin-post").call(run_input=run_input)
    
        clean_author = re.sub(r'[\\/*?:"<>|]', "", author_name)
        filename = f"{clean_author.replace(' ', '_').lower()}_linkedin_posts.md"
        filepath = os.path.join("research", "linkedin-posts", filename)
        
        with open(filepath, "w", encoding="utf-8") as file:
            file.write(f"# Recent LinkedIn Posts: {author_name}\n\n")
            file.write(f"**Source URL:** {linkedin_url}\n\n")
            file.write("---\n\n")
            
            #LOOP
            for item in client.dataset(run["defaultDatasetId"]).iterate_items():
                post_text = item.get('text', item.get('postContent', ''))
                if isinstance(post_text, list) or isinstance(post_text, dict):
                     continue

                likes = item.get('likes', item.get('numLikes', item.get('likeCount', 0)))
                comments_data = item.get('comments', [])
                comments_count = len(comments_data) if isinstance(comments_data, list) else item.get('numComments', 0)
                
                date = item.get('postedAt', item.get('date', item.get('publishedAt', 'Unknown Date')))

                if str(post_text).strip(): 
                    file.write(f"### Posted on: {date}\n")
                    file.write(f"**Engagement:** 👍 {likes} Likes | 💬 {comments_count} Comments\n\n")
                    file.write(f"{post_text}\n\n")
                    file.write("---\n\n")
                
        print(f"Succeed, saved on: {filepath}")

    except Exception as e:
        print(f"Failed. Error detail: {e}")
#changeable url n author
if __name__ == "__main__":
    scrape_linkedin_posts(
        linkedin_url="https://www.linkedin.com/in/bernardjhuang/", 
        author_name="Bernard Huang"
    )
