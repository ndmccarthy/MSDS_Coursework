require(lolcat)
require(fitdistrplus)

# Part 1
load.url <- "https://d3c33hcgiwev3.cloudfront.net/Lo_U1Co-SqaP1NQqPrqmNg_39850fb6415742ff80edf7ee4ef32ef1_Loading.dat?Expires=1754179200&Signature=OMGEhQhL9K7Npmouik~g1dAetsql8-HvtL5DsnB2bVAxYU1J9-SO3ZlbVSCvZqcJmd9Ht0iDyd~mvrx1i~CvF6hgJCV~-oyZ3bxETaEOInrizEV9tpZ7Ed-wQJAbJ1-VMZiG1yL-tG0OVH14RMHFCcjoHuu-KrU2PbR0sOv00b8_&Key-Pair-Id=APKAJLTNE6QMUY6HBC5A"
wait.url <- "https://d3c33hcgiwev3.cloudfront.net/meWHwGBITfmlh8BgSB35MA_e5ea51c1aae24b898c14dc0b2c800ff1_Wait.dat?Expires=1754179200&Signature=N909zIZiGT~7eB4Fd0HMGEC3Zp3-gaH3~KbJ1f4Fj-bvD27ysmg-ZUR9xf5up0fvsFLvXIvU6g6swzxcTbEG54HYna48mJ-OzoL20naGGVNoiJYarxU8VORQUQaLJTLcaIpQiBXiKQ1pzENkO3Gi61miBteRaImXJBBEyEKYYKs_&Key-Pair-Id=APKAJLTNE6QMUY6HBC5A"
load <- read.delim(load.url, header = TRUE)
wait <- read.delim(wait.url, header = TRUE)
L.USL <- 8
alpha <- 0.05

# transform data to independent format
load <- load[, -c(1)]
samp <- c()
load.time <- c()
trans.load <- data.frame(samp, load.time)
for (ii in seq(1:10)){ # loop through columns (samples)
  load.time <- c(unlist(load[, ii]))
  samp_num <- c(seq(1:30))
  samp.df <- data.frame(samp_num, load.time)
  trans.load <- rbind(trans.load, samp.df)
}

# check for distribution
load.data <- trans.load$load.time
hist.grouped(load.data, freq = T)
summary.continuous(load.data) # NOT normal
shapetest.exp.epps.pulley.1986(load.data) # NOT exponential
start.gamma <- mmedist(load.data, distr = "gamma")
start <- as.list(start.gamma$estimate)
load.fit <- fitdist(load.data, distr = "gamma", start = start)
load.shape <- load.fit$estimate[1]
load.rate <- load.fit$estimate[2]
gofstat(load.fit, fitnames = "gamma")

# new approach
new.load <- transform.dependent.format.to.independent.format(load)

# create control chart for Load and check for violations
load.chart <- spc.chart.variables.mean.and.meanstandarddeviation(trans.load$load.time,
                                                                 sample = trans.load$samp_num)
new.load.chart <- spc.chart.variables.mean.and.meanstandarddeviation(data = new.load$measure, sample = new.load$cell)
any(new.load.chart$chart1.is.control.violation$overall.results) # in control

# look at capability
mean_center <- unique(new.load.chart$chart1.center.line)
sd_center <- unique(new.load.chart$chart2.center.line)
load.cap <- spc.capability.summary.normal.simple(stat.usl = L.USL,
                                                 stat.lsl = NA,
                                                 process.center = mean_center,
                                                 process.variability.estimate = sd_center^2,
                                                 process.n.upper = sum(new.load > L.USL),
                                                 process.n = length(new.load$measure))
L.USL/(6 * sd_center) # Cp
spc.capability.cpk.simple(upper.specification = L.USL,
                          lower.specification = NA,
                          process.variability = sd_center^2,
                          process.center = mean_center,
                          n.sigma = 6)

# transform wait time
wait <- wait[, -c(1)]
trans.wait <- transform.dependent.format.to.independent.format(wait)

# create control chart and look for violations
wait.chart <- spc.chart.variables.mean.and.meanstandarddeviation(data = trans.wait$measure,
                                                                 sample = trans.wait$cell)
any(wait.chart$chart1.is.control.violation$overall.results) # in control

# mean and sd of waiting time
unique(wait.chart$chart1.center.line)
wait.sd <- unique(wait.chart$chart2.center.line)

# USL for wait
(nt.wait <- natural.tolerance.normal(trans.wait$measure))

# wait time capability
nt.wait$upper.limit/(6 * wait.sd) # Cp
# wait is capable



# Part 2
light.url <- "https://d3c33hcgiwev3.cloudfront.net/GXTLo7NhRoW0y6OzYVaFEw_9423bb8d466645d79fe4c74583a9daf1_Light.dat?Expires=1754179200&Signature=AQo4v6n5ASw~1xZjIc4PfQEI2pyrPd06YcgfOa4r2L~FkIy~q-XtxNiRfBMeW2wfaQk-QEcHLhMxLnPYvJ6lo71~YA78cNgejt1Xx4twRBOTLCAnGcp1vCfO6BNQ9408MuowK0PXbP4T2BL4QQghlPcYhU0lv4wM-LNd94qreis_&Key-Pair-Id=APKAJLTNE6QMUY6HBC5A"
light <- read.delim(light.url, header = T)
target <- 40
USL <- 50
LSL <- 30

ldat <- c(unlist(light$T_Index))

# check for normality
summary.continuous(ldat) # normal!

# create control chart and check violations
light.chart <- spc.chart.variables.individual.and.movingrange.normal.simple(individuals = ldat)
any(light.chart$chart1.is.control.violation$overall.results) # in control

# check performance
spc.capability.summary.ungrouped.nonnormal.simple.R(stat.lsl = LSL,
                                                    stat.target = target,
                                                    stat.usl = USL,
                                                    process.center.capability = mean(ldat),
                                                    process.center.performance = mean(ldat),
                                                    process.variability = var(ldat),
                                                    process.n.upper = sum(ldat > USL),
                                                    process.n.lower = sum(ldat < LSL),
                                                    process.n = length(ldat),
                                                    natural.tolerance = 6 * sd(ldat),
                                                    p.lower = pnorm(0.00135),
                                                    p.upper = pnorm(1 - 0.00135))
zu <- (USL - mean(ldat))/sd(ldat)
pnorm(zu, lower.tail = FALSE)



# Part 3
regulator.url <- "https://d3c33hcgiwev3.cloudfront.net/Uil6IYSgQP6peiGEoID-ug_1bbf3460a3ff4fee9bcc6751d0aa80f1_Voltage_Regulator.dat?Expires=1754179200&Signature=ABfUMCLUa7xRf~VYgF6WukT8cG9EbbOwxVCaacnaA7ei9WJ-W-yqgWVEex58fSkKQZV5pUGDhJKCa9GRbbZcLnwNn0jFdsCZlDSA-G~47g61IyeQAT-nMcuiCdPWWyfv4yNBORBMAcSdwsJy4S9JICl6gAFMzWavRPzHfk4LH2c_&Key-Pair-Id=APKAJLTNE6QMUY6HBC5A"
regulator <- read.delim(regulator.url, header = T)
n <- unique(regulator$Sample_Size)
num_defects <- c(unlist(regulator$Number_Defective))
USL <- 0.035

# use p chart because equal n and proportion
reg.chart <- spc.chart.attributes.proportion.p.binomialdistribution.simple(proportions = num_defects/n,
                                                                           sample.size = n)
# in control

(center <- unique(reg.chart$chart1.center.line))
(cpk <- qnorm(p = center, lower.tail = FALSE)/3)



# Part 4
disc.url <- "https://d3c33hcgiwev3.cloudfront.net/GYcAPD4eSNiHADw-HhjY8g_70b0dc29a2134e2e90bed8acdf5ed2f1_Disc_Drive.dat?Expires=1754179200&Signature=j-id8hIlmc-qSQIqQNHqZ56RzZukyxyfbYJxtzqs0Bee1e2bVUE1Ngqd2wbjgsjlOszsazmIwrY37G-QWbK1PxgtEYHMCuN-RghRnMUwvRkKeBLkz~Q~~TtsbqSZdlu7JXewfP9NumXrtQTvcdFiggrgZG8R-yfA5BVhFudOzV4_&Key-Pair-Id=APKAJLTNE6QMUY6HBC5A"
disc <- read.delim(disc.url, header = T)
USL <- 8

# constant n (1) and looking at defects per unit means c chart
overall.chart <- spc.chart.attributes.counts.c.poissondistribution.simple(counts = disc$Defects)
(overall.center <- unique(overall.chart$chart1.center.line))

# subset before and after gauge change
before <- subset(disc, subset = disc$Gauge_Change==1)
after <- subset(disc, subset = disc$Gauge_Change==2)

# new c chart for before and after
before.chart <- spc.chart.attributes.counts.c.poissondistribution.simple(counts = before$Defects)
(before.center <- unique(before.chart$chart1.center.line))

after.chart <- spc.chart.attributes.counts.c.poissondistribution.simple(counts = after$Defects)
(after.center <- unique(after.chart$chart1.center.line))

# new c chart for surface defects
surface.chart <- spc.chart.attributes.counts.c.poissondistribution.simple(counts = disc$Surface_Defect)
(surface.center <- unique(surface.chart$chart1.center.line))

bs.chart <- spc.chart.attributes.counts.c.poissondistribution.simple(before$Surface_Defect)
(bs.center <- unique(bs.chart$chart1.center.line))

as.chart <- spc.chart.attributes.counts.c.poissondistribution.simple(counts = after$Surface_Defect)
(as.center <- unique(as.chart$chart1.center.line))

# new c charts for connector defects
connector.chart <- spc.chart.attributes.counts.c.poissondistribution.simple(counts = disc$Connector_Defect)
(connect.center <- unique(connector.chart$chart1.center.line))

bc.chart <- spc.chart.attributes.counts.c.poissondistribution.simple(counts = before$Connector_Defect)
(bc.center <- unique(bc.chart$chart1.center.line))

ac.chart <- spc.chart.attributes.counts.c.poissondistribution.simple(counts = after$Connector_Defect)
(ac.center <- unique(ac.chart$chart1.center.line))

# Cpk with after.center
spc.capability.cpk.simple(lower.specification = NA,
                          upper.specification = USL,
                          process.variability = var(after$Defects),
                          process.center = after.center,
                          n.sigma = 6)
