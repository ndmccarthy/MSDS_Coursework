# Problem 1
viscocity <- c(2781, 2900, 3013, 2856, 2888)
alpha <- 0.05
n <- length(viscocity)
xbar <- mean(viscocity)
s <- sd(viscocity)

find_interval <- function(alpha, sample_sd, sample_size, sample_mean) {
  if (n > 30) {
    factor_zt <- qnorm(1-alpha/2) # use z factor
  } else {
    factor_zt <- qt(1 - alpha/2, n - 1) # use t factor
  }
  tail <- factor_zt * (sample_sd / sqrt(sample_size))
  lower <- sample_mean - tail
  upper <- sample_mean + tail
  return(c(lower, upper))
}

find_interval(alpha, s, n, xbar)


# Problem 2
n <- 138
xbar <- 83.14
s <- 2.73
alpha <- 0.1

find_interval(alpha, s, n, xbar)

# Problem 4
var <- 25.1 # true pop variance
n <- 12
xbar <- 23.7
alpha <- 0.2
s <- sqrt(var) # true pop sd

z <- qnorm(1-alpha/2) # must do by hand rather than use function because sigma known
tail <- z * (s / sqrt(n))
lower <- xbar - tail
upper <- xbar + tail
print(c(lower, upper))

# Problem 5
var <- 9
alpha <- 0.05
len.ci <- 2.7
s <- sqrt(var)
tail_max <- len.ci/2

(t <- qt(1-alpha/2, ))
(n <- tail_max / t)
(n <- s / n)
(n <- n^2)
