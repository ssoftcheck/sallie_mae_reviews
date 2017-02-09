library(ggplot2)
library(data.table)

frame = fread('nmf_data.csv')
frame[,datetime := strptime(datetime,format='%Y-%m-%d %H:%M:%S')]
frame[,sentiment := factor(sentiment)]

topic.count = len(grep('T\\d',names(frame))) - 1
  
frame[,topic := factor(apply(frame,1,function(x) which.max(x[paste0('T',0:topic.count)])-1))]

frame2 = melt(frame,id.vars = c('sentiment','datetime','topic'),variable.name = 't',value.name = 'tp', 
              measure.vars = sapply(0:topic.count,function (x) paste0('T',x)))
frame2[,t := factor(substr(t,2,2))]

ggplot(frame2) + aes(x=tp,fill=t) + geom_density(alpha=0.5) + scale_y_continuous('Topic Score')

ggplot(frame2) + aes(x=datetime,y=tp,color=sentiment) + geom_point(size=1) + facet_wrap(~t,nrow=2,ncol=5) +
  scale_y_continuous('Topic SCore')

ggplot(frame) + aes(x=topic,y=100*..count../sum(..count..)) + geom_bar() + scale_x_discrete('Topic') + 
  scale_y_continuous('Percent Occurrence')

frame[,.(p=.N/nrow(frame)),topic][order(topic)]



