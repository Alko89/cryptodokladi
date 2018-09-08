# -*- coding: utf-8 -*-
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from subprocess import call

# scrapy runspider CapoeiraLyrics.py -o capoeiralyrics.json -t json
class CapoeiraLyrics(CrawlSpider):
    name = "capoeiralyrics"
    allowed_domains = ['capoeiralyrics.info']
    start_urls = ['http://capoeiralyrics.info/']

    # this is for downloading tags
    """def parse(self, response):
        songs = response.css('li.song')
        for song in songs:
            title = song.css('a::text').extract_first()
            tags = song.css('a.tag::text').extract()
            yield {
                'title': title,
                'tags': tags
            }"""

    rules = (
        Rule(LinkExtractor(allow=[r'songs/\w+']), callback='parse_item'),
    )

    def parse_item(self, response):
        url = response.url

        title = response.css('h1.title::text').extract_first()
        subtitle = response.css('h1.subtitle::text').extract_first()
        ytplayer = response.css('#ytplayer::attr(src)').extract_first()

        ## if there is a video, download mp3
        #if ytplayer is not None:
            #call(['youtube-dl', ytplayer, '--extract-audio', '--audio-format', 'mp3', '--audio-quality', '0'])

        lyrics = {}

        n = 0
        for article in response.css('article'):
            lang = response.css('a::attr(name)').extract()[n]
            #if lang != 'text':
            #    lang = response.css('h3::text').extract()[n-1]

            lyric = article.css('article').extract_first()[9:-10]
            lyrics[lang] = lyric

            n = n + 1

        yield {
            'url': url,
            'title': title,
            'subtitle': subtitle,
            'ytplayer': ytplayer,
            'lyrics': lyrics
        }
