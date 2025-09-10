require(lolcat)

# upload info
height <- read.delim("~/GitHub/MSDS_Coursework/Quality_Improvement_Methods/Data_Files/height2.dat")
lsl <- 480
usl <- 495

# make part, repetition, and operator factors
height$Part <- factor(height$Part)
height$Operator <- factor(height$Operator)
height$Repetition <- factor(height$Repetition)

# conduct potential study analysis
(potential.height <- msa.continuous.repeatability.reproducibility(measurement = height$Value,
                                                                  part = height$Part,
                                                                  appraiser = height$Operator,
                                                                  stat.lsl = lsl,
                                                                  stat.usl = usl))
# find df for each factor
potential.height$summary.aov.full

# look at PEV for factors
potential.height$ev.full

# get P/T for Total GRR
var_gauge <- potential.height$ev.full[1]
(pt.height <- (6 * var_gauge) / (usl - lsl) * 100)

# get number of distinct categories
potential.height$ev.reduced.number.distinct.categories

# which operator has a higher mean value?
(op.summary <- summary.continuous(Value~Operator, height))

# which part has lowest mean?
(part.summary <- summary.continuous(Value~Part, height))

# create plot of part operator interaction
# get part means for each operator
(part.op.summary <- summary.continuous(Value~Part*Operator, height))
op1.part.means <- part.op.summary[part.op.summary$Operator == 1,]$mean
op2.part.means <- part.op.summary[part.op.summary$Operator == 2,]$mean

plot(op1.part.means, type = 'o',  col = 'blue',
     main = "Part-Operator Interaction")
lines(op2.part.means, type = 'o', col = 'darkgreen')
