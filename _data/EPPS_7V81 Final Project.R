# clears all objects in memory for this R session
rm(list=ls())

# sets my working directory to the specified path
setwd("~/PhD Program/EPPS_7V81/R_WD")

#Import from Python script and review data
df_full <- read.csv("C:/Users/patri/Desktop/df_full.csv")

summary(df_full)

#Load needed libraries

library(plm)
library(stargazer)
library(haven)
library(sf)
library(ggplot2)
library(tmap)
library(tmaptools)
library(leaflet)
library(magick)




#Set data as panel data by county and year
pdata <- pdata.frame(df_full, index=c("County","Year"))


#Regression Analysis
pooling <- plm(Turnout ~ Prez_Election + Voter_ID + Senate_2018 + Rep_Lean, data = pdata, model = "pooling")
summary(pooling)

between <- plm(Turnout ~ Prez_Election + Voter_ID + Senate_2018 + Rep_Lean, data = pdata, model = "between")
summary(between)

firstdiff <- plm(Turnout ~ Prez_Election + Voter_ID + Senate_2018 + Rep_Lean, data = pdata, model = "fd")
summary(firstdiff)

fixed <- plm(Turnout ~ Prez_Election + Voter_ID + Senate_2018 + Rep_Lean, data = pdata, model = "within")
summary(fixed)

random <- plm(Turnout ~ Prez_Election + Voter_ID + Senate_2018 + Rep_Lean, data = pdata, model = "random")
summary(random)

  #Note the high Theta value which suggests that the variation is coming from the county(Individual) level. Good outcome.


#LM Test for Random effects versus OLS
plmtest(pooling)
  #Small p-value means we prefer Random Effects over OLS

#LM Test for Fixed Effects Versus OLS
pFtest(fixed, pooling)
  #Small p-value and alternative hypothesis = "significant effects" means we prefer Fixed Effects to OLS

#Hausman Test for Fixed Versus Random effects Model
phtest(fixed, random)
  #HO: preferred model is random effects (no correlation between the two)
  #H1: model is fixed effects
  #Decision Rule: if p-value < .05, reject the null hypothesis and use a fixed effects model.
  #Resulting p-value is 1

options(scipen = 999)

mymap <- st_read("C:/Users/patri/Desktop/TX_County/County.shp", stringsAsFactors = FALSE)
str(mymap)
#Can use FIPS_ST_CN to match against pdata - need to rename

colnames(mymap)[colnames(mymap)=="FIPS_ST_CN"] <- "FIPS"
mymap$FIPS <- as.numeric(mymap$FIPS)
mymap$FIPS

map_and_data <- inner_join(mymap, df_full)

#merge the data using a left join

#Basic graph with county lines.
ggplot(map_and_data) +
geom_sf(aes(fill = Turnout)) +
  scale_fill_viridis_c(option = "plasma", trans = "sqrt")

#Basic tmap plot
map_and_data_2014 <- map_and_data %>%
  filter(Year == "2014")
tm_shape(map_and_data_2014) +
  tm_polygons("Turnout", palette = "plasma") +
  tm_layout(legend.outside = TRUE, 
            main.title = "Texas Voter Turnout by County: 2014",
            panel.labels = "Turnout as a percent of registered voters") +
  tmap_mode("plot")

#Interactive tmap for html viewing
map_and_data_2014 <- map_and_data %>%
  filter(Year == "2014")

tm_shape(map_and_data_2014) +
  tm_polygons("Turnout", id="County", palette = "plasma", popup.vars=TRUE) +
  tm_layout(legend.outside = TRUE, 
            main.title = "Texas Voter Turnout by County: 2014",
            panel.labels = "Turnout as a percent of registered voters") +
  tmap_mode("view")
tx_turnout_2014 <- tmap_last()
tmap_save(tx_turnout_2014, "tx_turnout_map_2014.html")

test_map <- tmap_last()
tmap_save(test_map, "test_map.html")

#Animated turnout map: 1992 - 2018
m1 <- tm_shape(map_and_data) +
        tm_polygons("Turnout", id = "County", palette = "plasma", n = 7) +
        tm_facets(along = "Year") +
        tm_layout(legend.outside = TRUE)

tmap_animation(m1, filename = "Texas_Turnout.gif", width = 1000, height = 1000, delay = 120)

#Show animated map
magick::image_read("Texas_Turnout.gif")


