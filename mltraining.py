from IPython import get_ipython
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import random

lol = pd.read_csv('./data/sample_SilverKDA.csv')
lol.drop(['Unnamed: 0'],axis=1,inplace=True)
print(lol)

f, ax = plt.subplots(1, 2, figsize=(18, 8))

lol['gameResult'].value_counts().plot.pie(explode= [0, 0.1], autopct='%1.1f%%', ax=ax[0], shadow=True)
ax[0].set_title('Pie plot - Game Result')
ax[0].set_ylabel('')
sns.countplot('gameResult', data=lol, ax=ax[1])
ax[1].set_title('Count plot - Game Result')

pd.crosstab(lol['JUNGLE'], lol['gameResult'], margins=True)
plt.show()

x = range(0,50)
print(x)
randInt = random.randint(0,lol['gameResult'].count()-50)
y0 = lol['gameResult'][randInt:randInt+50]
plt.plot(x, y0, label="gameResult")
y1 = lol['TOP'][randInt:randInt+50]
plt.plot(x, y1, label="TOP")
y2 = lol['JUNGLE'][randInt:randInt+50]
plt.plot(x, y2, label="JUNGLE")
y3 = lol['MIDDLE'][randInt:randInt+50]
plt.plot(x, y3, label="MIDDLE")
y4 = lol['BOTTOM'][randInt:randInt+50]
plt.plot(x, y4, label="BOTTOM")
y5 = lol['SUPPORT'][randInt:randInt+50]
plt.plot(x, y5, label="SUPPORT")
print(randInt)
plt.xlabel('count')
plt.ylabel('data')
plt.legend()

plt.show()

print(lol.head())
print(lol.info())

X = lol[['TOP','JUNGLE','MIDDLE','BOTTOM','SUPPORT']]
y = lol['gameResult']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=13)


lr = LogisticRegression(random_state=13, solver='liblinear')
lr.fit(X_train, y_train)

pred = lr.predict(X_test)
print(accuracy_score(y_test, pred))

import numpy as np
thisPic = np.array([[1.43, 1.84, 1.92, 2.50, 3.92]])
winRate = lr.predict_proba(thisPic)[0,1]
if winRate >= 0.5 and winRate <=0.6:
    print("해볼만합니다.")
elif winRate <0.5 and winRate >=0.3:
    print("팀상태보고 원하면 게임을 미리 포기하시길 바랍니다.")
elif winRate <0.3:
    print("게임을 미리 포기하길 추천드립니다.")
else:
    print("팀이 잘할 가능성이 매우 높아 보입니다.")
print('우리팀의 승률 : ',lr.predict_proba(thisPic)[0,1]*100,"%")




