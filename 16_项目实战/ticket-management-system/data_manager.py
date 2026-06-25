"""后台数据管理模块 - 负责车票的增删改查和JSON文件存储"""

import json
import os
from ticket import Ticket, BookingRecord

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
TICKETS_FILE = os.path.join(DATA_DIR, "tickets.json")
RECYCLE_BIN_FILE = os.path.join(DATA_DIR, "recycle_bin.json")
BOOKING_RECORDS_FILE = os.path.join(DATA_DIR, "booking_records.json")


def _ensure_data_dir():
    """确保数据目录存在"""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)


def load_data(file_path, cls):
    """通用加载函数：从JSON文件加载数据并转为对象列表"""
    _ensure_data_dir()
    if not os.path.exists(file_path):
        return []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data_list = json.load(f)
        return [cls.from_dict(data) for data in data_list]
    except (json.JSONDecodeError, IOError):
        return []


def save_data(file_path, obj_list):
    """通用保存函数：将对象列表保存为JSON文件"""
    _ensure_data_dir()
    try:
        data_list = [obj.to_dict() for obj in obj_list]
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data_list, f, ensure_ascii=False, indent=2)
        return True
    except IOError:
        return False


def load_tickets():
    """加载所有车票数据（不包含已删除的）"""
    all_tickets = load_data(TICKETS_FILE, Ticket)
    return [t for t in all_tickets if not t.is_deleted]


def load_all_tickets():
    """加载所有车票数据（包含已删除的）"""
    return load_data(TICKETS_FILE, Ticket)


def save_tickets(tickets):
    """保存车票数据"""
    return save_data(TICKETS_FILE, tickets)


def load_recycle_bin():
    """加载回收站（已删除的车票）"""
    all_tickets = load_all_tickets()
    return [t for t in all_tickets if t.is_deleted]


def add_ticket(ticket):
    """添加新车票"""
    tickets = load_all_tickets()
    for t in tickets:
        if t.train_no == ticket.train_no and not t.is_deleted:
            return False, f"车次 {ticket.train_no} 已存在"
    tickets.append(ticket)
    if save_tickets(tickets):
        return True, f"车次 {ticket.train_no} 添加成功"
    return False, "保存失败"


def find_ticket(train_no):
    """按车次精确查找车票"""
    tickets = load_tickets()
    for t in tickets:
        if t.train_no == train_no:
            return t
    return None


def update_ticket(train_no, **kwargs):
    """修改车票信息，自动更新修改时间戳"""
    tickets = load_all_tickets()
    for t in tickets:
        if t.train_no == train_no and not t.is_deleted:
            t.update(**kwargs)
            if save_tickets(tickets):
                return True, f"车次 {train_no} 修改成功"
            return False, "保存失败"
    return False, f"未找到车次 {train_no}"


def delete_ticket(train_no):
    """假删除车票（移到回收站）"""
    tickets = load_all_tickets()
    for t in tickets:
        if t.train_no == train_no and not t.is_deleted:
            t.soft_delete()
            if save_tickets(tickets):
                return True, f"车次 {train_no} 已删除（移入回收站）"
            return False, "保存失败"
    return False, f"未找到车次 {train_no}"


def restore_ticket(train_no):
    """从回收站恢复车票"""
    tickets = load_all_tickets()
    for t in tickets:
        if t.train_no == train_no and t.is_deleted:
            t.restore()
            if save_tickets(tickets):
                return True, f"车次 {train_no} 已恢复"
            return False, "保存失败"
    return False, f"回收站中未找到车次 {train_no}"


def load_booking_records():
    """加载购票记录"""
    return load_data(BOOKING_RECORDS_FILE, BookingRecord)


def save_booking_records(records):
    """保存购票记录"""
    return save_data(BOOKING_RECORDS_FILE, records)


def add_booking_record(record):
    """添加购票记录"""
    records = load_booking_records()
    records.append(record)
    if save_booking_records(records):
        return True, "购票记录添加成功"
    return False, "保存失败"


def get_next_record_id():
    """生成下一个购票记录ID"""
    records = load_booking_records()
    if not records:
        return "B001"
    max_id = 0
    for r in records:
        try:
            num = int(r.record_id[1:])
            if num > max_id:
                max_id = num
        except ValueError:
            continue
    return f"B{max_id + 1:03d}"
