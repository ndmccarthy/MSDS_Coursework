# Problem 1
n1 <- 10
xbar1 <- 2.7
n2 <- 12
xbar2 <- 3.2
var <- 0.8
# assuming normal distribution
alpha <- 0.1
df <- n1 + n2 - 2
z <- qnorm(1 - alpha/2, lower.tail = TRUE)
tail <- z * sqrt(var * (1/n1 + 1/n2))
xbar_diff <- xbar1 - xbar2
print(c(xbar_diff - tail, xbar_diff + tail))

# Problem 2
var1 <- 0.73
var2 <- 0.8
# assume true variance for both populations is the same
pooled_var <- ((n1 - 1) * var1 + (n2 - 1) * var2) / df
tail <- t * sqrt(pooled_var * (1/n1 + 1/n2))
print(c(xbar_diff - tail, xbar_diff + tail))

# Problem 3
smooth_n <- 138
smooth_mean <- 18.17
smooth_var <- 1.78
textured_n <- 110
textured_mean <- 21.66
textured_var <- 3.21
concrete_alpha <- 0.05
# cannot assume the variances for each population are the same
# using Welch's Approximation to solve Behrens-Fisher Problem
# calculate nu
numerator <- (smooth_var/smooth_n + textured_var/textured_n) ^ 2
denom1 <- ((smooth_var/smooth_n)^2)/(smooth_n - 1)
denom2 <- ((textured_var/textured_n)^2)/(textured_n - 1)
denominator <- denom1 + denom2
nu <- numerator / denominator
# approximately t-distribution of nu is what we're looking for
concrete_t <- qt(1 - concrete_alpha/2, nu, lower.tail = TRUE)
standard_error <- sqrt(smooth_var/smooth_n + textured_var/textured_n)
concrete_tail <- concrete_t * standard_error
concrete_xbar_diff <- smooth_mean - textured_mean
print(c(concrete_xbar_diff - concrete_tail, concrete_xbar_diff + concrete_tail))
