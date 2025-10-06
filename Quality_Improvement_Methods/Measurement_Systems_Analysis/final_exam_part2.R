# discrete msa with a standard, 100 samples, 3 inspectors (JL, MK, SF), 3 repetitions
# 1 = acceptable, 2 = unacceptable
# assessing Internal Consistency, Concordance between each pair of inspectors and overall, 
# and concordance with the standard (validity) between each pair of inspectors and for the overall system
# use 95% CI for all questions

# Startup code
require(lolcat)
require(dplyr)
require(flextable)
require(irr)
require(tibble)
ro<-round.object
nqtr<-function(x,d){noquote(t(round.object(x, d)))}
options(scipen=999)

# Discrete MSA ------------------------------------------------------------
# Import file 
DiscreteMSA <- read.delim("~/GitHub/MSDS_Coursework/Quality_Improvement_Methods/Data_Files/final2.txt")

# Internal Consistency Analysis -------------------------------------------

# JL Internal Consistency
JL <- msa.nominal.internalconsistency(DiscreteMSA$JL1
                                      ,DiscreteMSA$JL2
                                      ,DiscreteMSA$JL3)

sum.ic.JL<-as.data.frame(ro(summary(JL),4))
sum.ic.JL$Description<-c("JL1 vs JL2"
                         ,"JL1 vs JL3"
                         ,"JL2 vs JL3")

sum.ic.JL %>%
  t() %>% 
  as.data.frame() %>% 
  tibble::rownames_to_column() %>%
  flextable() %>%
  delete_part(part = "header") %>%
  add_header_lines(values = "Internal Consistency JL") %>%
  theme_box()

# Overall Internal Consistency for JL
kappam.light(DiscreteMSA[,c(3:5)]) # JL1, JL2 and JL3

# MK Internal Consistency
MK <- msa.nominal.internalconsistency(DiscreteMSA$MK1
                                      ,DiscreteMSA$MK2
                                      ,DiscreteMSA$MK3)

sum.ic.MK<-as.data.frame(ro(summary(MK),4))
sum.ic.MK$Description<-c("MK1 vs MK2"
                         ,"MK1 vs MK3"
                         ,"MK2 vs MK3")

sum.ic.MK %>%
  t() %>% 
  as.data.frame() %>% 
  tibble::rownames_to_column() %>%
  flextable() %>%
  delete_part(part = "header") %>%
  add_header_lines(values = "Internal Consistency MK") %>%
  theme_box()

# Overall Internal Consistency for MK
kappam.light(DiscreteMSA[,c(6:8)]) # MK1, MK2 and MK3



# SF Internal Consistency
SF <- msa.nominal.internalconsistency(DiscreteMSA$SF1
                                      ,DiscreteMSA$SF2
                                      ,DiscreteMSA$SF3)

sum.ic.SF<-as.data.frame(ro(summary(SF),4))
sum.ic.SF$Description<-c("SF1 vs SF2"
                         ,"SF1 vs SF3"
                         ,"SF2 vs SF3")

sum.ic.SF %>%
  t() %>% 
  as.data.frame() %>% 
  tibble::rownames_to_column() %>%
  flextable() %>%
  delete_part(part = "header") %>%
  add_header_lines(values = "Internal Consistency SF") %>%
  theme_box()

# Overall Internal Consistency for SF
kappam.light(DiscreteMSA[,c(9:11)]) # SF1, SF2 and SF3



# Concordance Between Operators -------------------------------------------
Concordance<-msa.nominal.concordance(JL, MK, SF, standard = DiscreteMSA$Correct)
summary.concord<-ro(summary(Concordance),4)

# Concordance Between Operators
between.ops<-as.data.frame(ro(summary.concord$BetweenOperators,4))




# Validity Analysis (Concordance with a Standard) -------------------------
with.std<-summary.concord$WithStandard



# Overall System Validity (Light's G)
# Analysis uses modal value for each operator
Subject<-c(1:100,1:100,1:100,1:100)
Rater<-rep(1:4, each=100)
Rating<-cbind(JL$mode, MK$mode, SF$mode,DiscreteMSA$Correct)

cor.light.g.onesample(subject = Subject,
                      rater = Rater,
                      rating = Rating,
                      rater.standard = 4)
