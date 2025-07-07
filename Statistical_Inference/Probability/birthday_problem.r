# The Birthday Problem
# This is a classic problem that has a nonintuitive answer.
# Suppose there are 𝑁 students in a room.
# We wish to figure out the probability that
# at least two of them have the same birthday (month and day).
# Assume that each day is equally likely to be a student's birthday,
# that there are no sets of twins, and that there are 365 days in the year.
# Do not include leap years.

birthday_problem <- function(n) {
  if (n > 365) {
    return(1)
  } else {
    1 - prod((365:(366 - n)) / 365)
  }
}

birthday_problem(23)

num_students <- 1:40
n_probability <- rep(0, 40)

for (i in 1:40) {
  n_probability[i] <- birthday_problem(i)
}

plot(num_students, n_probability)
