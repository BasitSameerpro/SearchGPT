from brave_search import Brave_SERP
from playwright.async_api import async_playwright
import requests
import asyncio
import random
import json
from inscriptis import get_text
from playwright._impl._errors import TimeoutError as PlaywrightTimeout
import re

class data():
    def __init__(self, user_agents=None):
        self.user_agents = user_agents or [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        ]
        
    def simple_get_html(self,url):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()  # Raises HTTPError for bad responses
            return response.text
        except requests.RequestException as e:
            print(f"[Request Failed] {e}")
            return None

    async def get_html(self,url):
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(
                user_agent = random.choice(self.user_agents),
                viewport = {'width':1920,'height':1080},
                java_script_enabled = True
            )
            async def block_resources(route, request):
                if request.resource_type in ["image", "stylesheet", "font"]:
                    await route.abort()
                else:
                    await route.continue_()

            await context.route("**/*", block_resources)
            await context.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
              get: () => undefined
            });
            Object.defineProperty(navigator, 'languages', {
              get: () => ['en-US', 'en']
            });
            Object.defineProperty(navigator, 'plugins', {
              get: () => [1, 2, 3, 4, 5]
            });
            window.chrome = {
              runtime: {}
            };
            """)
            page = await context.new_page()
            try:
                await page.goto(url, wait_until="domcontentloaded", timeout=30_000)
                await asyncio.sleep(2)
                content = await page.content()
            except PlaywrightTimeout:
                print(f"[Timeout] {url} (skipping)")
                content = ""
            except Exception as e:
                print(f"[Playwright error] {url}: {e}")
                content = ""
            finally:
                await browser.close()

        # always return a string (possibly empty) 
        return content
        
    def get_clean_text(self, html):
        text = get_text(html)  # strip HTML tags
        text = re.sub(r'\n\s*\n+', ' ', text)  # collapse multiple newlines
        text = re.sub(r'[ \t]+', ' ', text)       # collapse multiple spaces
        text = text.strip()                       # trim leading/trailing whitespace
        return text
        
    def remove_noise_blocks(self, text: str) -> str:
        lines = text.splitlines()
        cleaned = []
        for line in lines:
            if line.strip() == "":
                continue
            # Skip nav/footer menu patterns (optional heuristics)
            if line.lower().startswith(("about", "terms", "contact", "advertise")):
                continue
            cleaned.append(line)
        return "\n".join(cleaned)
    
    def need_playwright(self, html) -> bool:
        if not html or len(html) < 5000:
            return True
        keywords = ['<article', '<main', '<section', '<div', '<p', '<h1', 'content', 'Copyright']
        tag_score = sum(1 for k in keywords if k in html.lower())

        # If many scripts and very few content tags, it's likely JS-heavy
        script_count = html.lower().count('<script')
        if tag_score < 3 or script_count > 30:
            return True
        return False
    
    async def run(self,url) -> str:
        print(f"Fetching: {url}")
        html = self.simple_get_html(url)
        
        if html:
            print(f"[✓] Got HTML from simple request, length: {len(html)}")
        else:
            print("[!] Simple request failed or returned empty.")

        if self.need_playwright(html):
            print("[→] Falling back to Playwright...")
            html = await self.get_html(url)
            if html:
                print(f"[✓] Got HTML from Playwright, length: {len(html)}")
            else:
                print("[✗] Playwright failed too.")
        
        try:
            if not html:
                raise Exception("No HTML content to process")
        except:
            return ""

        text = self.get_clean_text(html)
        text = self.remove_noise_blocks(text)
        return text

    
# Run it with asyncio
async def main():
    try:
        d = data()
        text = await d.run('https://research.ibm.com/blog/what-are-ai-agents-llm')
        print(text)
    except Exception as e:
        print(f"Error occured {e}")

if __name__=='__main__':
    asyncio.run(main())