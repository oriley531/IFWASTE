# library
library(tidyverse)

# Pull the data
bought <- read.csv("outputs/bought_food_1.csv")
eaten <- read.csv("outputs/eaten_food_1.csv")
wasted <- read.csv("outputs/wasted_food_1.csv")

# Make the totals bargraph
b_sums <- bought %>%
    group(Type, Day.Bought) %>%
    summarise(Sum_Value = sum(kg))