---
layout: post
title: GetOldTweets3
---
# Twitter Analysis Using Data from GetOldTweets3

Overall, the process of obtaining data for analysis is faster and less complex than using the Twitter API method. The python code is quite short and efficient and entered through the Command Prompt on Windows.

<pre><code>python Exporter_py3.py --querysearch "Election2020" --maxtweets 100 --output election_tweets.csv
</code></pre>

After downloading the data, it was imported into R as a CSV file. Also listed are a number of libraries that can be useful for manipulating and analyzing Twitter data.

<pre><code># clears all objects in memory for this R session
rm(list=ls())

# sets my working directory to the specified path
setwd("~/PhD Program/EPPS_7V81/R_WD")

# load needed libraries
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

# Import dataset pulled from command prompt

e2020 <- read.csv("C:/Twitterdata/election_tweets.csv", sep=";")

View(e2020)

names(e2020)
</code></pre>

The first type of analysis completed was generating bar graphs to analyze the number of Favorites and Retweets within the data. Admittidly, the sample size of n=100 is small, but as an example, makes the data easier to work with for demonstration purposes.

<pre><code>  
barplot(count_favorites, main = "Bar Graph of #Election2020 Tweets: Number of Favorites",
          col=c("red"),
          xlab = "Number of Favorites",
          ylab = "Number of Observations")
barplot(count_retweets, main = "Bar Graph of #Election2020 Tweets: Number of Retweets",
        col=c("blue"),
        xlab = "Number of Retweets",
        ylab = "Number of Observations")
</code></pre>

The results of the bar graph plotting are interesting. It is notable that zero is by far the most frequent number among both Favorites and Retweets. Additionally, there seems to be a trend that as the number of Favorites or Retweets increases, the frequency decreases. If one were to assume this pattern is representative of all tweets, then the number of tweets that have large numbers of Favorites and or Retweets is rare.

![Elections2020 bar graph favorites](/images/bar_e2020_favorites.png "Elections2020 bar graph favorites")
![Elections2020 bar graph retweets](/images/bar_e2020_retweets.png "Elections2020 bar graph retweets")

Next, the content of the tweets was analyzed through a frequency count of the text within each tweet. Below is the code used to clean the tweets. There are a few notable things to mention. First, all so-called 'stop words' such as "the", "or", etc. were removed. Next, given that the search for the dataset was #Election2020, it was also dropped from the data. Additionally, the initial bar graph revealed high counts of odd characters. Examining the data, two of the tweets pulled were not written in English; those observations were dropped from the dataset bringing n=98. After cleaning, a frequency analysis was completed which visualized the results on a bar graph.

<pre><code># clean text box for analysis
e2020$text <- gsub("https\\S*", "",
                   e2020$text)
e2020$text <- gsub("@\\S*", "",
                   e2020$text)
e2020$text <- gsub("amp", "",
                   e2020$text)
e2020$text <- gsub("[\r\n]", "",
                   e2020$text)
e2020$text <- gsub("[[:punct:]]", "",
                   e2020$text)
e2020$text <- gsub("â€", "",
                   e2020$text)
e2020$text <- gsub("Election2020", "",
                   e2020$text)
e2020$text <- gsub("election2020", "",
                   e2020$text)

# Tweet from rows 11 and 17 are in Indian
e2020 <- e2020[-c(11,17),]

# Need to remove common words such as "the", "or" etc. Known as 'stop' words.
freq <- e2020 %>%
  select(text) %>%
  unnest_tokens(word, text)

freq <- freq %>%
  anti_join(stop_words)
  
e2020_word_count_plot <- freq %>%
  count(word, sort = TRUE) %>%
  top_n(10) %>%
  mutate(word = reorder(word, n)) %>%
  ggplot(aes(x = word, y = n)) +
  geom_col() +
  xlab(NULL) +
  coord_flip () +
  labs(y = "Count",
       x = "Unique Words",
       title = "Frequency Analysis of Words from Tweets Containing #Election2020",
       subtitle = "'Stop' words omitted")

e2020_word_count_plot
</code></pre>

Looking at the top ten results, Trump is mentioned at a rate nearly twice as much as the second term, vote; though if one counts vote and voting as the same, the results a bit more balanced. Another notable frequently used word is COVID-19 appearing in nearly 1 of 10 tweets from the sample.

![Elections2020 word freq top 10](/images/e2020_word_freq_top10.png "Elections2020 word freq top 10")

Next, both the hashtags and mentions were analyzed and visualized in a word clouds. The data were cleaned as follows:

<pre><code>## Hashtags - WordCloud
e2020$hashtags <-
  as.character(e2020$hashtags)
e2020$hashtags <- gsub("c\\(", "",e2020$hashtags)
e2020$hashtags <- gsub("Election2020", "",e2020$hashtags)

set.seed(1234)
wordcloud(e2020$hashtags, min.freq=5, scale=c(3.5,.5), random.order=FALSE, rot.per=0.35, colors = brewer.pal(8, "Dark2"))

## Mentions - WordCloud
e2020$mentions <-
  as.character(e2020$mentions)
e2020$mentions <- gsub("@", "",e2020$mentions)

set.seed(1234)
wordcloud(e2020$mentions, min.freq=2, scale=c(3.5,.5), random.order=FALSE, rot.per=0.35, colors = brewer.pal(8, "Dark2"))
</code></pre>

Expectedly, the results of the word cloud graphs are similar to the word frequency analysis with trump and realdonaldtrump being at the epicenter of the clouds. At a secondarly level, for the hashtag wor cloud, one sees groups of vote, covid19 and biden on one side and maga and gop on another. The mentions word cloud features almost exclusive references to democratic figures other than the most frequent mention, realdonaldtrump.


![Elections2020 hashtag wordcloud](/images/e2020_hashtag_wordcloud.png "Elections2020 hashtag wordcloud")
![Elections2020 mentions wordcloud](/images/e2020_mention_wordcloud.png "Elections2020 mentions wordcloud")

Finally, sentiment analysis was completed on the 98 tweets. The library syuzhet was used to perform the sentiment analysis. 

<pre><code>freq <- iconv(freq, from="UTF-8", to="ASCII", sub="")
freq <-gsub("(RT|via)((?:\\b\\w*@\\w+)+)","",freq)
freq <-gsub("@\\w+","",freq)

ew_sentiment<-get_nrc_sentiment((freq))
sentimentscores <- data.frame(colSums(ew_sentiment[,]))

names(sentimentscores) <- "Score"

sentimentscores <- cbind("sentiment"=rownames(sentimentscores),sentimentscores)

rownames(sentimentscores) <- NULL

e2020_sentiment_plot <- ggplot(data = sentimentscores,aes(x=sentiment,y=Score)) +
  geom_bar(aes(fill=sentiment),stat = "identity") +
  theme(legend.position = "none") +
  xlab("Sentiments") +ylab("Scores")+
  ggtitle("Sentiment Analysis of #Election2020") +
  theme_minimal()

e2020_sentiment_plot
</code></pre>

The sentiment analysis should positvity as the highest sentiment among the tweets with negativity just behind it. Interesting, trust was the next highest sentiment by a large margin with sadness and fear also being somewhat high, appearing in approximately one third of the tweets analyzed. 

![Elections2020 sentiment](/images/sentiment_analysis_hashtag_e2020.png "Elections2020 sentiment")

