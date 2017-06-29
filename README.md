# Google News Parser

Google changed the structure of Google News today, which broke an important portion of a project I am working on. In order to grab news links I was using (slightly modified version of) the python library gnp, which stopped working completely.

This is the result of a frantic effort to rebuild its functionality in as little time as possible.

The usage is simple: create an instace of the class with a string containing the parameters that determine the news edition and the language and tell the parser to dig into today's news (and any topics you want to focus on) as deep as you want, although the amount of links gets out of hand fairly quickly. The parser can of course do either one (dig by itself into today's news and search for specific topics) independently.

The resulting links will be contained in the parser's news dictionary. A slightly better formatted dictionary can be extracted using the parser's export_news_list method.

Let me know if you find it useful!