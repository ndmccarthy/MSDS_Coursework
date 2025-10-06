require(lolcat)
library(flextable)
library(dplyr)

# import data and get it ready for analysis
Continuous.ST.R <- read.delim("~/GitHub/MSDS_Coursework/Quality_Improvement_Methods/Data_Files/Continuous ST R.dat")
measurements <- Continuous.ST.R
measurements$Part <- factor(measurements$Part)
measurements$Operator <- factor(measurements$Operator)
measurements$Trial <- factor(measurements$Trial)

# LSL and USL
usl <- 25 + 3.5
lsl <- 25 - 3.5

# test part:operator for normality
part.op.summary <- summary.continuous(fx = Value~ Part*Operator, data = measurements)
(part.op.norm.results <- part.op.summary[,-c(3:7, 9)])
part.op.norm.results %>% 
  flextable %>%
  add_header_lines(values = "P-Values for Normality Test of Part:Operator Combinations") %>%
  color(~adtest.p < 0.05, ~adtest.p + Part + Operator, color = "red") %>%
  color(~swtest.p < 0.05, ~swtest.p + Part + Operator, color = "red") %>%
  theme_box()

# create range chart for each operator
op1 <- measurements[which(measurements$Operator == 1),]
op1 <- op1[order(op1$Part),]
op2 <- measurements[which(measurements$Operator == 2),]
op2 <- op2[order(op2$Part),]
op1.chart <- spc.chart.variables.mean.and.meanrange(data = op1$Value,
                                       sample = as.numeric(op1$Part),
                                       combine.charts = "separate",
                                       stat.lsl = lsl,
                                       stat.usl = usl,
                                       chart2.main = "Operator 1 Range Chart",
                                       chart2.xlab = "Part",
                                       chart2.ylab = "Average Value")
op2.chart <- spc.chart.variables.mean.and.meanrange(data = op2$Value,
                                                    sample = as.numeric(op2$Part),
                                                    combine.charts = "separate",
                                                    stat.lsl = lsl,
                                                    stat.usl = usl,
                                                    chart2.main = "Operator 2 Range Chart",
                                                    chart2.xlab = "Part",
                                                    chart2.ylab = "Average Value")
# Part 7 needs more investigation; for purposes of this assignment, it will be removed before proceeding
measurements <- measurements[which(measurements$Part != 7),]
# rerun code for splitting be operator and check charts (Lines 26 - 46)
# operator range charts are now in control

# get correlation for Operator 1
op1.mean <- aggregate(x = op1$Value,
                      by = list(op1$Part),
                      FUN = mean)
colnames(op1.mean) <- c("Part", "Avg.Value")
op1.sd <- aggregate(x = op1$Value,
                      by = list(op1$Part),
                      FUN = sd)
colnames(op1.sd) <- c("Part", "Value.Std")
op1.stats <- data.frame(op1.mean, op1.sd$Value.Std)
colnames(op1.stats) <- c("Part", "Avg", "Std")
cor.pearson.r.onesample(x = op1.stats$Avg,
                        y = op1.stats$Std)

# get correlation for Operator 2
op2.mean <- aggregate(x = op2$Value,
                      by = list(op2$Part),
                      FUN = mean)
colnames(op2.mean) <- c("Part", "Avg.Value")
op2.sd <- aggregate(x = op2$Value,
                    by = list(op2$Part),
                    FUN = sd)
colnames(op2.sd) <- c("Part", "Value.Std")
op2.stats <- data.frame(op2.mean, op2.sd$Value.Std)
colnames(op2.stats) <- c("Part", "Avg", "Std")
cor.pearson.r.onesample(x = op2.stats$Avg,
                        y = op2.stats$Std)

# conduct measurement system analysis
(short.term.msa <- msa.continuous.repeatability.reproducibility(measurement = measurements$Value,
                                                               part = measurements$Part,
                                                               appraiser = measurements$Operator,
                                                               stat.lsl = lsl,
                                                               stat.usl = usl))
short.term.msa$ev.full
short.term.msa$summary.full # to see p-values for components of variance

# look at number of distinct categories
short.term.msa$ev.full.number.distinct.categories

# compare operator means
mean(op1.stats$Avg)
mean(op2.stats$Avg)

# find lowest mean value of parts
part.means <- aggregate(x = measurements$Value,
                        by = list(measurements$Part),
                        FUN = mean)
colnames(part.means) <- c("Part", "Average")
part.means %>% 
  flextable %>%
  add_header_lines(values = "Average Values for each Part") %>%
  color(~Average == min(part.means$Average), ~Part + Average, color = "red") %>%
  theme_box()

# create part:operator interaction plot
plot(op1.stats$Avg, type = "o", col = "blue", main = "Part:Operator Interaction", xlab = "Part", ylab = "Average Value")
lines(op2.stats$Avg, type = "o", col = "darkgreen")
