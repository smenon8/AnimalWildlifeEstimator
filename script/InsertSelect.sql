CREATE TABLE IF NOT EXISTS `AnimalPhotoBias`.`HITResultsConsolidated` (
  `gid` INT(11) NOT NULL,
  `shared` INT(11) NULL DEFAULT NULL,
  `notShared` INT(11) NULL DEFAULT NULL,
  `total` INT(11) NULL DEFAULT NULL,
  `annotation_id` INT(11) NULL DEFAULT NULL,
  `species` VARCHAR(100) NULL DEFAULT NULL,
  `sex` VARCHAR(100) NULL DEFAULT NULL,
  `age_month` VARCHAR(100) NULL DEFAULT NULL,
  `exemplar` INT(11) NULL DEFAULT NULL,
  `image_quality` VARCHAR(100) NULL DEFAULT NULL,
  PRIMARY KEY (`gid`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;

create table if not exists workerData (workerID varchar(100),shares int,notShares int);

select image_quality as image_qual,sum(shared)/20 as SUM_NORMALIZED_SHARE_COUNT,
	sum(notShared)/20 as SUM_NORMALIZED_NOT_SHARED_COUNT,
    count(gid) as NORMALIZED_COUNT,
	sum(shared)*100/(20*count(gid)) as SHARED_PERCENTAGE,
    sum(notShared)*100/(20*count(gid)) as NOT_SHARED_PERCENTAGE
from HITResultsConsolidated
group by image_quality;