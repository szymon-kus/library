-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Cze 27, 2023 at 10:06 AM
-- Wersja serwera: 10.4.28-MariaDB
-- Wersja PHP: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `biblioteka`
--

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `czytelnicy`
--

CREATE TABLE `czytelnicy` (
  `id` int(11) NOT NULL,
  `imie` varchar(255) NOT NULL,
  `nazwisko` varchar(255) NOT NULL,
  `adres` varchar(255) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `numer_telefonu` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `czytelnicy`
--

INSERT INTO `czytelnicy` (`id`, `imie`, `nazwisko`, `adres`, `email`, `numer_telefonu`) VALUES
(1, 'Jan', 'Kowalski', NULL, NULL, NULL),
(2, 'Anna', 'Nowak', NULL, NULL, NULL),
(3, 'Piotr', 'Wójcik', NULL, NULL, NULL),
(4, 'Maria', 'Kowalczyk', NULL, NULL, NULL),
(5, 'Krzysztof', 'Lewandowski', NULL, NULL, NULL),
(6, 'Barbara', 'Zając', NULL, NULL, NULL),
(7, 'Tomasz', 'Szymański', NULL, NULL, NULL),
(8, 'Magdalena', 'Dąbrowska', NULL, NULL, NULL),
(9, 'Adam', 'Kozłowski', NULL, NULL, NULL),
(10, 'Katarzyna', 'Jankowska', NULL, NULL, NULL),
(11, 'Marek', 'Mazur', NULL, NULL, NULL),
(12, 'Agnieszka', 'Wojciechowska', NULL, NULL, NULL),
(13, 'Michał', 'Kwiatkowski', NULL, NULL, NULL),
(14, 'Joanna', 'Krawczyk', NULL, NULL, NULL),
(15, 'Marcin', 'Kaczmarek', NULL, NULL, NULL);

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `ksiazki`
--

CREATE TABLE `ksiazki` (
  `id` int(11) NOT NULL,
  `tytul` varchar(255) NOT NULL,
  `autor` varchar(255) NOT NULL,
  `gatunek` varchar(255) DEFAULT NULL,
  `rok_wydania` int(11) DEFAULT NULL,
  `liczba_egzemplarzy` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `ksiazki`
--

INSERT INTO `ksiazki` (`id`, `tytul`, `autor`, `gatunek`, `rok_wydania`, `liczba_egzemplarzy`) VALUES
(11, 'Dziady', 'Adam Mickiewicz', 'Dramat', 1822, 1),
(12, 'Wiedźmin', 'Andrzej Sapkowski', 'Fantasy', 1990, 1),
(13, 'Hobbit', 'J.R.R. Tolkien', 'Fantasy', 1937, 1),
(14, 'Harry Potter i Kamień Filozoficzny', 'J.K. Rowling', 'Fantasy', 1997, 1),
(15, '1984', 'George Orwell', 'Science Fiction', 1949, 1),
(16, 'Duma i uprzedzenie', 'Jane Austen', 'Romans', 1813, 1),
(17, 'Mistrz i Małgorzata', 'Michaił Bułhakow', 'Klasyczna literatura', 1967, 1),
(18, 'Zabić drozda', 'Harper Lee', 'Dramat', 1960, 1),
(19, 'Mały Książę', 'Antoine de Saint-Exupéry', 'Dziecięca literatura', 1943, 1),
(20, 'Pan Tadeusz', 'Adam Mickiewicz', 'Epika', 1834, 1),
(21, 'Lalka', 'Bolesław Prus', 'Realizm', 1890, 1),
(22, 'Harry Potter i Komnata Tajemnic', 'J.K. Rowling', 'Fantasy', 1998, 1),
(23, 'Dzieci z Bullerbyn', 'Astrid Lindgren', 'Dziecięca literatura', 1947, 1),
(24, 'W pustyni i w puszczy', 'Henryk Sienkiewicz', 'Przygodowa', 1910, 1),
(25, 'Mroczne materie', 'Philip Pullman', 'Fantasy', 1995, 1);

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `wypozyczenia`
--

CREATE TABLE `wypozyczenia` (
  `id` int(11) NOT NULL,
  `id_czytelnika` int(11) NOT NULL,
  `id_ksiazki` int(11) NOT NULL,
  `data_wypozyczenia` date NOT NULL,
  `data_zwrotu` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Indeksy dla zrzutów tabel
--

--
-- Indeksy dla tabeli `czytelnicy`
--
ALTER TABLE `czytelnicy`
  ADD PRIMARY KEY (`id`);

--
-- Indeksy dla tabeli `ksiazki`
--
ALTER TABLE `ksiazki`
  ADD PRIMARY KEY (`id`);

--
-- Indeksy dla tabeli `wypozyczenia`
--
ALTER TABLE `wypozyczenia`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_czytelnika` (`id_czytelnika`),
  ADD KEY `id_ksiazki` (`id_ksiazki`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `czytelnicy`
--
ALTER TABLE `czytelnicy`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;

--
-- AUTO_INCREMENT for table `ksiazki`
--
ALTER TABLE `ksiazki`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=26;

--
-- AUTO_INCREMENT for table `wypozyczenia`
--
ALTER TABLE `wypozyczenia`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `wypozyczenia`
--
ALTER TABLE `wypozyczenia`
  ADD CONSTRAINT `wypozyczenia_ibfk_1` FOREIGN KEY (`id_czytelnika`) REFERENCES `czytelnicy` (`id`),
  ADD CONSTRAINT `wypozyczenia_ibfk_2` FOREIGN KEY (`id_ksiazki`) REFERENCES `ksiazki` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
