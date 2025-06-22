# Let 𝑋 be a random variable such that 𝐸(𝑋)=3, 𝑠𝑑(𝑋)=4,
# and let 𝑌 be a r.v. such that 𝐸(𝑌)=1, 𝑠𝑑(𝑌)=2.
# 𝑋 and 𝑌 are not linearly independent, and 𝑐𝑜𝑟𝑟(𝑋,𝑌)=0.5.

ex <- 3
sx <- 4
ey <- 1
sy <- 2
corrxy <- 0.5

# What is 𝐸(𝑋+3𝑌+1)?
# E(X + 3Y + 1) = E(X) + [3 * E(Y)] + 1
e1.1 <- ex + (3 * ey) + 1
e1.1

# What is 𝑠𝑑(4𝑋+2𝑌+2)? Round your answer to two decimal places.
# sd(4X + 2Y + 2) = [V(4X + 2Y + 2)]**0.5
# V(4X + 2Y + 2) = V(4X + 2Y) + 0
# V(4X + 2Y) = V(4X) + V(2Y) + (2*4*2)Cov(X,Y)
# V(4X + 2Y) = 16V(X) + 4V(Y) + 16covxy
vx <- sx**2
vy <- sy**2
covxy <- corrxy * sx * sy
v4x2y <- 16 * vx + 4 * vy + 16 * covxy
sd1.2 <- round(v4x2y**0.5, 2)
sd1.2

# What is 𝐸(3𝑋−2𝑌−10)?
# 𝐸(3𝑋−2𝑌−10) = 3E(X) - 2E(Y) - 10
e1.3 <- 3 * ex - 2 * ey - 10
e1.3

# What is 𝑠𝑑(3𝑋−3𝑌−5)? Round your answer to two decimal places.
# sd(3X - 3Y - 5) = [V(3X - 3Y - 5)]**0.5
# V(3X - 3Y - 5) = 9V(X) + 9V(Y) - 18covxy
v3x_3y <- 9 * vx + 9 * vy - 18 * covxy
sd1.4 <- round(v3x_3y**0.5, 2)
sd1.4


# PROBLEM 2
# setting up joint distribution table in data frame
y7 <- c(0.05, 0.05, 0)
y9 <- c(0.05, 0.1, 0.2)
y10 <- c(0.1, 0.35, 0.1)
rows <- c("x7", "x9", "x10")
joint_dist_tbl <- data.frame(y7, y9, y10, row.names = rows)
joint_dist_tbl

# What is  𝐶𝑜𝑣(𝑋,𝑌)? Round your answer to three decimal places.
# store x/y values for easy use
vals <- c(7, 9, 10)

# get expected value of x
find_expected_value <- function(is_rows, probability_table, values) {
  if (is_rows == TRUE) {
    x_probs <- rowSums(probability_table)
  } else{
    x_probs <- colSums(probability_table)
  }
  x_expecteds <- values * x_probs
  expected_value <- sum(x_expecteds)
  round(expected_value, 3)
}

ex <- find_expected_value(TRUE, joint_dist_tbl, vals)

# get expected value of y
ey <- find_expected_value(FALSE, joint_dist_tbl, vals)

# get expected value of XY
find_joint_expected <- function(values, probability_table) {
  exy <- 0
  for (row in c(1:3)){
    xval <- values[row]
    for (col in c(1:3)){
      yval <- values[col]
      prob <- probability_table[row, col]
      exy <- exy + (xval * yval * prob)
    }
  }
  round(exy, 3)
}

exy <- find_joint_expected(vals, joint_dist_tbl)

# calculate cov
find_cov <- function(e1, e2, e12) {
  cov <- e12 - (e1 * e2)
  round(cov, 3)
}

cov.xy <- find_cov(ex, ey, exy)

# Suppose the random variables measure the cost of each part in dollars,
# rather than hundreds of dollars.
# In this case, the random variables would be 𝑈=100𝑋 and 𝑉=100𝑌.
# What is  𝐶𝑜𝑣(𝑈,𝑉)?
new_vals <- vals * 100
euv <- find_joint_expected(new_vals, joint_dist_tbl)
eu <- find_expected_value(TRUE, joint_dist_tbl, new_vals)
ev <- find_expected_value(FALSE, joint_dist_tbl, new_vals)
cov.uv <- find_cov(eu, ev, euv)
cov.uv

# What is the correlation coefficient 𝜌𝑋,𝑌? Save this value as rho.xy.
# What is the correlation coefficient 𝜌𝑈,𝑉? Save this value as rho.uv.
# Round your answers to three decimal places.

# find variation in X and Y
find_var <- function(is_rows, values, probability_table) {
  mean <- find_expected_value(is_rows, probability_table, values)
  mean_sq <- mean ** 2
  values_sq <- values ** 2
  e_xsq <- find_expected_value(is_rows, probability_table, values_sq)
  e_xsq - mean_sq # gives variation
}

find_correlation_coefficient <- function(covariation, sd1, sd2) {
  corr <- covariation / (sd1 * sd2)
  round(corr, 3)
}

vx <- find_var(TRUE, vals, joint_dist_tbl)
vy <- find_var(FALSE, vals, joint_dist_tbl)

sx <- vx ** 0.5
sy <- vy ** 0.5

rho.xy <- find_correlation_coefficient(cov.xy, sx, sy)
rho.xy

vu <- find_var(TRUE, new_vals, joint_dist_tbl)
vv <- find_var(FALSE, new_vals, joint_dist_tbl)

su <- vu ** 0.5
sv <- vv ** 0.5

rho.uv <- find_correlation_coefficient(cov.uv, su, sv)
rho.uv
