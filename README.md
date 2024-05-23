# news_bot

## Table of Contents
- [news\_bot](#news_bot)
  - [Table of Contents](#table-of-contents)
  - [Description](#description)
  - [Features](#features)
  - [Setup](#setup)
  - [Usage](#usage)
  - [Architechture](#architechture)
  - [Contributing](#contributing)
  - [License](#license)


## Description

This is a bot that utilizes the Robocorp framework for RPA to fetche articles from news websites based on a keyword (or phrase) search and a date range. It returns an excel file with article information and the downloaded images from the articles.

## Features

- Fetches news articles from multiple sources (*for now only LA Times website*)
- Fetch is based your chosen topic
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
   - start_date: <insert_start_date>
   - end_date: <insert_end_date>
   - search_phrase: <insert_search_phrase>
   - topic: <insert_news_topic>
5. After this, your process will start to run
6. You will find the outputs of the bot inside the artifacts folder

## Architechture

This project was made to be highly modularized and extensible (such as adding new websites, new functionality, etc...). Below is a diagram of how the different modules interact (click the link below for better visualization)

[text](https://tinyurl.com/newsbotdiagram)

## Contributing

Contributions are welcome! If you have any ideas or improvements for the news bot, feel free to submit a pull request. Please make sure to follow the coding conventions and include tests for any new features.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.