# Question 1
mu <- 40
n <- 10
xbar <- 38.8
s2 <- 2.8
lim <- (xbar - mu)/sqrt(s2/n)
2 *pt(lim, n-1)

# Question 2
n <- 15
xbar <- 53.87
s <- 6.82
# assume normality
mu <- 50
a <- 0.05
(t <- qt(1 - a, n-1))
se <- s/sqrt(n)
(c <- t*se + mu)

# Question 4
a.n <- 120
a.s <- 2.1
a.xbar <- 4.1
b.n <- 100
b.s <- 1.5
b.xbar <- 3.3
# assume normality
diff_means <- a.xbar - b.xbar
se <- sqrt((a.s^2/a.n) + (b.s^2/b.n))
z <- diff_means/se
