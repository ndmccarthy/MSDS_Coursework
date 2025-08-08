require(lolcat)


# Question 1 - 9
calls <- read.delim("~/GitHub/MSDS_Coursework/Quality_Improvement_Methods/Data_Files/calls.dat")

# create a subset for first and second periods
period1 <- subset(x = calls, subset = calls$call_period==1)
period2 <- subset(x = calls, subset = calls$call_period==2)

# create control chart for Period 1 and check for violations
# count and same n means np chart
period1.chart <- spc.chart.attributes.proportion.np.binomialdistribution.simple(nonconforming = period1$dropped_calls,
                                                                                sample.size = 250,
                                                                                chart1.main = "Period 1 np Chart")
any(period1.chart$chart1.is.control.violation$overall.results) # in control

# proportion of dropped calls in Period 1
p1.cbar <- unique(period1.chart$chart1.center.line)
(p1.p <- p1.cbar/250)

# Cpk for Period 1
# can use qnorm because large n
(p1.Cpk <- round(qnorm(p = p1.p, lower.tail = FALSE)/3, 4)) # 0.3588 means process is not capable

# create a control chart for Period 2 and check for violations
period2.chart <- spc.chart.attributes.proportion.np.binomialdistribution.simple(nonconforming = period2$dropped_calls,
                                                                                sample.size = 250,
                                                                                chart1.main = "Period 2 np Chart")
any(period2.chart$chart1.is.control.violation$overall.results) # in control

# proportion of dropped calls in Period 2
p2.cbar <- unique(period2.chart$chart1.center.line)
(p2.p <- p2.cbar / 250)

# Cpk for Period 2
(p2.Cpk <- round(qnorm(p = p2.p, lower.tail = FALSE)/3, 4)) # 0.256 means not capable
# Period 2 did not improve from Period 1



# Question 10 - 
errors <- read.delim("~/GitHub/MSDS_Coursework/Quality_Improvement_Methods/Data_Files/errors.dat")
# n = 5 for each sample

# separate into periods
period1 <- subset(x = errors, subset = errors$period==1)
period2 <- subset(x = errors, subset = errors$period==2)

# create  control chart for Period 1 and check for violations
# equivalent n and number of defects for a given unit size (5 cars) requires a c chart
period1.chart <- spc.chart.attributes.counts.c.poissondistribution.simple(counts = period1$defects,
                                                                          chart1.main = "Period 1 c Chart")
any(period1.chart$chart1.is.control.violation$overall.results) # in control

# check if Period 1 data from Poisson distribution
poisson.dist.test(period1$defects) # p-value = 0.1596 CORRECT

# calculate assembly error rate for Period 1
(p1.cbar <- mean(period1$defects)) # 16.32
#(p1.error_rate <- p1.cbar / 5) # 3.264

# create control chart for Period 2 and check for violations
period2.chart <- spc.chart.attributes.counts.c.poissondistribution.simple(counts = period2$defects,
                                                                          chart1.main = "Period 2 c Chart")
any(period2.chart$chart1.is.control.violation$overall.results) # in control

# check if Period 2 is from Poisson distribution
poisson.dist.test(period2$defects) # p-value = 0.9557 CORRECT

# assembly error rate for Period 2
(p2.cbar <- mean(period2$defects)) # 7.92
#(p2.error_rate <- p2.cbar / 5) # 1.584

# check if error rate has changed between periods
poisson.test.twosample.simple(sample.count.g1 = sum(period1$defects),
                              sample.size.g1 = length(period1$defects) * 5,
                              sample.count.g2 = sum(period2$defects),
                              sample.size.g2 = length(period2$defects) * 5)
# p-value < 2.2e-16 == rates are not the same 

# What percentage of the time in Period 2 would you expect to have 11+ errors?
round((1 - ppois(10, lambda = p2.cbar, lower.tail = TRUE)) * 100, 4) # 17.6253%
      