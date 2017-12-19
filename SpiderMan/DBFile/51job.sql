-- MySQL dump 10.13  Distrib 5.7.17, for macos10.12 (x86_64)
--
-- Host: 127.0.0.1    Database: spider
-- ------------------------------------------------------
-- Server version	5.7.19

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `51job_city`
--

DROP TABLE IF EXISTS `51job_city`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `51job_city` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `city_name` varchar(45) DEFAULT NULL COMMENT '''城市名称''',
  `city_code` varchar(45) DEFAULT NULL,
  `num` int(11) DEFAULT NULL COMMENT '招聘数量',
  `created_at` int(11) DEFAULT NULL COMMENT '创建时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `city_name_UNIQUE` (`city_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='51job的城市';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `51job_company`
--

DROP TABLE IF EXISTS `51job_company`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `51job_company` (
  `full_name` varchar(255) DEFAULT NULL COMMENT '公司名称',
  `size` varchar(45) DEFAULT NULL COMMENT '公司规模',
  `company_nature` varchar(255) DEFAULT NULL COMMENT '公司性质',
  `industry` varchar(255) DEFAULT NULL COMMENT '行业',
  `address` varchar(255) DEFAULT NULL COMMENT '公司地址',
  `company_url` varchar(255) DEFAULT NULL COMMENT '页面url',
  `postcode` varchar(45) DEFAULT NULL,
  `num` int(11) DEFAULT NULL COMMENT '招聘数量',
  `created_at` int(11) DEFAULT NULL COMMENT '创建时间',
  `company_md5` varchar(60) NOT NULL COMMENT '公司名称的md5值',
  PRIMARY KEY (`company_md5`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='51Job的招聘公司';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `51job_position`
--

DROP TABLE IF EXISTS `51job_position`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `51job_position` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(500) DEFAULT NULL COMMENT '职位名称',
  `city` varchar(45) DEFAULT NULL COMMENT '所在城市',
  `district` varchar(45) DEFAULT NULL COMMENT '所在地区',
  `salary` varchar(45) DEFAULT NULL,
  `work_year` varchar(45) DEFAULT NULL,
  `education` varchar(45) DEFAULT NULL COMMENT '学历',
  `recruit_num` varchar(45) DEFAULT NULL COMMENT '招聘人数',
  `publish_time` varchar(45) DEFAULT NULL COMMENT '招聘时间',
  `language` varchar(45) DEFAULT NULL COMMENT '外语条件',
  `industry` varchar(255) DEFAULT NULL COMMENT '职位标签',
  `position_labels` varchar(255) DEFAULT NULL,
  `advantage` varchar(500) DEFAULT NULL COMMENT '福利',
  `content` longtext COMMENT '职位描述',
  `location` varchar(255) DEFAULT NULL COMMENT '工作地点',
  `phone_num` varchar(255) DEFAULT NULL COMMENT '联系电话',
  `email` varchar(500) DEFAULT NULL COMMENT '联系邮箱',
  `created_at` int(11) DEFAULT NULL COMMENT '创建时间',
  `url` varchar(255) DEFAULT NULL COMMENT '页面地址',
  `url_md5` varchar(255) DEFAULT NULL COMMENT 'url的md5值',
  `company_md5` varchar(100) DEFAULT NULL COMMENT '公司名称的md5值',
  PRIMARY KEY (`id`),
  UNIQUE KEY `url_md5_UNIQUE` (`url_md5`),
  KEY `index_city` (`city`),
  FULLTEXT KEY `ft_name` (`name`),
  FULLTEXT KEY `ft_pn` (`name`,`position_labels`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COMMENT='51job职位详情';
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-10-26 19:16:53
