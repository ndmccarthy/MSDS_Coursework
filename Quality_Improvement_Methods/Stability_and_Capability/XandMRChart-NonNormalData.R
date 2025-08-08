require(lolcat)
require(fitdistrplus)

# Question 1 - 6
BagWeightsDev <- read.csv("~/GitHub/MSDS_Coursework/Quality_Improvement_Methods/Data_Files/BagWeightsDev.dat", sep="")
addition <- 2 * abs(min(BagWeightsDev$Deviation))
trans.devs <- log(addition + BagWeightsDev$Deviation)
summary.continuous(trans.devs) # now has a normal distribution
nt.trans <- natural.tolerance.normal(x = trans.devs)
(UNPL.trans <- round(nt.trans$upper.limit, 4))
(LNPL.trans <- round(nt.trans$lower.limit, 4))
(UNPL <- round(exp(mean(trans.devs) + 3 * sd(trans.devs)) - addition, 4))
(LNPL <- round(exp(LNPL.trans) - addition, 4))
wtdev.cc <- spc.chart.variables.individual.and.movingrange.generic.simple(individuals = BagWeightsDev$Deviation,
                                                                          chart1.center.line = median(BagWeightsDev$Deviation),
                                                                          chart1.control.limits.ucl = UNPL,
                                                                          chart1.control.limits.lcl = LNPL,
                                                                          chart1.main = "Individual Bag Weight Deviations")
lapply(wtdev.cc$chart1.is.control.violation$rule.results,
       FUN = function(v){any(v)})

# Problem 7 - 13
GreetTime <- read.csv("~/GitHub/MSDS_Coursework/Quality_Improvement_Methods/Data_Files/Store Greeting.dat", sep="")
times <- c(unlist(GreetTime$Time))
summary.continuous(times) # not normal
shapiro.wilk.exponentiality.test(times) # exponential distribution
(nt.times <- natural.tolerance.exp(x = times))
(UNPL <- round(nt.times$upper.limit, 4))
(LNPL <- round(nt.times$lower.limit, 4))
rate.times <- 1 / mean(times)
set.seed(100)
mc.vals <- rexp(10000, rate = rate.times)
mc.mr <- c(abs(diff(mc.vals)))
nt.mc.mr <- natural.tolerance.exp(x= mc.mr)
(UNPL.mr <- round(nt.mc.mr$upper.limit, 4))
(LNPL.mr <- round(nt.mc.mr$lower.limit, 5))
times.cc <- spc.chart.variables.individual.and.movingrange.generic.simple(individuals = times,
                                                                              chart1.control.limits.ucl = UNPL,
                                                                              chart1.control.limits.lcl = LNPL,
                                                                              chart1.center.line = mean(times),
                                                                              chart2.control.limits.lcl = LNPL.mr,
                                                                              chart2.control.limits.ucl = UNPL.mr,
                                                                              chart2.center.line = mr.mean)
lapply(times.cc$chart1.is.control.violation$rule.results,
       FUN = function(v){any(v)})
lapply(times.cc$chart2.is.control.violation$rule.results,
       FUN = function(v){any(v)})

# Problem 14 - 22
Furnace <- read.csv("~/GitHub/MSDS_Coursework/Quality_Improvement_Methods/Data_Files/Furnace2.dat", sep="")
rzt <- c(unlist(Furnace$RZT))
(start.gamma <- mmedist(rzt, distr = "gamma"))
(start <- as.list(start.gamma$estimate))
(rzt_fit <- fitdist(rzt, distr = "gamma", start = start))
alpha <- rzt_fit$estimate[1]
beta <- rzt_fit$estimate[2]
qval <- 1 - 0.00135
(UNPL <- round(qgamma(qval, shape = alpha, rate = beta), 4))
(LNPL <- round(qgamma(1 - qval, shape = alpha, rate = beta), 4))
(mr.rzt <- c(abs(diff(rzt))))
start.gamma.mr <- mmedist(mr.rzt, distr = "gamma")
(mr.start <- as.list(start.gamma.mr$estimate))
(mr.fit <- fitdist(mr.rzt, distr = "gamma", start = mr.start))
mr.a <- mr.fit$estimate[1]
mr.b <- mr.fit$estimate[2]
(UNPL.mr <- round(qgamma(qval, shape = mr.a,  rate = mr.b), 4))
(LNPL.mr <- round(qgamma(1 - qval, shape = mr.a, rate = mr.b), 4))
rzt_chart <- spc.chart.variables.individual.and.movingrange.generic.simple(individuals = rzt,
                                                                           chart1.main = "RZT Individuals",
                                                                           chart1.control.limits.lcl = LNPL,
                                                                           chart1.control.limits.ucl = UNPL,
                                                                           chart2.control.limits.lcl = LNPL.mr,
                                                                           chart2.control.limits.ucl = UNPL.mr,
                                                                           chart2.main = "RZT Moving Range")
lapply(rzt_chart$chart1.is.control.violation$rule.results,
       FUN = function(v){any(v)})
lapply(rzt_chart$chart2.is.control.violation$rule.results,
       FUN = function(v){any(v)})
