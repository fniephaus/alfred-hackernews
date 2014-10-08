from workflow import Workflow
from workflow import web

if __name__ == '__main__':
    wf = Workflow()
    if not wf.cached_data_fresh('hackernews_top_10', 60):

        items = web.get('https://hacker-news.firebaseio.com/v0/topstories.json').json()
        top_stories = []
        i = 1
        for item_id in items[:50]:

            item = web.get('https://hacker-news.firebaseio.com/v0/item/%s.json' % item_id).json()
            top_stories.append((item_id, item))

            if i % 10 == 0:
                wf.cache_data('hackernews_top_%s0' % (i / 10), top_stories)
                top_stories = []
            i += 1