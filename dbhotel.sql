-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jun 10, 2022 at 01:51 PM
-- Server version: 10.4.21-MariaDB
-- PHP Version: 8.0.11

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `dbhotel`
--

-- --------------------------------------------------------

--
-- Table structure for table `tbcheck`
--

CREATE TABLE `tbcheck` (
  `checkID` int(11) NOT NULL,
  `rentID` int(11) NOT NULL,
  `staffID` int(11) NOT NULL,
  `check_in_date` datetime NOT NULL DEFAULT current_timestamp(),
  `check_out_date` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `tbcheck`
--

INSERT INTO `tbcheck` (`checkID`, `rentID`, `staffID`, `check_in_date`, `check_out_date`) VALUES
(1, 1, 1, '2022-06-10 18:49:48', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `tbcustomer`
--

CREATE TABLE `tbcustomer` (
  `customerID` int(11) NOT NULL,
  `name` varchar(50) NOT NULL,
  `email` varchar(50) NOT NULL,
  `username` varchar(30) NOT NULL,
  `password` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `tbcustomer`
--

INSERT INTO `tbcustomer` (`customerID`, `name`, `email`, `username`, `password`) VALUES
(1, 'Alissa Civilia', 'alissacivilia@gmail.com', 'acivilia', 'pbkdf2:sha256:260000$lJWj5zIiC');

-- --------------------------------------------------------

--
-- Table structure for table `tbrent`
--

CREATE TABLE `tbrent` (
  `rentID` int(11) NOT NULL,
  `customerID` int(11) NOT NULL,
  `roomID` int(11) NOT NULL,
  `date_stamp` date NOT NULL DEFAULT current_timestamp(),
  `date_from` date NOT NULL DEFAULT current_timestamp(),
  `date_to` date NOT NULL DEFAULT current_timestamp(),
  `price` int(11) NOT NULL,
  `day` int(11) NOT NULL,
  `amount` int(11) NOT NULL,
  `total` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `tbrent`
--

INSERT INTO `tbrent` (`rentID`, `customerID`, `roomID`, `date_stamp`, `date_from`, `date_to`, `price`, `day`, `amount`, `total`) VALUES
(1, 1, 1, '2022-06-10', '2022-06-10', '2022-06-17', 400000, 2, 1, 800000);

-- --------------------------------------------------------

--
-- Table structure for table `tbroom`
--

CREATE TABLE `tbroom` (
  `roomID` int(11) NOT NULL,
  `name` varchar(50) NOT NULL,
  `price` int(11) NOT NULL,
  `stock` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `tbroom`
--

INSERT INTO `tbroom` (`roomID`, `name`, `price`, `stock`) VALUES
(1, 'Standard', 400000, 12),
(2, 'Standard - View', 500000, 15),
(3, 'Deluxe', 600000, 15),
(4, 'Deluxe - View', 700000, 15),
(5, 'Suite', 2500000, 0);

-- --------------------------------------------------------

--
-- Table structure for table `tbstaff`
--

CREATE TABLE `tbstaff` (
  `staffID` int(11) NOT NULL,
  `name` varchar(50) NOT NULL,
  `username` varchar(30) NOT NULL,
  `password` varchar(30) NOT NULL,
  `roleID` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `tbstaff`
--

INSERT INTO `tbstaff` (`staffID`, `name`, `username`, `password`, `roleID`) VALUES
(1, 'Super Admin', 'admin', 'admin', 1),
(2, 'George Washington', 'gwashington', 'gwashington', 2),
(3, 'Milly Brown', 'mbrown', 'mbrown', 3);

-- --------------------------------------------------------

--
-- Table structure for table `tbstaffrole`
--

CREATE TABLE `tbstaffrole` (
  `roleID` int(11) NOT NULL,
  `name` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `tbstaffrole`
--

INSERT INTO `tbstaffrole` (`roleID`, `name`) VALUES
(1, 'Admin'),
(2, 'Manager'),
(3, 'Staff');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `tbcheck`
--
ALTER TABLE `tbcheck`
  ADD PRIMARY KEY (`checkID`),
  ADD KEY `rentID` (`rentID`,`staffID`),
  ADD KEY `tb_check_ibfk_2` (`staffID`);

--
-- Indexes for table `tbcustomer`
--
ALTER TABLE `tbcustomer`
  ADD PRIMARY KEY (`customerID`);

--
-- Indexes for table `tbrent`
--
ALTER TABLE `tbrent`
  ADD PRIMARY KEY (`rentID`),
  ADD KEY `customerID` (`customerID`,`roomID`),
  ADD KEY `rent-room` (`roomID`);

--
-- Indexes for table `tbroom`
--
ALTER TABLE `tbroom`
  ADD PRIMARY KEY (`roomID`);

--
-- Indexes for table `tbstaff`
--
ALTER TABLE `tbstaff`
  ADD PRIMARY KEY (`staffID`),
  ADD KEY `roleID` (`roleID`);

--
-- Indexes for table `tbstaffrole`
--
ALTER TABLE `tbstaffrole`
  ADD PRIMARY KEY (`roleID`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `tbcheck`
--
ALTER TABLE `tbcheck`
  MODIFY `checkID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `tbcustomer`
--
ALTER TABLE `tbcustomer`
  MODIFY `customerID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `tbrent`
--
ALTER TABLE `tbrent`
  MODIFY `rentID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `tbroom`
--
ALTER TABLE `tbroom`
  MODIFY `roomID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `tbstaff`
--
ALTER TABLE `tbstaff`
  MODIFY `staffID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `tbstaffrole`
--
ALTER TABLE `tbstaffrole`
  MODIFY `roleID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `tbcheck`
--
ALTER TABLE `tbcheck`
  ADD CONSTRAINT `tbcheck_ibfk_1` FOREIGN KEY (`rentID`) REFERENCES `tbrent` (`rentID`),
  ADD CONSTRAINT `tbcheck_ibfk_2` FOREIGN KEY (`staffID`) REFERENCES `tbstaff` (`staffID`);

--
-- Constraints for table `tbrent`
--
ALTER TABLE `tbrent`
  ADD CONSTRAINT `rent-customer` FOREIGN KEY (`customerID`) REFERENCES `tbcustomer` (`customerID`),
  ADD CONSTRAINT `rent-room` FOREIGN KEY (`roomID`) REFERENCES `tbroom` (`roomID`);

--
-- Constraints for table `tbstaff`
--
ALTER TABLE `tbstaff`
  ADD CONSTRAINT `staff - role` FOREIGN KEY (`roleID`) REFERENCES `tbstaffrole` (`roleID`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
