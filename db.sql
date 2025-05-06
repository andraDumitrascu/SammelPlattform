-- MySQL dump 10.13  Distrib 8.0.42, for Win64 (x86_64)
--
-- Host: localhost    Database: sammelplattform
-- ------------------------------------------------------
-- Server version	8.0.42

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `bewertung`
--

DROP TABLE IF EXISTS `bewertung`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bewertung` (
  `sterneZahl` int NOT NULL,
  `BewertungID` int NOT NULL AUTO_INCREMENT,
  `Titel` varchar(25) NOT NULL,
  `Beschreibung` varchar(60) DEFAULT NULL,
  `NutzerID` int NOT NULL,
  `FotoID` int NOT NULL,
  PRIMARY KEY (`BewertungID`),
  KEY `fk_bewertung_schueler_idx` (`NutzerID`),
  KEY `fk_bewertung_foto_idx` (`FotoID`),
  CONSTRAINT `fk_bewertung_foto` FOREIGN KEY (`FotoID`) REFERENCES `foto` (`FotoID`),
  CONSTRAINT `fk_bewertung_schueler` FOREIGN KEY (`NutzerID`) REFERENCES `nutzer` (`NutzerID`),
  CONSTRAINT `chk_sterneZahl` CHECK (((`sterneZahl` >= 0) and (`sterneZahl` <= 5)))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bewertung`
--

LOCK TABLES `bewertung` WRITE;
/*!40000 ALTER TABLE `bewertung` DISABLE KEYS */;
/*!40000 ALTER TABLE `bewertung` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `foto`
--

DROP TABLE IF EXISTS `foto`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `foto` (
  `Beschreibung` varchar(60) DEFAULT NULL,
  `KategorieID` int NOT NULL,
  `FotoID` int NOT NULL AUTO_INCREMENT,
  `HochladeDatum` date DEFAULT NULL,
  `Gesamtbewertung` double NOT NULL,
  `OrdID` int unsigned NOT NULL,
  PRIMARY KEY (`FotoID`),
  KEY `fk_foto_kategorie_idx` (`KategorieID`),
  KEY `fk_foto_ordner_idx` (`OrdID`),
  CONSTRAINT `fk_foto_kategorie` FOREIGN KEY (`KategorieID`) REFERENCES `kategorie` (`KategorieID`),
  CONSTRAINT `fk_foto_ordner` FOREIGN KEY (`OrdID`) REFERENCES `ordner` (`OrdID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `foto`
--

LOCK TABLES `foto` WRITE;
/*!40000 ALTER TABLE `foto` DISABLE KEYS */;
/*!40000 ALTER TABLE `foto` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Temporary view structure for view `foto_mit_bewertungen`
--

DROP TABLE IF EXISTS `foto_mit_bewertungen`;
/*!50001 DROP VIEW IF EXISTS `foto_mit_bewertungen`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `foto_mit_bewertungen` AS SELECT 
 1 AS `FotoID`,
 1 AS `Gesamtbewertung`,
 1 AS `Bewertungsanzahl`*/;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `kategorie`
--

DROP TABLE IF EXISTS `kategorie`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `kategorie` (
  `KategorieID` int NOT NULL AUTO_INCREMENT,
  `Name` varchar(45) NOT NULL,
  PRIMARY KEY (`KategorieID`),
  UNIQUE KEY `Name_UNIQUE` (`Name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `kategorie`
--

LOCK TABLES `kategorie` WRITE;
/*!40000 ALTER TABLE `kategorie` DISABLE KEYS */;
/*!40000 ALTER TABLE `kategorie` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `nutzer`
--

DROP TABLE IF EXISTS `nutzer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `nutzer` (
  `Email` varchar(30) NOT NULL,
  `Passwort` varchar(45) NOT NULL,
  `Eingeloggt` tinyint NOT NULL,
  `Gesperrt` tinyint NOT NULL,
  `NutzerID` int NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`NutzerID`),
  UNIQUE KEY `Email_UNIQUE` (`Email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `nutzer`
--

LOCK TABLES `nutzer` WRITE;
/*!40000 ALTER TABLE `nutzer` DISABLE KEYS */;
/*!40000 ALTER TABLE `nutzer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ordner`
--

DROP TABLE IF EXISTS `ordner`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ordner` (
  `OrdID` int unsigned NOT NULL AUTO_INCREMENT,
  `titel` varchar(45) NOT NULL,
  `pfad` varchar(45) NOT NULL,
  `inOrdner` int unsigned DEFAULT NULL,
  PRIMARY KEY (`OrdID`),
  UNIQUE KEY `titel_UNIQUE` (`titel`),
  KEY `fk_inOrdner_idx` (`inOrdner`),
  CONSTRAINT `fk_inOrdner` FOREIGN KEY (`inOrdner`) REFERENCES `ordner` (`OrdID`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ordner`
--

LOCK TABLES `ordner` WRITE;
/*!40000 ALTER TABLE `ordner` DISABLE KEYS */;
/*!40000 ALTER TABLE `ordner` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Final view structure for view `foto_mit_bewertungen`
--

/*!50001 DROP VIEW IF EXISTS `foto_mit_bewertungen`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`admin`@`%` SQL SECURITY DEFINER */
/*!50001 VIEW `foto_mit_bewertungen` AS select `f`.`FotoID` AS `FotoID`,ifnull(round(avg(`b`.`sterneZahl`),2),0) AS `Gesamtbewertung`,count(`b`.`BewertungID`) AS `Bewertungsanzahl` from (`foto` `f` left join `bewertung` `b` on((`f`.`FotoID` = `b`.`FotoID`))) group by `f`.`FotoID` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-04-30 11:13:04
