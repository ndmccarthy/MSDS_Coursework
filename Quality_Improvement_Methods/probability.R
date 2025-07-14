require(lolcat)

airline <- read.csv("~/GitHub/MSDS_Coursework/Quality_Improvement_Methods/airline.dat", sep="")

#find percentage of tickets bought that were under $930
prices <- airline$Price
low_prices <- prices[prices < 930]
(percent_low_price <- round(length(low_prices) / length(prices)*100, 2))
# different approach
hist(prices)  # approximately normal distribution
price_mu <- mean(prices)
price_sd <- sd(prices)  
price_zscore <- (930 - price_mu) / price_sd
(low_price_prob <- pnorm(price_zscore))


# out of 20 flights, what is the probability that at least 2 were canceled?
# create vector of probabilities of flights being canceled that day
num_canceled_per500 <- airline$Number_Cancelled_per_Day_per_500[1:450]
prob_canceled <- airline$Number_Cancelled_per_Day_per_500[1:450] / 500 # only 450 days in set
# if flight is canceled or not is bernoulli trial; total RV is binomial
(prob_2ormore <- pbinom(q = 1.99, # just under 2 so inclusive of 2
                        size = 20, 
                        prob = mean(prob_canceled), # expected probability of flight being canceled
                        lower.tail = FALSE)) # want upper end

# probability of two independent flights canceled?
expected_prob_canceled <- mean(prob_canceled)
(iid2 <- expected_prob_canceled ** 2)

# 25 minute carousel wait time or more probability?
# this is an exponential function; time until event occurs
wait_times <- airline$Bag_Delivery_Time[1:75]
avg_wait <- mean(wait_times)
(prob_long_wait <- pexp(q = 25,
                        rate = 1 / avg_wait,
                        lower.tail = FALSE))

# confirm exponential distribution of carousel wait times
# less than 100 sample size so shapiro_wilk test
shapiro.wilk.exponentiality.test(wait_times)

# probability that exactly 5 bags were lost out of 100 travelers?
# poisson distribution
bags_lost_per100 <- airline$Number_Lost_Bags[1:50]
prob_bag_lost <- bags_lost_per100 / 100
lambda <- mean(prob_bag_lost)
prob_5orless <- pbinom(q = 5,
                       size = 100,
                       prob = mean(prob_bag_lost),
                       lower.tail = TRUE)
prob_4orless <- pbinom(q = 4,
                       size = 100,
                       prob = mean(prob_bag_lost),
                       lower.tail = TRUE)
(prob_5lost <- prob_5orless - prob_4orless)

# probability that more than 8 bags had been lost per 100 passengers?
(prob_morethan8 <- 1 - pnorm(q = 8/100,
                              rate =  mean(prob_bag_lost),
                              sd = sd(prob_bag_lost),
                              lower.tail = TRUE))

# check normality of bags lost
# n > 25, so skewness and kurtosis tests
summary.continuous(bags_lost_per100)
anderson.darling.normality.test(bags_lost_per100)
shapiro.wilk.normality.test(bags_lost_per100)
hist(prob_bag_lost)

shapiro.wilk.exponentiality.test(bags_lost_per100)

#----------------- Assessment --------------------------

pbinom(q = 4,
       size = 400,
       prob = 0.02,
       lower.tail = TRUE)

1 - ppois(q = 49, lambda = 65, lower.tail = TRUE)

ptoolow <- pnorm(q = 154,
                 mean = 153,
                 sd = 10,
                 lower.tail = TRUE)
ptoohigh <- 1 - pnorm(q = 164,
                      mean = 153,
                      sd = 10,
                      lower.tail = TRUE)
(poutofspec <- ptoolow + ptoohigh)

pexp(q = 10000,
     rate = 1/40000,
     lower.tail = TRUE)
