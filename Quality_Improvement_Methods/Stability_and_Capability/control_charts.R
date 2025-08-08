require(lolcat)

# Problem 1 - 8
BagWeight <- read.delim("~/GitHub/MSDS_Coursework/Quality_Improvement_Methods/BagWeight.dat")
(bag_weight_control <- spc.chart.variables.mean.and.meanrange(data = BagWeight$Bag_Weight,
                                                              sample = BagWeight$Week,
                                                              chart1.main = "Xbar Chart of Bag Weights",
                                                              chart2.main = "Mean Range of Bag Weights"))
unique(bag_weight_control$chart1.center.line)
(Rbar <- unique(bag_weight_control$chart2.center.line))
unique(bag_weight_control$chart1.control.limits.ucl)
unique(bag_weight_control$chart1.control.limits.lcl)
unique(bag_weight_control$chart2.control.limits.ucl)
unique(bag_weight_control$chart2.control.limits.lcl)
lapply(bag_weight_control$chart1.is.control.violation$rule.results,
       FUN = function(v) {any(v)})
lapply(bag_weight_control$chart2.is.control.violation$rule.results,
       FUN = function(v) {any(v)})
d2 <- spc.constant.calculation.d2(sample.size = 5)
est.sigma <- Rbar / (d2 * 5)

# Problem 9 - 20
ShearedSheet <- read.delim("~/GitHub/MSDS_Coursework/Quality_Improvement_Methods/ShearedSheet.dat")
(shear_chart <- spc.chart.variables.mean.and.meanstandarddeviation(data = ShearedSheet$Width_Deviation,
                                                                   sample = ShearedSheet$Subgroup,
                                                                   chart1.main = "Xbar Chart of Shear Width",
                                                                   chart2.main = "Standard Deviations for Shear Width"))
unique(shear_chart$chart1.center.line)
unique(shear_chart$chart2.center.line)
unique(shear_chart$chart1.control.limits.ucl)
unique(shear_chart$chart1.control.limits.lcl)
unique(shear_chart$chart2.control.limits.ucl)
unique(shear_chart$chart2.control.limits.lcl)
lapply(shear_chart$chart1.is.control.violation$rule.results,
       FUN = function(v) {any(v)})
lapply(shear_chart$chart2.is.control.violation$rule.results,
       FUN = function(v) {any(v)})
hist(ShearedSheet$Width_Deviation)
shapetest.exp.epps.pulley.1986(ShearedSheet$Width_Deviation)
shear_avgs <- aggregate(x = ShearedSheet$Width_Deviation,
                         by = list(ShearedSheet$Subgroup),
                         FUN = mean)
hist(shear_avgs$x)
anderson.darling.normality.test(shear_avgs$x)

# Problem 21 - 30
Furnace <- read.delim("~/GitHub/MSDS_Coursework/Quality_Improvement_Methods/Furnace.dat")
anderson.darling.normality.test(Furnace$Furnace_Temperature)
shapiro.wilk.normality.test(Furnace$Furnace_Temperature)
hist(Furnace$Furnace_Temperature)
(furnace_chart <- spc.chart.variables.individual.and.movingrange.generic.simple(Furnace$Furnace_Temperature))
unique(furnace_chart$chart1.center.line)
unique(furnace_chart$chart2.center.line)
unique(furnace_chart$chart1.control.limits.ucl)
unique(furnace_chart$chart1.control.limits.lcl)
unique(furnace_chart$chart2.control.limits.ucl)
unique(furnace_chart$chart2.control.limits.lcl)
lapply(furnace_chart$chart1.is.control.violation$rule.results, FUN = function(v) {any(v)})
MR_points <- furnace_chart$chart2.series[-c(1)]
MRbar <- mean(MR_points)
d2 <- spc.constant.calculation.d2(sample.size = 12)
est.sigma <- MRbar / d2
