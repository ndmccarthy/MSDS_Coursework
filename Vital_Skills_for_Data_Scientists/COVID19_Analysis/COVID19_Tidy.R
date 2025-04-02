# set up
library(tidyverse)
library(tidyr)
library(dplyr)
library(readr)

# read in Johns Hopkins' CSVs from github
US_Cases <- read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/refs/heads/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv')
Global_Cases <- read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/refs/heads/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')
US_Deaths <- read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/refs/heads/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_US.csv')
Global_Deaths <- read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/refs/heads/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv')

# clean up US_Cases
US_Cases <- US_Cases %>%
  filter(Admin2 != "Unassigned") %>% # get rid of unassigned deaths/cases
  filter(Admin2 != str_detect(Admin2, "Out of")) %>% # get rid of deaths/cases occurring out of state
  select(-c(1:6, 8:10)) # get rid of UID, iso2, iso3, code3, FIPS, Admin2, Country_Region, Lat, and Long_

# clean up US_Deaths
US_Deaths <- US_Deaths %>%
  filter(Admin2 != "Unassigned") %>% # get rid of unassigned deaths/cases
  filter(Admin2 != str_detect(Admin2, "Out of")) %>%
  select(-c(1:10)) # get rid of UID, iso2, iso3, code3, FIPS, Admin2, Province_State, Country_Region, Lat, and Long_

# pivot US_Cases and add #_Days column
Temporal_US_Cases <- US_Cases %>%
  pivot_longer(cols = 6:ncol(.), 
               names_to = "Date",
               values_to = "Cases") %>%
  mutate(Date = as.Date(Date, format = "%m/%d/%y")) %>%
  drop_na(Combined_Key) %>%
  group_by(Combined_Key, Date) %>%  
  summarise(Cases = sum(Cases, na.rm = TRUE), .groups = "drop") %>% 
  pivot_wider(names_from = "Combined_Key",
              values_from = "Cases")  %>%
  mutate(Day_Number = row_number() - 1)
Temporal_US_Cases <- Temporal_US_Cases[, c(1, 3344, 2:3343)] # wanted Day_Number as 2nd column instead of last

# Find out number of new cases per day (not totals)
New_US_Cases <- Temporal_US_Cases %>%
  pivot_longer(cols = -c(Date, Day_Number),
               names_to = "County",
               values_to = "Cases") %>%
  mutate(New_Cases = Cases - lag(Cases))

# create new tibble with each county's day_number with highest number of cases and population
Peak_Pop_County <- Temporal_US_Cases %>%
  pivot_longer(cols = -c(Date, Day_Number),  # Keep Date and Day_Number fixed
               names_to = "County",  # County names were in column headers
               values_to = "Cases")
Peak_Pop_County <- Peak_Pop_County %>%
  group_by(County) %>%
  slice_max(Cases, n = 1, with_ties = FALSE) %>%  # Get the first peak if there are ties
  select(County, Day_Number, Date, Cases)

# grab US county population data ---> turns out to not be needed because included in deaths data
County_Pops <- read_csv('co-est2024-pop.csv')
setdiff(US_Cases$County, County_Pops$County)
County_Pops <- County_Pops[, -c(7)]

# make data frame of totals of cases and deaths by county
US_Deaths_Sum <- US_Deaths %>%
  select(1, 2, ncol(US_Deaths)) # only include Combined_Key, Population, and last recorded date (final tally)
colnames(US_Deaths_Sum)[3] <- "Total_Deaths" # rename last column

US_Cases_Sum <- US_Cases %>%
  select(Combined_Key, Province_State, ncol(US_Cases))
colnames(US_Cases_Sum)[3] <- "Total_Cases"

US_Sums <- merge(US_Deaths_Sum, US_Cases_Sum)

County_Sums <- US_Sums %>%
  mutate(Death_Case_Ratio = Total_Deaths/Total_Cases) %>%
  filter(Death_Case_Ratio <= 1) %>% # get rid of data where deaths are larger than cases (incorrect)
  filter(Population < 4000000) %>% # remove population outliers to see trends better
  select(1, 4, 2, 3, 5, 6) # rearrange columns

# make data frame based on state
states <- list(US_Sums$Province_State)
states <- unique(states)
State_Sums <- aggregate(US_Sums[, c("Population", "Total_Deaths", "Total_Cases")],
                        by = list(State = US_Sums$Province_State),
                        FUN = sum)
State_Sums <- mutate(State_Sums, Death_Case_Ratio = Total_Deaths/Total_Cases)

# make data frame for country level
Global_Population <- read_csv("WorldBank_Country_Pop_Data.csv")
Global_Population <- Global_Population[, c("Country Name", "2020")]
colnames(Global_Population)[2] <- "Population"
colnames(Global_Population)[1] <- "Country_Region"
Global_Cases <- Global_Cases[, -c(1, 3, 4)] # remove Province/State, Lat, and Long
Global_Cases <- select(Global_Cases, "Country/Region", "3/9/23")
colnames(Global_Cases)[2] <- "Total_Cases"
Global_Cases <- aggregate(Global_Cases[, "Total_Cases"],
                          by = list(Country_Region = Global_Cases$`Country/Region`),
                          FUN = sum)
Global_Deaths <- select(Global_Deaths, "Country/Region", "3/9/23")
colnames(Global_Deaths)[2] <- "Total_Deaths"
Global_Deaths <- aggregate(Global_Deaths[, "Total_Deaths"],
                          by = list(Country_Region = Global_Deaths$`Country/Region`),
                          FUN = sum)
Global_Sums <- merge(Global_Cases, Global_Deaths)
country_names_to_fix <- setdiff(Global_Population$`Country Name`, Global_Sums$Country_Region)
Global_Sums <- merge(Global_Sums, Global_Population)
Global_Sums <- mutate(Global_Sums, Death_Case_Ratio = Total_Deaths/Total_Cases)
