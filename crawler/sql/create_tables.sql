CREATE TABLE `urls` (
  `id` bigint(11) NOT NULL AUTO_INCREMENT,
  `url` varchar(500) NOT NULL,
  PRIMARY KEY (`id`),
  KEY (`url`(200))
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `words` (
  `id` bigint(11) NOT NULL AUTO_INCREMENT,
  `word` varchar(200) NOT NULL,
  PRIMARY KEY (`id`),
  KEY (`word`(200))
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `links` (
  `id` bigint(11) NOT NULL AUTO_INCREMENT,
  `from` bigint(11) NOT NULL,
  `to` bigint(11) NOT NULL,
  PRIMARY KEY (`id`),
  FOREIGN KEY (`from`) references `urls` (`id`),
  FOREIGN KEY (`to`) references `urls` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `link_words` (
  `word` bigint(11) NOT NULL,
  `link` bigint(11) NOT NULL,
  FOREIGN KEY (`word`) references `words`(`id`),
  FOREIGN KEY (`link`) references `links`(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

create table `word_location` (
	`url` bigint(11) NOT NULL,
	`word` bigint(11) NOT NULL,
	`location` varchar(100) NOT NULL,
	FOREIGN KEY (`word`) references `words`(`id`),
	FOREIGN KEY (`url`) references `urls`(`id`),
	KEY (`word`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;










