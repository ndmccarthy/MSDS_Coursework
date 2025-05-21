# Suppose you roll a fair six-sided die two times.
# Let 𝐴 be the event "the sum of the throws equals 5"
# and 𝐵 be the event "at least one of the throws is a  4".
#
# By hand, solve for the probability that the sum of the throws equals 5,
# given that at least one of the throws is a 4. That is, solve 𝑃(𝐴|𝐵).
# This probability is 2 / 11, or approximately 0.182.
#
# Write a simple simulation to confirm your result.
# Make sure you run your simulation enough times to be confident in your result.

# Simulate values
roll1 <- sample(1:6, 1000, replace = TRUE)
roll2 <- sample(1:6, 1000, replace = TRUE)

# Put the two columns together ("cbind" stands for "column bind")
double_dice <- cbind(roll1, roll2)

# Change from a matrix to a data frame so that we can access elements
# using the names "roll1" and "roll2"
double_dice <- as.data.frame(double_dice)
double_dice$roll_sum <- double_dice$roll1 + double_dice$roll2

# Here is a subset of the data frame that you might want to look at.
# Recall that the squre brackets can be read as "such that".
event_b <- double_dice[double_dice$roll1 == 4 | double_dice$roll2 == 4,]
a_inter_b <- event_b[event_b$roll_sum == 5,]

cardinality <- 6 ** 2
num_event_b <- nrow(event_b)
p_b <- num_event_b / cardinality
num_a_inter_b <- nrow(a_inter_b)
p_a_inter_b <- num_a_inter_b / cardinality

p_a_given_b <- p_a_inter_b / p_b
p_a_given_b


# Suppose you have two bags of marbles that are in a box.
# Bag 1 contains 7 white marbles, 6 black marbles, and 3 gold marbles.
# Bag 2 contains 4 white marbles, 5 black marbles, and 15 gold marbles.
# You will reach into the box to pull out a bag.
# Suppose that, due to the size and shapes of the bags,
# the probability of grabbing Bag 1 from the box is
# twice the probability of grabbing Bag 2.
#
# If you close your eyes, grab a bag from the box,
# and then grab a marble from that bag, what is the probability that it is gold?
#
# When calculating this probability by hand, I got 1 /3.
#
# Create a simulation to estimate the probability of pulling a gold marble.
# Make sure to run the simulation enough times to be
# confident in your final result!

pick_marble <- function(bag) {
  if (bag == 1) sample(1:3, 1, prob = bag1_marble_probabilities)
  else if (bag == 2) sample(1:3, 1, prob = bag2_marble_probabilities)
}

bag_probabilities <- c(2 / 3, 1 / 3)
bag1_marble_probabilities <- c(7 / 16, 6 / 16, 3 / 16)
bag2_marble_probabilities <- c(4 / 24, 5 / 24, 15 / 24)

bag_choices <- sample(1:2, 1000, replace = TRUE, prob = bag_probabilities)
marble_choices <- sapply(bag_choices, FUN = pick_marble)

num_gold <- length(marble_choices[marble_choices == 3])
p_gold <- num_gold / 1000
p_gold
