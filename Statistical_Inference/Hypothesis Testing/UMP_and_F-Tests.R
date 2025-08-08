# Question 1
var_nought <- 16
n <- 10
s <- 5.2
v <- s^2
chi <- (v * (n - 1)) / var_nought
pchisq(chi, n-1, lower.tail = FALSE)

# Question 3
n1 <- 8
v1 <- 13.2
n2 <- 6
v2 <- 15.1
a <- 0.03
Fval <- v2/v1
(fstat <- qf(a/2, n2-1, n1-1, lower.tail = FALSE))
