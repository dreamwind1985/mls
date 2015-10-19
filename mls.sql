--
-- Current Database: mls
--


DROP DATABASE `mls`;CREATE DATABASE `mls` DEFAULT CHARACTER SET utf8;

USE `mls`;

DROP TABLE IF EXISTS `link_info`;
CREATE TABLE `link_info`(
	`link` varchar(256) NOT NULL,
	`id` varchar(64) DEFAULT NULL,
	`name` varchar(128) DEFAULT NULL,
	`kind` int(8) DEFAULT NULL,
	`type` int(8) DEFAULT NULL,
	`date` timestamp,
	PRIMARY KEY (`link`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `statistic`;
CREATE TABLE `statistic`(
	`id` varchar(64) DEFAULT NULL,
	`xiaoliang` int(8) DEFAULT NULL,
	`pinglun` int(8) DEFAULT NULL,
	`time` timestamp ,
	`xihuan` int(12) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8;


