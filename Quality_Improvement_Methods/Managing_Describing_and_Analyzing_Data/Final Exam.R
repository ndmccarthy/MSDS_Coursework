require(lolcat)

# Part 1
height <- read.csv("~/GitHub/MSDS_Coursework/Quality_Improvement_Methods/height.dat", sep="")
defectives <- read.csv("~/GitHub/MSDS_Coursework/Quality_Improvement_Methods/defectives.dat", sep="")
defects <- read.csv("~/GitHub/MSDS_Coursework/Quality_Improvement_Methods/defects.dat", sep="")

summary.continuous(height)
height <- as.vector(unlist(height))
anderson.darling.normality.test(height) # normal distribution found
pnorm(q = 4.802, mean = mean(height), sd = sd(height))
mean(height)
t.test.onesample.simple(sample.mean = mean(height),
                        sample.variance = var(height),
                        sample.size = length(height),
                        conf.level = 0.95)
t.test(height)

defectives <- as.vector(unlist(defectives))
anderson.darling.normality.test(height) # normal distribution found
pnorm(q = 3, mean = mean(defectives), sd = sd(defectives), lower.tail = FALSE)
defectives_p <- mean(defectives)/100
proportion.test.onesample.exact.simple(sample.proportion = defectives_p,
                                       sample.size = length(defectives),
                                       conf.level = 0.9)

defects <- as.vector(unlist(defects))
anderson.darling.normality.test(defects)
shapiro.wilk.exponentiality.test(defects)
poisson.dist.test(defects) # Poisson distribution found
ppois(q = 0, lambda = mean(defects), lower.tail = TRUE)

# Part 2
alpha <- 0.025
beta <- 0.01
delta_mu <- 5
s <- 2
delta_s <- 1
sample.size.mean.z.onesample(effect.size = delta_mu,
                             variance = s^2,
                             alpha = alpha,
                             beta = beta,
                             alternative = "two.sided")
sample.size.variance.onesample(null.hypothesis.variance = s^2,
                               alternative.hypothesis.variance = (s + delta_s)^2,
                               alpha = alpha,
                               beta = beta,
                               alternative = "two.sided")
sample.size.variance.onesample(null.hypothesis.variance = s^2,
                               alternative.hypothesis.variance = (s - delta_s)^2,
                               alpha = alpha,
                               beta = beta,
                               alternative = "two.sided")

#Part 3
pushforce <- read.csv("~/GitHub/MSDS_Coursework/Quality_Improvement_Methods/pushforce.dat", sep="")
alpha <- 0.05
line1 <- pushforce[pushforce$Line == 1, 2]
line2 <- pushforce[pushforce$Line == 2, 2]
line_forces <- data.frame(line1, line2)
summary.continuous(pushforce)
variance.test.twosample.independent(line_forces$line1, line_forces$line2)
t.test.twosample.independent(line_forces$line1, line_forces$line2)

# Part 4
spa <- read.csv("~/GitHub/MSDS_Coursework/Quality_Improvement_Methods/spa.dat", sep="")
claimed_mean <- 17
alpha <- 0.05
summary.continuous(spa)
variance.test.twosample.dependent(spa$Before, spa$After, alternative = "two.sided", conf.level = 1 - alpha, assume.normality = "yes")
t.test.twosample.dependent(spa$Before, spa$After, alternative = "two.sided", conf.level = 1 - alpha)

# Part 5
cracked <- read.csv("~/GitHub/MSDS_Coursework/Quality_Improvement_Methods/cracked.dat", sep="")
alpha <- 0.1
plant1 <- cracked[cracked$Line == 1, 2]
plant2 <- cracked[cracked$Line == 2, 2]
n1 <- length(plant1)
n2 <- length(plant2)
p1 <- 1 - sum(plant1)/n1
p2 <- 1 - sum(plant2)/n2
proportion.test.twosample.exact.simple(sample.proportion.g1 = p1,
                                       sample.size.g1 = n1,
                                       sample.proportion.g2 = p2,
                                       sample.size.g2 = n2,
                                       conf.level = 1 - alpha)
variance.test.twosample.independent(plant1, plant2, alternative = "two.sided", conf.level = 1 - alpha, assume.normality = "no")
