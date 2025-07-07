# The planning department for the local county requires a contractor to submit
# one, two, three, four, or five forms (depending on the nature of the project)
# when applying for a building permit.
# Let 𝑌 be the number of forms required for the next applicant.
# The probability that 𝑦 forms are required is known to be proportional to 𝑦;
# that is, 𝑃(𝑌=𝑦)=𝑘𝑦 for 𝑦=1,...,5.

# What is k?
y <- 0
for (ii in 1:5) {
  y <- y + ii
}
y
k <- 1 / y
k

# What is the probability that at most three forms are required?
probability_of_partial_set <- function(start, end, total_count) {
  p_partial_set <- 0
  for (ii in start:end) {
    prob <- ii / total_count
    p_partial_set <- p_partial_set + prob
  }
  p_partial_set
}

p_three_or_less_required <- probability_of_partial_set(1, 3, y)
p_three_or_less_required

# What is the probability that between two and four forms are required?
two_to_four_required <- probability_of_partial_set(2, 4, y)
two_to_four_required

# Could 𝑃(𝑌=𝑦) = (𝑦**2)/50 for  𝑦=1,...,5 be the pmf of 𝑌?

determine_pmf <- function(limit, total_count) {
  pmf_found <- TRUE
  for (ii in 1:limit) {
    prob <- ii / total_count
    func_val <- (ii**2) / 50
    if (prob != func_val) {
      pmf_found <- FALSE
      break
    }
  }
  pmf_found
}

is_pmf <- determine_pmf(5, y)
is_pmf


# Individuals A and B play a sequence of chess games
# until one player wins 9 games. A wins an individual game with probability p,
# and B wins a game with probability 1 − p.
# Let X denote the number of games played.

# What are the possible values of X?
# need at least 9 games for one success
# at most we'd have one player with 8 wins and the other with 9; total is 17
chess_s <- c(9:17)
chess_s

# Let 𝑝=0.5. Find 𝑃(𝑋=12). Round your answer to four decimal places.
a_wins <- dnbinom(3, 9, 0.5)
p_x_12 <- round(2 * a_wins, 4)
p_x_12


# X = the leading digit of a randomly selected number from an accounting ledger.
# The pmf for this random variable has been found to be defined by:
# 𝑃(𝑋=𝑥)=𝑓(𝑥)=𝑙𝑜𝑔10(𝑥+1/𝑥),  𝑥=1,2,...,9.

# Find E(X). Round your answer to two decimal places.
expected_value <- 0
for (ii in 1:9) {
  prob <- log10((ii + 1) / ii)
  val <- ii * prob
  expected_value <- expected_value + val
}
expected_value <- round(expected_value, 2)
expected_value


# Suppose we have an unfair coin with a probability of 0.6
# of obtaining a heads on any given toss.
# As is typical for coin toss problems, assume each coin toss is independent.

# What is the expected number of flips before we get a heads?
# Round your answer to two decimal places.

# This is a negative binomial random variable. We are looking at expected value.
coin_p <- 0.6
coin_expected <- function(r, p) {
  round((r * (1 - p)) / p, 2)
}
expected_1head <- coin_expected(1, coin_p)
expected_1head

# How many tails do you expect to see before getting three heads?
expected_3heads <- coin_expected(3, coin_p)
expected_3heads