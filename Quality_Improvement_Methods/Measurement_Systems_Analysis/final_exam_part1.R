require(lolcat)
library(flextable)
library(dplyr)

# upload data
final1 <- read.delim("~/GitHub/MSDS_Coursework/Quality_Improvement_Methods/Data_Files/final1.txt")

# make part, operator, and repetition columns factors
final1$Part <- factor(final1$Part)
final1$Operator <- factor(final1$Operator)
final1$Repetition <- factor(final1$Repetition)

# short-term study, 2 operators, 25 samples each, now conducting continuous MSA
lsl <- 15
usl <- 13.5

# test part: operator combinations for normality (Anderson-Darling)
op.part.summ <- summary.continuous(Value ~ Operator*Part, final1)
op.part.summ <- op.part.summ[, -c(3, 4, 9, 10)]
# highlight p-values lower than 0.05 to make more obvious
(op.part.table <- op.part.summ %>% flextable %>%
    add_header_lines(values = "Part:Operator Summary") %>%
    color(~adtest.p < 0.05, ~adtest.p + Operator + Part, color = "red") %>% theme_box())

# check range charts for each operator (to see if in control)
# subset data by operator and order by part
op1 <- final1[which(final1$Operator == 1), ]
op2 <- final1[which(final1$Operator == 2), ]
op1 <- op1[order(op1$Part), ]
op2 <- op2[order(op2$Part), ]
# create charts
(op1.chart <- spc.chart.variables.mean.and.meanrange(data = op1$Value,
                                                    sample = as.numeric(op1$Part),
                                                    combine.charts = "separate",
                                                    stat.lsl = lsl,
                                                    stat.usl = usl,
                                                    chart2.main = "Operator 1 Range Chart",
                                                    chart2.xlab = "Part",
                                                    chart2.ylab = "Average Value"))
(op2.chart <- spc.chart.variables.mean.and.meanrange(data = op2$Value,
                                                     sample = as.numeric(op2$Part),
                                                     combine.charts = "separate",
                                                     stat.lsl = lsl,
                                                     stat.usl = usl,
                                                     chart2.main = "Operator 2 Range Chart",
                                                     chart2.xlab = "Part",
                                                     chart2.ylab = "Average Value"))

# check Pearson Product Moment Correlation Coefficients for mean and sd of each operator
# first get means for each part (and operator)
op1.mean <- aggregate(x = op1$Value,
                      by = list(op1$Part),
                      FUN = mean)
colnames(op1.mean) <- c("Part", "Mean.Value")
op2.mean <- aggregate(x = op2$Value,
                      by = list(op2$Part),
                      FUN = mean)
colnames(op2.mean) <- c("Part", "Mean.Value")
# second get sd for each part (and operator)
op1.sd <- aggregate(x = op1$Value,
                      by = list(op1$Part),
                      FUN = sd)
colnames(op1.sd) <- c("Part", "Standard.Deviation")
op2.sd <- aggregate(x = op2$Value,
                    by = list(op2$Part),
                    FUN = sd)
colnames(op2.sd) <- c("Part", "Standard.Deviation")
# third, combine into one df per operator
op1.stats <- merge(op1.mean, op1.sd, by = "Part")
op2.stats <- merge(op2.mean, op2.sd, by = "Part")
# now test for significance
(op1.cor <- cor.pearson.r.onesample(x = op1.stats$Mean.Value,
                                    y = op1.stats$Standard.Deviation))
(op2.cor <- cor.pearson.r.onesample(x = op2.stats$Mean.Value,
                                    y = op2.stats$Standard.Deviation))

# conduct MSA
msa <- msa.continuous.repeatability.reproducibility(measurement = final1$Value,
                                                     part = final1$Part,
                                                     appraiser = final1$Operator,
                                                     stat.lsl = lsl,
                                                     stat.usl = usl)
# check ANOVA to see which parts were significant
(msa.anova <- data.frame(msa$summary.aov.full[[1]]))
# check components of variance
(msa.comp.var <- data.frame(msa$ev.full))
# check NDC
(msa.ndc <- msa$ev.reduced.number.distinct.categories[1])

# to compare operator variability, plot sds
plot(op1.stats$Standard.Deviation,
     col = 'blue',
     type = 'o',
     xlab = "Part",
     ylab = "Standard Deviation",
     main = "Operator Variability by Part",
     ylim = c(0, 0.8))
lines(op2.stats$Standard.Deviation,
      col = 'darkgreen',
      type = 'o')
legend("topleft",
       legend = c("Operator 1", "Operator 2"),
       col = c('blue', 'darkgreen'),
       lty = c(1, 1))

# create part:operator interaction plot
plot(op1.stats$Mean.Value,
     col = 'blue',
     type = 'o',
     xlab = "Part",
     ylab = "Mean Value",
     main = "Part:Operator Interaction Plot")
lines(op2.stats$Mean.Value,
      col = 'darkgreen',
      type = 'o')
legend("topleft",
       legend = c("Operator 1", "Operator 2"),
       col = c('blue', 'darkgreen'),
       lty = c(1, 1))