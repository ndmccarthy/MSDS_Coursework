# Problem 1
n <- 250
p_hat <- 112 / n
alpha <- 0.05
# check if normal dist will work
var_hat <- (p_hat * (1 - p_hat)) / n
s_hat <- sqrt(var_hat)
print(c(p_hat - 3 * s_hat, p_hat + 3 * s_hat))
# 0.3536461 0.5423539 is within [0,1]
# calculate interval
z <- qnorm(1 - alpha/2)
margin <- z * s_hat
print(c(p_hat - margin, p_hat + margin))

# Problem 2
n <- 150 # same sample size for sample 1 and sample 2
p1 <- 78/n
p2 <- 92/n
alpha <- 0.5
p_diff <- p2 - p1
# check for normality
v1 <- (p1 * (1 - p1))/n
v2 <- (p2 * (1- p2))/n
diff_v <- v1 + v2
diff_s <- sqrt(diff_v)
z <- qnorm(1 - alpha/2)
margin <- z * diff_s
print(c(p_diff - margin, p_diff + margin))

# Problem 3
data <- c(9.2229, 8.3665, 8.797058, 10.2195, 6.5629)
s <- sd(data)
v <- s^2
alpha <- 0.08
n <- length(data)
chi_lower <- qchisq(1 - alpha/2, n - 1, lower.tail = TRUE)
chi_upper <- qchisq(alpha/2, n - 1, lower.tail = TRUE)
operator <- v * (n - 1)
low_bound <- chi_lower / operator
high_bound <- chi_upper / operator
low_bound <- 1 / low_bound
high_bound <- 1 / high_bound
print(c(low_bound, high_bound))