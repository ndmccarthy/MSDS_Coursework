library(tidyverse)
library(tidyr)
library(dplyr)
library(ggplot2)

HOU_data <- read.csv("HOU-Airport_Daily-Weather-Reports_1930-2025.csv")

# change DATE column to date type (instead of character)
HOU_data$DATE <- mdy(HOU_data$DATE)

# remove 1930 and 2024 since not complete
HOU_data <- filter(HOU_data, 
                   HOU_data$DATE < as.Date("2025-01-01"), 
                   HOU_data$DATE > as.Date("1930-12-31"))

# fix NULLS
HOU_data$TAVG <- (HOU_data$TMAX + HOU_data$TMIN) / 2
HOU_data$PRCP <- replace_na(HOU_data$PRCP, 0)
HOU_data <- filter(HOU_data, !is.na(HOU_data$TAVG), !is.na(HOU_data$PRCP))

# aggregate columns into months, years, and decades (using average)
HOU_months <- HOU_data %>%
              group_by(year = year(DATE), month = month(DATE)) %>%
              summarise(avg_temp = mean(TAVG), avg_prcp = mean(PRCP))
HOU_annual <- HOU_data %>%
              group_by(year = year(DATE)) %>%
              summarise(avg_temp = mean(TAVG), total_prcp = sum(PRCP))
HOU_decades <- HOU_annual %>%
                mutate(decade = floor(year/10)*10) %>%
                group_by(decade) %>%
                summarise(avg_temp = mean(avg_temp), avg_prcp = mean(total_prcp)) %>%
                select(decade, avg_temp, avg_prcp) # get rid of year column

# remove 1942-1946 because outliers in temp
HOU_annual_updated <- filter(HOU_annual, avg_temp > 65)
              
# plot average temperature and precipitation separately
ggplot(HOU_annual, 
        mapping = aes(x = year, y = avg_temp)) +
  geom_point() +
  labs(title = "Average Annual Temperature in Houston, TX",
       subtitle = "Recorded at Houston Hobby Airport 1931-2024") +
  xlab("Year") +
  ylab("Average Annual Temperature (\u00B0 F)") +
  geom_smooth()

ggplot(HOU_annual_updated, 
       mapping = aes(x = year, y = avg_temp)) +
  geom_point() +
  labs(title = "Average Annual Temperature in Houston, TX without 1942-1946",
       subtitle = "Recorded at Houston Hobby Airport 1931-2024") +
  xlab("Year") +
  ylab("Average Annual Temperature (\u00B0 F)") +
  geom_smooth()

ggplot(HOU_annual, 
       mapping = aes(x = year, y = total_prcp)) +
  geom_point() +
  labs(title = "Annual Precipitation in Houston, TX",
       subtitle = "Recorded at Houston Hobby Airport 1931-2024") +
  xlab("Year") +
  ylab("Total Precipitation (inches)") +
  geom_smooth()

ggplot(HOU_decades, 
       mapping = aes(x = factor(decade), y = avg_temp)) +
  geom_col(fill = "steelblue") +
  labs(title = "Average Temperature per Decade in Houston, TX",
       subtitle = "Recorded at Houston Hobby Airport 1931-2024") +
  xlab("Decade") +
  ylab("Average Temperature (\u00B0 F)") +
  coord_cartesian(ylim = c(60, NA))

ggplot(HOU_decades, 
       mapping = aes(x = factor(decade), y = avg_prcp)) +
  geom_col(fill = "steelblue") +
  labs(title = "Average Annual Precipitation per Decade in Houston, TX",
       subtitle = "Recorded at Houston Hobby Airport 1931-2024") +
  xlab("Decade") +
  ylab("Average Annual Precipitation (inches)")
