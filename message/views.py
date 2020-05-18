# Create your views here.
from django.contrib import messages
from django.http import HttpResponse

from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import MessageForm


@require_POST
def message(request):
    # django 将用户提交的数据封装在 request.POST 中，这是一个类字典对象。
    # 我们利用这些数据构造了 CommentForm 的实例，这样就生成了一个绑定了用户提交数据的表单。
    form = MessageForm(request.POST)

    # 当调用 form.is_valid() 方法时，django 自动帮我们检查表单的数据是否符合格式要求。
    if form.is_valid():
        # 检查到数据是合法的，调用表单的 save 方法保存数据到数据库，
        # commit=False 的作用是仅仅利用表单的数据生成 Comment 模型类的实例，但还不保存评论数据到数据库。
        message = form.save(commit=False)

        # 最终将评论数据保存进数据库，调用模型实例的 save 方法
        message.save()

        messages.add_message(request, messages.SUCCESS, '消息发送成功！', extra_tags='success')
        # 重定向到 post 的详情页，实际上当 redirect 函数接收一个模型的实例时，它会调用这个模型实例的 get_absolute_url 方法，
        # 然后重定向到 get_absolute_url 方法返回的 URL。
        return redirect('/contact')
        # return HttpResponse('消息发送成功！')
    # 检查到数据不合法，我们渲染一个预览页面，用于展示表单的错误。
    # 注意这里被评论的文章 post 也传给了模板，因为我们需要根据 post 来生成表单的提交地址。
    # context = {
    #     'form': form,
    # }
    # messages.add_message(request, messages.ERROR, '消息发送失败！请修改表单中的错误后重新提交。', extra_tags='danger')
    # return render(request, 'message/inclusions/preview.html', context=context)
