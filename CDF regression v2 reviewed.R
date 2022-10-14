library('stats')
library('ggplot2')

df <- read.csv('')
# View(df)

df <- within(df, Time_of_Day <- relevel(Time_of_Day, ref = 'Late Morning/Afternoon'))
#df$Num_Hashtag <- as.factor(df$Num_Hashtag)

subset <- df[df$Likes < 200, ]


############# FINAL MODEL ##############

# passive engagement = likes + retweets
lin_full <- lm(Total_Passive_Eng ~
                 Media +
                 #Mon +
                 #Tue +
                 #Wed +
                 #Thu +
                 #Fri +
                 #Sat +
                 #Sun +
                 #Poll +
                 #URL +
                 #Thread +
                 Thread_Pos +
                 Hashtag +
                 Num_Hashtag +
                 #Weekday +
                 Day_of_Week +
                 Time_of_Day,
               data=subset
)

summary(lin_full)


############# OTHER MODELS #############

##### Full Linear Model ##### 

# total reach (using dummy variables)
lin_full <- lm(Total_Reach ~
               Media +
               Mon +
               Tue +
               Wed +
               Thu +
               #Fri +
               Sat +
               Sun +
               #Poll +
               #URL +
               #Thread +
               Thread_Pos +
               Hashtag +
               Num_Hashtag +
               #Weekday +
               #Day_of_Week +
               Time_of_Day,
             data=subset
               )

summary(lin_full)

# total reach (using factoring)
lin_full <- lm(Total_Reach ~
                 Media +
                 #Mon +
                 #Tue +
                 #Wed +
                 #Thu +
                 #Fri +
                 #Sat +
                 #Sun +
                 #Poll +
                 #URL +
                 #Thread +
                 #Thread_Pos +
                 #Hashtag +
                 Num_Hashtag +
                 #Weekday +
                 Day_of_Week +
                 Time_of_Day,
               data=subset
)

summary(lin_full)

# high retweets
log_full <- glm(High_Retweets ~
                  Poll +
                  Media +
                  #URL +
                  #Thread +
                  #Thread_Pos,
                  Hashtag +
                  Num_Hashtag +
                  #Weekday,
                  Day_of_Week +
                  Time_of_Day,
                  family=binomial(),
                  data=subset
)

summary(log_full)


# high replies
log_full <- glm(High_Replies ~
                  Poll +
                  Media +
                  URL +
                  #Thread +
                  #Thread_Pos,
                  Hashtag +
                  Num_Hashtag +
                  #Weekday,
                  Day_of_Week +
                  Time_of_Day,
                family=binomial(),
                data=subset
)

summary(log_full)


##### EID Linear Model ##### 
lin_eid <- glm(Total_Reach ~
               Media +
               # Poll +
               URL +
               # Thread +
               Thread_Pos +
               # Hashtag +
               Num_Hashtag +
               # Weekday +
               # Day_of_Week +
               Time_of_Day,
             data=df
               )

summary(lin_eid)


############# Logistic #############

##### Full Logistic Model ##### 
log_full <- glm(High_Likes ~
               Poll +
               Media +
               URL +
               #Thread +
               #Thread_Pos,
               Hashtag +
               Num_Hashtag,
               #Weekday,
               #Day_of_Week,
               #Time_of_Day,
              family=binomial(),
             data=df
               )


summary(log_full)

##### EID Logistic Model ##### 
log_eid <- glm(High_ER ~
               Media +
               # Poll +
               URL +
               # Thread +
               Thread_Pos +
               # Hashtag +
               Num_Hashtag +
               # Weekday +
               # Day_of_Week +
               Time_of_Day,
              family=binomial(),
             data=df
               )

summary(log_eid)


####### Visualize

outData = fortify(lin_full)
##### Residual plot - linearity (want cloud-like)
ggplot(outData, aes(x=.fitted, y=.stdresid)) +
  geom_point(shape=16, size=2) +
  labs(x = "Predicted Engagement Rate",y="Standardized Residuals",title="Standardized Residual Plot")+theme_bw()+
  geom_hline(yintercept=0)+
  theme(plot.title = element_text(hjust=0.5, size = rel(2)))+
  theme(axis.title.y = element_text(size = rel(1.4)))+
  theme(axis.title.x = element_text(size = rel(1.4)))+
  theme(axis.text.x = element_text(size = rel(1.6)))+
  theme(axis.text.y = element_text(size = rel(1.6)))

##### Homoskedasticiy plots
hist(outData$.resid, main="Histogram of Residuals", xlab="Residuals")
qqnorm(outData$.resid, main = "Normal Q-Q Plot",
       xlab = "Theoretical Normal Quantiles", ylab = "Residuals",
       plot.it = TRUE, datax = FALSE)
qqline(outData$.resid)  ##Adds line to plot
##### Homeoskedasticity - Lavene test - if less than 0.05, there IS a difference in the variances - reject H0 that there is not a difference in variances of population
outData$yHatCategory <- ifelse(outData$.fitted < median(outData$.fitted), c("group1"), c("group2"))
leveneTest(.resid ~ yHatCategory, data=outData)

##### Normality - Shapiro-Wilk test - if less than 0.05, data is NOT normally distributed - reject H0 that data is from normally distributed sample
shapiro.test(outData$.resid)
       


