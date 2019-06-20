-- MySQL dump 10.13  Distrib 8.0.16, for Win64 (x86_64)
--
-- Host: localhost    Database: rakugaki_battle
-- ------------------------------------------------------
-- Server version	8.0.16

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
 SET NAMES utf8mb4 ;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `player_data`
--

DROP TABLE IF EXISTS `player_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `player_data` (
  `id` char(8) NOT NULL,
  `name` varchar(512) DEFAULT NULL,
  `score` int(11) DEFAULT NULL,
  `odai` varchar(512) DEFAULT NULL,
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `player_data`
--

LOCK TABLES `player_data` WRITE;
/*!40000 ALTER TABLE `player_data` DISABLE KEYS */;
INSERT INTO `player_data` VALUES ('FnOQGua6','',747,'car','2019-06-19 09:06:59'),('iccFKLHt','くらはし',544,'cat','2019-06-19 08:48:45'),('JL7eTVWZ','ssss',452,'cat','2019-06-19 08:05:12'),('KbYoKCUa','ななな',78,'mouse','2019-06-20 03:34:16'),('KKpmbQ48','ss',NULL,'cat','2019-06-19 08:01:31'),('KTtZ34gz','',NULL,'rabbit','2019-06-19 09:20:26'),('QFYcMBha','',NULL,'rabbit','2019-06-19 09:12:07'),('tiz6oWKu','',NULL,'cat','2019-06-19 09:20:21'),('v70Lsnvb','みじんこ',432,'car','2019-06-19 08:49:29'),('xNYkbFvX','ssss',837,'cat','2019-06-19 08:02:46'),('ZLwlJnoK','ssss',NULL,'rabbit','2019-06-19 09:50:27');
/*!40000 ALTER TABLE `player_data` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-06-20 16:25:11
