# library
library(tidyverse)
library(conflicted)

# Pull the data
bought <- read.csv("outputs/bought_food_1.csv")
eaten <- read.csv("outputs/eaten_food_1.csv")
wasted <- read.csv("outputs/wasted_food_1.csv")

# Make the totals bargraph's
bought %>%
  group_by(Day.Bought, Type) %>%
  summarise(total_kg = sum(kg)) %>%
  ggplot(aes(x = Day.Bought, y = total_kg, fill = Type)) +
  geom_bar(stat = "identity")

eaten %>%
  group_by(Day.Eaten, Type) %>%
  summarise(total_kg = sum(kg)) %>%
  ggplot(aes(x = Day.Eaten, y = total_kg, fill = Type)) +
  geom_bar(stat = "identity")

wasted %>%
  group_by(Day.Wasted, Type) %>%
  summarise(total_kg = sum(kg)) %>%
  ggplot(aes(x = Day.Wasted, y = total_kg, fill = Type)) +
  geom_bar(stat = "identity")