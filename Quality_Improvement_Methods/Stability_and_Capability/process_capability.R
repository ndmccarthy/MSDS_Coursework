require(lolcat)
require(fitdistrplus)

# Question 1 - 7
BagWeight <- read.delim("~/GitHub/MSDS_Coursework/Quality_Improvement_Methods/Data_Files/BagWeight.dat")
target <- 110
USL <- 112
LSL <- 108
summary.continuous(BagWeight$Bag_Weight) # normal distribution
bag.chart <- spc.chart.variables.mean.and.meanstandarddeviation(data = BagWeight$Bag_Weight,
                                       sample = BagWeight$Week,
                                       chart1.main = "Average Bag Weights",
                                       chart2.main = "Standard Deviation of Bag Weight Samples (n=5)")
lapply(bag.chart$chart1.is.control.violation$rule.results,
       FUN = function(v){any(v)})
sbar <- unique(bag.chart$chart2.center.line)
c4 <- spc.constant.calculation.c4(length(BagWeight$Bag_Weight))
sigma.est <- sbar/c4
xbarbar <- unique(bag.chart$chart1.center.line)
nt.bag <- natural.tolerance.normal(BagWeight$Bag_Weight)
(bag.cp <- round(spc.capability.cp.simple(lower.specification = LSL,
                                    upper.specification = USL,
                                    process.center = xbarbar,
                                    process.natural.tolerance = nt.bag$natural.tolerance), 4))
(bag.cpk <- round(spc.capability.cpk.simple(lower.specification = LSL,
                                            upper.specification = USL,
                                            process.variability = sigma.est,
                                            process.center = xbarbar,
                                            n.sigma = 6), 4))
(bag.cpm <- round(spc.capability.cpm.simple(lower.specification = LSL,
                                            upper.specification = USL,
                                            process.variability = sigma.est,
                                            process.center = xbarbar,
                                            nominal.center = target,
                                            n.sigma = 6) ,4))
hist.grouped(BagWeight$Bag_Weight, main = "Bag Weight Distribution",
             stat.lsl = LSL, stat.target = target, stat.usl = USL)
hist.add.distribution.curve.normal(BagWeight$Bag_Weight)
expect.low <- pnorm(LSL, mean = mean(BagWeight$Bag_Weight), sd = sd(BagWeight$Bag_Weight), lower.tail = TRUE)
expect.upp <- pnorm(USL, mean = mean(BagWeight$Bag_Weight), sd = sd(BagWeight$Bag_Weight), lower.tail = FALSE)
(total.expect <- round((expect.low + expect.upp) * 100, 4))

round((USL - LSL)/(6*sd(BagWeight$Bag_Weight)), 4) # correct Cp

round(pnorm(USL, mean = mean(BagWeight$Bag_Weight), sd = sd(BagWeight$Bag_Weight), lower.tail = FALSE)/3, 4) # Cpk

round((USL-LSL)/(6 * sqrt(var(BagWeight$Bag_Weight) + (mean(BagWeight$Bag_Weight) - target)^2)), 4)

weights <- c(unlist(BagWeight$Bag_Weight))
spc.capability.summary.normal.simple(stat.lsl = LSL,
                                     stat.target = target,
                                     stat.usl = USL,
                                     process.center = mean(weights),
                                     process.variability.estimate = var(weights),
                                     process.n.upper = sum(weights > USL),
                                     process.n.lower = sum(weights < LSL),
                                     process.n = length(weights))

# Question 8 - 14
ShearedSheet <- read.delim("~/GitHub/MSDS_Coursework/Quality_Improvement_Methods/Data_Files/ShearedSheet.dat")
target <- 0
USL <- 7
LSL <- NA
summary.continuous(ShearedSheet$Width_Deviation) # not normal
shapetest.exp.epps.pulley.1986(ShearedSheet$Width_Deviation) # exponential distribution
hist.grouped(ShearedSheet$Width_Deviation, main = "Shear Width Distribution",
             stat.usl = USL, stat.target = target)
hist.add.distribution.curve.exp(ShearedSheet$Width_Deviation)

shear.mr <- c(abs(diff(ShearedSheet$Width_Deviation)))
summary.continuous(shear.mr) # not normal
shapetest.exp.epps.pulley.1986(shear.mr + 1) # not exponential
hist.grouped(shear.mr,
             anchor.value = 0,
             main = "Shear Width Moving Range Distribution",
             freq = F)
start.gamma <- mmedist(shear.mr, distr = "gamma")
start <- as.list(start.gamma$estimate)
shear.mr.fit <- fitdist(shear.mr, distr = "gamma", start = start)
gofstat(shear.mr.fit, fitnames = "gamma") # likely a gamma distribution
mr.shape <- shear.mr.fit$estimate[1]
mr.rate <- shear.mr.fit$estimate[2]

mrbar <- mean(shear.mr)
tail <- 0.00135
(mr.UCL <- qgamma(1 - tail, shape = mr.shape, rate = mr.rate))
(mr.LCL <- qgamma(tail, shape = mr.shape, rate = mr.rate)) # not used because not necessary?

sw.chart <- spc.chart.variables.individual.and.movingrange.exponential.low.simple(individuals = ShearedSheet$Width_Deviation,
                                                                                  low = target,
                                                                                  chart2.control.limits.ucl = mr.UCL,
                                                                                  chart2.center.line = mrbar,
                                                                                  chart2.control.limits.lcl = NA)
lapply(sw.chart$chart1.is.control.violation$rule.results,
       FUN = function(v){any(v)})
lapply(sw.chart$chart2.is.control.violation$rule.results,
       FUN = function(v){any(v)})
ind.median <- median(ShearedSheet$Width_Deviation)
ind.mean <- mean(ShearedSheet$Width_Deviation)
lambda.hat <- 1/ind.mean
nt.sw <- natural.tolerance.exp(ShearedSheet$Width_Deviation)
(expect.upp <- pexp(q = USL, rate = lambda.hat, lower.tail =  FALSE))
(sw.cap <- spc.capability.summary.ungrouped.nonnormal.simple.R(stat.lsl = LSL,
                                                               stat.target = target,
                                                               stat.usl = USL,
                                                               process.center.capability = ind.median,
                                                               process.center.performance = ind.mean,
                                                               process.variability = var(ShearedSheet$Width_Deviation),
                                                               process.n.upper = sum(ShearedSheet$Width_Deviation > USL),
                                                               process.n = length(ShearedSheet$Width_Deviation),
                                                               natural.tolerance = nt.sw$natural.tolerance,
                                                               p.upper = expect.upp))
expect.upp*100

# Question 15 - 21
Furnace <- read.delim("~/GitHub/MSDS_Coursework/Quality_Improvement_Methods/Data_Files/Furnace2.dat")
rzt <- c(unlist(Furnace$RZT))
target <- 1.285
USL <- 1.34
LSL <- 1.23
start.gamma <- mmedist(Furnace$RZT, distr = "gamma")
start <- as.list(start.gamma$estimate)
rzt.fit <- fitdist(Furnace$RZT, distr = "gamma", start = start)
rzt.shape <- rzt.fit$estimate[1]
rzt.rate <- rzt.fit$estimate[2]
hist.grouped(Furnace$RZT,  stat.lsl = LSL, stat.target = target, stat.usl = USL)
(UCL <- qgamma(1 - tail, shape = rzt.shape, rate = rzt.rate))
(LCL <- qgamma(tail, shape = rzt.shape, rate = rzt.rate))

rzt.mr <- c(abs(diff(rzt)))
hist.grouped(rzt.mr)
#time to test which distribution fits best
distributions <- c("norm", "lnorm", "exp", "gamma", "logis", "beta")
fit_results <- rep(NA, length(distributions))
for (ii in seq(1, length(distributions), 1)) {
  distribution <- distributions[ii]
  mr.mme <- mmedist(rzt.mr, distr = distribution)
  mr.start <- as.list(mr.mme$estimate)
  rzt.mr.fit <- fitdist(rzt.mr, distr = distribution, start = mr.start)
  goodness <- gofstat(rzt.mr.fit, fitnames = distribution)
  fit_results[ii] <- goodness$bic
}
(fit.df <- data.frame(distributions, fit_results))
# appears to be a gamma distribution
mr.mme <- mmedist(rzt.mr, distr = "gamma")
mr.start <- as.list(mr.mme$estimate)
rzt.mr.fit <- fitdist(rzt.mr, distr = "gamma", start = mr.start)
mr.shape <- rzt.mr.fit$estimate[1]
mr.rate <- rzt.mr.fit$estimate[2]

(mr.UCL <- qgamma(1 - tail, shape = mr.shape, rate = mr.rate))
(mr.LCL <- qgamma(tail, shape = mr.shape, rate = mr.rate))

rzt.chart <- spc.chart.variables.individual.and.movingrange.generic.simple(individuals = Furnace$RZT,
                                                                           chart1.center.line = median(Furnace$RZT),
                                                                           chart1.control.limits.ucl = UCL,
                                                                           chart1.control.limits.lcl = LCL,
                                                                           chart2.center.line = mean(rzt.mr),
                                                                           chart2.control.limits.lcl = mr.LCL,
                                                                           chart2.control.limits.ucl = mr.UCL)
f <- function(p, lower.tail){
  qgamma(p = p, shape = rzt.shape, rate = rzt.rate, lower.tail =  lower.tail)
}
(nt.rzt <- natural.tolerance(f))
(expect.low <- pgamma(LSL, shape = rzt.shape, rate = rzt.rate, lower.tail = TRUE))
(expect.upp <- pgamma(USL, shape = rzt.shape, rate = rzt.rate, lower.tail = FALSE))
(rzt.cap <- spc.capability.summary.ungrouped.nonnormal.simple.R(stat.lsl = LSL,
                                                                stat.target = target,
                                                                stat.usl = USL,
                                                                process.center.capability = median(rzt),
                                                                process.center.performance = mean(rzt),
                                                                process.variability = var(rzt),
                                                                process.n.upper = sum(rzt > USL),
                                                                process.n.lower = sum(rzt < LSL),
                                                                process.n = length(rzt),
                                                                natural.tolerance = nt.rzt$natural.tolerance,
                                                                p.lower = expect.low,
                                                                p.upper = expect.upp))
(expect.low + expect.upp) * 100
