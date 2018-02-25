CREATE TABLE `proxy_ip` (
  `pid` int(11) NOT NULL AUTO_INCREMENT,
  `ip` varchar(100) NOT NULL,
  `port` int(11) NOT NULL,
  `position` varchar(100) DEFAULT NULL,
  `anonymous` varchar(100) DEFAULT NULL,
  `type` varchar(100) NOT NULL,
  `speed` float DEFAULT NULL,
  `link_time` float DEFAULT NULL,
  `ttl` varchar(10) NOT NULL,
  `ttl_minutes` int(11) NOT NULL,
  `last_check_time` varchar(100) NOT NULL,
  PRIMARY KEY (`pid`)
) ENGINE=InnoDB AUTO_INCREMENT=169 DEFAULT CHARSET=utf8