CREATE TABLE IF NOT EXISTS `experiences` (
    `experience_id`        int(11)       NOT NULL AUTO_INCREMENT  COMMENT 'the primary key, and unique identifier for each experience',
    `position_id`           int(11)       NOT NULL                 COMMENT 'a foreign key that references positions.position_id', 
    `name`                  varchar(100)  NOT NULL                 COMMENT 'the name of the experience',
    `description`           varchar(100)  DEFAULT NULL             COMMENT ' a description of the experience.',
    `hyperlink`             varchar(100)  DEFAULT NULL             COMMENT 'a link where people can learn more about the experience',
    `start_date`            DATE          DEFAULT NULL             COMMENT 'the state date of the experience',
    `end_date`              DATE          DEFAULT NULL             COMMENT 'the end date of the experience',
    PRIMARY KEY  (`experience_id`),
    FOREIGN KEY (`position_id`) REFERENCES `positions`(`position_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COMMENT=" ";
