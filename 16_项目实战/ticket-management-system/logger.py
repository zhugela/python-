"""日志审计模块 - 记录所有操作，实现操作可追溯"""

import os
import time

LOG_DIR = os.path.join(os.path.dirname(__file__), "logs")
LOG_FILE = os.path.join(LOG_DIR, "log.txt")


def _ensure_log_dir():
    """确保日志目录存在"""
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)


def write_log(operation, detail):
    """写入操作日志

    Args:
        operation: 操作类型（如：添加车票、修改车票、删除车票、购票等）
        detail: 操作详情
    """
    _ensure_log_dir()
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"[{timestamp}] {operation} - {detail}\n"
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(log_line)
        return True
    except IOError:
        return False


def log_add_ticket(train_no, departure, destination):
    """记录添加车票操作"""
    write_log("添加车票", f"车次:{train_no} {departure}->{destination}")


def log_update_ticket(train_no, changes):
    """记录修改车票操作"""
    change_str = ", ".join([f"{k}={v}" for k, v in changes.items()])
    write_log("修改车票", f"车次:{train_no} 修改内容:[{change_str}]")


def log_delete_ticket(train_no):
    """记录删除车票操作"""
    write_log("删除车票", f"车次:{train_no} (假删除-移入回收站)")


def log_restore_ticket(train_no):
    """记录恢复车票操作"""
    write_log("恢复车票", f"车次:{train_no} (从回收站恢复)")


def log_booking(record_id, train_no, passenger_name, quantity, total_price):
    """记录购票操作"""
    write_log("购票", f"记录号:{record_id} 车次:{train_no} 乘客:{passenger_name} 数量:{quantity}张 总价:¥{total_price}")


def read_logs(line_count=None):
    """读取日志

    Args:
        line_count: 读取最后N行，None则读取全部

    Returns:
        日志行列表
    """
    _ensure_log_dir()
    if not os.path.exists(LOG_FILE):
        return []
    try:
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            lines = f.readlines()
        if line_count and line_count > 0:
            return lines[-line_count:]
        return lines
    except IOError:
        return []
