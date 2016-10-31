create database IPL6;
use IPL6;
create table clusterStats(batsmanNumber int,bowlerNumber int,zeros int,ones int,twos int,threes int,fours int,fives int,sixes int,sevens int,Wickets int,Runs int,Balls int) row format delimited fields terminated by ',';
LOAD DATA LOCAL INPATH 'Dataset/clusterVcluster.csv' OVERWRITE INTO TABLE clusterStats;
Select * from clusterStats;
