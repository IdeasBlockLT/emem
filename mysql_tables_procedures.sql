
create database compendium;
use compendium;

DELIMITER ;;
CREATE TABLE `user_info` (
  `user_id`           bigint(20)    NOT NULL AUTO_INCREMENT,
  `user_name`         varchar(45)   COLLATE utf8_bin DEFAULT NULL,
  `facebook_name`     varchar(45)   COLLATE utf8_bin DEFAULT NULL,
  `user_email`        varchar(45)   COLLATE utf8_bin DEFAULT NULL,
  `user_password`     varchar(127)  COLLATE utf8_bin DEFAULT NULL,
  `notificaciones`    char(8)       COLLATE utf8_bin DEFAULT NULL,
  `android_token`     char(255)     COLLATE utf8_bin DEFAULT NULL,
  `latitude`          double(7,4)   COLLATE utf8_bin DEFAULT NULL, 
  `longitude`         double(7,4)   COLLATE utf8_bin DEFAULT NULL,
  `location`          char(64)      COLLATE utf8_bin DEFAULT NULL,
  `birthday`          char(32)      COLLATE utf8_bin DEFAULT NULL,
  `activity`          varchar(64)   COLLATE utf8_bin DEFAULT NULL,
  `description`      varchar(256)  COLLATE utf8_bin DEFAULT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

DELIMITER ;;
CREATE TABLE `img_info` (
  `img_id`            bigint(20)    NOT NULL AUTO_INCREMENT,
  `user_id`           bigint(20)    NOT NULL,
  `img_url`           varchar(256)   COLLATE utf8_bin DEFAULT NULL,
  `description`       varchar(256)   COLLATE utf8_bin DEFAULT NULL,
  `type`              varchar(127)  COLLATE utf8_bin DEFAULT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
DELIMITER ;;


-- ==========================================
-- PROCEDURES
-- ==========================================
DELIMITER ;;
CREATE DEFINER=`iopaveqd_compendium`@`localhost` PROCEDURE `sp_create_user_compendium`(
    IN p_name VARCHAR(45),
    IN p_useremail VARCHAR(45),
    IN p_password VARCHAR(127),
    IN p_description VARCHAR(256),
    IN p_latitude DOUBLE(7,4),
    IN p_longitude DOUBLE(7,4)
)
BEGIN
    if  ( select exists (select 1 from user_info where user_name = p_name) ) THEN
        select 'User Exists!';
    ELSE
        insert into user_info
        (
            user_name,
            facebook_name,
            user_email,
            user_password,
            description,
            latitude, 
            longitude
        )
        values
        (
            p_name,
            p_name,
            p_useremail,
            p_password,
            p_description,
            p_latitude,
            p_longitude
        );
    END IF;             
END ;;
DELIMITER ;

