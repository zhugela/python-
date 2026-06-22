"""JSON文件读写与CRUD操作"""

import json
import os

DATA_FILE = os.path.join(os.path.dirname(__file__), "data.json")

from student import Student


def load_students():
    """从JSON文件读取所有学生"""
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    return [Student.from_dict(item) for item in data]


def save_students(students):
    """保存所有学生到JSON文件"""
    data = [s.to_dict() for s in students]
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def add_student(student):
    """添加学生"""
    students = load_students()
    # 检查学号是否已存在
    for s in students:
        if s.student_id == student.student_id:
            return False, f"学号 {student.student_id} 已存在！"
    students.append(student)
    save_students(students)
    return True, f"学生 {student.name} 添加成功！"


def delete_student(student_id):
    """删除学生"""
    students = load_students()
    for i, s in enumerate(students):
        if s.student_id == student_id:
            del students[i]
            save_students(students)
            return True, f"学号 {student_id} 已删除"
    return False, f"未找到学号 {student_id}"


def find_student(student_id):
    """按学号查找学生"""
    students = load_students()
    for s in students:
        if s.student_id == student_id:
            return s
    return None


def find_student_by_name(name):
    """按姓名查找学生"""
    students = load_students()
    result = []
    for s in students:
        if name in s.name:
            result.append(s)
    return result


def update_grade(student_id, subject, score):
    """录入/修改成绩"""
    student = find_student(student_id)
    if not student:
        return False, f"未找到学号 {student_id}"
    student.set_grade(subject, score)
    students = load_students()
    for i, s in enumerate(students):
        if s.student_id == student_id:
            students[i] = student
            break
    save_students(students)
    return True, f"{student.name} 的 {subject} 成绩已设为 {score} 分"


def get_all_students():
    """获取所有学生列表"""
    return load_students()
