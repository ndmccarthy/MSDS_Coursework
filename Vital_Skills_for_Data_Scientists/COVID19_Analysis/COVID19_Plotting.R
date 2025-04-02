
# import ggplot
library(tidyverse)
library(dplyr)
library(tidyselect)
library(ggplot2)

# plot cases over time for a random selection of 15 counties
county_names <- US_Cases[, "Combined_Key"]
county_cols <- Temporal_US_Cases[, -c(1:2)]
set.seed(123)
random_ids <- sample.int(3342, size = 15)

random_counties <- county_cols %>%
  select(all_of(random_ids)) %>%
  cbind(Temporal_US_Cases[c(1:2)])
random_counties <- random_counties[, c(16:17, 1:15)] # get date and day number in front

random_counties_long <- random_counties %>%
  pivot_longer(cols = -c(Date, Day_Number),
               names_to = "County",
               values_to = "Cases") %>%
  arrange(County, Date) %>%  # Ensure data is ordered by County and Date
  group_by(County) %>%
  mutate(New_Cases = Cases - lag(Cases),
         New_Cases = ifelse(New_Cases < 0, 0, New_Cases)) %>%
  ungroup() %>%
  filter(Cases > 0)

ggplot(random_counties_long,
       aes(x = Date,
           y = New_Cases,
           color = County)) +
  geom_line() +
  labs(title = "COVID19 Cases in 15 Random US Counties",
       x = "Date",
       y = "Number of New Cases",
       color = "County") +
  geom_smooth()

# plot County_Sums for death:cases ratio and population
ggplot(County_Sums,
       aes(x = Population,
           y = Death_Case_Ratio)) +
  labs(title = "Ratio  of Deaths to Cases by Population in US Counties",
       subtitle = "Totals for January 22, 2020 to March 9, 2023") +
  xlab("Population Size") +
  ylab("Ratio of Deaths to Cases") +
  geom_point() +
  geom_smooth()

# plot State_Sums for death:case ratio and population
ggplot(State_Sums,
       aes(x = Population,
           y = Death_Case_Ratio)) +
  labs(title = "Ratio  of Deaths to Cases by Population in US States",
       subtitle = "Totals for January 22, 2020 to March 9, 2023") +
  xlab("Population Size") +
  ylab("Ratio of Deaths to Cases") +
  geom_point() +
  geom_smooth()
# remove outliers in population
Plottable_State_Sums <- State_Sums %>%
  filter(Population < 15000000) %>%
  filter(Death_Case_Ratio > 0.003)
ggplot(Plottable_State_Sums,
       aes(x = Population,
           y = Death_Case_Ratio)) +
  labs(title = "Ratio  of Deaths to Cases by Population in US States",
       subtitle = "Totals for January 22, 2020 to March 9, 2023") +
  xlab("Population Size") +
  ylab("Ratio of Deaths to Cases") +
  geom_point() +
  geom_smooth()

# plot death:case ratio by pop for Countries
ggplot(Global_Sums,
       aes(x = Population,
           y = Death_Case_Ratio)) +
  labs(title = "Ratio  of Deaths to Cases by Population of Countries",
       subtitle = "Totals for January 22, 2020 to March 9, 2023") +
  xlab("Population Size") +
  ylab("Ratio of Deaths to Cases") +
  geom_point() +
  geom_smooth()
# try without outliers in population
Plottable_Global_Sums <- filter(Global_Sums, Population < 500000000)
ggplot(Plottable_Global_Sums,
       aes(x = Population,
           y = Death_Case_Ratio)) +
  labs(title = "Ratio  of Deaths to Cases by Population of Countries",
       subtitle = "Totals for January 22, 2020 to March 9, 2023") +
  xlab("Population Size") +
  ylab("Ratio of Deaths to Cases") +
  geom_point() +
  geom_smooth()
