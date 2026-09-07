import pymysql

# PyMySQL is a pure-Python MySQL driver, so it needs no C compiler or MySQL
# development headers to install - unlike mysqlclient, this makes the project
# easy to build on any machine and on platforms like Render out of the box.
# This shim makes Django's "django.db.backends.mysql" engine use it.
pymysql.install_as_MySQLdb()
pymysql.version_info = (2, 2, 4, "final", 0)  # satisfies Django's minimum version check
