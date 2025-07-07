# Suppose that 𝑋∼𝑏𝑖𝑛(8,0.3). Find P(X=2).

bin_pmf <- function(n_trials, p_success, k_option) {
  possibilities <- choose(n_trials, k_option)
  successes <- p_success ** k_option
  failures <- (1 - p_success) ** (n_trials - k_option)
  possibilities * successes * failures
}

trial_run <- bin_pmf(8, 0.3, 2)

# R has several built-in probability mass functions.
# For example, for 𝑋∼𝑏𝑖𝑛(𝑛,𝑝), 𝑃(𝑋=𝑥) can be computed by typing dbinom(x,n,p).
# Confirm your previous calculation of 𝑃(𝑋=2)
# for 𝑋∼𝑏𝑖𝑛(8,0.3) by using this function.

if (round(trial_run, 4) == round(dbinom(2, 8, 0.3), 4)) {
  TRUE
} else {
  FALSE
}

# Compute 𝑃(𝑋≤2.6)=𝑃(𝑋=0)+𝑃(𝑋=1)+𝑃(𝑋=2).
# Do this using the dbinom function.

cumul_trial <- dbinom(0, 8, 0.3) + dbinom(1, 8, 0.3) + dbinom(2, 8, 0.3)

# R has a built-in cumulative distribution function for the
# binomial distribution as well as many other commonly used distributions.
# To compute 𝑃(𝑋≤𝑥) for the 𝑏𝑖𝑛(𝑛,𝑝) distribution,
# we would type pbinom(x,n,p).
# Use this to verify your calculation of 𝑃(𝑋≤2.6) when 𝑋∼𝑏𝑖𝑛(8,0.3).

if (round(cumul_trial, 4) == round(pbinom(2, 8, 0.3), 4)) {
  TRUE
} else {
  FALSE
}

# Suppose that 𝑋 has a Poisson distribution with parameter 𝜆=3.2.
# Compute 𝑃(𝑋=5).

pois_pmf <- function(k, lambda) {
  numerator <- (lambda ** k) * exp(-1 * lambda)
  denominator <- factorial(k)
  numerator / denominator
}
my_pois_pmf <- pois_pmf(5, 3.2)

# Guess at the command to do this with the built-in
# probability mass function based on what you learned
# with the binomial distribution.
# Make sure your answers match!

if (round(my_pois_pmf, 4) == round(dpois(5, 3.2), 4)) {
  TRUE
} else {
  FALSE
}

# Use the R function for the cdf to determine, via trial and error,
# the smallest value of 𝑥 so that 𝑃(𝑋≤𝑥) first becomes greater than 0.9.

pois_cdf_test <- function(lamb) {
  cdf_complete <- FALSE
  ii <- 0
  while (cdf_complete == FALSE) {
    if (ppois(ii, lamb) > 0.9) {
      cdf_complete <- TRUE
    } else {
      ii <- ii + 1
    }
  }
  ii
}
pois_cdf_test(0.9)

mysample = rbinom(10000,8,0.3)

# To simulate 10,000 values from the 𝑏𝑖𝑛(8,0.3) distribution,
# we would type rbinom(10000,8,0.3).
# Write code here to determine the proportion of times the output is 2
# and compare it to the true probability that P(X=2).
mysample <- rbinom(10000, 8, 0.3)
num_2s <- length(mysample[mysample == 2])
proportion_2s <- num_2s / 10000
proportion_2s - dbinom(2, 8, 0.3)

# Here is a function to tabulate the frequencies for all values
# then divide by 10,000 to get proportions.
table(mysample) / 10000
# now let's make a histogram of our table
br <- seq(-0.5, 8.5, 1)
hist(mysample, prob = TRUE, breaks = br)
