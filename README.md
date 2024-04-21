# Reddit Link Gatherer
I made this repository in the attempt to find links to all posts of a subreddit. It works by using this query template</br> 
`site:https://www.reddit.com/r/<subreddit name> before:YYYY/MM/DD`
<br/>
The script will maintain a database of links and previously used dates. The table of dates is used to prevent the system from overworking by avoiding querying previously used dates.
# Installation
You will have to install the requirements to the project but it is only one library due to most the librarys being part of the Python standard library

```
pip install -r requirements.txt
```

# Usage
You can specify a few different arguments with this program to provide more functionality.

```
python RedditLinkGatherer.py r/arduino -y 2019 -d 8
```

The following command will begin to scrape the internet for posts in r/arduino starting at the date 2019/1/1 (YYYY/MM/DD) with a delay of 8 seconds. You can set the delay to be lower but the higher the delay the lower the likelihood of being rate-limited.

</hr>


```
python RedditLinkGatherer.py r/SubSimGPT2Interactive -y 2021 -m 4 -r
```

This command starts in the year 2021 but also starts in April. The first date queried by the system will be 2021/4/1 with a default delay of 1 second. the `-r` options specifys a requery which means ignore previously scraped dates.
