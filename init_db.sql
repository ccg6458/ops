CREATE DATABASE ops /*!40100 DEFAULT CHARACTER SET utf8 */;
CREATE TABLE business
(
    id INT(11) PRIMARY KEY NOT NULL AUTO_INCREMENT,
    name VARCHAR(32) NOT NULL,
    host VARCHAR(32)
);
CREATE TABLE log
(
    id INT(11) PRIMARY KEY NOT NULL AUTO_INCREMENT,
    username VARCHAR(32),
    behavior VARCHAR(512), 
    create_time VARCHAR(64)
);
CREATE TABLE operation
(
    id INT(11) PRIMARY KEY NOT NULL AUTO_INCREMENT,
    action VARCHAR(32)
);
CREATE TABLE permission
(
    id INT(11) PRIMARY KEY NOT NULL AUTO_INCREMENT,
    user_id INT(11),
    business_id INT(11)
);
CREATE UNIQUE INDEX permission_business_id_user_id_uindex ON permission (business_id, user_id);
CREATE TABLE sidebar
(
    id INT(11) PRIMARY KEY NOT NULL AUTO_INCREMENT,
    `index` VARCHAR(32),
    icon VARCHAR(32),
    tab VARCHAR(32),
    routelink VARCHAR(32),
    is_super INT(11) DEFAULT '0'
);
CREATE TABLE task
(
    id INT(11) PRIMARY KEY NOT NULL AUTO_INCREMENT,
    business_id INT(11),
    schedule VARCHAR(64),
    shell VARCHAR(128),
    create_time VARCHAR(64)
);
CREATE TABLE user
(
    id INT(11) PRIMARY KEY NOT NULL AUTO_INCREMENT,
    name VARCHAR(32),
    status TINYINT(4) DEFAULT '1',
    email VARCHAR(32),
    `_password` VARCHAR(128),
    super TINYINT(4) DEFAULT '0' NOT NULL
);
CREATE UNIQUE INDEX user_name_uindex ON user (name);
CREATE TABLE workorder
(
    id INT(11) PRIMARY KEY NOT NULL AUTO_INCREMENT,
    type INT(11),
    name VARCHAR(128),
    `sql` TEXT,
    audit INT(11),
    finish INT(11),
    user_id INT(11),
    create_time VARCHAR(64),
    comment VARCHAR(128),
    `database` VARCHAR(32)
);
INSERT INTO test.sidebar (id, index, icon, tab, routelink, is_super) VALUES (1, 1, 'el-icon-s-order', '定时任务', '/task', 0);
INSERT INTO test.sidebar (id, index, icon, tab, routelink, is_super) VALUES (2, 2, 'el-icon-user-solid', '用户管理', '/user', 1);
INSERT INTO test.sidebar (id, index, icon, tab, routelink, is_super) VALUES (4, 4, 'el-icon-message-solid', '操作日志', '/audit', 1);
INSERT INTO test.sidebar (id, index, icon, tab, routelink, is_super) VALUES (5, 5, 'el-icon-s-platform', '业务主机', '/business', 1);
INSERT INTO test.sidebar (id, index, icon, tab, routelink, is_super) VALUES (6, 6, 'el-icon-s-operation', '工单管理', '/order', 0);

