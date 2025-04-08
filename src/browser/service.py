from playwright.async_api import async_playwright
import asyncio


class BrowserService:
    def __init__(self):
        self.browser = None
        self.page = None
        
    async def find_price(self, url: str = "https://dw4.co/t/A/1rqr7kBzL"):
        """Найти цену на странице"""
        try:
            async with async_playwright() as p:
                self.browser = await p.firefox.launch(headless=False)
                self.page = await self.browser.new_page()
                await self.page.goto(url)
                
                # Ждем появления элемента с ценой
                await self.page.wait_for_selector("span.amount")
                
                # Получаем все элементы с классом amount
                price_elements = await self.page.query_selector_all("span.amount")
                
                # Берем первый элемент и получаем его текст
                if price_elements:
                    price = await price_elements[0].text_content()
                    print(f"Найдена цена: {price}")
                    return price
                else:
                    print("Цена не найдена")
                    return None
                    
        except Exception as e:
            print(f"Ошибка при получении цены: {e}")
            return None
        finally:
            await self.close()
    
    async def close(self):
        """Закрыть браузер"""
        if self.page:
            await self.page.close()
        if self.browser:
            await self.browser.close()
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()


if __name__ == "__main__":
    async def main():
        browser = BrowserService()
        print(await browser.find_price())
    
    asyncio.run(main())