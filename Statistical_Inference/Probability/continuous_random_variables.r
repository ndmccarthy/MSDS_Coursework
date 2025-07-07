# Suppose that car accidents in a given town have a Poisson distribution,
# with an average of 5 per week (i.e. λ = 5).
# Also, note that, given a Poisson process with mean λ,
# the waiting time until the first outcome has an exponential
# distribution with mean  1/λ.

# What is the probability that more than 6 accidents occur in a given week?
# Round your answer to four decimal places.

# accidents ~ Pois(5)
# P(accidents > 6) = 1 - P(accidents <= 6)

p1.1 <- round(1 - ppois(6, 5), 4)
p1.1

# What is the probability that the time until an accident
# will be at least one week?
# Give the exact answer or round your answer to four decimal places.

# time ~ Expo(5)
# Finding P(time >= 1)
p1.2 <- round(pexp(1, 5, lower.tail = FALSE), 4)
p1.2

# Suppose that no accidents have occurred for two weeks.
# What is the probability that no accidents will occur for another two weeks?
# Give the exact value or round your answer to six decimal places.

# number of accidents that have occurred in last two weeks is irrelevant
# finding P(time >= 2)
p1.3 <- round(pexp(2, 5, lower.tail = FALSE), 6)
p1.3



# Let X = the outcome when a fair die is rolled once.
# Suppose that, before the die is rolled, you are offered a choice:
# Option 1: a guarantee of 1/4 dollars (whatever the outcome of the roll)
# Option 2:  ℎ(𝑋)=1/𝑋 dollars.
# Which option would you prefer?
# Store your answer in the given variable as a numeric 1 or 2.

# comparing normal distributions of options
# option 1 averages $0.25
option2 <- 0
for (roll in 1:6) {
  dollar_amt <- 1 / roll
  option2 <- option2 + dollar_amt
}
option2_mean <- option2 / 6
option2_mean
# option 2 averages $0.41
# because each roll outcome is equally likely, I would choose option 2
option <- 2



# Suppose 𝑋 is a random variable for the length of time (in hours)
# it takes for a piece of machinery to fail.
# Let 𝑋 have PDF 𝑓(𝑥)=𝑐𝑒^(−𝑥/50) for 𝑥>0 and 𝑓(𝑥)=0 for 𝑥≤0.
#
# What is the value of c?

# X is an exponential variable.
# PDF for Expo is le^(-le)
# that makes c = 1/50
c <- 1 / 50

# What is the probability that the machine will function for at least 100 hours?
# Give the exact value or round your answer to three decimal places.

# finding P(X >= 100)
# X ~ Expo(1/50)
p3.b <- round(pexp(100, 1 / 50, lower.tail = FALSE), 3)
p3.b

# What is the expected amount of time for the machine to break?

# E(X) for Expo is 1/l
p3.c <- 1 / (1 / 50)
p3.c
