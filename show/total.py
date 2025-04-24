
import csv
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm


def read_csv_and_count_columns(file_path):
    column_data = []
    with open(file_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            row_data = row[0].split()
            for i, value in enumerate(row_data):
                if len(column_data) <= i:
                    column_data.append({})
                if value in column_data[i]:
                    column_data[i][value] += 1
                else:
                    column_data[i][value] = 1
    return column_data


def plot_column_data(column_data):
    # 设置支持中文的字体
    font_path = fm.findfont(fm.FontProperties(family='SimHei'))
    plt.rcParams['font.family'] = fm.FontProperties(fname=font_path).get_name()
    plt.rcParams['axes.unicode_minus'] = False

    fig = plt.figure(figsize=(10, 7))

    # 第一排左侧：第一列数据柱形图
    if len(column_data) > 0:
        first_column_data = column_data[0]
        labels = list(first_column_data.keys())
        values = list(first_column_data.values())
        total = sum(values)
        percentages = [val / total * 100 for val in values]
        ax1 = plt.subplot2grid((2, 2), (0, 0))
        ax1.bar(labels, percentages)
        ax1.set_xlabel('姿势类别')
        ax1.set_ylabel('占比 (%)')
        ax1.set_title('正反手姿势统计')
        ax1.tick_params(axis='x', rotation=90)

    # 第一排右侧：第二列数据扇形图
    if len(column_data) > 1:
        second_column_data = column_data[1]
        labels = list(second_column_data.keys())
        sizes = list(second_column_data.values())
        ax2 = plt.subplot2grid((2, 2), (0, 1))
        ax2.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
        ax2.axis('equal')
        ax2.set_title('评分等级占比饼图')

    # 第二排：第三列数据按频次展示
    if len(column_data) > 2:
        third_column_data = column_data[2]
        sorted_items = sorted(third_column_data.items(), key=lambda item: item[1], reverse=True)
        ax3 = plt.subplot2grid((2, 2), (1, 0), colspan=2)
        ax3.axis('off')
        max_count = sorted_items[0][1] if sorted_items else 1
        for i, (label, count) in enumerate(sorted_items):
            font_size = 10 + (count / max_count) * 20  # 根据频次调整字体大小
            ax3.text(0.1, 0.9 - i * 0.1, f'{label}', fontsize=font_size, transform=ax3.transAxes)

    plt.tight_layout()
    plt.savefig('analysis_result.png', dpi=300, bbox_inches='tight')
    plt.show()


if __name__ == "__main__":
    file_path = 'E:/MyTennis/Tennis_System/pose_analyze/results.csv' #修改路径
    column_data = read_csv_and_count_columns(file_path)
    plot_column_data(column_data)
