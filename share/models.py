from datetime import datetime

from django.db import models


# Create your models here.
class Upload(models.Model):
    """
    default         设置值默认值
    max_length      设置字段长度最大值
    min_length      设置字段长度最小值
    verbose_name    解释说明易于理解
    """
    # 访问该页面的次数 IntegerField 表示整数字段
    download_docount = models.IntegerField(verbose_name=u"访问次数", default=0)
    # 唯一标识一个文件 CharField 表示字符串字段
    code = models.CharField(max_length=8, verbose_name=u"code")
    # Datatime 表示文件上传的时间，其中datetime.now 不能加括号,否则时间
    # 就变成了orm生成model的时间, 这里一定要注意！！
    data_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")
    # path 代表文件存储的路径
    path = models.CharField(max_length=32, verbose_name=u"下载路径")
    # name 文件名
    name = models.CharField(max_length=32, verbose_name=u"文件名", default="")
    # Filesize 文件大小
    file_size = models.CharField(max_length=10, verbose_name=u"文件大小")
    # PCIP 上传文件的IP
    PCIP = models.CharField(max_length=32, verbose_name=u"IP地址", default="")

    class Meta():  # Meta 可用于定义数据表名，排序方式等。
        verbose_name = "download"  # 指明一个易于理解和表示的单词形式的对象。
        db_table = "download"  # 声明数据表的名。

    def __str__(self):  # 表示在做查询操作时，我们看到的是 name 字段
        return self.name

    def increase_views(self):
        self.download_docount += 1
        self.save(update_fields=['download_docount'])
