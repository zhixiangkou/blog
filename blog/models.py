from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
import markdown
from django.utils.html import strip_tags


# Create your models here.
# 在数据库中创建Category表格，列名为name
class Category(models.Model):
    """
        django 要求模型必须继承 models.Model 类。
        Category 只需要一个简单的分类名 name 就可以了。
        CharField 指定了分类名 name 的数据类型，CharField 是字符型，
        CharField 的 max_length 参数指定其最大长度，超过这个长度的分类名就不能被存入数据库。
        当然 django 还为我们提供了多种其它的数据类型，如日期时间类型 DateTimeField、整数类型 IntegerField 等等。
        django 内置的全部类型可查看文档：
        https://docs.djangoproject.com/en/2.2/ref/models/fields/#field-types
        """
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Tag(models.Model):
    """
      标签 Tag 也比较简单，和 Category 一样。
      再次强调一定要继承 models.Model 类！
      """
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Post(models.Model):
    # 文章标题
    title = models.CharField('标题', max_length=100)
    short_title = models.CharField('简写标题', max_length=50, blank=True)

    # 文章正文，使用TextField存储较长文本
    body = models.TextField('正文')

    # 文章创建时间和最后修改时间
    created_time = models.DateTimeField('创建时间', default=timezone.now)
    modified_time = models.DateTimeField('修改时间')

    # 文章摘要，默认CharFiled必须存入数据，指定blank=True将允许空值
    excerpt = models.CharField('摘要', max_length=300, blank=True)

    image = models.ImageField(upload_to='coverimage/%Y/%m/%d/', verbose_name='封面图片', default='coverimage/default.jpg')

    # 文章与分类为一对多关系使用ForeignKey，on_delete表示数据删除时被关联数据的行为，models.CASCADE表示级联删除
    # ManyToManyField表示多对多，文章可以没有标签
    category = models.ForeignKey(Category, verbose_name='分类', on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, verbose_name='标签', blank=True)

    # User是从django.contrib.auth.models导入，文章与作者为一对多关系
    author = models.ForeignKey(User, verbose_name='作者', on_delete=models.CASCADE)

    views = models.PositiveIntegerField(default=0, editable=False)

    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name
        ordering = ['-created_time']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.modified_time = timezone.now()
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
        ])
        self.excerpt = strip_tags(md.convert(self.body))[:150]
        self.short_title = strip_tags(md.convert(self.title))[:18]
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})

    # def image_url(self):
    #     if self.image and hasattr(self.image, 'url'):
    #         return self.image.url
    #     else:
    #     return 'blog/assets/i/f10.jpg'


class Profile(models.Model):

    name = models.CharField(max_length=100)
    text1 = models.TextField('封面简介', blank=True)
    text2 = models.TextField('博客简介', blank=True)
    text3 = models.TextField('关于简介', blank=True)
    image1 = models.ImageField(upload_to='coverimage/', verbose_name='封面图片', default='coverimage/zhixiang1.jpg')
    image2 = models.ImageField(upload_to='coverimage/', verbose_name='博客图片', default='coverimage/zhixiang2.jpg')
    image3 = models.ImageField(upload_to='coverimage/', verbose_name='关于图片', default='coverimage/zhixiang1.jpg')
    class Meta:
        verbose_name = '个人简介'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
