# Google News Parser

Google changed the structure of Google News, which broke an important portion of a project I am working on. In order to grab news links I was using (a slightly modified version of) the python library gnp, which stopped working completely.

This is the result of a frantic effort to rebuild its functionality in as little time as possible (in order for the project not to be impacted). It still works quite well!

The usage is simple: create an instace of the class with a string containing the parameters that determine the news edition and the language and tell the parser to grab today's news.

```
my_gnp=gnp(lang='hl=en-US&gl=US&ceid=US:en')
my_gnp.extract_main_news()
```
The function should return a dictionary like this one:
```
{'Business':
  {'cards':
    [['http://www.independent.co.uk/voices/rupert-murdoch-fox-sky-media-plurality-phone-hacking-sun-jeremy-corbyn-a7814711.html',
      'https://www.washingtonpost.com/world/europe/uk-government-to-rule-on-sky-merger/2017/06/29/44019860-5cae-11e7-aa69-3964a7d55207_story.html',
      'http://www.latimes.com/business/hollywood/la-fi-ct-murdoch-fox-sky-deal-20170627-story.html'],

[...]

     ['http://www.cnbc.com/2017/06/28/amazon-declares-july-11-is-prime-day-but-deals-start-sooner.html',
      'https://www.youtube.com/watch?v=vCX_ERiBt1Y',
      'http://www.businessinsider.com/amazon-prime-day-july-11-2017']],
   'extra_topics':
     {'Amazon Prime',
      'Amazon.com, Inc.',
      'Blue Apron',
      'Metropolitan Transportation Authority',
      'Rupert Murdoch',
      'Sky UK'}},
 'Entertainment':
  {'cards':
    [['http://www.hollywoodreporter.com/heat-vision/fans-have-inherited-film-industry-a-problem-rest-us-guest-column-1015340',
      'http://variety.com/2017/film/reviews/spider-man-homecoming-review-tom-holland-1202481638/',
      'http://www.indiewire.com/2017/06/spider-man-homecoming-review-marvel-future-superhero-movies-tom-holland-zendaya-1201848553/'],

[...]

}
```

A slightly better formatted dictionary can be extracted using the parser's export_news_list method.

Let me know if you find it useful!
