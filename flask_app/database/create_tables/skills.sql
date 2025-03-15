CREATE TABLE IF NOT EXISTS `skills` (
    `skill_id`        int(11)       NOT NULL AUTO_INCREMENT COMMENT 'The primary key and unique identifier for each skill',
    `experience_id`   int(11)       NOT NULL COMMENT 'A foreign key that references experiences.experience_id',
    `name`           varchar(100)  NOT NULL COMMENT 'The name of the skill',
    `skill_level`     varchar(100)  DEFAULT NULL COMMENT 'The level of the skill (1 being worst, 10 being best)',
    PRIMARY KEY  (`skill_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COMMENT="Skills I have acquired";
