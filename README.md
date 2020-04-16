# hn-best

**Hosted on: https://hnbest.pythonanywhere.com/**

This API was created for my personal use. However, if you wish to use the API (**for personal use only**), here is the documentation:

RSS Feed: https://hnbest.pythonanywhere.com/rss

RSS parameters:
  
  - limit: number of items from the best page of Hacker News (items are not stored locally but fetched in real time, so avoid large limit values).
    - default: 10
    - example: `https://hnbest.pythonanywhere.com/rss?limit=10`

  - nowords: filters out titles containing these words (words are in list format).
    - default: None
    - example: `https://hnbest.pythonanywhere.com/rss?nowords=['google', 'apple', 'facebook']`

  - similar: instead of directly matching two words, the API is using a similarity metric. This parameter assigns the metric's threshold. for eg: 'covid-19' and 'Covid19' has a similarity score of 0.8.
    - default: 0.8
    - example: `https://hnbest.pythonanywhere.com/rss?similar=0.75`
    
Hacker News API: https://github.com/HackerNews/API
