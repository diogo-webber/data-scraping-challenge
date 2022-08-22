import scrapy
from main import output_path
from scripts.Printer import Printer
from scripts.strings_misc import cc, tint_text

def is_in_stock(string):
    return string == "instock availability"

class BooksSpiderSpider(scrapy.Spider):
    name = 'books_spider'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['http://books.toscrape.com/']
    
    book_page_content_xpath = '//*[@id="content_inner"]/article/div[1]/div[2]'
    
    count = 0
    
    stars_map = {
        'One':   1, 
        'Two':   2, 
        'Three': 3, 
        'Four':  4, 
        'Five':  5, 
    }
    
    def parse_book_page(self, response):
        
        self.count += 1
        
        print(f"\r    Pages Scrapped: {tint_text(self.count, cc.YELLOW)}", end='')
        
        return {
                'title': response.xpath(self.book_page_content_xpath + '/h1/text()').get(),
                'category': response.xpath('//*[@id="default"]/div/div/ul/li[3]/a/text()').get(),
                'stars': self.stars_map.get(response.xpath(self.book_page_content_xpath + '/p[3]/@class').get().removeprefix("star-rating ")),
                'price_in_pounds': response.xpath(self.book_page_content_xpath + '/p[1]/text()').get().removeprefix("£"),
                'in_stock': is_in_stock(response.xpath(self.book_page_content_xpath + '/p[2]/@class').get()),
            }

    def parse(self, response):
        for book_showcase in response.css('article.product_pod'):
            next_book = book_showcase.css('h3 a::attr("href")').get()
            
            yield response.follow(next_book, self.parse_book_page)
            
        next_page = response.css('li.next a::attr("href")').get()
        
        if next_page is not None:
            yield response.follow(next_page, self.parse)
            
    def closed(self, reason):
        stats = self.crawler.stats.get_stats()
        
        count = stats['item_scraped_count']
        total_time = round(stats['elapsed_time_seconds'], 2)
        
        print(tint_text(
            f"\r    ✔  {count} web pages scrapped in {total_time} seconds."
        , cc.GREEN))
        
        Printer.output_message("CREATE_CSV", file=output_path)