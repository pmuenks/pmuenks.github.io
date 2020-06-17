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

To start, I began by selecting former Vice-President and the presumptive Democratic nominee for President, Joe Bide, as the user whose account would be analyzed. I began by retrieving the 3200 most recent tweets from @JoeBiden which is his official Twitter account.

<pre><code>biden <- get_timeline("JoeBiden", n = 3200)</code></pre>

Next, to analyze the data, I looked at some examples of content analysis of Tweets. One example was particularly influential by [Celine Van den Rul, published at towards data science, entitled “A Guide to Mining and Analysing Tweets with R”]( https://towardsdatascience.com/a-guide-to-mining-and-analysing-tweets-with-r-2f56818fdd16). 
The first set of analysis I performed was to analyze the types of tweets that Vice-President Biden has been publishing. The types are broke into three categories: 

  * Organic Tweets: those which are authored by the user. 
  * Retweets: when a user re-tweets something published by another user.
  * Replies: when the user responds to a comment made by another user.

This type of analysis seemed useful as it would give one some indication of which ways Vice-President Biden engages and utilizes Twitter.

<pre><code>biden_tweets_organic <- biden[biden$is_retweet==FALSE,]
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
  
biden_ratio_plot</code></pre>

