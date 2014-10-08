import multiprocessing
from workflow import Workflow, web

def load_item(item_id):
    return web.get('https://hacker-news.firebaseio.com/v0/item/%s.json' % item_id).json()

def load_chunk(n, items):
    pool = multiprocessing.Pool(processes=5)
    content = pool.map(load_item, items)
    wf.cache_data('hn_page_%s' % n, content)


if __name__ == '__main__':
    wf = Workflow()
    if not wf.cached_data_fresh('hn_page_1', 30):
        items = web.get('https://hacker-news.firebaseio.com/v0/topstories.json').json()
        for i in range(4):
            offset = i*15
            load_chunk(i + 1, items[offset:offset+15])
