# Problem 1
p0 <- 0.6
n <- 100
p1 <- 0.68
alpha <- 0.03
# test for normality
s <- sqrt((p1 * (1 - p1))/n)
p1 - 3 * s
p1 + 3 * s
# normality ok
z <- qnorm(1 - alpha, lower.tail = TRUE)
# reject H0 if p1 > c
z * s + p0

# Problem 2
samp <- c(179, 156, 167,183, 178, 165)
sigma <- 4.2
mu <- 170
alpha <- 0.2
# Reject H0 if Xbar > c
z <- qnorm(1 - alpha, lower.tail = TRUE)
c <- z * sigma + mu
Xbar <- mean(samp)
Xbar > c
1 - pnorm(z)

# Problem 4
n <- 10
Xbar <- 232
s <- 15
mu <- 220
alphas <- seq(0, 1, 0.001)
zs <- qnorm(1 - alphas)
se <- s/n
cs <- zs * se + mu
phis <- pnorm(zs)
plot(x = cs, y = phis)

# Problem 5
mu <- 14
sigma <- 0.08
n <- 20
Xbar <- 13.8
alpha <- 0.05
z <- qnorm(1 - alpha/2)
# reject H0 (mu0 = 14) if Xbar < mu - c OR Xbar > mu + c
se <- sigma/sqrt(n)
c <- mu + z * se
cneg <- mu - z * se
