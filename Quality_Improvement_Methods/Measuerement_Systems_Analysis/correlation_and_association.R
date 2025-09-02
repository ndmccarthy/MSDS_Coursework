require(lolcat)

# Question 1 - 5
CapPull <- read.delim("~/GitHub/MSDS_Coursework/Quality_Improvement_Methods/Data_Files/CapPull.dat")
alpha <- 0.1
cor(CapPull)
cor.pearson.r.onesample(x = CapPull$fid,
                        y = CapPull$cpf,
                        conf.level = 1 - alpha)

# Question 6 - 10
rho <- 0.73
r <- 0.84
n <- 75
alpha <- 0.05
cor.pearson.r.onesample.simple(sample.r = r,
                               sample.size = n,
                               null.hypothesis.rho = rho,
                               alternative = "two.sided",
                               conf.level = 1 - alpha)

# Question 11 - 15
LawnChair <- read.delim("~/GitHub/MSDS_Coursework/Quality_Improvement_Methods/Data_Files/LawnChr.dat")
alpha <- 0.05
cor.spearman.rank(x1 = LawnChair$Surface_Quality,
                  x2 = LawnChair$Speed_FPM,
                  conf.level = 1 - alpha,
                  alternative = "two.sided")

# Question 16 - 20
Sales <- read.delim("~/GitHub/MSDS_Coursework/Quality_Improvement_Methods/Data_Files/Sales.dat")
alpha <- 0.05
cor.point.biserial(discrete_var = Sales$clerk,
                   continuous_var = Sales$time,
                   conf.level = 1 - alpha)

# Question 21 - 24
Beverage <- read.delim("~/GitHub/MSDS_Coursework/Quality_Improvement_Methods/Data_Files/Beverage.dat")
alpha <- 0.05
container.conting <- transform.individual.format.to.xt(x_row = Beverage$ct,
                                                       x_col = Beverage$region,
                                                       weight = Beverage$count,
                                                       x_row_name = "Containter Type",
                                                       x_col_name = "Region")
cor.cramer.v(container.conting)
