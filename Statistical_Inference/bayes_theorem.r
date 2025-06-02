# The CU Boulder triathlon team has 12 women and 9 men.
# The team is going to a race and can only enter 5 participants.
# What is the probability of randomly selecting a race squad of
# 5 participants with exactly 3 women?
# Round your answer to three decimal places.
# Enter your solution into variable p1.1.

ncombinationx <- function(n, x) {
  factorial(n) / (factorial(n - x) * factorial(x))
}

# First find the number of ways to pick 3 women and 2 men.
women_count <- ncombinationx(12, 3)
men_count <- ncombinationx(9, 2)
favorable_possibilities <- women_count + men_count

# Get total number of possibilities to choose 5 people.
all_possibilities <- ncombinationx(12 + 9, 5)

p1_1 <- favorable_possibilities / all_possibilities
p1_1


# We’d like to know whether Newman is guilty of a crime.
# We are torn as to whether we think he is guilty:
# we think it’s equally likely that he is guilty or not guilty.
# Suppose that, in similar situations, we know that if a suspect is guilty,
# 85% of the time their finger prints are found at the scene, and,
# we know that if a suspect is not guilty,
# 30% of the time their finger prints are found at the scene.
#
# What is the probability that Newman’s finger prints are found at the scene?
# Round your answer to three decimal places.

# known information
p_f_given_g <- 0.85
p_f_given_i <- 0.3
p_g <- 0.5
p_i <- 0.5

# use law of total probability
p_f <- (p_f_given_g * p_g) + (p_f_given_i * p_i)
p_f

# If Newman’s finger prints are found at the scene,
# how likely is it that he is guilty?
# Round your answer to three decimal places.

# use Bayes Theory
p_g_given_f <- round((p_f_given_g * p_g) / p_f, 3)
p_g_given_f

# If Newman’s finger prints are not found at the scene,
# how likely is it that he is guilty?
# Round your answer to three decimal places.

# use Bayes Theory again
p_n <- 1 - p_f
p_n_given_g <- 1 - p_f_given_g
p_g_given_n <- round((p_n_given_g * p_g) / p_n, 3)
p_g_given_n


# The game of Yahtzee is played with five fair dice.
# The goal is to roll certain ‘hands’, such as Yahtzee
# (all five dice showing the same number) or a full house
# (three of a kind and two of a kind).
# In the first round of a player’s turn, the player rolls all five dice.
# Based on the outcome of that roll, the player has a second and third round,
# where he/she can then choose to re-roll any subset of the dice to get
# a desired hand.
#
# What is the probability of rolling a Yahtzee
# (all 5 dice showing the same number) on the first round?
# Round your answer to 4 decimal places.

yahtzee <- round((1 / 6) ** (5 - 1), 4)
yahtzee

# Suppose that, on the second round, the dice are {2, 3, 4, 6, 6}.
# You decide to re-roll both sixes in the third round.
# What is the probability that you roll either a small straight
# (exactly four dice are in a row) or a large straight
# (exactly five dice are in a row)?
# Round your answer to three decimal places.

check_for_lrg_straight <- function(five_dice) {
  dice_set <- sort(unique(five_dice))
  if (length(dice_set) == 5 && all(diff(dice_set) == 1)) {
    return(TRUE)
  }
  return(FALSE)
}

check_for_sm_straight <- function(five_dice) {
  dice_set <- sort(unique(five_dice))
  if (length(dice_set) == 5) {
    if (check_for_lrg_straight(dice_set)) {
      return(FALSE)
    } else {
      for (ii in 1:2) {
        if (all(diff(dice_set[ii:(ii + 3)]) == 1)) {
          return(TRUE)
        }
      }
    }
  } else if (length(dice_set) == 4) {
    if (all(diff(dice_set) == 1)) {
      return(TRUE)
    }
  }
  return(FALSE)
}

straight_count <- 0
for (die1 in 1:6) {
  for (die2 in 1:6) {
    rolls <- c(2, 3, 4, die1, die2)
    if (check_for_lrg_straight(rolls) == TRUE || check_for_sm_straight(rolls) == TRUE) {
      straight_count <- straight_count + 1
    }
  }
}
total_count <- 6 ** 2
p3_2 <- round(straight_count / total_count, 3)
p3_2

# What is the probability of rolling a small straight
# (exactly four dice in a row) on the first round?
# Round your answer to have three decimal places.

roll_5_dice <- function() {
  sample(1:6, 5, replace = TRUE)
}
sm_straight_achieved <- 0
for (ii in 1:1000) {
  roll <- roll_5_dice()
  if (check_for_sm_straight(roll) == TRUE) {
    sm_straight_achieved <- sm_straight_achieved + 1
  }
}
p3_3 <- round(sm_straight_achieved / 1000, 3)
p3_3


# In 2008, 3% of adults (age 25 or older) in Boulder, CO had a PhD,
# 45% had at least a bachelor’s degree, and 75% were employed full-time.
# Consider randomly selecting an adult from Boulder, CO for an interview.
# Let 𝐴 denote the event that the individual has a PhD,
# let 𝐵 be the event that the individual has a bachelor’s degree,
# and let 𝐶 be the event that the individual is employed full-time.
# Assume that, in order to have a PhD, you must have a bachelor’s degree.

# Is it possible for  𝑃(𝐴∩𝐵)=0.03?
# Enter your answer as a boolean TRUE or FALSE.
# Enter your solution into variable TF_4.1.

p_phd <- 0.03
p_bach <- 0.45
p_emp <- 0.75

# p_phd is encased by p_bach
TF_4_1 <- TRUE

# For the remaining questions, let 𝑃(𝐵∪𝐶)=0.75.
# Compute the probability that the selected individual
# has a bachelor’s degree and full time employment.
# Round your answer to two decimal points.
# Enter your solution into variable p4.2.

p_bach_or_emp <- 0.75
p_bach_and_emp <- p_bach + p_emp - p_bach_or_emp

# What is the probability that the selected individual
# has a bachelor’s degree given that they are employed full-time?
# Round your answers to two decimal places. Save your solution as variable p4.3.

p_bach_given_emp <- p_bach_and_emp / p_emp
p_bach_given_emp
