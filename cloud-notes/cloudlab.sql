-- MySQL dump 10.13  Distrib 9.7.1, for Linux (x86_64)
--
-- Host: localhost    Database: cloudlab
-- ------------------------------------------------------
-- Server version	9.7.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
SET @MYSQLDUMP_TEMP_LOG_BIN = @@SESSION.SQL_LOG_BIN;
SET @@SESSION.SQL_LOG_BIN= 0;

--
-- GTID state at the beginning of the backup 
--

SET @@GLOBAL.GTID_PURGED=/*!80000 '+'*/ '77ac3f0a-7480-11f1-aa83-0242ac140002:1-94';

--
-- Table structure for table `notes`
--

DROP TABLE IF EXISTS `notes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `notes` (
  `id` int NOT NULL AUTO_INCREMENT,
  `note` text NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `user_id` int DEFAULT NULL,
  `title` varchar(255) DEFAULT NULL,
  `pinned` tinyint(1) DEFAULT '0',
  `category` varchar(50) DEFAULT 'General',
  `filename` varchar(255) DEFAULT NULL,
  `favorite` tinyint(1) DEFAULT '0',
  `deleted` tinyint(1) DEFAULT '0',
  `attachment` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `notes_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `notes`
--

LOCK TABLES `notes` WRITE;
/*!40000 ALTER TABLE `notes` DISABLE KEYS */;
INSERT INTO `notes` VALUES (1,'Welcome to Cloud Notes!','2026-07-07 13:30:02',NULL,NULL,0,'General',NULL,0,0,NULL),(11,'perfectto','2026-07-08 15:52:26',NULL,NULL,0,'General',NULL,0,0,NULL),(14,'hai i am raja','2026-07-11 13:25:56',4,NULL,0,'General',NULL,0,0,NULL),(15,'vengo dall Italia','2026-07-13 12:22:47',5,NULL,1,'General',NULL,0,1,NULL),(16,'ti amo','2026-07-15 13:27:16',5,NULL,0,'General',NULL,0,0,NULL),(18,'Roma in Italia','2026-07-15 13:59:04',5,'In Italia',0,'General',NULL,0,0,NULL),(19,'L\'auto dei miei sogini','2026-07-18 13:37:35',5,'Il mio sogno',0,'Personal','maserati.jpeg',0,1,NULL),(20,'Amo la mia car','2026-07-22 12:57:52',5,'Maserati',1,'Personal','maserati.jpeg',0,1,NULL),(21,'my car\r\n','2026-07-22 13:06:40',5,'',0,'General','maserati.jpeg',0,1,NULL),(22,'IL mio sogno','2026-07-22 13:19:36',5,'maseratri',0,'General','maserati.jpeg',0,1,NULL),(23,'car','2026-07-22 13:22:09',5,'car',0,'General','maserati.jpeg',0,1,NULL),(24,'la car e songo','2026-07-24 14:06:21',5,'Maserati',1,'Personal','maserati.jpeg',0,0,NULL);
/*!40000 ALTER TABLE `notes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `password` varchar(225) NOT NULL,
  `theme` varchar(10) DEFAULT 'light',
  `email` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (4,'senthilraja','$2b$12$NstutTmDmGaALdVoQtrES.z6KGKR0iRGKMmCRBgSX83l1zkZpGD82','light',NULL),(5,'suryaa','$2b$12$y8CSwc38ndBr1LUglw.Z9eUMQm1Bab2Vwgq4yvfb7pZDH.vpcR9jG','dark','suryaa4428@gmail.com');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
SET @@SESSION.SQL_LOG_BIN = @MYSQLDUMP_TEMP_LOG_BIN;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-08-02 11:09:43
