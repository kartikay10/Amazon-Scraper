import scrapy
from ..items import AmazonScraperItem

class AmazonSpiderSpider(scrapy.Spider):
    name = 'amazon_spider'
    start_urls = ['https://www.amazon.com/']
    page_no=1
    page=1
    def parse(self, response):
        '''
        parse each department to get the categories

        '''
        # if( response.xpath('//*[@id="s-refinements"]/div[1]/ul/li/span/a/@href').extract()):
        #     category_links = response.xpath('//*[@id="s-refinements"]/div[1]/ul/li/span/a/@href').extract() 


        # category_links = response.xpath('//*[(@id = "zg_browseRoot")]//a/@href ').extract()
        # # print(category_links)
        # for link in category_links:
        #     # print("https://www.amazon.com"+link)
        #     # scrapy.Request("https://www.amazon.com"+link,callback=self.parseCategory)
        #     # print("in category")
        #     yield response.follow(link,self.parseCategory)
        urls_a = ['https://www.amazon.com/s?i=automotive&bbn=15684181&rh=n%3A15684181&dc&fs=true','https://www.amazon.com/s?rh=n%3A165796011&fs=true','https://www.amazon.com/s?rh=n%3A16225006011&fs=true','https://www.amazon.com/s?rh=n%3A16225007011&fs=true','https://www.amazon.com/s?rh=n%3A16225010011&fs=true','https://www.amazon.com/s?rh=n%3A16225012011&fs=true','https://www.amazon.com/s?i=fashion-luggage&bbn=16225017011','https://www.amazon.com/s?rh=n%3A16225013011&fs=true','https://www.amazon.com/s?rh=n%3A16225014011&fs=true','https://www.amazon.com/s?rh=n%3A256643011&fs=true','https://www.amazon.com/s?rh=n%3A16225015011&fs=true','https://www.amazon.com/s?rh=n%3A2617941011&fs=true','https://www.amazon.com/s?i=computers&bbn=172282&rh=n%3A172282&dc&fs=true','https://www.amazon.com/s?k=clothing&rh=n%3A7141123011&dc&qid=1631777521']
        urls_b = ['https://www.amazon.com/s?i=stripbooks&bbn=283155&rh=n%3A283155&dc&fs=true','https://www.amazon.com/s?i=digital-music-album&bbn=163856011&rh=n%3A163856011&dc&fs=true','https://www.amazon.com/s?i=digital-text&s=relevance','https://www.amazon.com/s?i=instant-video','https://www.amazon.com/s?i=movies-tv&bbn=2625373011&rh=n%3A2625373011&dc&fs=true','https://www.amazon.com/s?i=popular&bbn=5174&rh=n%3A5174&dc&fs=true','https://www.amazon.com/s?i=software&bbn=229534&rh=n%3A229534&dc&fs=true']
        for url in urls_a:
            self.page_no=1
            yield response.follow(url,self.parseA)
            
        for url in urls_b:
            self.page=1
            yield response.follow(url,self.parseB)

    def parseA(self, response):
        
        product_links =  response.xpath('//*[@id="search"]/div/div/div/span/div/div/div/span/div/div/div/div/h2/a/@href').extract()
        nextPage = response.xpath('//*[@id="search"]/div/div/div/span/div/div/span/div/div/ul/li/a/@href').extract()[-1]
        for link in product_links:
            # scrapy.Request("https://www.amazon.com"+link,callback=self.parseProduct)
            if(link.find('ref')):
                link= link[:link.find('ref')]
            yield response.follow(link,self.parseProduct)
        
        
        if(self.page_no<400 ):
            print(self.page_no)
            self.page_no += 1
            yield response.follow(nextPage,self.parseA)
            
        
    def parseB(self, response):
        
        product_links =  response.xpath('//*[@id="search"]/div/div/div/span/div/div/div/span/div/div/div/div/div/div/div/h2/a/@href').extract()
        nextPage = response.xpath('//*[@id="search"]/div/div/div/span/div/div/span/div/div/ul/li/a/@href').extract()[-1]
        for link in product_links:   # change to product_links[] to get all products
            # scrapy.Request("https://www.amazon.com"+link,callback=self.parseProduct)
            if(link.find('ref')):
                link= link[:link.find('ref')]
            yield response.follow(link,self.parseProduct)
        
        
        # print(nextPage)
        if(self.page<300):
            print(self.page)
            self.page += 1
            yield response.follow(nextPage,self.parseB)
            
            


    
    def parseProduct(self, response):
        product =  AmazonScraperItem()
        product['name'] = response.xpath('//*[@id="a-page"]/meta[3]/@content').extract_first()
        
        # for l in response.css('#feature-bullets .a-list-item::text').extract():
        #     string+=(l.strip())
        product['description'] = response.xpath('//*[@id="a-page"]/meta[2]/@content').extract_first()
        try:
            product['category']  = response.xpath('//div[@id="wayfinding-breadcrumbs_feature_div"]/ul/li/span/a/text()').extract()[0].strip()
        except:
            product['category']  = ''
        if(product['category']=='Back to results'):
            product['category']=product['name'][product['name'].find(':',13)+2:]
 
        try:
            if((product['name'].find('Amazon.com: '))!=-1):
                product['name']= product['name'].replace('Amazon.com: ','')
        
            if((product['description']).find('Amazon.com: ')!=-1):
                product['description'] = product['description'].replace('Amazon.com: ','')

            if((product['name'].find('Amazon.com : '))!=-1):
                product['name']= product['name'].replace('Amazon.com : ','')

            if((product['description']).find('Amazon.com : ')!=-1):
                product['description'] = product['description'].replace('Amazon.com : ','')

            if((product['name'].find('Amazon.com | '))!=-1):
                product['name']= product['name'].replace('Amazon.com | ','')

            if((product['description']).find('Amazon.com | ')!=-1):
                product['description'] = product['description'].replace('Amazon.com | ','')
        except:
            pass
        
        product['image_urls'] = response.xpath('//*[@id="altImages"]//img/@src').extract()
        print(product)
        if(product['name']!=None):
            yield product

