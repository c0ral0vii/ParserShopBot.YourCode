from typing import Any, Dict, List, Optional
from playwright.async_api import async_playwright
import asyncio
import random

class BrowserService:
    def __init__(self):
        self.browser = None
        self.page = None
        self.context = None
        
    async def find_item(self, url: str) -> Dict[str, Any]:
        """Найти цены на странице"""
        try:
            async with async_playwright() as p:
                # Запускаем браузер
                self.browser = await p.firefox.launch(
                    headless=True,
                )
                
                # Создаем новый контекст
                self.context = await self.browser.new_context(
                    viewport=None,
                    user_agent=self._generate_user_agent(),
                    extra_http_headers={
                        'Accept-Language': 'en-US,en;q=0.9',
                    }
                )
                
                self.page = await self.context.new_page()
                await self.page.goto(url, timeout=60000)
                
                await self.page.wait_for_selector("h1.Ty")
                
                title_element = await self.page.query_selector("h1.Ty")
                price_elements = await self.page.query_selector_all("div.TC")
                img_element = await self.page.query_selector("img.ql")
                
                size_elements = await self.page.query_selector_all("div.Vu")
                price_elements = await self.page.query_selector_all("div.Vv")
                
                sizes_prices = []
                for size_el, price_el in zip(size_elements, price_elements):
                    size = await size_el.text_content()
                    price = await price_el.text_content()
                    if size and price:
                        sizes_prices.append({
                            "size": size.strip(),
                            "price": price.strip()
                        })
                
                valid_sizes_prices = [
                    item for item in sizes_prices 
                    if item["price"] and not item["price"].startswith("$--")
                ]
                
                prices = []
                for element in price_elements:
                    price_text = await element.text_content()
                    if price_text:
                        prices.append(price_text.strip())
                
                data = {
                    "title_img": await img_element.get_attribute('src') if img_element else None,
                    "title": await title_element.text_content() if title_element else None,
                    "sizes": valid_sizes_prices,
                    "prices": prices,
                    "currency": prices[0][0] if prices else None,
                    "standart_price": prices[0] if prices else None
                }
                
                return data
                       
        except Exception as e:
            print(f"Ошибка при получении цены: {e}")
            return None
    
    def _generate_user_agent(self) -> str:
        """Генерация случайного User-Agent"""
        agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"
        ]
        return random.choice(agents)
    
    async def close(self) -> None:
        """Закрыть браузер и контекст"""
        if self.page:
            await self.page.close()
        if self.context:
            await self.context.close()
        if self.browser:
            await self.browser.close()


if __name__ == "__main__":
    async def main():
        browser = BrowserService()
        result = await browser.find_item("https://www.poizon.com/product/adidas-originals-yeezy-slide-onyx-54836740?track_referer_page_id=2307&track_referer_block_type=4776&track_referer_position=1")  # Замените на ваш URL
        print(result)
    
    asyncio.run(main())