# news_bot

## Table of Contents
- [news\_bot](#news_bot)
  - [Table of Contents](#table-of-contents)
  - [Description](#description)
  - [Features](#features)
  - [Installation](#installation)
  - [Usage](#usage)
    - [Example Command](#example-command)
  - [Contributing](#contributing)
  - [License](#license)


## Description

This is a bot that fetches news articles based on a keyword (or phrase) search and a date range, returning an excel file with article information and the downloaded images from the articles.

## Features

- Fetches news articles from multiple sources (for now only LA Times website)
- Allows customization of news preferences
- Fetch is based on a keywork search
- Fetch is also based on a date range
- Returns images that were contained in the articles
- Returns also an Excel file that contains article information suchas:
  - Title
  - Description
  - Date
  - How many times the keyword (or phrase) you searched shows up in the title or description
  - If the article contains a mention to a monetary value in dollars (i.e. $11.1 | $111,111.11 | 11 dollars | 11 USD)
  - The name of the image that was downloaded from the article

## Installation

To install and run the news bot, follow these steps:

1. Clone the repository: `git clone https://github.com/your-username/news_bot.git`
2. Navigate to the project directory: `cd news_bot`
3. Run the setup script: `./setup.sh`

```sh
git clone https://github.com/your-username/news_bot.git
cd news_bot
./setup.sh
```

## Usage

After running the setup script, the News Bot will be ready to fetch news articles based on the arguments you pass it. 

To run the bot, run:

```sh
python main.py
```

This will summon an interactive command line prompt guiding you through the bot configuration to fetch your desired articles.

Another option is to use flags to pass the configuration arguments directly without having to go through the interactive command line prompt:

- Use `-s` or `--search_phrase` to specify the search keyword (or phrase) the bot will use to fetch your articles
- Use `-e` or `--excel_dir` to specify the directory where Excel files will be saved
- Use `-i` or `--image_dir` to specify the directory where article images will be saved
- Use `-l` or `--log_dir` to specify the directory where log files will be saved
- Use `-sd` or `--start_date` to specify the start date (in MM/DD/YYYY format) the bot will use to fetch your articles
- Use `-ed` or `--end_date` to specify the end date (in MM/DD/YYYY format) the bot will use to fetch your articles

### Example Command

To run the News Bot with all the arguments:

```sh
conda activate rpa_env
python main.py -s "Dollar" -e "excel_files" -i "article_images" -l "logs" -sd "05/23/2024" -ed "05/23/2024"
```

## Contributing

Contributions are welcome! If you have any ideas or improvements for the news bot, feel free to submit a pull request. Please make sure to follow the coding conventions and include tests for any new features.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.