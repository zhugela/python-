"""学生成绩数据模型"""


class Student:
    """学生类，包含学号、姓名、成绩"""

    def __init__(self, student_id, name):
        self.student_id = student_id
        self.name = name
        self.grades = {}  # {科目: 分数}

    def set_grade(self, subject, score):
        """设置/修改单科成绩"""
        self.grades[subject] = score

    def get_total_score(self):
        """计算总分"""
        return sum(self.grades.values())

    def get_average_score(self):
        """计算平均分"""
        if not self.grades:
            return 0.0
        return round(self.get_total_score() / len(self.grades), 2)

    def get_subject_count(self):
        """返回科目数"""
        return len(self.grades)

    def to_dict(self):
        """转为字典（用于JSON序列化）"""
        return {
            "student_id": self.student_id,
            "name": self.name,
            "grades": self.grades
        }

    @classmethod
    def from_dict(cls, data):
        """从字典创建Student实例"""
        student = cls(data["student_id"], data["name"])
        student.grades = data.get("grades", {})
        return student

    def __str__(self):
        return f"{self.student_id}  {self.name}  {len(self.grades)}科"
