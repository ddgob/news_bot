from RPA.Robocorp.WorkItems import WorkItems

from news_bot import NewsBot, config

if __name__ == '__main__':

    work_items = WorkItems()
    work_items.get_input_work_item()

    search_phrase = work_items.get_work_item_variable('search_phrase')
    start_date = work_items.get_work_item_variable('start_date')
    end_date = work_items.get_work_item_variable('end_date')
    topic = work_items.get_work_item_variable('topic')

    config.LOG_FILE_DIR = 'output'

    news_bot = NewsBot()
    news_bot.scrape_articles_by_date_range(
        'https://www.latimes.com/', 
        search_phrase, 
        start_date, 
        end_date, 
        'output', 
        'output',
        topic
    )
