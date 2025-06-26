# login_and_save_state.py

from playwright.sync_api import sync_playwright

STATE_FILE = "facebook_state.json"

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        print("🌐 Opening Facebook login page...")
        page.goto("https://www.facebook.com")

        input("⏳ Log in to Facebook manually, then press Enter here to continue...")

        print(f"💾 Saving session to '{STATE_FILE}'")
        context.storage_state(path=STATE_FILE)
        browser.close()

        print("✅ Login state saved. You can now run main.py using this session.")

if __name__ == "__main__":
    main()
    
