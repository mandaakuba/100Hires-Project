import os
import re
from dotenv import load_dotenv
from apify_client import ApifyClient

# 1. Load API Key dari file .env
load_dotenv()
APIFY_TOKEN = os.getenv('APIFY_API_TOKEN')

# Validasi keamanan token
if not APIFY_TOKEN:
    print("ERROR: APIFY_API_TOKEN tidak ditemukan di file .env!")
    exit()

# Inisialisasi client Apify
client = ApifyClient(APIFY_TOKEN)

def scrape_linkedin_posts(linkedin_url, author_name):
    print(f"Memulai misi scraping LinkedIn untuk: {author_name}...")
    
    # 2. Setup Input untuk Actor Apify ('supreme_coder/linkedin-post')
    run_input = {
        "urls": [linkedin_url],
        "limitPerSource": 5 # Ambil 5 post terakhir
    }

    try:
        # 3. Panggil Actor Apify
        print("Sedang memproses di server Apify menggunakan 'supreme_coder'. Harap tunggu 1-2 menit...")
        run = client.actor("supreme_coder/linkedin-post").call(run_input=run_input)
        
        # 4. Siapkan format nama file dan pastikan masuk ke folder yang benar
        clean_author = re.sub(r'[\\/*?:"<>|]', "", author_name)
        filename = f"{clean_author.replace(' ', '_').lower()}_linkedin_posts.md"
        filepath = os.path.join("research", "linkedin-posts", filename)
        
        # 5. Tarik hasil dari dataset Apify dan simpan ke Markdown
        with open(filepath, "w", encoding="utf-8") as file:
            file.write(f"# Recent LinkedIn Posts: {author_name}\n\n")
            file.write(f"**Source URL:** {linkedin_url}\n\n")
            file.write("---\n\n")
            
            # Kita loop setiap data yang dikembalikan oleh scraper
            for item in client.dataset(run["defaultDatasetId"]).iterate_items():
                # --- LOGIC PEMBERSIHAN DATA ---
                # Mencari Teks Utama: Mengambil atribut 'text' atau 'postContent'.
                post_text = item.get('text', item.get('postContent', ''))
                
                # Seringkali scraper mengembalikan list of comments di dalam atribut 'text' jika salah parsing,
                # jadi kita harus pastikan kita memisahkan teks utama.
                # Pada scraper supreme_coder, teks utamanya kadang ada di atribut 'text' 
                # sedangkan komentarnya ada di atribut 'comments'. Kita abaikan 'comments' sepenuhnya.
                
                # Membersihkan dictionary/list yang ikut terbawa menjadi string
                if isinstance(post_text, list) or isinstance(post_text, dict):
                     # Kalau dia nge-dump list, kita skip aja atau ambil item pertama kalau itu string
                     continue
                
                # Mengambil metrics
                likes = item.get('likes', item.get('numLikes', item.get('likeCount', 0)))
                # Karena kadang 'comments' itu isinya list orang komentar, kita ambil panjang list-nya saja untuk metrik
                comments_data = item.get('comments', [])
                comments_count = len(comments_data) if isinstance(comments_data, list) else item.get('numComments', 0)
                
                date = item.get('postedAt', item.get('date', item.get('publishedAt', 'Unknown Date')))
                
                # --- FORMAT PENULISAN BERSIH ---
                if str(post_text).strip(): # Pastikan teks tidak kosong
                    file.write(f"### Posted on: {date}\n")
                    file.write(f"**Engagement:** 👍 {likes} Likes | 💬 {comments_count} Comments\n\n")
                    file.write(f"{post_text}\n\n")
                    file.write("---\n\n")
                
        print(f"Sukses! Data tersimpan dengan BERSIH di: {filepath}")

    except Exception as e:
        print(f"Gagal mengeksekusi script. Error detail: {e}")

# --- CARA PENGGUNAAN ---
if __name__ == "__main__":
    # Masukkan URL profil LinkedIn expert
    scrape_linkedin_posts(
        linkedin_url="https://www.linkedin.com/in/bernardjhuang/", 
        author_name="Bernard Huang"
    )