require(lolcat)
require(sjstats)

# import data
Earing <- read.delim("~/GitHub/MSDS_Coursework/Quality_Improvement_Methods/Data_Files/Earing.dat")

# get data into correct format
lot.labels <- as.vector(unique(Earing$lot))
Earing$lot <- factor(Earing$lot, labels = lot.labels)

# get descriptive statistics for each group (lot)
(lot.stats <- summary.continuous(earing~lot, data = Earing))

# store means in own vector
lot.means <- lot.stats$mean

# get descriptive statistics for all means
(total.stats <- summary(lot.means))

# test for normality of means
anderson.darling.normality.test(lot.means)
# normality among means found

# testing if variance of means = 0
# find Sum of Squares Between lots

# first find out if variance is the same among each lot
# because they don't all come from normal distributions, use ADMn1 test
# use ADMn1 to test differences in dispersion
(lot.admn1 <- compute.group.dispersion.ADMn1(earing~lot, Earing))
# now do ANOVA on ADMn1 results 
Earing$ADMn1 <- lot.admn1
(lot.disp.anova <- aov(ADMn1~lot, Earing))
summary(lot.disp.anova)
# findings indicate that the lots have equal variance

# conduct ANOVA for means with equal variance (Fisher's)
(lot.fisher.anova <- aov(earing~lot, Earing))
# SSb is 5.116859
summary(lot.fisher.anova)
# p-value for F is < 0.05
# Reject hypothesis that means are the same; variance of means is not 0

# test for statistical importance
lot.mean.model <- lm(earing~lot, Earing)
(lot.mean.anova.stats <- anova_stats(lot.mean.model))
# 54% of variability can be explained by between coil differences