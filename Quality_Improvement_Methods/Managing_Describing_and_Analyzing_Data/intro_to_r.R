install.packages("devtools")
require(devtools)
install_github("burrm/lolcat")
require(lolcat)

mean(airline$Price)
var(airline$Price)
IQR(airline$Price)
price_range <- range(airline$Price)
price_range[2]-price_range[1]
round.object(skewness(airline$Price), 4)
round.object(kurtosis(airline$Price), 4)

# Graphic Assessment -- pencil set
pencils <- c(6.649, 6.639, 6.629, 6.642, 6.624, 6.616, 6.649, 6.654, 6.649, 6.642, 6.649, 6.637, 6.649, 6.647, 6.644, 6.657, 6.654, 6.634, 6.644, 6.649)
pencil_df <- data.frame(pencils)

spc.run.chart(pencil_df$pencils, main="Pencil Length Observations", ylab = "Millimeters")
frequency.polygon.ungrouped(pencil_df$pencils, main="Frequency Polygon of Pencil Lengths", xlab="Millimeters")

# Graphic Assessment -- viscosity set
visc_fd <- frequency.dist.grouped(viscosity$centistokes)
hist.grouped(viscosity$centistokes, main = "Histogram of Viscocity", xlab = "Centistokes")
lines(density(viscosity$centistokes), col='red')
boxplot(viscosity$centistokes, main= "Boxplot of Viscosity", ylab = "Centistokes")
summary(viscosity)

# Graphic Assessment -- yield set
hist(yield$strength, prob=T, main = "Histogram of Tensile Tests", xlab = "Yield Strength")
lines(density(yield$strength), col='red')

# Numeric Assessment -- pencils
mean(pencils)
median(pencils)
sample.mode(pencils)
sd(pencils)
var(pencils)

# Numeric Assessment -- viscosity
frequency.dist.ungrouped(viscosity$centistokes)
visc_range <- range(viscosity$centistokes)
visc_range[2]-visc_range[1]
quantile(viscosity$centistokes, probs = 0.45)
summary.continuous(viscosity$centistokes)

# Numeric Assessment -- yield
yield <- read.csv("~/GitHub/MSDS_Coursework/Quality_Improvement_Methods/yield.txt", sep="")
skewness(yield$strength)
kurtosis(yield$strength)

# Numeric Assessment -- body
body <- read.csv("~/GitHub/MSDS_Coursework/Quality_Improvement_Methods/body.txt", sep="")
cor(body$height, body$weight, method = 'pearson')
