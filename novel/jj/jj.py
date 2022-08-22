import requests
from lxml import etree
import re


def book_request(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers, timeout=5)
        response.encoding = 'gb18030'
        html = etree.HTML(response.text)
        return html
    except requests.exceptions.RequestException as e:
        print(e)


# 获取书名和目录
def get_catalog(book_url):
    # 书本html
    html = book_request(book_url)
    # 书本名字
    book_name = html.xpath('//h1/span/text()')[0]
    # print(f'成功获取书名:《{book_name}》')
    # 书本目录
    catalog_list = html.xpath('//tr/td//div/a/@href')[9:]
    return [book_name, catalog_list]


# 获取章节标题及内容
def get_chapter(chapter_url, needs):
    # 章节地址解析
    html = book_request(chapter_url)
    # 获取章节标题
    chapter_name = html.xpath('//h2/text()')[0]
    # 获取章节内容
    chapter_list = html.xpath('//div[@class = "noveltext"]/text()')[3:-5]
    # 处理章节内容
    chapter_content = '\n'.join(chapter_list).replace(' ', '').replace('\u3000', '').replace('\r', '')
    # 标题章节内容合并
    if needs == 1:
        num = re.findall(r'\d+', chapter_url)[1]
        chapter = f'\n\n第{num}章 {chapter_name}\n\n{chapter_content}\n\n'
    else:
        chapter = f'\n\n{chapter_name}\n{chapter_content}\n\n'
    return chapter


def main(book_url, needs):
    res = get_catalog(book_url)
    book_name = res[0]
    count = 0
    for item in res[1]:
        count = count + 1
        chapter = get_chapter(item, needs)
        with open(f'{book_name}.txt', 'a', encoding='utf-8') as f:
            f.write(chapter)
        print('\r', '已下载：%.1f%%' % float((count / len(res[1])) * 100), end=' ', flush=True)
    print(f'\n{book_name}下载完成')


if __name__ == '__main__':
    book_url = input('请输入晋江书本地址：')
    needs = input('是否需要添加章节（yes:1，no:0）:')
    main(book_url, needs)
