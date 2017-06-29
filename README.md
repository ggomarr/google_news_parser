# Google News Parser

Google changed the structure of Google News today, which broke an important portion of a project I am working on. In order to grab news links I was using (a slightly modified version of) the python library gnp, which stopped working completely.

This is the result of a frantic effort to rebuild its functionality in as little time as possible (in order for the project not to be impacted). It still works very well!

The usage is simple: create an instace of the class with a string containing the parameters that determine the news edition and the language and tell the parser to dig into today's news (and any topics you want to focus on) as deep as you want, although the amount of links gets out of hand fairly quickly. The parser can of course do either one (dig by itself into today's news and search for specific topics) independently.

Some examples:

- Grabbing the main news of the day:
```
gnp=gnp('hl=en&ned=us')
gnp.extract_main_news()
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

- Grabbing news about the topic 'very furry dogs':
```
gnp=gnp('hl=en&ned=us')
gnp.extract_topic_news('very furry dogs')
```
The function should return a dictionary like this one:
```
{'very furry dogs':
  {'cards':
    [['https://www.sbnation.com/lookit/2017/6/26/15876060/dogs-surfing-video-paddle-board'],
     ['https://www.washingtonpost.com/news/animalia/wp/2017/06/27/these-states-have-the-fattest-pets-and-they-might-surprise-you/',
      'https://www.banfield.com/state-of-pet-health/obesity',
      'https://www.banfield.com/state-of-pet-health',
      'http://www.prnewswire.com/news-releases/new-banfield-pet-hospital-research-reveals-one-in-three-us-pets-is-overweight-300479528.html',
      'https://www.usatoday.com/story/news/nation-now/2017/06/27/u-s-pets-getting-fatter-according-new-banfield-pet-hospital-report/428140001/',
      'http://gazette.com/colorado-humans-are-among-the-fittest-in-the-country.-their-pets-not-so-much./article/1606116',
      'https://www.banfield.com/Banfield/media/PDF/Downloads/soph/2017-SOPH-Infographic.pdf'],

[...]

    ],
  'extra_topics': {'Banfield Pet Hospital', 'United States of America'}}
}
```

- Or you can ask the parser to dig on its own into the news of the day:
```
gnp=gnp('hl=en&ned=us')
gnp.dig_into_news(dig_levels=1,seed_news={'Business':['NASDAQ','Oil']})
```
In this case the resulting links will be contained in the parser's news dictionary, which is huge and looks just as the examples above, so I will not show it here. A slightly better formatted dictionary can be extracted using the parser's export_news_list method.

Let me know if you find it useful!
