import logging
from logging.handlers import RotatingFileHandler
import os


def setup_logging(app):
    if not app.debug:
        log_dir = os.path.join(app.instance_path, 'logs')
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        log_file = os.path.join(log_dir, 'weekend_overtime.log')

        # 设置日志文件（最大1KB，保留1个备份）
        file_handler = RotatingFileHandler(
                log_file,
                maxBytes=1024,
                backupCount=1,
                encoding='utf-8'
            )
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
            ))
        file_handler.setLevel(logging.INFO)

        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('Weekend Overtime application startup')
