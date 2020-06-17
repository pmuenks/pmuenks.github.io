---
layout: post
title: Twitter API Exercise
---

To complete these exercises, the first step was to secure a Developer Account with Twitter. Once this was completed, I used the code provided by Dr. Ho as a starting point - the list of libraries was expanded to include all packages for analysis and grapichs in this post:

<pre><code>#Clear environment
rm(list=ls())

##install.packages(c("rtweet","igraph","tidyverse","syuzhet","ggraph","data.table","radiant.data","ggplot2","tidytext","wordcloud","tm"), repos = "https://cran.r-project.org")
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
