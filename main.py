from playwright.sync_api import sync_playwright
import time

DESIRED_POSTS = 50
# ⚠️ THAY ĐỔI URL NÀY THÀNH URL NHÓM FACEBOOK CỦA BẠN
GROUP_URL = "https://www.facebook.com/groups/YOUR_GROUP_ID_HERE"
OUTPUT_FILE = "fb_posts_output.txt"
STORAGE_STATE = "facebook_state.json"
MAX_SCROLLS   = 30    # safety limit

def run_scraper():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        ctx = browser.new_context(storage_state=STORAGE_STATE)
        page = ctx.new_page()

        print("🔄 Navigating to group...")
        page.goto(GROUP_URL)
        time.sleep(5)  # wait a bit for feed to load

        posts = []
        scrolls = 0
        processed_posts = set()  # track processed posts by their text content

        # keep scrolling until we have DESIRED_POSTS or reach MAX_SCROLLS
        while len(posts) < DESIRED_POSTS and scrolls < MAX_SCROLLS:
            scrolls += 1
            print(f"📜 Scroll {scrolls}/{MAX_SCROLLS}…")

            # scroll the entire page
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            time.sleep(2)  # wait a bit for new content

            # click all "See more" buttons in the feed
            more_buttons = page.locator("text='Xem thêm'")
            for i in range(more_buttons.count()):
                try:
                    more_buttons.nth(i).click(timeout=500)
                except:
                    pass
            time.sleep(1)

            # find all story_message divs
            elems = page.locator("div[data-ad-rendering-role='story_message']")
            count = elems.count()
            print(f"   → {count} elements found in DOM")

            # process all elements and check for new posts
            for i in range(count):
                try:
                    text = elems.nth(i).inner_text().strip()
                    if text and text not in processed_posts:
                        posts.append(text)
                        processed_posts.add(text)
                        print(f"   ✓ Post #{len(posts)} loaded")
                        if len(posts) >= DESIRED_POSTS:
                            break
                except Exception as e:
                    print(f"   ⚠️ Error processing element {i}: {e}")
                    continue

            # If no new posts found in this scroll, wait a bit more
            if len(posts) < DESIRED_POSTS:
                time.sleep(1)

        # write results to file
        print(f"✅ Total {len(posts)} posts found. Saving…")
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            for idx, ptext in enumerate(posts[:DESIRED_POSTS], 1):
                f.write(f"--- POST {idx} ---\n{ptext}\n\n")

        browser.close()
        print(f"📁 Done! Check {OUTPUT_FILE}")

if __name__ == "__main__":
    run_scraper()
