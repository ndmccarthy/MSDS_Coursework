require(lolcat)
library(dplyr)
library(flextable)

# import data
Kevin.Oscar <- read.delim("~/GitHub/MSDS_Coursework/Quality_Improvement_Methods/Data_Files/Kevin-Oscar.txt")

# create contingency table between Kevin and Oscar
k.o.contingency <- table(Kevin.Oscar$Kevin, Kevin.Oscar$Oscar)
inspector.contingency <- matrix(data = k.o.contingency,
                                nrow = 2,
                                byrow = FALSE,
                                dimnames = list("Kevin" = c("Pass", "Fail"),
                                                "Oscar" = c("Pass", "Fail")))
# Kevin and Oscar agreed on 281 units (256 good, 25 bad)

# determine if agreement between Kevin and Oscar is significantly different from 0
dmsa.inspectors <- msa.nominal.concordance(Kevin.Oscar$Kevin, Kevin.Oscar$Oscar,
                                           standard = Kevin.Oscar$Lab)
(inspector.summary <- summary(dmsa.inspectors))
# Kappa = 0.6895 with a p-value of 0 (interval = 0.56-0.82)
# Their agreement is statistically significant

# calculate Light's G
Subject<-c(1:300,1:300,1:300)
Rater<-rep(1:3, each=300)
Rating<-cbind(Kevin.Oscar$Kevin, Kevin.Oscar$Oscar, Kevin.Oscar$Lab)
validity.lightg <- cor.light.g.onesample(subject = Subject,
                                         rater = Rater,
                                         rating = Rating,
                                         rater.standard = 3)


# load new data set
beer <- read.delim("~/GitHub/MSDS_Coursework/Quality_Improvement_Methods/Data_Files/beer.txt")

# create contingency table
j.s.contingency <- table(beer$Jeff, beer$Steve)
j.s.matrix <- matrix(data = j.s.contingency,
                     nrow = 4,
                     dimnames = list("Jeff" = c('Acceptable', "Grainy", "Metallic", "Musty"),
                                     "Steve" = c('Acceptable', "Grainy", "Metallic", "Musty")))

# change data to be acceptable vs. unacceptable
beer.updated <- beer
beer.updated[beer > 1] <- 2

# determine if agreement is significantly different from 0
beer.dmsa <- msa.nominal.concordance(beer.updated$Jeff, beer.updated$Steve)
summary(beer.dmsa)

# now only look at unacceptable reasons
unacceptable.beer <- beer[(beer$Jeff > 1 & beer$Steve > 1), ]

# look at agreement for unacceptable reasons
beer.reasons.dmsa <- msa.nominal.concordance(unacceptable.beer$Jeff, unacceptable.beer$Steve)
summary(beer.reasons.dmsa)

# now compare grainy vs. other reasons
grainy.beer <- unacceptable.beer
grainy.beer[unacceptable.beer > 2] <- 5

grainy.dmsa <- msa.nominal.concordance(grainy.beer$Jeff, grainy.beer$Steve)
grainy.sum <- summary(grainy.dmsa)
grainy.int <- c(grainy.sum$BetweenOperators['kappa'],
               grainy.sum$BetweenOperators['kappa.ci.low'],
               grainy.sum$BetweenOperators['kappa.ci.high'])

# compare metallic vs. other reasons
metallic.beer <- unacceptable.beer
metallic.beer[unacceptable.beer != 3] <- 5

metallic.dmsa <- msa.nominal.concordance(metallic.beer$Jeff, metallic.beer$Steve)
metallic.sum <- summary(metallic.dmsa)
metallic.int <- c(metallic.sum$BetweenOperators['kappa'],
               metallic.sum$BetweenOperators['kappa.ci.low'],
               metallic.sum$BetweenOperators['kappa.ci.high'])

# compare musty vs. other reasons
musty.beer <- unacceptable.beer
musty.beer[unacceptable.beer != 4] <- 5

musty.dmsa <- msa.nominal.concordance(musty.beer$Jeff, musty.beer$Steve)
musty.sum <- summary(musty.dmsa)
musty.int <- c(musty.sum$BetweenOperators['kappa'],
               musty.sum$BetweenOperators['kappa.ci.low'],
               musty.sum$BetweenOperators['kappa.ci.high'])

# make table of unacceptable reasons' kappa and CIs
kappa.table <- matrix(data = c(grainy.int, metallic.int, musty.int),
                      nrow = 3, ncol = 3,
                      dimnames = list('Statistics' = c("Kappa", "CI.Lower", "CI.Upper"),
                                      'Reasons' = c("Grainy", "Metallic", "Musty")))
