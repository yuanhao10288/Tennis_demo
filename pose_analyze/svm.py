import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
from sklearn import svm
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import f1_score, classification_report, confusion_matrix
import joblib

# 加载数据
data = pd.read_csv('data.csv')

# 检查并处理缺失值
print("Missing values:\n", data.isnull().sum())
data.fillna(data.median(), inplace=True)

# 特征与目标变量
features = ['langle', 'rangle', 'lsangle', 'rsangle', 'lhangle', 'rhangle', 'lkangle', 'rkangle']
x = data[features].values
y = data['class'].values

# 划分数据集（分层抽样）
x_train, x_test, y_train, y_test = train_test_split(
    x, y, test_size=0.2, random_state=20, stratify=y
)

# 特征标准化
scaler = StandardScaler()
x_train = scaler.fit_transform(x_train)
x_test = scaler.transform(x_test)

# 超参数调优
param_grid = {'C': [0.1, 1, 1.2, 10], 'gamma': ['scale', 'auto', 0.1, 1]}
grid = GridSearchCV(
    svm.SVC(kernel='rbf', probability=True, decision_function_shape='ovr'),
    param_grid, cv=5, scoring='f1_micro'
)
grid.fit(x_train, y_train)
best_model = grid.best_estimator_

# 交叉验证评估
cv_scores = cross_val_score(best_model, x_train, y_train, cv=5, scoring='f1_micro')
print("Cross-Validation Scores:", cv_scores)

# 训练最终模型
best_model.fit(x_train, y_train)

# 预测与评估
result_test = best_model.predict(x_test)
print("Test F1 (micro): {0:.2f}".format(f1_score(y_test, result_test, average='micro')))
print("\nClassification Report:\n", classification_report(y_test, result_test))
print("\nConfusion Matrix:\n", confusion_matrix(y_test, result_test))

# 保存模型和标准化器
joblib.dump(best_model, 'svm_model/optimized_tennis_pose_svm.pkl')
joblib.dump(scaler, 'svm_model/scaler.pkl')