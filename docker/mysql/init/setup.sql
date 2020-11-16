-- Workaround MySQL 8 new caching_sha2_password as default authentication
ALTER  USER 'root'@'%' IDENTIFIED WITH mysql_native_password BY '';