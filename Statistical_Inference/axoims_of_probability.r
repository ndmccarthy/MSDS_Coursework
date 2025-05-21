# Suppose we are interested in the buying habits of shoppers
# at a particular grocery store with regards to whether they
# purchase apples, milk, and/or bread. Now suppose 30% of all
# shoppers at this particular grocery store buy apples, 45%
# buy milk, and 40% buy a loaf of bread. Let 𝐴 be the event
# that a randomly selected shopper buys apples, 𝐵 be the event
# that the same randomly selected shopper buys milk, and  𝐶
# the event that they buy bread. Suppose we also know (from
# data collected) the following information:
#
# The probability that the shopper buys apples and milk is 0.20.
# The probability that the shopper buys milk and bread is 0.25.
# The probability that the shopper buys apples and bread is 0.12.
# The probability that the shopper buys all three items is 0.07.


# For our purposes, we will use a numeric representation for each
# event. For example, (010) would be an event in the sample space
# where a zero in the first place represents no apples were bought
# while a 1 means they were. Similarly, the second place is the presence
# of milk and the third place of bread. The example given (010) represents
# the purchase of milk but not apples or bread.
# Insert into vector S the events that belong to the sample space.
# Then insert the events from the sample space that would correspond to 𝐴
# occuring into vector A. Repeat this with vector B for 𝐵 and vector C for 𝐶.

s <- c()
a <- c()
b <- c()
c <- c()

check_event_membership <- function(event) {
  a_member <- event >= 100
  b_member <- (event >= 10 && event < 100) || event >= 110
  c_member <- event %% 10 == 1
  c(a_member, b_member, c_member)
}

for (ii in 1:8) {
  # 8 because 2^3=8 and we have 2 choices (0 or 1) to make 3 times (a, b, c)
  # initialize event vector
  event <- 0
  # make a present for last 4 events
  if (ii > 4) event <- event + 100
  # make b present for middle 4 events
  if (ii > 2 && ii < 7) event <- event + 10
  # make c present for every other event (when ii is even)
  if (ii %% 2 == 0) event <- event + 1
  # append all events to s and then append to appropriate vectors
  s <- append(s, event)
  membership <- check_event_membership(event)
  if (membership[1]) a <- append(a, event)
  if (membership[2]) b <- append(b, event)
  if (membership[3]) c <- append(c, event)
}

# Find the probability that the shopper purchases at least
# one of the three items. Store answer in p1_1.
# store probabilities of each outcome in a vector
s_p <- c(0.35, 0.1, 0.07, 0.18, 0.13, 0.07, 0.05, 0.05)

check_at_least_1 <- function(set) {
  results <- set > 0
  results
}
probability_of_check <- function(check_results, probability_vector) {
  true_ids <- which(check_results == TRUE)
  relevant_probabilities <- probability_vector[true_ids]
  answer <- sum(relevant_probabilities)
  answer
}
p1_1 <- probability_of_check(check_at_least_1(s), s_p)
p1_1

# Find the probability that the shopper purchases none of the three items.
# Store your answer in a variable p1_2.

check_none <- function(set) {
  results <- set == 0
  results
}
p1_2 <- probability_of_check(check_none(s), s_p)
p1_2

# Find the probability that the shopper buys milk and bread but not apples.
# Store your answer in a variable p1_3.

check_2_not_3 <- function(set, excluded_itemset) {
  # excluded_itemset must be a string
  membership_matrix <- t(sapply(set, check_event_membership))
  colnames(membership_matrix) <- c("a", "b", "c")
  included_itemsets <- setdiff(c("a", "b", "c"), excluded_itemset)
  apply(membership_matrix, 1, function(row) {
    row[excluded_itemset] == FALSE && all(row[included_itemsets] == TRUE)
  })
}
p1_3 <- probability_of_check(check_2_not_3(s, "a"), s_p)
p1_3

# A student takes a multiple choice test with  20 questions.
# Each question has 5 possible answers, only one of which is correct.

cardinality <- 5 ** 20

# If a student answers each question at random, what is the probability that
# they will answer at least 14 questions correctly?
# Round your answer to seven decimal places. Store your answer in p2_b.

ncombinationx <- function(n, x) {
  factorial(n) / (factorial(n - x) * factorial(x))
}

binomial_distribution <- function(n, x, p) {
  q <- 1 - p
  diff <- n - x
  ncx <- ncombinationx(n, x)
  ncx * (p ** x) * (q ** diff)
}

p2_b <- round(binomial_distribution(20, 14, 1 / 5),  7)
p2_b

# If a student knows the answer to each question with probability  0.9,
# what is the chance they will answer at least  14 correctly?
# Round your answer to four decimal places. Save your answer as p2_c.

p2_c <- round(binomial_distribution(20, 14, 0.9), 4)
p2_c

# There are 20 employees on the day shift, 15 on swing, and 10 on nights.
# You would like to choose 6 at random for an in-depth interview. Let 𝐴1 be the
# event that all 6 are chosen from the day shift, 𝐴2 be the event that all  6
# are chosen from the swing shift, and  𝐴3 the event that all 6 are chosen from
# the night shift.

# What is the cardinality of the sample space
# (the drawing of 6 employees from all shifts)?

# The cardinality is looking at combinations since order doesn't matter.

size <- ncombinationx(45, 6)
size

# Assuming that each employee is chosen with equal probaiblity,
# what is the probability that all 6 chosen employees work the day shift?
# Note that the employees are chosen sequentially, not all at once.
# Round your answer to 5 decimal places. Save your answer as p_allday.

day_shift <- 20
swing_shift <- 15
night_shift <- 10
total_employees <- day_shift + swing_shift + night_shift

day_combos <- ncombinationx(day_shift, 6)

p_allday <- round(day_combos / size, 5)
p_allday

# What is the probability that all 6 workers are selected from the same shift?
# Again, assume the employees are selected sequentially and not all at once.
# Round your answer to four decimal places. Save your answer as P_AllSame.

# I need to calculate the combinations of each shift and add them together.
# Then I can divide that by the total combinations.

swing_combos <- ncombinationx(swing_shift, 6)
night_combos <- ncombinationx(night_shift, 6)
single_shift_combos <- day_combos + swing_combos + night_combos
p_allsame <- round(single_shift_combos / size, 4)
p_allsame

# Find the probability that at least one of the shifts will be unrepresented in
# the sample of 6 workers. Round your answer to four decimal places.
# Save your answer as P_NoneOfOneShift.

# I need to calculate the combinations of each two shift combo
# and then one shift combos to make sure I'm not overcounting.
# Then I can divide by size.

day_swing <- ncombinationx(day_shift + swing_shift, 6)
day_night <- ncombinationx(day_shift + night_shift, 6)
swing_night <- ncombinationx(swing_shift + night_shift, 6)
two_shift_combos <- day_swing + day_night + swing_night

p_noneofoneshift <- round((two_shift_combos - single_shift_combos) / size, 4)
p_noneofoneshift
