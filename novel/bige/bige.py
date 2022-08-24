from concurrent.futures import ThreadPoolExecutor
import brequests


def get_bookName(html):
    booK_name = html.xpath('//h1/text()')[0]
    return booK_name


def get_catalog(html):
    catalog = html.xpath('/html/body/div[4]/div[2]/a/@href')
    return catalog


def get_content(url, book_name):
    html = brequests.book_requests(url)
    title = html.xpath('//h1/text()')[0]
    content = html.xpath('//article[@id="article"]/p/text()')
    content = '\n'.join(list)
    chapter = f'\n\n{title}\n\n{content}\n'
    with open(f"{book_name}.txt", 'a', encoding='utf-8') as f:
        f.write(chapter)


def main(url):
    html = brequests.book_requests(url)
    book_name = get_bookName(html)
    catalog = get_catalog(html)
    with ThreadPoolExecutor(20) as t:
        for i in range(len(catalog)):
            t.submit(get_content(catalog[i], book_name))
            print('\r', '已下载：%.1f%%' % float((i / len(catalog)) * 100), end=' ', flush=True)
    print(f'\n{book_name}下载完成')


if __name__ == "__main__":
    url = input('请输入书本地址：')
    main(url)
