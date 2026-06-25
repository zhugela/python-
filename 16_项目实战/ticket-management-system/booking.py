"""前台业务模块 - 负责车票查询和购票功能"""

import data_manager as dm
from ticket import BookingRecord


def search_by_train_no(train_no, exact=True):
    """按车次查询
    exact=True 精确查询，exact=False 模糊查询
    """
    tickets = dm.load_tickets()
    if exact:
        results = [t for t in tickets if t.train_no == train_no]
    else:
        results = [t for t in tickets if train_no in t.train_no]
    return results


def search_by_departure(departure, exact=True):
    """按出发地查询
    exact=True 精确查询，exact=False 模糊查询
    """
    tickets = dm.load_tickets()
    if exact:
        results = [t for t in tickets if t.departure == departure]
    else:
        results = [t for t in tickets if departure in t.departure]
    return results


def search_by_destination(destination, exact=True):
    """按目的地查询"""
    tickets = dm.load_tickets()
    if exact:
        results = [t for t in tickets if t.destination == destination]
    else:
        results = [t for t in tickets if destination in t.destination]
    return results


def search_tickets(keyword):
    """综合模糊查询（车次、出发地、目的地）"""
    tickets = dm.load_tickets()
    results = []
    for t in tickets:
        if (keyword in t.train_no
                or keyword in t.departure
                or keyword in t.destination):
            results.append(t)
    return results


def book_ticket(train_no, passenger_name, id_card, quantity):
    """购票功能
    1. 判断余票 >= 购买数量
    2. 减库存
    3. 生成带乘客姓名+身份证的购票记录
    4. 自动计算总价
    """
    ticket = dm.find_ticket(train_no)
    if not ticket:
        return False, f"未找到车次 {train_no}", None

    if ticket.seats_available < quantity:
        return False, f"余票不足！当前余票: {ticket.seats_available} 张", None

    if quantity <= 0:
        return False, "购票数量必须大于0", None

    total_price = round(ticket.price * quantity, 2)

    new_seats = ticket.seats_available - quantity
    success, msg = dm.update_ticket(train_no, seats_available=new_seats)
    if not success:
        return False, f"扣减库存失败: {msg}", None

    record_id = dm.get_next_record_id()
    record = BookingRecord(
        record_id=record_id,
        train_no=train_no,
        passenger_name=passenger_name,
        id_card=id_card,
        quantity=quantity,
        total_price=total_price,
    )

    success, msg = dm.add_booking_record(record)
    if not success:
        dm.update_ticket(train_no, seats_available=ticket.seats_available)
        return False, f"生成购票记录失败: {msg}", None

    return True, "购票成功！", record
