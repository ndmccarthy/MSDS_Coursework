push <- read.csv("~/GitHub/MSDS_Coursework/Quality_Improvement_Methods/Push.dat", sep="")

require(lolcat)
nqtr <- function(x, d) {
  noquote(t(round.object(x, d)))
}

# given information
n <- 24
target <- 140
lower_bound <- 126

# test for distribution
nqtr(summary.continuous(push$Force), 4)
# adtest.p    0.2312   indicates normal distribution

# what is the total percentage of expected failures?
failures <- push$Force[push$Force < lower_bound]
(p <- length(failures) / n)

# what is the 90% confidence interval for mean mu?
xbar <- mean(push$Force)
s <- sd(push$Force)

t.test.onesample.simple(sample.mean = xbar,
                        sample.variance = s^2,
                        sample.size = n,
                        conf.level = 0.9)

# what is the 90% confidence interval for the variance?
variance.test.onesample.simple(sample.variance = s^2,
                               sample.size = n,
                               conf.level = 0.9)

# worst case scenario for 90% confidence interval
worst_mean <- 118.4525
worst_var <- 128.2729
worst_case_samples <- replicate(1000, rnorm(100, mean = worst_mean, sd = sqrt(worst_var)))
worst_case_failure_counts <- sapply(worst_case_samples, function(x) sum(x < lower_bound))
mean(worst_case_failure_counts) # expected number of failures out of 100



# Assessment

set.seed(145)
normdata <- rnorm(10000, mean = 5, sd = 1)
round(mean(normdata), 4)

set.seed(100)
expdata <- replicate(5000, rexp(100, 5))
exp_means <- colMeans(expdata)
nqtr(summary.continuous(exp_means), 4)

xbar <- 150
s <- 10
n <- 15
(round(standard_error <- s / sqrt(n), 4))

xbar <- 1.575
s <- 0.01
n <- 5
target_mean <- 1.580
standard_error <- s / sqrt(n)
z <- (xbar - target_mean) / standard_error
round(pnorm(target_mean, mean = xbar, sd = standard_error, lower.tail = FALSE), 4)


xbar <- 1.575
s <- 0.01
n <- 10
target_mean <- 1.572
standard_error <- s / sqrt(n)
z <- (xbar - target_mean) / standard_error
round(pnorm(target_mean, mean = xbar, sd = standard_error, lower.tail = TRUE), 4)

preforms <- read.csv("~/GitHub/MSDS_Coursework/Quality_Improvement_Methods/preforms.dat", sep="")

(avg_weight <- mean(preforms$weight))
weight_sd <- sd(preforms$weight)
t.test.onesample.simple(sample.mean = avg_weight,
                        sample.variance = weight_sd ^ 2,
                        sample.size = length(preforms$weight),
                        conf.level = 0.95)
(weight_var <- weight_sd ^ 2)
variance.test.onesample.simple(sample.variance = weight_sd^2,
                        sample.size = length(preforms$weight),
                        conf.level = 0.90)

n <- 500
defects <- 15
alpha <- 0.95
proportion.test.onesample.exact.simple(sample.proportion = defects/n,
                                       sample.size = n,
                                       conf.level = alpha)

n <- 250
defect_lambda <- 2.58
alpha <- 0.9
poisson.test.onesample.simple(sample.count = defect_lambda * n,
                              sample.size = n,
                              conf.level = alpha)