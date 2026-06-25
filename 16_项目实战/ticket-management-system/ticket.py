"""车票数据模型"""

import time


class Ticket:
    """车票类，包含车次、出发地、目的地、时间、价格、余票等信息"""

    def __init__(self, train_no, departure, destination, departure_time, price, seats_available):
        self.train_no = train_no
        self.departure = departure
        self.destination = destination
        self.departure_time = departure_time
        self.price = float(price)
        self.seats_available = int(seats_available)
        self.created_at = time.strftime("%Y-%m-%d %H:%M:%S")
        self.updated_at = self.created_at
        self.is_deleted = False
        self.deleted_at = None

    def update(self, **kwargs):
        """更新车票信息，自动记录修改时间"""
        for key, value in kwargs.items():
            if hasattr(self, key) and key not in ("created_at", "updated_at", "is_deleted", "deleted_at"):
                setattr(self, key, value)
        self.updated_at = time.strftime("%Y-%m-%d %H:%M:%S")

    def soft_delete(self):
        """假删除，标记删除状态和删除时间"""
        self.is_deleted = True
        self.deleted_at = time.strftime("%Y-%m-%d %H:%M:%S")

    def restore(self):
        """恢复被删除的车票"""
        self.is_deleted = False
        self.deleted_at = None
        self.updated_at = time.strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self):
        """转为字典（用于JSON序列化）"""
        return {
            "train_no": self.train_no,
            "departure": self.departure,
            "destination": self.destination,
            "departure_time": self.departure_time,
            "price": self.price,
            "seats_available": self.seats_available,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "is_deleted": self.is_deleted,
            "deleted_at": self.deleted_at,
        }

    @classmethod
    def from_dict(cls, data):
        """从字典创建Ticket实例"""
        ticket = cls(
            data["train_no"],
            data["departure"],
            data["destination"],
            data["departure_time"],
            data["price"],
            data["seats_available"],
        )
        ticket.created_at = data.get("created_at", ticket.created_at)
        ticket.updated_at = data.get("updated_at", ticket.updated_at)
        ticket.is_deleted = data.get("is_deleted", False)
        ticket.deleted_at = data.get("deleted_at", None)
        return ticket

    def __str__(self):
        return f"{self.train_no}  {self.departure}->{self.destination}  {self.departure_time}  ¥{self.price}  余票:{self.seats_available}"


class BookingRecord:
    """购票记录类"""

    def __init__(self, record_id, train_no, passenger_name, id_card, quantity, total_price):
        self.record_id = record_id
        self.train_no = train_no
        self.passenger_name = passenger_name
        self.id_card = id_card
        self.quantity = int(quantity)
        self.total_price = float(total_price)
        self.booking_time = time.strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self):
        """转为字典（用于JSON序列化）"""
        return {
            "record_id": self.record_id,
            "train_no": self.train_no,
            "passenger_name": self.passenger_name,
            "id_card": self.id_card,
            "quantity": self.quantity,
            "total_price": self.total_price,
            "booking_time": self.booking_time,
        }

    @classmethod
    def from_dict(cls, data):
        """从字典创建BookingRecord实例"""
        record = cls(
            data["record_id"],
            data["train_no"],
            data["passenger_name"],
            data["id_card"],
            data["quantity"],
            data["total_price"],
        )
        record.booking_time = data.get("booking_time", record.booking_time)
        return record

    def __str__(self):
        return f"[{self.record_id}] {self.train_no}  {self.passenger_name}({self.id_card})  {self.quantity}张  总价:¥{self.total_price}"
