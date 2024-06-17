# rpa_news_bot

## Table of Contents
- [rpa\_news\_bot](#rpa_news_bot)
  - [Table of Contents](#table-of-contents)
  - [Description](#description)
  - [Features](#features)
  - [Setup](#setup)
  - [Usage](#usage)
  - [License](#license)


## Description

This is a bot that utilizes the Robocorp framework for RPA to fetch articles from news websites based on a keyword (or phrase) search, a topic of interest and a date range (number of months). It returns an excel file with article information and the downloaded images from the articles.

## Features

- Fetches news articles from multiple sources (*for now only LA Times website*)
- Fetch is based your chosen topic
- Fetch is based on a keywork search
- Fetch is also based on a number of months (how many months back the articles should be fetched for)
- Returns images that were contained in the articles
- Returns also an Excel file that contains article information suchas:
  - Title
  - Description
  - Date
  - How many times the keyword (or phrase) you searched shows up in the title or description
  - If the article contains a mention to a monetary value in dollars (i.e. $11.1 | $111,111.11 | 11 dollars | 11 USD)
  - The name of the image that was downloaded from the article

## Setup

To install and run the news bot, follow these steps:

1. Log in to your Robocloud account.
2. Navigate to Tasks
3. Add a new task package (robot).
4. Upload this bot's files to the task package, including the robot.yaml, conda.yaml, and all necessary Python scripts (this can also be done by adding the url of this github project)
5. Navigate to Unattended
6. Navigate to Processes (submenu of unattended)
7. Add new process
8. Go through the steps, making sure to add `Run News Bot` task to the process
9. Finish creating the process
10. Now, your bot will be ready to fetch articles

## Usage

To run the bot

1. Click on the process you just created
2. Press Run Process
3. Select option `Run with input data`
4. Enter the following key-value pairs:
   - phrase: "<insert_search_phrase>"
   - number_of_months: <insert_start_date>
   - topic: "<insert_news_topic>"
5. After this, your process will start to run
6. You will find the outputs of the bot inside the artifacts folder

## License

This project is licensed under the Apache License. See the [LICENSE](LICENSE) file for more details.