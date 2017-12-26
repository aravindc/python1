import io
import datetime
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

now = datetime.datetime.now()
#mydata = np.genfromtxt(now.strftime("%Y%m%d")+'.csv', delimiter='|',
#                 names=['date', 'videoCategoryId', 'region','title','description','publishedAt','viewCount','likeCount','dislikeCount','commentCount'])
mydata = pd.read_csv(now.strftime("%Y%m%d")+'.csv',index_col=3,
            names=['date', 'videoCategoryId', 'region','id','title','publishedAt','viewCount','likeCount','dislikeCount','commentCount'])
#usdata = mydata[(mydata.region=='US') & (mydata.videoCategoryId==1)]
usdata = mydata[mydata.region=='US']
us1data = usdata.groupby(usdata.videoCategoryId,as_index=False).max()

us1data['likeCount'].replace('None', 0, inplace=True)
us1data['dislikeCount'].replace('None', 0, inplace=True)
us1data['commentCount'].replace('None', 0, inplace=True)
us1data.likeCount = pd.to_numeric(us1data.likeCount, errors='coerce').fillna(0).astype(np.int64)
us1data.dislikeCount = pd.to_numeric(us1data.dislikeCount, errors='coerce').fillna(0).astype(np.int64)
us1data.commentCount = pd.to_numeric(us1data.commentCount, errors='coerce').fillna(0).astype(np.int64)
#print(usdata)
print(us1data)
#sns.lmplot(x="videoCategoryId",y="likeCount",data=us1data)
#sns.countplot(x="videoCategoryId",data=us1data)
plt.show()
