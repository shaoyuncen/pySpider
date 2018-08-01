文件目录说明：
    /govSpider
        ./govSpider        
            ./spiders    用于存放爬虫代码，本示例中是先获取待爬取url，然后添加到scrapy的调度器中，由调度器执行调度程序抓取html网页，再通过xpath or re 解析至item中
            ./commands    当有多个爬虫时在这里编写代码来执行，相当于run.py，因为本示例中只有一个，还未编写，可以参照网上示例
            items.py    定义数据字段的地方，格式为 item['name'] = scrapy.Field( 处理程序，没有不写 )
            pipelines.py    数据存储的管道，本示例中通过pymysql存入MySQL数据库
            settings.py    配置文件，定义了爬虫配置，数据库的配置属性等

scrapy的官方文档： https://docs.scrapy.org/en/latest/index.html