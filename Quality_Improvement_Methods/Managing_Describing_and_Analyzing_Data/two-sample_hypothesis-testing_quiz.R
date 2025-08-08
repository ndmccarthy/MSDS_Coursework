require(lolcat)
require(ggplot2)

# Question 7
alpha <- 0.01
delta_mu <- 1
n <- 20
s <- 2
se <- s / sqrt(n)
z <- delta_mu / se
pnorm(z, lower.tail = FALSE)
power.mean.t.onesample(sample.size = n,
                       effect.size = delta_mu,
                       variance.est = s^2,
                       alpha = alpha,
                       alternative = "two.sided")

# Question 8
beta <- 0.05
sample.size.mean.t.onesample(effect.size = delta_mu,
                             variance.est = s^2,
                             alpha = alpha,
                             beta = beta,
                             alternative = "two.sided")

# Question 11
earmuff_mu <- 72
earmuff_n <- 12
earmuff_s <- 15
foam_mu <- 64
foam_n <- 15
foam_s <- 19
delta_mu <- earmuff_mu - foam_mu
earmuff_se <- earmuff_s / sqrt(earmuff_n)
foam_se <- foam_s / sqrt(foam_n)
se <- sqrt(earmuff_se + foam_se)
t <- delta_mu / se
# Question 23
alpha <- 0.05
variance.test.twosample.independent.simple(sample.variance.g1 = earmuff_s^2,
                                           sample.size.g1 = earmuff_n,
                                           sample.variance.g2 = foam_s^2,
                                           sample.size.g2 = foam_n,
                                           conf.level = 1-alpha)

# Question 12
alpha <- 0.05
earmuff_part <- (earmuff_s ^ 2) / earmuff_n
foam_part <- (foam_s ^ 2) / foam_n
df <- ((earmuff_part + foam_part)^2) / ((earmuff_part^2)/(earmuff_n - 1) + (foam_part^2)/(foam_n - 1))
t_given <- qt(1 - alpha/2, df)
t.test.twosample.independent.simple(sample.mean.g1 = earmuff_mu,
                                    sample.variance.g1 = earmuff_s^2,
                                    sample.size.g1 = earmuff_n,
                                    sample.mean.g2 = foam_mu,
                                    sample.variance.g2 = foam_s^2,
                                    sample.size.g2 = foam_n,
                                    conf.level = 1 - alpha)

# Question 13 - 16
ToolLife <- read.delim("~/GitHub/MSDS_Coursework/Quality_Improvement_Methods/ToolLife.dat")
vendor1 <- as.vector(unlist(ToolLife$life[ToolLife$vendor == 1]))
vendor2 <- as.vector(unlist(ToolLife$life[ToolLife$vendor == 2]))
LifeSpan <- data.frame(vendor1, vendor2)
mean(LifeSpan$vendor1)
mean(LifeSpan$vendor2)
var(LifeSpan$vendor1)
var(LifeSpan$vendor2)

# Question 17-19
Straight <- read.delim("~/GitHub/MSDS_Coursework/Quality_Improvement_Methods/Straight.dat")
alpha <- 0.01
t.test.twosample.dependent.simple.meandiff(sample.mean.g1 = mean(Straight$before),
                                           sample.mean.g2 = mean(Straight$after),
                                           sample.variance.g1 = var(Straight$before),
                                           sample.variance.g2 = var(Straight$after),
                                           sample.size = length(Straight$before),
                                           conf.level = 1 - alpha)
t.test.twosample.dependent(Straight$before, Straight$after)

# Question 21-22
alpha <- 0.05
alloy_mean <- 3671
alloy_s <- 246
pure_mean <- 4228
pure_s <- 182
n <- 50
rho <- 0.78
t.test.twosample.dependent.simple.meandiff(sample.mean.g1 = alloy_mean,
                                           sample.mean.g2 = pure_mean,
                                           sample.variance.g1 = alloy_s^2,
                                           sample.variance.g2 = pure_s^2,
                                           sample.size = n,
                                           rho.estimate = rho,
                                           conf.level = 1-alpha)

# Question 26-30
Temper <- read.delim("~/GitHub/MSDS_Coursework/Quality_Improvement_Methods/Temper.dat")
alpha <- 0.05
summary.continuous(Temper)
variance.test.twosample.dependent.simple(sample.variance.g1 = var(Temper$before),
                                         sample.variance.g2 = var(Temper$after),
                                         sample.size = length(Temper$before),
                                         conf.level = 1 - alpha,
                                         rho.estimate = cor(Temper$before, Temper$after, method = "pearson"))
t.test.twosample.dependent.simple.meandiff(sample.mean.g1 = mean(Temper$before),
                                           sample.mean.g2 = mean(Temper$after),
                                           sample.variance.g1 = var(Temper$before),
                                           sample.variance.g2 = var(Temper$after),
                                           sample.size = length(Temper$before),
                                           conf.level = 1 - alpha)
t.test.twosample.dependent(Temper$before, Temper$after)
ggplot(data = Temper, mapping = aes(x = before, y = after)) + geom_smooth()

# Question 32
p1 <- 0.054
p2 <- 0.036
n <- 500
alpha <- 0.05
proportion.test.twosample.exact.simple(sample.proportion.g1 = p1,
                                       sample.size.g1 = n,
                                       sample.proportion.g2 = p2,
                                       sample.size.g2 = n)

# Question 35-36
b <- 34
c <- 4
n <- 150
alpha <- 0.05
proportion.test.mcnemar.simple(b = b, c = c)

# Question 37-38
alpha <- 0.05
count1 <- 15
n1 <- 2
count2 <- 10
n2 <- 1
poisson.test.twosample.simple(sample.count.g1 = count1,
                              sample.size.g1 = n1,
                              sample.count.g2 = count2,
                              sample.size.g2 = n2,
                              conf.level = 1 - alpha,
                              alternative = "two.sided")
