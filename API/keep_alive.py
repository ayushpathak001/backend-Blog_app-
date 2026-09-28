import time
import requests


RENDER_APP_URL = "https://backend-blog-app-2-l45t.onrender.com/" 

print("⏰ Starting Render Keep-Alive monitoring script...")

while True:
    try:
        response = requests.get(RENDER_APP_URL)
        if response.status_code == 200:
            print(f"⚡ Ping successful! Server status: {response.status_code}. Keeping awake...")
        else:
            print(f"⚠️ Server responded with status: {response.status_code}")
    except Exception as e:
        print(f"❌ Failed to reach server: {e}")
    
    # Wait for 14 minutes (840 seconds) before pinging again
    time.sleep(840)
