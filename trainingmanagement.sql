-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Apr 04, 2023 at 10:32 AM
-- Server version: 8.0.31
-- PHP Version: 8.0.26

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `trainingmanagement`
--

-- --------------------------------------------------------

--
-- Table structure for table `batch`
--

DROP TABLE IF EXISTS `batch`;
CREATE TABLE IF NOT EXISTS `batch` (
  `id` int NOT NULL AUTO_INCREMENT,
  `batchname` varchar(255) NOT NULL,
  `coursename` varchar(255) NOT NULL,
  `courseID` int NOT NULL,
  `trainername` varchar(255) NOT NULL,
  `courseduration` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `batchstartdate` date NOT NULL,
  `batchenddate` date NOT NULL,
  `batchtime` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=59 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `batch`
--

INSERT INTO `batch` (`id`, `batchname`, `coursename`, `courseID`, `trainername`, `courseduration`, `batchstartdate`, `batchenddate`, `batchtime`) VALUES
(55, 'JavaBatch1', 'Java', 27, 'Santhosh', '4', '2023-04-04', '2023-08-03', '9:00 AM - 10:00 AM'),
(56, 'PythonBatch1', 'Python', 26, 'Pradeep', '4', '2023-04-03', '2023-08-04', '10:00 AM - 11:00 AM'),
(57, 'JavaBatch2', 'Java', 27, 'Santhosh', '4', '2023-04-04', '2023-08-04', '2:00 PM - 3:00 PM'),
(58, 'PythonBatch2', 'Python', 26, 'Keshav', '4', '2023-04-03', '2023-08-03', '2:00 PM - 3:00 PM');

-- --------------------------------------------------------

--
-- Table structure for table `course`
--

DROP TABLE IF EXISTS `course`;
CREATE TABLE IF NOT EXISTS `course` (
  `id` int NOT NULL AUTO_INCREMENT,
  `course_name` varchar(255) NOT NULL,
  `course_description` varchar(255) NOT NULL,
  `course_duration` varchar(255) NOT NULL,
  `course_price` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=28 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `course`
--

INSERT INTO `course` (`id`, `course_name`, `course_description`, `course_duration`, `course_price`) VALUES
(27, 'Java', 'Basic concepts', '4 months', '200'),
(26, 'Python', 'Basic concepts', '4 months', '200');

-- --------------------------------------------------------

--
-- Table structure for table `info`
--

DROP TABLE IF EXISTS `info`;
CREATE TABLE IF NOT EXISTS `info` (
  `username` varchar(200) NOT NULL,
  `password` varchar(500) DEFAULT NULL,
  `name` varchar(100) DEFAULT NULL,
  `prof` int DEFAULT NULL,
  `street` varchar(100) DEFAULT NULL,
  `city` varchar(50) DEFAULT NULL,
  `phone` varchar(32) DEFAULT NULL,
  `time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`username`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `info`
--

INSERT INTO `info` (`username`, `password`, `name`, `prof`, `street`, `city`, `phone`, `time`) VALUES
('Shivraj', '$5$rounds=535000$4QV3OBUG2A4x7X3N$iaabPvN./ko192De46O3Epwj5q697BgYHHdnQ/aDO1B', 'Shivraj', 4, 'Street1', 'City1', '0123456777', '2023-04-03 18:59:08'),
('Admin', '$5$rounds=535000$ieyp6HcB3HxFQBrM$DOIzUkDfDQ8Q4PMYXopPKum392DuG.gRNZDpw5c0r4B', 'Devika', 1, 'Castle house', 'Dublin 1', '123456789', '2023-02-22 21:17:34'),
('Sandhya', '$5$rounds=535000$0rEW49D91hz3gWI8$sifkJV3yn4QX0spV62Wp3ljJSHFReib4EMFJrFOmJ81', 'Sandhya', 2, 'Street8', 'City8', '0123456722', '2023-03-27 13:40:17'),
('Pradeep', '$5$rounds=535000$eS8XKyn.0./bDNTK$m5U6uPxsOvd8zBqlf2cTjRRYK8d96hSmrEdDEze5WM9', 'Pradeep', 3, 'Street1', 'City1', '0123456788', '2023-04-03 15:36:43'),
('Jayraj', '$5$rounds=535000$M.UGek8JpwU2hq6k$/s3OuoB.zAoki17Av8UFMHkzvkmX8fJgq/J/v3VJdTD', 'Jayraj', 4, 'southwood', 'dublin', '0123456777', '2023-04-03 19:00:35'),
('Raj', '$5$rounds=535000$R6u9KZSrxQmz8Zen$lK2UaibhibgkU8t1pnuhtRtsYW680UogH009JPa/wq0', 'Raj', 4, 'ssdd', 'cc', '0123456777', '2023-04-03 19:11:53'),
('Santhosh', '$5$rounds=535000$RuJ36zsrIuNPG6vh$UdX4m2ko8JgFZrYsGbwnmbhPW4/7p4CRR.ip03igq15', 'Santhosh', 3, 'Street1', 'City1', '0123456722', '2023-04-03 19:10:34'),
('Keshav', '$5$rounds=535000$eyFWd82J5oOQU7rO$SG5FjOd4/znvewUNYYWIP4E.O53BogMMZBADqW6qNf9', 'Keshav', 3, 'Street1', 'city1', '0123456777', '2023-04-04 09:37:01'),
('Akshay', '$5$rounds=535000$HjlIVtaYPvLiyi19$GSnLT9kfTyKEGhzeRr5e8NXDdB5QdAKF9RMj9KlRnt1', 'Akshay', 4, 'Street1', 'City1', '0123456723', '2023-04-04 09:41:10'),
('Akshaypythonbatch', '$5$rounds=535000$kQzyLVzMZ6GZeXa.$wWwQw3998Py8RYII/hccO2TMQVgMurKLpcPvKJrLlh1', 'Akshay', 4, 'Street1', 'City1', '0123456722', '2023-04-04 09:42:20'),
('Rajpythonbatch', '$5$rounds=535000$07OkWImBtOW.9SdG$uvZxBkx13VXxAJrf/0XdRE5Q6fA0szJjeypHON9l47A', 'Raj', 4, 'street2', 'city2', '0123456788', '2023-04-04 09:43:41'),
('Gopal', '$5$rounds=535000$R.CPnCpWxUnqjVtl$R8nVxGRdm7kFBqITgVR76ksEzLc6lpcrUkm9V0zMOsA', 'Gopal', 4, 'Street1', 'City1', '0123456788', '2023-04-04 09:46:33'),
('1234', '$5$rounds=535000$bmewVYIjgHShbrSq$1qr/9T8igvto9cOz6I.Lg5eAGMoa840SRzy3ly1lUh5', 'Antony', 4, 'Street8', 'City8', '0123456723', '2023-04-04 09:47:18'),
('Teena', '$5$rounds=535000$DEPOa8j8BxBREoBS$n/It7ONMspYdOcXRqzsHlvO/MeVyvkO/d3b6ckkT1UD', 'Teena', 4, 'Stree3', 'cirty4', '0123456734', '2023-04-04 09:48:04'),
('Amith', '$5$rounds=535000$JGCqqdAiSRqvz62k$ITnzK6beu4wsrJebX4UJGK2aDYwut.lPbXWrXSOanTD', 'Amith', 4, 'Street1', 'City1', '0123456789', '2023-04-04 09:48:41'),
('Keerthi', '$5$rounds=535000$Xc5DGA.TW.UH3Ny7$Yzsg3Gt/y2k/zbwbhAcyJoBH9tlz1FBEk3VL04ibgNA', 'Keerthi', 4, 'Strett9', 'Cit1', '0123456777', '2023-04-04 09:49:20');

-- --------------------------------------------------------

--
-- Table structure for table `members`
--

DROP TABLE IF EXISTS `members`;
CREATE TABLE IF NOT EXISTS `members` (
  `username` varchar(200) NOT NULL,
  `coursename` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `trainor` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `batch` varchar(255) NOT NULL,
  `courseID` int NOT NULL,
  `batchID` int NOT NULL,
  PRIMARY KEY (`username`),
  KEY `plan` (`coursename`),
  KEY `trainor` (`trainor`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `members`
--

INSERT INTO `members` (`username`, `coursename`, `trainor`, `batch`, `courseID`, `batchID`) VALUES
('Akshay', 'Java', 'Santhosh', 'JavaBatch1', 27, 55),
('Raj', 'Java', 'Santhosh', 'JavaBatch1', 27, 55),
('Akshaypythonbatch', 'Python', 'Pradeep', 'PythonBatch1', 26, 56),
('Rajpythonbatch', 'Python', 'Pradeep', 'PythonBatch1', 26, 56),
('Gopal', 'Java', 'Santhosh', 'JavaBatch2', 27, 57),
('1234', 'Java', 'Santhosh', 'JavaBatch2', 27, 57),
('Teena', 'Java', 'Santhosh', 'JavaBatch2', 27, 57),
('Amith', 'Python', 'Keshav', 'PythonBatch2', 26, 58),
('Keerthi', 'Python', 'Keshav', 'PythonBatch2', 26, 58);

-- --------------------------------------------------------

--
-- Table structure for table `progress`
--

DROP TABLE IF EXISTS `progress`;
CREATE TABLE IF NOT EXISTS `progress` (
  `username` varchar(200) NOT NULL,
  `testdate` date NOT NULL,
  `batchname` varchar(255) NOT NULL,
  `date` date NOT NULL,
  `daily_result` varchar(200) DEFAULT NULL,
  `time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `rate` varchar(200) DEFAULT NULL,
  `batchID` int NOT NULL,
  PRIMARY KEY (`username`,`date`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `progress`
--

INSERT INTO `progress` (`username`, `testdate`, `batchname`, `date`, `daily_result`, `time`, `rate`, `batchID`) VALUES
('Rajpythonbatch', '2023-04-04', 'PythonBatch1', '2023-04-04', 'Practice more', '2023-04-04 09:53:30', '2', 56);

-- --------------------------------------------------------

--
-- Table structure for table `receps`
--

DROP TABLE IF EXISTS `receps`;
CREATE TABLE IF NOT EXISTS `receps` (
  `username` varchar(200) NOT NULL,
  PRIMARY KEY (`username`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `receps`
--

INSERT INTO `receps` (`username`) VALUES
('Receptionist'),
('Sandhya');

-- --------------------------------------------------------

--
-- Table structure for table `test`
--

DROP TABLE IF EXISTS `test`;
CREATE TABLE IF NOT EXISTS `test` (
  `id` int NOT NULL AUTO_INCREMENT,
  `coursename` varchar(255) NOT NULL,
  `batchname` varchar(255) NOT NULL,
  `testname` varchar(255) NOT NULL,
  `testdate` date NOT NULL,
  `teststarttime` time(6) NOT NULL,
  `testendtime` time(6) NOT NULL,
  `courseID` int NOT NULL,
  `batchID` int NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `test`
--

INSERT INTO `test` (`id`, `coursename`, `batchname`, `testname`, `testdate`, `teststarttime`, `testendtime`, `courseID`, `batchID`) VALUES
(8, 'Python', 'PythonBatch1', 'aptitude', '2023-04-04', '10:00:00.000000', '11:00:00.000000', 26, 53),
(11, 'Python', 'PythonBatch1', 'aptitude', '2023-04-04', '10:30:00.000000', '11:30:00.000000', 26, 56);

-- --------------------------------------------------------

--
-- Table structure for table `trainors`
--

DROP TABLE IF EXISTS `trainors`;
CREATE TABLE IF NOT EXISTS `trainors` (
  `username` varchar(200) NOT NULL,
  `expertise` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `courseID` int NOT NULL,
  PRIMARY KEY (`username`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `trainors`
--

INSERT INTO `trainors` (`username`, `expertise`, `courseID`) VALUES
('Santhosh', 'Java', 27),
('Pradeep', 'Python', 26),
('Keshav', 'Python', 26);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
