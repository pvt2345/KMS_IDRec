-- MySQL dump 10.13  Distrib 5.7.17, for Win64 (x86_64)
--
-- Host: localhost    Database: qlvb
-- ------------------------------------------------------
-- Server version	5.7.21-log
CREATE DATABASE qlvb IF NOT EXISTS;
use qlvb;
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
-- Table structure for table `dm_type`
--

DROP TABLE IF EXISTS `dm_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dm_type` (
  `code` varchar(45) NOT NULL,
  `name` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dm_type`
--

LOCK TABLES `dm_type` WRITE;
/*!40000 ALTER TABLE `dm_type` DISABLE KEYS */;
/*!40000 ALTER TABLE `dm_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `document`
--

DROP TABLE IF EXISTS `document`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `document` (
  `id` int(11) NOT NULL auto_increment,
  `can_cu` text,
  `loai_van_ban` varchar(75) DEFAULT NULL,
  `noi_ban_hanh` varchar(100) DEFAULT NULL,
  `noi_nhan` text,
  `so_van_ban` varchar(45) DEFAULT NULL,
  `phu_luc` text,
  `thoi_gian` varchar(45) DEFAULT NULL,
  `trich_yeu` text,
  `yeu_cau` text,
  `dia_diem` varchar(45) DEFAULT NULL,
  `path` text,
  `title` text,
  `subtitle` text,
  `content` text,
  `file` blob,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `document`
--

LOCK TABLES `document` WRITE;
/*!40000 ALTER TABLE `document` DISABLE KEYS */;
/*!40000 ALTER TABLE `document` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `document_dtl`
--

DROP TABLE IF EXISTS `document_dtl`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `document_dtl` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `parent` varchar(45) DEFAULT NULL,
  `type` varchar(45) DEFAULT NULL,
  `stt` varchar(45) DEFAULT NULL,
  `tieu_de` text,
  `content` text,
  `reference` text,
  `tokens` text,
  `page` int(11),
  FULLTEXT (tieu_de, content),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- ALTER TABLE document_dtl ADD FULLTEXT (tieu_de, content);
--
--
-- Dumping data for table `document_dtl`
--

LOCK TABLES `document_dtl` WRITE;
/*!40000 ALTER TABLE `document_dtl` DISABLE KEYS */;
/*!40000 ALTER TABLE `document_dtl` ENABLE KEYS */;
UNLOCK TABLES;

--

DROP TABLE IF EXISTS `type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name_type` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

LOCK TABLES `type` WRITE;
/*!40000 ALTER TABLE `type` DISABLE KEYS */;
/*!40000 ALTER TABLE  `type` ENABLE KEYS */;
UNLOCK TABLES;

--

DROP TABLE IF EXISTS `lien_ket_vb`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `lien_ket_vb` (
    `so_van_ban` varchar(20),
    `vb_lien_ket` varchar(20),
    `type_id` int,
  PRIMARY KEY (`so_van_ban`, `vb_lien_ket`),
  FOREIGN KEY (type_id) REFERENCES `type`(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

LOCK TABLES `lien_ket_vb` WRITE;
/*!40000 ALTER TABLE `lien_ket_vb` DISABLE KEYS */;
/*!40000 ALTER TABLE `lien_ket_vb` ENABLE KEYS */;
UNLOCK TABLES;


INSERT INTO `type` (`name_type`) VALUES('Căn cứ');

DROP VIEW IF EXISTS `lien_ket`;

CREATE VIEW `lien_ket` AS SELECT lk.so_van_ban as `Số văn bản`, lk.vb_lien_ket as `Văn bản liên kết`, `type`.name_type
as `Loại liên kết` from lien_ket_vb as lk INNER JOIN `type` ON lk.type_id = `type`.id;
--
-- Dumping routines for database 'qlvb'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-08-15 14:31:17