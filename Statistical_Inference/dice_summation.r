# Consider rolling two fair six-sided dice.
# What is the probability that the
# sum of the results is greater than or equal to 5?

dice_sum <- function(num_dice, sum_min) {
  # calculate the probability that the number of dice
  # results in the sum_min or greater
  total_count <- 6 ** num_dice
  if (sum_min > num_dice * 6) {
    return("Summation not possible with this number of dice.")
  } else {
    # calculate the compliment as it is easier
    max_compliment <- sum_min - 2
    compliment_count <- sum(1:max_compliment)
    p_compliment <- compliment_count / total_count
    p_sum <- 1 - p_compliment
    p_sum
  }
}
dice_sum(2, 5)