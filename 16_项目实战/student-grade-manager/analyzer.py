"""统计分析 + matplotlib图表"""

from file_handler import get_all_students


def get_all_subjects(students):
    """获取所有科目列表"""
    subjects = set()
    for s in students:
        subjects.update(s.grades.keys())
    return sorted(subjects)


def calc_class_stats(students):
    """计算全班统计数据"""
    stats = {}
    subjects = get_all_subjects(students)

    for subject in subjects:
        scores = [s.grades[subject] for s in students if subject in s.grades]
        if not scores:
            continue
        stats[subject] = {
            "最高分": max(scores),
            "最低分": min(scores),
            "平均分": round(sum(scores) / len(scores), 2),
            "参考人数": len(scores)
        }

    return stats


def calc_grade_distribution(students):
    """计算各科分数段分布"""
    subjects = get_all_subjects(students)
    distribution = {}

    for subject in subjects:
        levels = {"优秀(≥90)": 0, "良好(80-89)": 0, "及格(60-79)": 0, "不及格(<60)": 0}
        for s in students:
            if subject in s.grades:
                score = s.grades[subject]
                if score >= 90:
                    levels["优秀(≥90)"] += 1
                elif score >= 80:
                    levels["良好(80-89)"] += 1
                elif score >= 60:
                    levels["及格(60-79)"] += 1
                else:
                    levels["不及格(<60)"] += 1
        distribution[subject] = levels

    return distribution


def print_class_stats(students):
    """打印全班统计信息"""
    if not students:
        print("暂无学生数据")
        return

    print(f"\n{'='*50}")
    print(f"📊 全班统计报告（共 {len(students)} 人）")
    print(f"{'='*50}")

    stats = calc_class_stats(students)
    distribution = calc_grade_distribution(students)

    for subject, data in stats.items():
        print(f"\n【{subject}】")
        print(f"  参考人数: {data['参考人数']}")
        print(f"  最高分: {data['最高分']}")
        print(f"  最低分: {data['最低分']}")
        print(f"  平均分: {data['平均分']}")

        levels = distribution[subject]
        print(f"  分数段分布:")
        for level, count in levels.items():
            bar = "█" * count + " " * (max(0, 20 - count))
            print(f"    {level}: {count}人  {bar}")

    print(f"\n{'='*50}\n")


def print_rankings(students):
    """打印成绩排名（按总分降序）"""
    if not students:
        print("暂无学生数据")
        return

    # 过滤有成绩的学生
    valid = [s for s in students if s.grades]
    if not valid:
        print("暂无学生成绩数据")
        return

    # 按总分排序
    ranked = sorted(valid, key=lambda s: s.get_total_score(), reverse=True)

    print(f"\n{'='*60}")
    print(f"🏆 成绩排名")
    print(f"{'='*60}")
    print(f"{'排名':<6}{'学号':<10}{'姓名':<10}{'总分':<8}{'平均分':<8}{'科目数':<6}")
    print(f"{'-'*60}")

    subjects = get_all_subjects(students)
    header = "  ".join(subjects)
    print(f"{' ':<6}{'':<10}{'':<10}{'':<8}{'':<8}{'':<6}{header}")
    print(f"{'-'*60}")

    for i, s in enumerate(ranked, 1):
        grades_str = "  ".join(str(s.grades.get(sub, "")) for sub in subjects)
        print(f"{i:<6}{s.student_id:<10}{s.name:<10}{s.get_total_score():<8}{s.get_average_score():<8}{s.get_subject_count():<6}{grades_str}")

    print(f"{'='*60}\n")


def show_charts(students):
    """显示统计图表"""
    try:
        import matplotlib.pyplot as plt
        import matplotlib
        matplotlib.rc("font", family="Microsoft YaHei", size=10)
    except Exception:
        try:
            import matplotlib.pyplot as plt
            import matplotlib
            matplotlib.rc("font", family="SimHei", size=10)
        except Exception:
            print("无法加载中文字体，图表中文可能显示为方框")

    if not students:
        print("暂无学生数据，无法生成图表")
        return

    valid = [s for s in students if s.grades]
    if not valid:
        print("暂无成绩数据，无法生成图表")
        return

    subjects = get_all_subjects(valid)
    stats = calc_class_stats(valid)

    # 创建子图1：各科平均分柱状图
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    sub_names = list(stats.keys())
    sub_avgs = [stats[s]["平均分"] for s in sub_names]

    axes[0].bar(sub_names, sub_avgs, color="skyblue", edgecolor="navy")
    axes[0].set_title("各科目平均分", fontsize=14, fontweight="bold")
    axes[0].set_ylabel("平均分")
    axes[0].set_ylim(0, 100)
    for i, v in enumerate(sub_avgs):
        axes[0].text(i, v + 1, str(v), ha="center", fontweight="bold")

    # 子图2：分数段分布饼图（取第一科）
    first_sub = sub_names[0]
    distribution = calc_grade_distribution(valid)
    levels = distribution[first_sub]
    labels = list(levels.keys())
    sizes = list(levels.values())
    colors = ["#ffd700", "#87ceeb", "#98fb98", "#ff9999"]

    axes[1].pie(sizes, labels=labels, autopct="%1.1f%%", colors=colors,
                startangle=90, wedgeprops={"edgecolor": "white", "linewidth": 1.5})
    axes[1].set_title(f"{first_sub} 分数段分布", fontsize=14, fontweight="bold")

    plt.suptitle("📊 学生成绩统计分析", fontsize=16, fontweight="bold", y=1.02)
    plt.tight_layout()
    plt.show()
