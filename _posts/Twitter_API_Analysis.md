---
layout: post
title: Twitter API Exercise
---

To complete these exercises, the first step was to secure a Developer Account with Twitter. Once this was completed, I used the code provided by Dr. Ho as a starting point - the list of libraries was expanded to include all packages for analysis and grapichs in this post:

'''
#Clear environment
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

rtweet::get_token()
'''
