# You are a quality assurance tester for hardware equipment
# and been given a lot of  10,000 nails to test.
# You decide to randomly sample 100 nails from the lot
# and test if they are defective.
# The whole lot would be considered defective
# if the average of the sample is less than 11.97 cm or greater than 12.04 cm.
# Given that the true population mean 𝜇 is 12 cm
# with a true standard deviation 𝜎 of 0.2 cm,
# what is the probability that the lot is not defective?
# Round your answer to two decimal places. Save your answer as p1.

# P(11.97 <= Xbar <= 12.04) = ?
# m = 12, s = 0.2
# pop = 10000, n = 100
nail_count <- 100
nail_mean <- 12
nail_std <- 0.2
nail_var <- (nail_std ** 2) / nail_count
# Xbar ~ N(12, 0.0004)
Xbar_std <- nail_var ** 0.5
stand_lower <- (11.97 - nail_mean) / Xbar_std
stand_upper <- (12.04 - nail_mean) / Xbar_std
# stand_lower <= Z <= stand_upper
phi_lower <- pnorm(stand_lower)
phi_upper <- pnorm(stand_upper)
p1 <- round(phi_upper - phi_lower, 2)
p1


# Suppose you are out fishing and you want to predict
# the amount of time (in minutes) it takes to catch 3 fish.
# Let 𝑇𝐹∼𝑁(15,10) be the time it takes to reel in a fish.
# Let 𝑇𝑇∼𝑁(10,8) be the amount of time you spend waiting
# for the fish to take the bait. Assume 𝑇𝐹 and 𝑇𝑇 are independent.
# Also assume you start timing as soon as you start reeling in the first fish,
# and the time ends when you have finished catching the third fish.

# Let 𝑇 be the random variable for the total amount of time spent fishing.
# What is 𝐸[𝑇] and 𝑉𝑎𝑟[𝑇]?
# Save your variables as exp.T and var.T.
# (Hint: Note that a variance of 122 is incorrect for this problem. Why?
# If 𝑍1 and 𝑍2 are indepedent N(0,1) random variables,
# the distribution of 𝑍1+𝑍2 is not the same as 2𝑍1.
# If you want to explore this, you can run simulations to see for yourself.)

# T = 3TF + TT
# E(T) = 3E(TF) + E(TT)
# V(T) = 9E(TF) + E(TT)

# expected values are the same as the means
e_tf <- 15
e_tt <- 10
exp.T <- 3 * e_tf + e_tt
var.T <- 9 * e_tf + e_tt
exp.T
var.T

# What is the probability that you finish catching the three fish
# in 60 minutes or less?
# Round your answer to three decimal places. Save your answer as p2.2.

# P(T <= 60) = ?
# standardize
T_std <- var.T ** 0.5
time_limit <- (60 - exp.T) / T_std
p2.2 <- round(pnorm(time_limit), 3)
p2.2


# Exams given by a particular instructor in a freshman-level
# statistics course have a mean of 75 and a standard deviation of 17.
# The instructor gives an exam to two classes,
# one with 30 students and the other with 90 students.

class1 <- 30
class2 <- 90
Xbar_mean <- 75
Xbar_std <- 17

# Let  𝑋¯ represent the average exam score in the class of 30.
# Approximate the probability that the average test score 𝑋¯ exceeds 80,
# that is, estimate 𝑃(𝑋¯≥80).
# Round your answer to four decimal places. Save your answer as p3.a.

# P(Xbar >= 80) = 1 - P(Xbar < 80)
# standardize
avg_score <- (80 - Xbar_mean) / Xbar_std
p3.a <- round(1 - pnorm(avg_score), 4)
p3.a

# Let  𝑌¯ represent the average exam score in the class of 90.
# Approximate the probability that the average test score 𝑌¯ exceeds 80,
# that is, estimate 𝑃(𝑌¯≥80).
# Round your answer to four decimal places. Save your answer as p3.b.

p3.b <- p3.a

# Estimate the probability that the averages of the two classe
# are within one point of each other, that is, estimate 𝑃(−1≤𝑌¯−𝑋¯≤1).
# Hint: What is the distribution of 𝑌¯−𝑋¯?
# Round your answer to two decimal places. Save your answer as p3.c.

p3.c <- 1
p3.c


# Suppose a machine requires a specific type of battery that lasts
# an exponential amount of time with mean 25 hours.
# As soon as the battery fails, you replace it immediately.
# If you have 50 such batteries,
# estimate the probability that the machine is still operating after 1300 hours.
# Round your answer to three decimal places. Save your answer as p4.

# L ~ Expo(25)

Lmean <- 1 / 25
batteries <- 50
total_hours <- 1300
Lbar_limit <- total_hours / batteries
e_Lbar_limit <- 1 / Lbar_limit

# P(Lbar >= 26) = 1 - P(Lbar < 26)
# standardize
Lbar_var <- 1 / (Lbar_limit ** 2)
bound <- (Lbar_mean - Lmean) / Lbar_var
p4 <- round(1 - pnorm(bound), 3)
p4