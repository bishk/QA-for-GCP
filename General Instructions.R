#For this particular file, save as excel file to csv.
THEDATA <- read.csv(file.choose(), header=TRUE)
name_column1<-THEDATA$Column_Of_Interest1
name_column2<-THEDATA$Column_of_Interset2
#First we need to see if our data is not too skewed.
hist(THEDATAstuff$Column_of_intest1)
hist(THEDATA$Column_of_Interest2)
#If not, we can run the t.test. If Data is paired, let "paired=T", otherwise, leave as is.
t.test(stuff$DeltaMulti, stuff$DeltaSingle, paired=F)
plot(name_column1, nane_column2)

#When studiying more than 2 variables, replicate analogously to the follwoing
#THE NUMBER OF ITERATIONS STUDIED
All_four_possible <-read.csv(file.choose(), header=TRUE)
qa<-All_four_possible$Quantum
psa<-All_four_possible$PSA
sa<-All_four_possible$SA
ba<-All_four_possible$BA
Number_of_iterations<-c(qa, psa, sa, ba)
Type_of_annealing<-c(rep("QA", 100), rep("PSA", 100), rep("SA", 100), rep("BA", 100))
distribu=data.frame(Number_of_iterations, Type_of_annealing)
plot(Number_of_iterations~Type_of_annealing, data=distribu)
results_iter = aov(Number_of_iterations ~ Type_of_annealing, data=distribu)
results_iter
#TukeyHSD test finds means which are significnatly different from one-another
TukeyHSD(results_iter)
#Pairwise.t.test does a pairwise t test between our variables.
pairwise.t.test(Number_of_iterations, Type_of_annealing, p.adjust="bonferroni")
