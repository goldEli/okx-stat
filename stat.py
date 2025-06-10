import os
from datetime import datetime

mouth = 6

def analyze_salary():
    # 检查文件是否存在
    file_path = f'data/{mouth}.txt'
    if not os.path.exists(file_path):
        print(f"错误：文件 {file_path} 不存在")
        return

    total_salary = 0.0
    count = 0
    salaries = []
    # 定义薪水区间
    ranges = [
        (0, 1000),
        (1000, 2000),
        (2000, 3000),
        (3000, 4000),
        (4000, 5000),
        (5000, 6000),
        (6000, 7000),
        (7000, 8000),
        (8000, 9000),
        (9000, 10000),
        (10000, 12000),
        (12000, 15000),
        (15000, float('inf'))

    ]
    # 初始化区间统计字典
    range_counts = {f"{r[0]}-{r[1] if r[1] != float('inf') else '以上'}": 0 for r in ranges}

    try:
        with open(file_path, 'r') as f:
            for line in f:
                # 去除行尾的空白字符
                line = line.strip()
                if not line:
                    continue

                # 分割行数据，获取最后一列（薪水）
                parts = line.split()
                if len(parts) < 3:  # 确保至少有日期、时间和薪水三部分
                    continue

                try:
                    salary = float(parts[-1])
                    salaries.append(salary)
                    total_salary += salary
                    count += 1
                except ValueError:
                    print(f"警告：无法解析薪水金额：{parts[-1]}")
                    continue

        if count > 0:
            average_salary = total_salary / count
            max_salary = max(salaries)
            min_salary = min(salaries)

            # 统计薪水分布
            for salary in salaries:
                for r in ranges:
                    if r[0] <= salary < r[1]:
                        range_key = f"{r[0]}-{r[1] if r[1] != float('inf') else '以上'}"
                        range_counts[range_key] += 1
                        break

            print(f"\n{mouth}月份薪水统计情况：")
            print(f"总计：{total_salary:.2f}")
            print(f"平均值：{average_salary:.2f}")
            print(f"最高值：{max_salary:.2f}")
            print(f"最低值：{min_salary:.2f}")
            print(f"总记录数：{count}人")
            
            print("\n薪水分布情况：")
            for range_key, range_count in range_counts.items():
                percentage = (range_count / count) * 100 if count > 0 else 0
                print(f"{range_key}：{range_count}人 ({percentage:.1f}%)")

        else:
            print("没有找到有效的薪水记录")

    except Exception as e:
        print(f"处理文件时发生错误：{e}")

if __name__ == '__main__':
    analyze_salary()
    