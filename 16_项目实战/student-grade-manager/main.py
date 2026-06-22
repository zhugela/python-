"""学生成绩管理系统 - 主程序入口"""

import sys
from student import Student
import file_handler as fh
from analyzer import print_class_stats, print_rankings, show_charts
from exporter import export_excel


def print_header():
    """打印系统标题"""
    print()
    print("=" * 50)
    print("       🏫 学生成绩管理系统")
    print("       Python程序设计 课程设计")
    print("=" * 50)


def print_menu():
    """打印主菜单"""
    print("\n" + "─" * 50)
    print("【主菜单】")
    print("  1. 添加学生")
    print("  2. 查看所有学生")
    print("  3. 查找学生")
    print("  4. 录入/修改成绩")
    print("  5. 统计分析")
    print("  6. 成绩排名")
    print("  7. 显示图表")
    print("  8. 导出 Excel")
    print("  9. 删除学生")
    print("  0. 退出系统")
    print("─" * 50)


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


def input_float(prompt, min_val=0, max_val=100):
    """安全输入浮点数"""
    while True:
        try:
            val = float(input(prompt))
            if val < min_val or val > max_val:
                print(f"请输入 {min_val} ~ {max_val} 之间的数字")
                continue
            return val
        except ValueError:
            print("请输入有效的数字")


def add_student():
    """添加学生"""
    print("\n--- 添加学生 ---")
    student_id = input("请输入学号: ").strip()
    if not student_id:
        print("学号不能为空")
        return

    name = input("请输入姓名: ").strip()
    if not name:
        print("姓名不能为空")
        return

    student = Student(student_id, name)
    success, msg = fh.add_student(student)
    print("✅" if success else "❌", msg)


def list_students():
    """查看所有学生"""
    students = fh.get_all_students()
    if not students:
        print("📭 暂无学生数据")
        return

    print(f"\n{'='*60}")
    print(f"📋 学生列表（共 {len(students)} 人）")
    print(f"{'='*60}")
    print(f"{'学号':<12}{'姓名':<10}{'科目数':<8}{'总分':<8}{'平均分':<8}")
    print(f"{'-'*60}")

    for s in students:
        total = s.get_total_score() if s.grades else "-"
        avg = s.get_average_score() if s.grades else "-"
        count = s.get_subject_count()
        print(f"{s.student_id:<12}{s.name:<10}{count:<8}{total:<8}{avg:<8}")

    print(f"{'='*60}\n")


def find_student():
    """查找学生"""
    print("\n--- 查找学生 ---")
    print("1. 按学号查找")
    print("2. 按姓名查找")
    choice = input("请选择 (1/2): ").strip()

    if choice == "1":
        sid = input("请输入学号: ").strip()
        s = fh.find_student(sid)
    elif choice == "2":
        name = input("请输入姓名: ").strip()
        results = fh.find_student_by_name(name)
        if results:
            print(f"\n找到 {len(results)} 个学生:")
            for s in results:
                _print_student_detail(s)
            return
        else:
            print("未找到匹配的学生")
            return
    else:
        print("无效选择")
        return

    if s:
        _print_student_detail(s)
    else:
        print("未找到该学生")


def _print_student_detail(student):
    """打印学生详细信息"""
    print(f"\n{'='*40}")
    print(f"学号: {student.student_id}")
    print(f"姓名: {student.name}")
    print(f"{'='*40}")
    if student.grades:
        print(f"{'科目':<12}{'成绩':<8}{'等级':<8}")
        print(f"{'-'*28}")
        for subject, score in student.grades.items():
            level = _get_grade_level(score)
            print(f"{subject:<12}{score:<8}{level:<8}")
        print(f"{'-'*28}")
        print(f"{'总分':<12}{student.get_total_score():<8}")
        print(f"{'平均分':<12}{student.get_average_score():<8}")
    else:
        print("暂无成绩数据")
    print(f"{'='*40}\n")


def _get_grade_level(score):
    """获取成绩等级"""
    if score >= 90:
        return "优秀"
    elif score >= 80:
        return "良好"
    elif score >= 60:
        return "及格"
    else:
        return "不及格"


def input_grades():
    """录入/修改成绩"""
    student_id = input("请输入学号: ").strip()
    student = fh.find_student(student_id)
    if not student:
        print(f"未找到学号 {student_id}")
        return

    print(f"\n正在为 {student.name} 录入成绩")
    print("(输入科目名称为空时结束)")

    while True:
        subject = input("\n请输入科目名称 (直接回车结束): ").strip()
        if not subject:
            break
        score = input_float(f"请输入 {subject} 成绩 (0-100): ", 0, 100)
        success, msg = fh.update_grade(student_id, subject, score)
        print("✅" if success else "❌", msg)

    print(f"\n{student.name} 的成绩录入完成")


def delete_student():
    """删除学生"""
    student_id = input("请输入要删除的学号: ").strip()
    student = fh.find_student(student_id)
    if not student:
        print(f"未找到学号 {student_id}")
        return

    confirm = input(f"确定要删除 {student.name} (学号 {student_id}) 吗？(y/n): ").strip().lower()
    if confirm == "y":
        success, msg = fh.delete_student(student_id)
        print("✅" if success else "❌", msg)
    else:
        print("已取消删除")


def main():
    """主程序入口"""
    while True:
        print_header()
        print_menu()

        choice = input("\n请输入选项: ").strip()

        if choice == "1":
            add_student()
        elif choice == "2":
            list_students()
        elif choice == "3":
            find_student()
        elif choice == "4":
            input_grades()
        elif choice == "5":
            students = fh.get_all_students()
            print_class_stats(students)
        elif choice == "6":
            students = fh.get_all_students()
            print_rankings(students)
        elif choice == "7":
            students = fh.get_all_students()
            show_charts(students)
        elif choice == "8":
            export_excel()
        elif choice == "9":
            delete_student()
        elif choice == "0":
            print("\n感谢使用学生成绩管理系统！再见！")
            sys.exit(0)
        else:
            print("无效选项，请重新选择")

        input("\n按回车键继续...")


if __name__ == "__main__":
    main()
