require(lolcat)
library(flextable)
library(dplyr)

# upload data and get it ready to use
Continuous.LT.R <- read.csv("~/GitHub/MSDS_Coursework/Quality_Improvement_Methods/Data_Files/Continuous LT R.dat", sep="")
measurements <- Continuous.LT.R

measurements$Operator <- 1

measurements$Trial <- factor(measurements$Trial)
measurements$Part <- factor(measurements$Part)
measurements$Operator <- factor(measurements$Operator)



lsl = 25 - 3.5
usl = 25 + 3.5

# test each part for normality
summary.continuous(fx = Measure ~ Part, data = measurements)
# all part measurements come from normal distributions

# check for control of parts by individual chart
total_num_parts <- max(as.numeric(measurements$Part))
for (part_num in seq(1, total_num_parts)) {
  part.df <- measurements[measurements$Part == part_num,]
  spc.chart.variables.individual.and.movingrange.normal.simple(individuals = part.df$Measure,
                                                               chart1.main = paste("Measurements of Part",  part_num),
                                                               chart1.ylab = "Measurement Values",
                                                               chart1.xlab = "Trial Number",
                                                               stat.lsl = lsl,
                                                               stat.usl = usl)
  
}


# get sd for each part and check for control
part.sds <- aggregate(measurements$Measure,
                      by = list(as.numeric(measurements$Part)),
                      FUN = sd)
colnames(part.sds) <- c("Part", "Std")
spc.chart.variables.individual.and.movingrange.generic.simple(individuals = part.sds$Std,
                                                              chart1.main = "Standard Deviations by Part",
                                                              chart1.ylab = "Standard Deviation",
                                                              chart1.xlab = "Part Number")

# get means for each part and check for control
part.means <- aggregate(measurements$Measure,
                        by = list(as.numeric(measurements$Part)),
                        FUN = mean)
colnames(part.means) <- c("Part", "Average")
spc.chart.variables.individual.and.movingrange.generic.simple(individuals = part.means$Average,
                                                              chart1.main = "Means by Part",
                                                              chart1.ylab = "Mean",
                                                              chart1.xlab = "Part Number",
                                                              stat.lsl = lsl,
                                                              stat.usl = usl)

# check for correlation between means and stds
cor.pearson.r.onesample(part.means$Average, part.sds$Std)

# conduct msa test
long.term.msa <- msa.continuous.repeatability.reproducibility(measurement = measurements$Measure,
                                                              part = measurements$Part,
                                                              appraiser = measurements$Operator)
long.term.msa$summary.aov.full
long.term.msa$ev.full
long.term.msa$summary.full
long.term.msa$ev.full.number.distinct.categories
