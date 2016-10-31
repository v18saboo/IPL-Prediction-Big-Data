use IPL6;
INSERT OVERWRITE LOCAL DIRECTORY '/home/Dataset/final.txt'
ROW FORMAT DELIMITED
FIELDS TERMINATED BY '\t'
STORED AS TEXTFILE
select batsmanNumber,bowlerNumber,zeros/Balls,ones/Balls,twos/Balls,threes/Balls,fours/Balls,fives/Balls,sixes/Balls,Wickets/Balls,Runs,Balls from clusterStats;

