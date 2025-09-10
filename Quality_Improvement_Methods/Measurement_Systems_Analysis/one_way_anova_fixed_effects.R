require(lolcat)
require(sjstats)
library(dplyr)
require(flextable)


Wash <- read.delim("~/GitHub/MSDS_Coursework/Quality_Improvement_Methods/Data_Files/Wash.dat")

# calculate descriptive statistics for all groups
vendor.labels <- c("Acme", "Quality R Us", "FBN", "Wash Up With Us", "Ezy Clean", "Rock On Cleaners", "Nimno Agents")
Wash$Vendor <- factor(Wash$Vendor, labels = vendor.labels)
(vendor.desc <- summary.continuous(Cleanliness~Vendor, Wash))
# all come from a normal distribution

# test if equal variances
(vendor.disp.results <- compute.group.dispersion.ADA(fx = Cleanliness~Vendor, data = Wash))
Wash$ADA_results <- vendor.disp.results
vendor.disp.aov <- aov(ADA_results~Vendor, data = Wash)
summary(vendor.disp.aov) # p-value indicates the variances are unequal

# calculate statistical importance (percent explained variability)
vendor.model <- lm(ADA_results~Vendor, data = Wash)
(vendor.disp.stats <- anova_stats(vendor.model))
vendor.disp.stats$omegasq[1]

# conduct post hoc analysis to see where differences in dispersion are
(vendor.tukey <- TukeyHSD(vendor.disp.aov))


# test if equal means (with unequal variance)
(vendor.welch <- oneway.test(Cleanliness~Vendor, data = Wash))

# test for statistical importance  of mean differences
vendor.F <- vendor.welch$statistic
df.vendor <- vendor.welch$parameter[1]
n <- length(Wash$Cleanliness)
(omegasq.vendor <- (df.vendor * (vendor.F - 1)) / (df.vendor * (vendor.F - 1) + n))

# create visualization of means
plot(vendor.desc$mean, xaxt = "n", type = "b",
     main = "Cleanliness Means by Vendor", ylab = "Cleanliness Mean", xlab = "")
axis(1, at = 1:7, labels = vendor.labels, las = 2)

# conduct post hoc analysis to see where differences in means are
vendor.gh <- contrasts.games.howell.kgroups.simple(group.label = vendor.labels,
                                                   group.mean = vendor.desc$mean,
                                                   group.variance = vendor.desc$var,
                                                   group.sample.size = vendor.desc$n)
gh.decision.matrix <- data.frame(vendor.gh$matrix.decision)
gh.decision.matrix$rownames <- colnames(gh.decision.matrix)
gh.decision.matrix <- gh.decision.matrix[c(8, 1, 2, 3, 4, 5, 6, 7)]
(gh.decision.matrix.tbl <- gh.decision.matrix %>%
                          rename(vendors = rownames) %>%
                          flextable() %>%
                          add_header_lines(values = "Vendor Mean Games-Howell Decision Matrix") %>%
                          theme_box())

# creating boxplot for visualization of dispersion
boxplot(Cleanliness~Vendor, data = Wash)