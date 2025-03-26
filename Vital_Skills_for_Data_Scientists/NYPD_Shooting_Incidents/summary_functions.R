library(dplyr)
library(tidyr)
library(ggplot2)
library(lubridate)

# determine number of shootings per boro per year

boro_shootings <- NYPD_Shootings_Data %>%
  group_by(YEAR = year(OCCUR_DATE), BORO) %>%
  summarise(INCIDENTS = n(), .groups = "drop")

boro_totals_plot <- ggplot(boro_shootings,
                           aes(x = YEAR,
                               y = INCIDENTS,
                               color = BORO))+ 
                           geom_line()+
                           labs(title = "Shootings in NYC by Boro over Time",
                                x = "Year",
                                y = "Number of Incidents")

# determine number of murders by boro over time
NYC_Murders <- filter(NYPD_Shootings_Data, STATISTICAL_MURDER_FLAG == TRUE)
boro_murders <- NYC_Murders %>%
  group_by(YEAR = year(OCCUR_DATE), BORO) %>%
  summarise(MURDERS = n(), .groups = "drop")

boro_murders_plot <- ggplot(boro_murders,
                            aes(x = YEAR,
                                y = MURDERS,
                                color = BORO))+
                      geom_line()+
                      labs(title = "Murders in NYC by Boro over Time",
                           xlab("Year"),
                           ylab("Number of Murders"))

# determine frequency of murders by boro over time
boro_murders$INCIDENTS <- boro_shootings$INCIDENTS
boro_murders$MURDER_FREQUENCY <- (boro_murders$MURDERS/boro_murders$INCIDENTS)*100

boro_murder_freq_plot <- ggplot(boro_murders,
                            aes(x = YEAR,
                                y = MURDER_FREQUENCY))+
                          geom_point(aes(color = BORO))+
                          labs(title = "Murder Frequency in NYC by Boro over Time",
                               x = "Year",
                               y = "Frequency of Murders")+
                          geom_smooth(method = "lm",formula = 'y ~ x', se = TRUE)
                          
                          