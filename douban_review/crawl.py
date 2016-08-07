#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import path
import re

from argparse import ArgumentParser

import requests
import lxml.html

parser = ArgumentParser()
parser.add_argument('-u', '--reviews-url', metavar="REVIEWS_URL", required=True, help=u"影评的第一页链接. 比如：https://movie.douban.com/subject/21817627/reviews")
parser.add_argument('-p', '--page', dest="page", metavar="MAX_PAGE", type=int, default=1, help=u"抓取多少页. 默认1页")
args = parser.parse_args()

def crawl_one_page(url):
    reviews = []

    response = requests.get(url)
    doc = lxml.html.fromstring(response.text)

    for review_url in doc.xpath('//div[@class="review-hd-expand"]/a[1]/@href'):
        print 'crawling review: %s' %(review_url)
        review_res = requests.get(review_url)
        review_doc = lxml.html.fromstring(review_res.text)

        review_text = ' '.join(review_doc.xpath('//div[@class="main-bd"]/div[@id="link-report"]/div[1]//text()'))
        reviews.append(review_text.strip())

    return reviews

def main():
    start_url = args.reviews_url
    max_page = args.page

    subject_id = int(re.search(r'subject/(\d+)/.+$', start_url).group(1))

    reviews = []
    for i in range(max_page):
        print "crawling page: %d" %(i+1,)
        # 默认每页20条
        param_start = i*20
        url = start_url + '?start=%d' %param_start
        reviews += crawl_one_page(url)

    write_file = path.join(
        path.dirname(path.dirname(path.abspath(__file__))),
        'files',
        'subject_%d.txt' %subject_id
    )
    with open(write_file, 'wb') as f:
        for review in reviews:
            f.write(review.encode('utf-8') + "\n")
    print u"评论已保存到 %s" %write_file


if __name__ == "__main__":
    main()

