import scrapy  # 避免import的模块名与自己源代码的文件名相同


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    start_urls = [
        'http://quotes.toscrape.com/tag/love/',
    ]

    def parse(self,response):
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').extract_first(),
                'autor': quote.css('span/small/text()').extract_first(),
            }
        next = response.css('li.next a::attr("href")').extract_first()
        if next is not None:
            yield response.follow(next, self.parse)
