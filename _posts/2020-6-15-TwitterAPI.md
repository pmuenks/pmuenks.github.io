---
layout: post
title: Twitter API Exercise
---

To complete these exercises, the first step was to secure a Developer Account with Twitter. Once this was completed, I used the code provided by Dr. Ho as a starting point - the list of libraries was expanded to include all packages for analysis and grapichs in this post:

<pre><code>#Clear environment
rm(list=ls())

##install.packages(c("rtweet","igraph","tidyverse","syuzhet","ggraph","data.table",
"radiant.data","ggplot2","tidytext","wordcloud","tm"), repos = "https://cran.r-project.org")
library(rtweet)
library(igraph)
library(tidyverse)
library(ggraph)
library(data.table)
library(radiant.data)
library(ggplot2)
library(tidytext)
library(wordcloud)
library(tm)
library(syuzhet)

## Acquire API key and token from Twitter developer website
# Check https://datageneration.org/adp/twitter/ for detail

# Create token for direct authentication to access Twitter data
# Enter key and tokens from Twitter developer account 
# (Account--> Apps--> detail--> Keys and tokens)
token <- rtweet::create_token(
  app = "",
  consumer_key <- "",
  consumer_secret <- "",
  access_token <- "",
  access_secret <- "")

## Check token

rtweet::get_token()</code></pre>

The exercise for querying, analyzing, and visualizing data using the API method asked us to complete two searches; one using a username search and the other using a keyword search. The only other specified requirement was to utilize the igraph package to create a simple network chart – this was completed for the keyword search.

### User Search and Analysis
To start, I began by selecting former Vice-President and the presumptive Democratic nominee for President, Joe Bide, as the user whose account would be analyzed. I began by retrieving the 3200 most recent tweets from @JoeBiden which is his official Twitter account.

<pre><code>biden <- get_timeline("JoeBiden", n = 3200)</code></pre>

Next, to analyze the data, I looked at some examples of content analysis of Tweets. One example was particularly influential by [Celine Van den Rul, published at towards data science, entitled “A Guide to Mining and Analysing Tweets with R”]( https://towardsdatascience.com/a-guide-to-mining-and-analysing-tweets-with-r-2f56818fdd16). 
The first set of analysis I performed was to analyze the types of tweets that Vice-President Biden has been publishing. The types are broke into three categories: 

  * Organic Tweets: those which are authored by the user. 
  * Retweets: when a user re-tweets something published by another user.
  * Replies: when the user responds to a comment made by another user.

This type of analysis seemed useful as it would give one some indication of which ways Vice-President Biden engages and utilizes Twitter.

<pre><code>
biden_tweets_organic <- biden[biden$is_retweet==FALSE,]
biden_retweets <- biden[biden$is_retweet==TRUE,]
biden_replies <- subset(biden,
                        !is.na(biden$reply_to_status_id))
                        
# Create dataframe to compare counts
ratio_data_biden <- data.frame(
  category=c("Organic", "Retweets", "Replies"),
  count=c(2811, 130, 259)
)

ratio_data_biden$fraction = ratio_data_biden$count / sum(ratio_data_biden$count)
ratio_data_biden$percentage = ratio_data_biden$count / sum(ratio_data_biden$count) * 100
ratio_data_biden$ymax = cumsum(ratio_data_biden$fraction)
ratio_data_biden$ymin = c(0, head(ratio_data_biden$ymax, n=-1))

ratio_data_biden <- round_df(ratio_data_biden, dec = 0)

Type_of_Tweet <- paste(ratio_data_biden$category, ratio_data_biden$percentage, "%")

# Plot the data as a circle chart to show ratios

biden_ratio_plot <- ggplot(ratio_data_biden, aes(ymax=ymax, ymin=ymin, xmax=4, xmin=3,
                             fill=Type_of_Tweet)) +
  geom_rect() +
  coord_polar(theta = "y") +
  xlim(c(2, 4)) +
  theme_void() +
  theme(legend.position = "right") +
  ggtitle("Ratio of Tweets from @JoeBiden by Type")
  
biden_ratio_plot
</code></pre>

Looking at the visualization below, it is apparent that @JoeBiden posts Organic Tweets almost exclusive - they account for over 87% of his most recent 3200 posts on Twitter.

![Biden Tweet Ratio Graphic](/images/biden_ratio_plot.png "Biden Ratio Graphic")

An additional bit of analysis that can be completed by sorting tweets into the three aforementioned categories is to analysis which tweet is favorited and/or retweeted the most. For this type of analysis, Organic Tweets would be the most appropriate to analyze given that one would want to examine which original posts have generated the most interest. In the case of @JoeBiden, the most favorited post also happens to be the most retweeted post.  

[I can't believe I have to say this, but please don't drink bleach.](https://twitter.com/JoeBiden/status/1253751812194070529)

The code to complete this analysis is:

<pre><code>
biden_tweets_organic <- biden_tweets_organic %>% arrange(-favorite_count)
biden_tweets_organic[1,5]

biden_tweets_organic <- biden_tweets_organic %>% arrange(-retweet_count)
biden_tweets_organic[1,5]
</code></pre>

Another interesting piece of analysis is to analyze how often tweets are being posted. As seen in the graph below, it would appear that the frequency with which Vice-President Biden was tweeting increased alongside the lockdowns which start in late-March and in earnest through April of 2020.

![Biden Tweet Historical](/images/biden_freq_by_month.png "Biden Tweet Historical")

Here is the code used to produce this graph. Note that it is using the biden dataframe which will include all 3200 tweets. Aggeragating the tweets by month gave a better result than by year. 

<code><pre>
colnames(biden)[colnames(biden)=="screen_name"] <- "Twitter_Account"

biden_frequency_plot <- ts_plot(dplyr::group_by(biden, Twitter_Account), "month") +
  ggplot2::theme_minimal() +
  ggplot2::theme(plot.title = ggplot2::element_text(face = "bold")) +
  ggplot2::labs(
    x= NULL, y = NULL,
    title = "Frequency of Tweets from @JoeBiden",
    subtitle = "Tweet Counts Aggregated by Month",
    caption = "\nSource: Data collected from Twitter's REST API via r-package 'rtweet'"
  )
biden_frequency_plot
</code></pre>

The aforementioned analysis examined the mechanics of the tweets. The next section analyzes the content of tweets from @JoeBiden. Again, for content analysis, it would be best to examine Organic Tweets as it is original content. However, a future iteration may compare Organic Tweets versus Retweets for a comparative analysis.

To begin, it is necessary to clean the data. This cleaning occurs at two levels. First, Twitter specific artifacts such as "@" and punctuation need to be removed. 

<code><pre>
biden_tweets_organic$text <- gsub("https\\S*", "",
                             biden_tweets_organic$text)
biden_tweets_organic$text <- gsub("@\\S*", "",
                                  biden_tweets_organic$text)
biden_tweets_organic$text <- gsub("amp", "",
                                  biden_tweets_organic$text)
biden_tweets_organic$text <- gsub("[\r\n]", "",
                                  biden_tweets_organic$text)
biden_tweets_organic$text <- gsub("[[:punct:]]", "",
                                  biden_tweets_organic$text)
</code></pre>

Next, using the unnest_tokens function, so-called 'stop' words are removed. Examples of stop words include "the", "or", "a", etc. While in a literal sense, these may be the most frequent words used, such words are not useful for content analysis.

<code><pre>
organic_freq <- biden_tweets_organic %>%
  select(text) %>%
  unnest_tokens(word, text)

organic_freq <- organic_freq %>%
  anti_join(stop_words)
</code></pre>

Finally, the frequency of the words needs to be visualized. Here, a bar graph is used to represent the top ten most frequently used words in Organic Tweets from @JoeBiden.

<code><pre>
biden_word_freq_plot <- organic_freq %>%
  count(word, sort = TRUE) %>%
  top_n(10) %>%
  mutate(word = reorder(word, n)) %>%
  ggplot(aes(x = word, y = n)) +
  geom_col() +
  xlab(NULL) +
  coord_flip () +
  labs(y = "Count",
       x = "Unique Words",
       title = "Frequency Analysis of Words from @JoeBiden Tweets",
       subtitle = "'Stop' words omitted")

biden_word_freq_plot
</code></pre>

As one can see in the graph below, the most frequent words Tweeted by Vice-President Biden reflect that he is running for President against President Trump. What is notable is the absence of the term Democratic or any other explicitly partisan words. The terms "country", "nation", "american", and "people" are suggestive of rhetoric and language that is absent of partisanship.

![Biden Word Freq Count](/images/biden_word_freq_plot.png "Biden Word Freq Count")

Relatedly, one can conduct analysis of the most frequent hashtags used by @JoeBiden.

<code><pre>
biden_tweets_organic$hashtags <-
  as.character(biden_tweets_organic$hashtags)
biden_tweets_organic$hashtags <- gsub("c\\(", "",biden_tweets_organic$hashtags)

set.seed(1234)
wordcloud(biden_tweets_organic$hashtags, min.freq=5, scale=c(3.5,.5), random.order=FALSE, rot.per=0.35, colors = brewer.pal(8, "Dark2"))
</code></pre>

Here, the use of hashtags in Organic Tweets by Vice-President Biden is quite sparse as the most frequent hastag relates to the now post Democratic Primary debates. If Vice-President Biden was looking for an area to improve his Twitter usage, a more robust ues of hashtags could be one habit to develop.

![Biden Word Cloud](/images/biden_hashtag_wordcloud.png "Biden Word Cloud")

The final bit of analysis comes from sentiment analysis. This analysis realies the package ‘syuzhet’. While teh technical elements are detailed, the basic idea is that sentences are categorized or scored based on various attributes. As a simple example, the sentence 'I feel good." may be scored as positive. What this analysis does is examine the tweets and score them on the following ten attributes.
* Anger
* Anticipation
* Disgust
* Fear
* Joy
* Negative
* Positive
* Sadness
* Surprise
* Trust

The code for this analysis is: 

<code><pre>
organic_freq <- iconv(organic_freq, from="UTF-8", to="ASCII", sub="")
organic_freq <-gsub("(RT|via)((?:\\b\\w*@\\w+)+)","",organic_freq)
organic_freq <-gsub("@\\w+","",organic_freq)

ew_sentiment<-get_nrc_sentiment((organic_freq))
sentimentscores <- data.frame(colSums(ew_sentiment[,]))

names(sentimentscores) <- "Score"

sentimentscores <- cbind("sentiment"=rownames(sentimentscores),sentimentscores)

rownames(sentimentscores) <- NULL

biden_sentiment_plot <- ggplot(data = sentimentscores,aes(x=sentiment,y=Score)) +
  geom_bar(aes(fill=sentiment),stat = "identity") +
  theme(legend.position = "none") +
  xlab("Sentiments") +ylab("Scores")+
  ggtitle("Sentiment Analysis of @JoeBiden") +
  theme_minimal()

biden_sentiment_plot
</code></pre>

Looking at the results, the two most common sentiments expressed by Vice-President Biden on Twitter are positivity and negativity. As a quick analysis, this duality would seem to fit with a presidential candidate that is challenging a sitting President. The communication strategy would be to discuss all of the things going poorly (negative) but provide messages that suggest an electoral victory for Vice-President Biden would bring about positive change (postive).

![Biden Sentiment Analysis](/images/biden_sentiment_analysis.png "Biden Sentiment Analysis")

### Searching by Hashtag and Analysis

The search term analysis uses a smaller dataset as the igraph package used for network analysis is quite resource intensive. Accordingly, a dataset of only 50 observations was pulled from Twitter for analysis. By including retweets, the analysis should yield a more active network when the connections are graphed. The search term analyzed was the hashtag #Election2020. 

<code><pre>
e2020_small <- search_tweets(
  "#Election2020", n = 50, include_rts = TRUE
)
</code></pre>
  
Next, using the network_data and network_graph functions from the igraph library, the data are prepared for graphical network representation.

<code><pre>
e2020_small_net <- network_data(e2020_small, "retweet,mention,reply")

attr(e2020_small_net, "idsn")

  e2020_small_net <- network_graph(e2020_small)
  plot(e2020_small_net)
</code></pre>

Finally, the results of the network analysis should distnict nodes, notably forming around @FoxNews and @realDonaldTrump as seen the graphic below. Also notable is with very few exceptions, everyone of the 50 accounts pulled have a connection with at least on other user. 

![Hashtag Election2020 Network](/images/igraph_keyword.png "Hashtag Election2020 Network")
