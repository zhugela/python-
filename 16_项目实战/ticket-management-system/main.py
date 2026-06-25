"""车票管理系统 - 主程序入口"""

import sys
from ticket import Ticket
import data_manager as dm
import booking as bk
import logger as lg


def print_header():
    """打印系统标题"""
    print()
    print("=" * 60)
    print("       🚄 车票管理系统")
    print("       Python程序设计 课程设计")
    print("=" * 60)


def print_main_menu():
    """打印主菜单"""
    print("\n" + "─" * 60)
    print("【主菜单】")
    print("  ── 后台数据管控 ──")
    print("  1. 添加车票")
    print("  2. 查看所有车票")
    print("  3. 修改车票信息")
    print("  4. 删除车票（假删除）")
    print("  5. 回收站管理")
    print("  ── 前台核心业务 ──")
    print("  6. 查询车票")
    print("  7. 购票")
    print("  8. 查看购票记录")
    print("  ── 日志审计 ──")
    print("  9. 查看操作日志")
    print("  ──")
    print("  0. 退出系统")
    print("─" * 60)


def input_int(prompt, min_val=None, max_val=None):
    """安全输入整数"""
    while True:
        try:
            val = int(input(prompt))
            if min_val is not None and val < min_val:
                print(f"请输入大于等于 {min_val} 的数字")
                continue
            if max_val is not None and val > max_val:
                print(f"请输入小于等于 {max_val} 的数字")
                continue
            return val
        except ValueError:
            print("请输入有效的数字")


def input_float(prompt, min_val=None):
    """安全输入浮点数"""
    while True:
        try:
            val = float(input(prompt))
            if min_val is not None and val < min_val:
                print(f"请输入大于等于 {min_val} 的数字")
                continue
            return val
        except ValueError:
            print("请输入有效的数字")


def print_ticket_table(tickets, show_detail=False):
    """打印车票表格"""
    if not tickets:
        print("📭 暂无车票数据")
        return

    print(f"\n{'='*75}")
    print(f"📋 车票列表（共 {len(tickets)} 条）")
    print(f"{'='*75}")
    print(f"{'车次':<10}{'出发地':<10}{'目的地':<10}{'发车时间':<18}{'价格':<8}{'余票':<6}")
    print(f"{'-'*75}")

    for t in tickets:
        print(f"{t.train_no:<10}{t.departure:<10}{t.destination:<10}"
              f"{t.departure_time:<18}¥{t.price:<7}{t.seats_available:<6}")

        if show_detail:
            print(f"  └ 创建时间: {t.created_at}  |  修改时间: {t.updated_at}")

    print(f"{'='*75}\n")


def add_ticket():
    """添加车票"""
    print("\n--- 添加车票 ---")
    train_no = input("请输入车次: ").strip()
    if not train_no:
        print("车次不能为空")
        return

    departure = input("请输入出发地: ").strip()
    if not departure:
        print("出发地不能为空")
        return

    destination = input("请输入目的地: ").strip()
    if not destination:
        print("目的地不能为空")
        return

    departure_time = input("请输入发车时间 (如 2026-06-25 08:00): ").strip()
    if not departure_time:
        print("发车时间不能为空")
        return

    price = input_float("请输入票价: ", min_val=0)
    seats = input_int("请输入余票数量: ", min_val=0)

    ticket = Ticket(train_no, departure, destination, departure_time, price, seats)
    success, msg = dm.add_ticket(ticket)

    if success:
        lg.log_add_ticket(train_no, departure, destination)

    print("✅" if success else "❌", msg)


def list_all_tickets():
    """查看所有车票"""
    tickets = dm.load_tickets()
    print_ticket_table(tickets, show_detail=True)


def update_ticket():
    """修改车票信息"""
    print("\n--- 修改车票 ---")
    train_no = input("请输入要修改的车次: ").strip()
    ticket = dm.find_ticket(train_no)

    if not ticket:
        print(f"未找到车次 {train_no}")
        return

    print(f"\n当前信息:")
    print_ticket_table([ticket], show_detail=True)

    print("请输入新信息（直接回车保持不变）:")
    changes = {}

    new_departure = input(f"出发地 [{ticket.departure}]: ").strip()
    if new_departure:
        changes["departure"] = new_departure

    new_destination = input(f"目的地 [{ticket.destination}]: ").strip()
    if new_destination:
        changes["destination"] = new_destination

    new_time = input(f"发车时间 [{ticket.departure_time}]: ").strip()
    if new_time:
        changes["departure_time"] = new_time

    new_price = input(f"票价 [{ticket.price}]: ").strip()
    if new_price:
        try:
            changes["price"] = float(new_price)
        except ValueError:
            print("价格格式错误，跳过价格修改")

    new_seats = input(f"余票数量 [{ticket.seats_available}]: ").strip()
    if new_seats:
        try:
            changes["seats_available"] = int(new_seats)
        except ValueError:
            print("数量格式错误，跳过余票修改")

    if not changes:
        print("没有修改任何内容")
        return

    success, msg = dm.update_ticket(train_no, **changes)
    if success:
        lg.log_update_ticket(train_no, changes)

    print("✅" if success else "❌", msg)


def delete_ticket():
    """删除车票（假删除）"""
    print("\n--- 删除车票 ---")
    train_no = input("请输入要删除的车次: ").strip()
    ticket = dm.find_ticket(train_no)

    if not ticket:
        print(f"未找到车次 {train_no}")
        return

    confirm = input(f"确定要删除 {train_no} ({ticket.departure}->{ticket.destination}) 吗？(y/n): ").strip().lower()
    if confirm == "y":
        success, msg = dm.delete_ticket(train_no)
        if success:
            lg.log_delete_ticket(train_no)
        print("✅" if success else "❌", msg)
    else:
        print("已取消删除")


def recycle_bin_menu():
    """回收站管理"""
    while True:
        print("\n--- 回收站管理 ---")
        print("1. 查看回收站")
        print("2. 恢复车票")
        print("0. 返回主菜单")
        choice = input("请选择: ").strip()

        if choice == "1":
            tickets = dm.load_recycle_bin()
            if not tickets:
                print("📭 回收站为空")
            else:
                print(f"\n{'='*75}")
                print(f"🗑️  回收站（共 {len(tickets)} 条）")
                print(f"{'='*75}")
                print(f"{'车次':<10}{'出发地':<10}{'目的地':<10}{'删除时间':<20}")
                print(f"{'-'*75}")
                for t in tickets:
                    print(f"{t.train_no:<10}{t.departure:<10}{t.destination:<10}{t.deleted_at:<20}")
                print(f"{'='*75}\n")

        elif choice == "2":
            train_no = input("请输入要恢复的车次: ").strip()
            success, msg = dm.restore_ticket(train_no)
            if success:
                lg.log_restore_ticket(train_no)
            print("✅" if success else "❌", msg)

        elif choice == "0":
            break
        else:
            print("无效选项")


def search_tickets():
    """查询车票"""
    while True:
        print("\n--- 查询车票 ---")
        print("1. 按车次查询")
        print("2. 按出发地查询")
        print("3. 按目的地查询")
        print("4. 综合模糊查询")
        print("0. 返回主菜单")
        choice = input("请选择: ").strip()

        if choice == "1":
            keyword = input("请输入车次: ").strip()
            print("1. 精确查询  2. 模糊查询")
            mode = input("请选择查询方式 (1/2): ").strip()
            exact = (mode == "1")
            results = bk.search_by_train_no(keyword, exact=exact)
            print_ticket_table(results)

        elif choice == "2":
            keyword = input("请输入出发地: ").strip()
            print("1. 精确查询  2. 模糊查询")
            mode = input("请选择查询方式 (1/2): ").strip()
            exact = (mode == "1")
            results = bk.search_by_departure(keyword, exact=exact)
            print_ticket_table(results)

        elif choice == "3":
            keyword = input("请输入目的地: ").strip()
            print("1. 精确查询  2. 模糊查询")
            mode = input("请选择查询方式 (1/2): ").strip()
            exact = (mode == "1")
            results = bk.search_by_destination(keyword, exact=exact)
            print_ticket_table(results)

        elif choice == "4":
            keyword = input("请输入关键词 (车次/出发地/目的地): ").strip()
            results = bk.search_tickets(keyword)
            print_ticket_table(results)

        elif choice == "0":
            break
        else:
            print("无效选项")


def book_ticket():
    """购票"""
    print("\n--- 购票 ---")
    train_no = input("请输入要购买的车次: ").strip()
    ticket = dm.find_ticket(train_no)

    if not ticket:
        print(f"未找到车次 {train_no}")
        return

    print(f"\n车次信息:")
    print_ticket_table([ticket])

    passenger_name = input("请输入乘客姓名: ").strip()
    if not passenger_name:
        print("乘客姓名不能为空")
        return

    id_card = input("请输入身份证号: ").strip()
    if not id_card:
        print("身份证号不能为空")
        return

    quantity = input_int("请输入购买数量: ", min_val=1)

    success, msg, record = bk.book_ticket(train_no, passenger_name, id_card, quantity)

    if success and record:
        lg.log_booking(record.record_id, train_no, passenger_name, quantity, record.total_price)
        print(f"\n{'='*50}")
        print("🎫 购票成功！")
        print(f"{'='*50}")
        print(f"  记录编号: {record.record_id}")
        print(f"  车次: {record.train_no}")
        print(f"  乘客: {record.passenger_name}")
        print(f"  身份证: {record.id_card}")
        print(f"  购票数量: {record.quantity} 张")
        print(f"  总价: ¥{record.total_price}")
        print(f"  购票时间: {record.booking_time}")
        print(f"{'='*50}\n")
    else:
        print("❌", msg)


def list_booking_records():
    """查看购票记录"""
    records = dm.load_booking_records()
    if not records:
        print("📭 暂无购票记录")
        return

    print(f"\n{'='*75}")
    print(f"🎫 购票记录（共 {len(records)} 条）")
    print(f"{'='*75}")
    print(f"{'记录号':<8}{'车次':<10}{'乘客姓名':<10}{'身份证号':<20}{'数量':<6}{'总价':<8}")
    print(f"{'-'*75}")

    for r in records:
        print(f"{r.record_id:<8}{r.train_no:<10}{r.passenger_name:<10}"
              f"{r.id_card:<20}{r.quantity:<6}¥{r.total_price:<7}")
        print(f"  └ 购票时间: {r.booking_time}")

    print(f"{'='*75}\n")

    total_amount = sum(r.total_price for r in records)
    total_tickets = sum(r.quantity for r in records)
    print(f"统计: 共 {len(records)} 笔订单，{total_tickets} 张车票，总金额 ¥{total_amount:.2f}")


def view_logs():
    """查看操作日志"""
    print("\n--- 操作日志 ---")
    count = input("请输入要查看的最近日志条数 (直接回车查看全部): ").strip()
    if count:
        try:
            n = int(count)
            logs = lg.read_logs(n)
        except ValueError:
            print("输入无效，查看全部日志")
            logs = lg.read_logs()
    else:
        logs = lg.read_logs()

    if not logs:
        print("📭 暂无日志记录")
        return

    print(f"\n{'='*70}")
    print(f"📝 操作日志（共 {len(logs)} 条）")
    print(f"{'='*70}")
    for line in logs:
        print(line.rstrip())
    print(f"{'='*70}\n")


def init_sample_data():
    """初始化示例数据"""
    tickets = dm.load_tickets()
    if tickets:
        return

    sample_tickets = [
        Ticket("G101", "北京", "上海", "2026-06-26 08:00", 553.0, 100),
        Ticket("G102", "上海", "北京", "2026-06-26 09:30", 553.0, 80),
        Ticket("G201", "广州", "深圳", "2026-06-26 07:00", 74.5, 200),
        Ticket("D301", "成都", "重庆", "2026-06-26 10:00", 96.5, 150),
        Ticket("K501", "武汉", "长沙", "2026-06-26 12:00", 53.5, 300),
    ]

    for t in sample_tickets:
        dm.add_ticket(t)

    print("已初始化示例车票数据")


def main():
    """主程序入口"""
    init_sample_data()

    while True:
        print_header()
        print_main_menu()

        choice = input("\n请输入选项: ").strip()

        if choice == "1":
            add_ticket()
        elif choice == "2":
            list_all_tickets()
        elif choice == "3":
            update_ticket()
        elif choice == "4":
            delete_ticket()
        elif choice == "5":
            recycle_bin_menu()
        elif choice == "6":
            search_tickets()
        elif choice == "7":
            book_ticket()
        elif choice == "8":
            list_booking_records()
        elif choice == "9":
            view_logs()
        elif choice == "0":
            print("\n感谢使用车票管理系统！再见！")
            sys.exit(0)
        else:
            print("无效选项，请重新选择")

        input("\n按回车键继续...")


if __name__ == "__main__":
    main()
