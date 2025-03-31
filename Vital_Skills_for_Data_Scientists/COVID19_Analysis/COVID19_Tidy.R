
# read in Johns Hopkins' CSVs from github
US_Cases <- read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/refs/heads/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv')
Global_Cases <- read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/refs/heads/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')
US_Deaths <- read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/refs/heads/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_US.csv')
Global_Deaths <- read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/refs/heads/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv')

# clean up US_Cases
US_Cases <- US_Cases[, -c(1:5)]
US_Cases <- US_Cases[, -c(4:5)]
colnames(US_Cases)[colnames(US_Cases) == "Admin2"] <- "County"
US_Cases <- US_Cases[, -c(3:4)]

# grab US county population data
County_Pops <- read_csv('co-est2024-pop.csv')
setdiff(US_Cases$County, County_Pops$County)
County_Pops <- County_Pops[, -c(7)]
