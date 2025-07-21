# Practice Assessment #5
require(lolcat)

# Problem 1
sample.size.mean.t.onesample(effect.size = 0.05,
                             #variance.est = ,
                             alpha = 0.1,
                             beta = 0.1,
                             alternative = "two.sided")
# Problem 2-5
airlineA <- 75
Astd <- 15 # normal dist.
# must be less than 85 minutes late
reduction_needed <- 6.2
alpha <- 0.05
n_flights <- 10
airline_se <- Astd / sqrt(n_flights)
z <- qnorm(1 - alpha/2)
margin <- z * airline_se
airlineA - margin
airlineA + margin

power.mean.t.onesample(sample.size = n_flights,
                       effect.size = reduction_needed,
                       variance.est = Astd^2,
                       alpha = alpha,
                       alternative = "two.sided")

fixed_beta <- 0.1
sample.size.mean.t.onesample(effect.size = reduction_needed,
                             variance.est = Astd ^ 2,
                             alpha = alpha,
                             beta = fixed_beta,
                             alternative = "two.sided")

new_std <- 0.7 * Astd
sample.size.variance.onesample(null.hypothesis.variance = Astd^2,
                               alternative.hypothesis.variance = new_std^2,
                               alpha = alpha,
                               beta = fixed_beta,
                               alternative = "two.sided")
new_std <- (Astd * 0.3) + Astd
sample.size.variance.onesample(null.hypothesis.variance = Astd^2,
                               alternative.hypothesis.variance = new_std^2,
                               alpha = alpha,
                               beta = fixed_beta,
                               alternative = "two.sided")

# Problem 6-13
flights <- read.delim("~/GitHub/MSDS_Coursework/Quality_Improvement_Methods/flights.dat")
alpha <- 0.15
n_A <- length(flights$Airline_A)
n_B <- length(flights$Airline_B)
t.test.twosample.independent.simple(sample.mean.g1 = mean(flights$Airline_A),
                                    sample.variance.g1 = var(flights$Airline_A),
                                    sample.size.g1 = n_A,
                                    sample.mean.g2 = mean(flights$Airline_B),
                                    sample.variance.g2 = var(flights$Airline_B),
                                    sample.size.g2 = n_B,
                                    conf.level = 1 - alpha)

# P(B >= 45) = ?
B_expected <- mean(flights$Airline_B)
std_B <- sd(flights$Airline_B)
pnorm(45, mean = B_expected, sd = std_B, lower.tail = FALSE)

# Problem 14 - 22
maintenance <- read.delim("~/GitHub/MSDS_Coursework/Quality_Improvement_Methods/maintenance.dat")
summary.continuous(maintenance$January)

alpha <- 0.05
t.test.twosample.dependent(x1 = maintenance$January,
                           x2 = maintenance$February)
rho <- cor(maintenance$January, maintenance$February, method = "pearson")
var.test(maintenance$January, maintenance$February)

# Problem 23-27
returns <- read.delim("~/GitHub/MSDS_Coursework/Quality_Improvement_Methods/returns.dat")
alpha <- 0.1
t.test.twosample.independent.simple(sample.mean.g1 = mean(returns$OldSite),
                                    sample.variance.g1 = var(returns$OldSite),
                                    sample.size.g1 = length(returns$OldSite),
                                    sample.mean.g2 = mean(returns$YourSite),
                                    sample.variance.g2 = var(returns$YourSite),
                                    sample.size.g2 = length(returns$YourSite),
                                    conf.level = 1 - alpha)
t.test.onesample.simple(sample.mean = mean(returns$OldSite),
                        sample.variance = var(returns$OldSite),
                        sample.size = length(returns$OldSite),
                        conf.level = 1 - alpha)
t.test.onesample.simple(sample.mean = mean(returns$YourSite),
                        sample.variance = var(returns$YourSite),
                        sample.size = length(returns$YourSite),
                        conf.level = 1 - alpha)
