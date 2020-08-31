# CodereviewDataDownload
all questions from codereview.stackexchange.com

`test.py`: 通过官方提供api下载问题相关信息。数据库去重后有66463条记录。带回答的问题59490个。

`sqlutil.py`： 数据库相关操作。`addaQuestionRecord`往数据库里插入问题记录。

`resetvis.py`：重设vis字段。存数据库的时候有时候发生错误跳过了某些数据/请求超时但还是设置成了已访问
把收集到的回答个数不足question[answer_count]的问题重设为未访问
