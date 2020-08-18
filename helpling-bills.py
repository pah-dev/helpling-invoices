import scrapy
from scrapy.item import Item, Field
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from bs4 import BeautifulSoup


class HelplingPayment(Item):
    amount = Field()
    name = Field()
    status = Field()
    date = Field()
    link = Field()


class HelplingEvent(Item):
    name = Field()
    date = Field()
    time = Field()
    frecuency = Field()
    duration = Field()
    customer_price = Field()
    fee = Field()
    invoice_date = Field()
    invoice_type = Field()
    invoice_amount = Field()
    invoice_number = Field()
    invoice_link = Field()


class HelplingCrawler(CrawlSpider):
    name = "helplingcrawler"
    allowed_domain = ["helpling.de"]
    start_urls = ["https://app.helpling.de/mobile/provider/bank_transfers"]

    rules = (
        Rule(LinkExtractor(allow=r"/bank_transfers/\d+"), follow=True),
        Rule(
            LinkExtractor(allow=r"/events/\d+"), follow=True, callback="parse_payments"
        ),
    )

    def parse_payments(self, response):
        item = scrapy.loader.ItemLoader(HelplingEvent(), response)

        soup = BeautifulSoup(response.body)

        rows = soup.find(id="table.tbody.tr")
        invoice_date = rows[0].text
        invoice_type = rows[1].text
        invoice_amount = rows[2].text
        invoice_number = rows[3].text

        item.add_xpath("invoice_number", invoice_number)
        item.add_xpath("invoice_type", invoice_type)
        item.add_xpath("invoice_amount", invoice_amount)
        item.add_xpath("invoice_date", invoice_date)

        yield item.load_item
