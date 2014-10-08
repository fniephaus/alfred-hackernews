import sys
import time
from datetime import datetime
from ago import human
from workflow import Workflow
from workflow.background import run_in_background, is_running


def main(wf):
    user_input = ''.join(wf.args)

    if wf.update_available:
        wf.add_item("An update is available!",
                    autocomplete='workflow:update', valid=False)

    refresh(wf)
    top_stories = wf.cached_data('hackernews_top_10', max_age=60)
    while top_stories is None:
        top_stories = wf.cached_data('hackernews_top_10', max_age=60)
        time.sleep(1)

    for i in range(2,11):
        if wf.cached_data_fresh('hackernews_top_%s0' % i, 60):
            top_stories += wf.cached_data('hackernews_top_%s0' % i, max_age=0)
        else:
            break
    
    for item_id, item in top_stories:
        title = item['title']
        date = human(datetime.fromtimestamp(int(item['time'])))
        subtitle = '%s points by %s %s' % (item['score'], item['by'], date)
        url = item['url'] if 'url' in item else 'https://news.ycombinator.com/item?id=%s' % item_id
        if user_input.lower() in title.lower() or user_input.lower() in subtitle.lower():
            wf.add_item(title, subtitle, arg=url, valid=True)

    wf.send_feedback()


def refresh(wf):
    if not is_running('hackernews_refresh'):
        cmd = ['/usr/bin/python', wf.workflowfile('hackernews_refresh.py')]
        run_in_background('hackernews_refresh', cmd)


if __name__ == '__main__':
    wf = Workflow(update_settings={
        'github_slug': 'fniephaus/alfred-hackernews',
        'version': 'v0.9.1',
    })
    sys.exit(wf.run(main))
