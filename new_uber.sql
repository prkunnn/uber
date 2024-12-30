-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- 主機： 127.0.0.1
-- 產生時間： 2024-12-29 13:40:39
-- 伺服器版本： 10.4.32-MariaDB
-- PHP 版本： 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- 資料庫： `foodpangolin`
--

-- --------------------------------------------------------

--
-- 資料表結構 `customer`
--

CREATE TABLE `customer` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `contact_info` varchar(255) DEFAULT NULL,
  `address` varchar(255) DEFAULT NULL,
  `delivery_status` enum('Idle','Accepted','PickedUp','Delivered') DEFAULT 'Idle',
  `password` varchar(13) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- 傾印資料表的資料 `customer`
--

INSERT INTO `customer` (`id`, `name`, `contact_info`, `address`, `delivery_status`, `password`) VALUES
(1, 'daniel', '0909090909', '台北市中正區仁愛路一段123號5樓', 'Idle', '321'),
(2, 'sebastian', '0912345678', '新北市板橋區民族路10巷20號', 'Idle', '321'),
(3, 'sam', '0912121212', '台中市西屯區台灣大道二段456巷78號', 'Idle', '321');

-- --------------------------------------------------------

--
-- 資料表結構 `deliveryperson`
--

CREATE TABLE `deliveryperson` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `vehicle_info` varchar(255) DEFAULT NULL,
  `contact_info` varchar(255) DEFAULT NULL,
  `current_status` enum('Idle','Accepted','PickedUp','Delivered') DEFAULT 'Idle'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- 資料表結構 `feedback`
--

CREATE TABLE `feedback` (
  `id` int(11) NOT NULL,
  `customer_id` int(11) DEFAULT NULL,
  `target_id` int(11) DEFAULT NULL,
  `feedback_text` text DEFAULT NULL,
  `rating` int(11) DEFAULT NULL,
  `created_at` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- 傾印資料表的資料 `feedback`
--

INSERT INTO `feedback` (`id`, `customer_id`, `target_id`, `feedback_text`, `rating`, `created_at`) VALUES
(10, 1, 4, '我最近光顧了這家位於市中心的鰻魚料理店，真是一次絕佳的美食體驗！店內裝潢典雅，環境舒適，服務人員親切且專業。', 5, '2024-12-26 00:00:00'),
(11, 2, 4, '他們的鰻魚飯絕對是招牌菜，烤得恰到好處的鰻魚搭配香軟的米飯，再淋上特製醬汁，每一口都是享受。      ', 4, '2024-12-26 00:00:00'),
(12, 3, 4, '這家鰻魚料理店無論是在食物的品質還是用餐的體驗上都無可挑剔。如果你是鰻魚愛好者，這裡絕對是值得一去的美食天堂。', 5, '2024-12-26 00:00:00'),
(22, 1, 4, '測試信息hello', 5, '2024-12-27 20:16:16'),
(23, 3, 11, 'very good', 5, '2024-12-29 20:16:58');

-- --------------------------------------------------------

--
-- 資料表結構 `menuitem`
--

CREATE TABLE `menuitem` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `price` int(11) NOT NULL,
  `description` text DEFAULT NULL,
  `availability_status` varchar(50) DEFAULT NULL,
  `merchant_id` int(11) DEFAULT NULL,
  `imgfile` varchar(100) NOT NULL DEFAULT 'dish_default.png',
  `type` varchar(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- 傾印資料表的資料 `menuitem`
--

INSERT INTO `menuitem` (`id`, `name`, `price`, `description`, `availability_status`, `merchant_id`, `imgfile`, `type`) VALUES
(6, '美式咖啡 (Americano)', 80, '濃郁的黑咖啡，不加奶和糖，咖啡的原味體驗。', 'Available', 1, 'menu-1.jpg', 'drink'),
(7, '拿鐵 (Latte)', 90, '濃縮咖啡加上絲滑的蒸汽牛奶，帶來濃郁奶香。', 'Available', 1, 'menu-2.jpg', 'hotdrink'),
(8, '卡布奇諾 (Cappuccino)', 95, '濃縮咖啡、少量牛奶和豐富的奶泡，口感豐富。', 'Available', 1, 'menu-3.jpg', 'drink'),
(9, '摩卡 (Mocha)', 55, '巧克力風味的咖啡，帶有絲滑的巧克力和咖啡香。', 'Available', 1, 'menu-4.jpg', 'drink'),
(10, '冰美式咖啡 (Iced Americano)', 80, '冰鎮的黑咖啡，清涼提神，適合夏日飲用。', 'Available', 1, 'menu-11.jpg', 'drink'),
(11, '冰拿鐵 (Iced Latte)', 90, '冰鎮的拿鐵，結合濃縮咖啡和冰涼牛奶的清爽口感。', 'Available', 1, 'menu-12.jpg', 'drink'),
(12, '冰焦糖瑪奇朵 (Iced Caramel Macchiato)', 100, '甜美的焦糖和濃縮咖啡的完美結合，甜蜜涼爽。', 'Available', 1, 'menu-13.jpg', 'drink'),
(13, '鰻魚飯 (Unagi Don)', 300, '精心烤製的鰻魚配上香軟的米飯，淋上特製的醬汁。', 'Available', 4, 'dishes_401.jpg', ''),
(14, '鰻魚壽司 (Unagi Sushi)', 200, '鰻魚片搭配壽司飯，用海苔捲起，口感豐富。', 'Available', 4, 'dishes_402.jpg', ''),
(15, '鰻魚天婦羅 (Unagi Tempura)', 280, '鰻魚裹上天婦羅漿後酥炸，外酥內嫩。', 'Available', 4, 'dishes_403.jpg', ''),
(16, '鰻魚烏龍麵 (Unagi Udon)', 250, '鰻魚與烏冬麵在熱湯中融合，鮮美無比。', 'Available', 4, 'dishes_404.jpg', ''),
(17, '草莓鮮奶油蛋糕', 300, '鮮甜草莓搭配綿密鮮奶油的經典蛋糕', 'Available', 11, 'dish_default.png', ''),
(18, '巧克力熔岩蛋糕', 333, '濃郁巧克力內餡，入口即化', 'Available', 11, 'dish_default.png', ''),
(19, '芒果慕斯蛋糕', 380, '清爽芒果慕斯，口感清新脆爽', 'Available', 11, 'dish_default.png', '');

-- --------------------------------------------------------

--
-- 資料表結構 `merchant`
--

CREATE TABLE `merchant` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `email` varchar(60) NOT NULL,
  `password` varchar(12) NOT NULL,
  `location` varchar(255) DEFAULT NULL,
  `contact_info` varchar(255) DEFAULT NULL,
  `delivery_status` enum('Idle','Accepted','PickedUp','Delivered') DEFAULT 'Idle',
  `img` varchar(55) NOT NULL DEFAULT 'restaurant_default.png'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- 傾印資料表的資料 `merchant`
--

INSERT INTO `merchant` (`id`, `name`, `email`, `password`, `location`, `contact_info`, `delivery_status`, `img`) VALUES
(4, '鰻魚屋', ' a@gmail.com', '123', NULL, NULL, 'Idle', 'restaurant_1.jpg'),
(5, '健康餐盒', ' b@gmail.com', '123', NULL, NULL, 'Idle', 'restaurant_2.jpg'),
(6, '春水堂', 'c@gmail.com', '123', NULL, NULL, 'Idle', 'restaurant_3.jpg'),
(7, '大和料理', ' e@gmail.com', '123', NULL, NULL, 'Idle', 'restaurant_4.jpg'),
(8, '品珍香', ' f@gmail.com', '123', NULL, NULL, 'Idle', 'restaurant_5.jpg'),
(9, 'Dan\'s cafe', ' g@gmail.com', '123', NULL, NULL, 'Idle', 'restaurant_6.jpg'),
(10, 'Dan\'s kitchen', 'h@edu.tw', '123', NULL, NULL, 'Idle', 'restaurant_default.png'),
(11, 'Dan\'s Cake Parlor', 'i@edu.tw', '321', NULL, NULL, 'Idle', 'restaurant_default.png');

-- --------------------------------------------------------

--
-- 資料表結構 `order`
--

CREATE TABLE `order` (
  `id` int(11) NOT NULL,
  `customer_id` int(11) DEFAULT NULL,
  `merchant_id` int(11) DEFAULT NULL,
  `delivery_person_id` int(11) DEFAULT NULL,
  `status` varchar(50) DEFAULT 'Pending',
  `delivery_address` varchar(255) DEFAULT NULL,
  `total_price` float DEFAULT NULL,
  `created_at` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- 傾印資料表的資料 `order`
--

INSERT INTO `order` (`id`, `customer_id`, `merchant_id`, `delivery_person_id`, `status`, `delivery_address`, `total_price`, `created_at`) VALUES
(28, 1, 4, NULL, 'Pending', '台北市中正區仁愛路一段123號5樓', 3570, '2024-12-29 11:47:07'),
(29, 2, 4, NULL, 'delivering', '新北市板橋區民族路10巷20號', 3850, '2024-12-29 12:13:05'),
(57, 2, 4, NULL, 'complete', '新北市板橋區民族路10巷20號', 500, '2024-12-29 13:00:48'),
(79, 1, 4, NULL, 'Pending', '台北市中正區仁愛路一段123號5樓', 3240, '2024-12-29 15:29:08'),
(80, 1, 4, NULL, 'Pending', '台北市中正區仁愛路一段123號5樓', 3240, '2024-12-29 15:34:45'),
(81, 1, 4, NULL, 'Pending', '台北市中正區仁愛路一段123號5樓', 3240, '2024-12-29 15:34:52'),
(84, 1, 4, NULL, 'Pending', '台北市中正區仁愛路一段123號5樓', 3240, '2024-12-29 15:37:51'),
(88, 1, 4, NULL, 'Pending', '台北市中正區仁愛路一段123號5樓', 3240, '2024-12-29 15:45:48'),
(89, 1, 4, NULL, 'Pending', '台北市中正區仁愛路一段123號5樓', 3240, '2024-12-29 15:46:50'),
(90, 1, 4, NULL, 'Pending', '台北市中正區仁愛路一段123號5樓', 3240, '2024-12-29 15:46:57'),
(93, 1, 4, NULL, 'Pending', '台北市中正區仁愛路一段123號5樓', 3240, '2024-12-29 15:51:12'),
(94, 1, 4, NULL, 'Pending', '台北市中正區仁愛路一段123號5樓', 3240, '2024-12-29 15:51:20'),
(95, 1, 4, NULL, 'Pending', '台北市中正區仁愛路一段123號5樓', 3240, '2024-12-29 15:51:41'),
(96, 1, 4, NULL, 'Pending', '台北市中正區仁愛路一段123號5樓', 3240, '2024-12-29 16:14:23'),
(97, 1, 4, NULL, 'Pending', '台北市中正區仁愛路一段123號5樓', 3240, '2024-12-29 16:15:11'),
(99, 1, 4, NULL, 'Pending', '台北市中正區仁愛路一段123號5樓', 3240, '2024-12-29 16:19:05'),
(100, 1, 4, NULL, 'Pending', '台北市中正區仁愛路一段123號5樓', 3240, '2024-12-29 16:20:07'),
(101, 1, 4, NULL, 'Pending', '台北市中正區仁愛路一段123號5樓', 3240, '2024-12-29 16:20:39'),
(102, 1, 4, NULL, 'Pending', '台北市中正區仁愛路一段123號5樓', 3240, '2024-12-29 16:21:15'),
(104, 1, 4, NULL, 'Pending', '台北市中正區仁愛路一段123號5樓', 3240, '2024-12-29 16:25:36'),
(105, 1, 4, NULL, 'Pending', '台北市中正區仁愛路一段123號5樓', 3240, '2024-12-29 16:25:56'),
(106, 1, 4, NULL, 'Pending', '台北市中正區仁愛路一段123號5樓', 3240, '2024-12-29 16:26:59'),
(107, 1, 4, NULL, 'Pending', '台北市中正區仁愛路一段123號5樓', 3240, '2024-12-29 16:28:40'),
(109, 1, 4, NULL, 'Delivered', '台北市中正區仁愛路一段123號5樓', 3240, '2024-12-29 16:36:17'),
(110, 3, 4, NULL, 'Delivered', '台中市西屯區台灣大道二段456巷78號', 3180, '2024-12-29 16:41:14'),
(111, 3, 4, NULL, 'Delivered', '台中市西屯區台灣大道二段456巷78號', 2300, '2024-12-29 17:06:20'),
(112, 3, 4, NULL, 'Delivered', '台中市西屯區台灣大道二段456巷78號', 2300, '2024-12-29 17:18:04'),
(113, 3, 4, NULL, 'Delivered', '台中市西屯區台灣大道二段456巷78號', 2300, '2024-12-29 17:19:23'),
(114, 3, 11, NULL, 'Delivered', '台中市西屯區台灣大道二段456巷78號', 1946, '2024-12-29 20:17:39');

-- --------------------------------------------------------

--
-- 資料表結構 `orderitem`
--

CREATE TABLE `orderitem` (
  `id` int(11) NOT NULL,
  `order_id` int(11) DEFAULT NULL,
  `menu_item_id` int(11) DEFAULT NULL,
  `quantity` int(11) NOT NULL,
  `price` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- 傾印資料表的資料 `orderitem`
--

INSERT INTO `orderitem` (`id`, `order_id`, `menu_item_id`, `quantity`, `price`) VALUES
(1, 60, 13, 5, 1500),
(2, 60, 14, 4, 800),
(3, 60, 15, 3, 840),
(120, 99, 15, 3, 840),
(150, 107, 13, 4, 1200),
(151, 107, 14, 6, 1200),
(152, 107, 15, 3, 840),
(153, 107, 16, 0, 0),
(154, 108, 13, 4, 1200),
(155, 108, 14, 6, 1200),
(156, 108, 15, 3, 840),
(157, 108, 16, 0, 0),
(158, 109, 13, 4, 1200),
(159, 109, 14, 6, 1200),
(160, 109, 15, 3, 840),
(161, 109, 16, 0, 0),
(162, 110, 13, 3, 900),
(163, 110, 14, 5, 1000),
(164, 110, 15, 1, 280),
(165, 110, 16, 4, 1000),
(166, 111, 13, 3, 900),
(167, 111, 14, 0, 0),
(168, 111, 15, 5, 1400),
(169, 111, 16, 0, 0),
(170, 112, 13, 3, 900),
(171, 112, 14, 0, 0),
(172, 112, 15, 5, 1400),
(173, 112, 16, 0, 0),
(174, 113, 13, 3, 900),
(175, 113, 14, 0, 0),
(176, 113, 15, 5, 1400),
(177, 113, 16, 0, 0),
(178, 114, 17, 3, 900),
(179, 114, 18, 2, 666),
(180, 114, 19, 1, 380);

--
-- 已傾印資料表的索引
--

--
-- 資料表索引 `customer`
--
ALTER TABLE `customer`
  ADD PRIMARY KEY (`id`);

--
-- 資料表索引 `feedback`
--
ALTER TABLE `feedback`
  ADD PRIMARY KEY (`id`),
  ADD KEY `customer_id` (`customer_id`);

--
-- 資料表索引 `menuitem`
--
ALTER TABLE `menuitem`
  ADD PRIMARY KEY (`id`),
  ADD KEY `merchant_id` (`merchant_id`);

--
-- 資料表索引 `merchant`
--
ALTER TABLE `merchant`
  ADD PRIMARY KEY (`id`);

--
-- 資料表索引 `order`
--
ALTER TABLE `order`
  ADD PRIMARY KEY (`id`),
  ADD KEY `customer_id` (`customer_id`),
  ADD KEY `merchant_id` (`merchant_id`),
  ADD KEY `delivery_person_id` (`delivery_person_id`);

--
-- 資料表索引 `orderitem`
--
ALTER TABLE `orderitem`
  ADD PRIMARY KEY (`id`),
  ADD KEY `order_id` (`order_id`),
  ADD KEY `menu_item_id` (`menu_item_id`);

--
-- 在傾印的資料表使用自動遞增(AUTO_INCREMENT)
--

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `customer`
--
ALTER TABLE `customer`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `feedback`
--
ALTER TABLE `feedback`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=24;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `menuitem`
--
ALTER TABLE `menuitem`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `merchant`
--
ALTER TABLE `merchant`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `order`
--
ALTER TABLE `order`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=115;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `orderitem`
--
ALTER TABLE `orderitem`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=181;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
