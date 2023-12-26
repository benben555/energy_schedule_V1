import copy

from django.utils.safestring import mark_safe


class Pagination(object):
    def __init__(self, request, queryset, page_param="page", plus=5, page_size=10):
        query_dict = copy.deepcopy(request.GET)
        query_dict._mutable = True
        self.query_dict = query_dict
        self.page_param = page_param
        page = request.GET.get(page_param, "1")
        if page.isdecimal():
            page = int(page)
        else:
            page = 1
        self.page = page
        self.page_size = page_size
        self.start = (self.page - 1) * self.page_size
        self.end = self.page * self.page_size
        self.page_queryset = queryset[self.start:self.end]
        total_count = queryset.count()
        total_page_count, div = divmod(total_count, self.page_size)
        if div:
            total_page_count += 1
        self.total_page_count = total_page_count
        self.plus = plus

    def html(self):
        page_str_list = []
        start_page = max(1, min(self.page - 5, self.total_page_count - 2 * self.plus))
        end_page = min(self.total_page_count, max(2 * self.plus + 1, self.page + self.plus))
        self.query_dict.setlist(self.page_param, [1])  # 加上搜索条件

        page_str_list.append('<li><a href="?{}">首页</a></li>'.format(self.query_dict.urlencode()))
        self.query_dict.setlist(self.page_param, [max(1, self.page - 1)])
        prev = '<li><a href="?{}">上一页</a></li>'.format(self.query_dict.urlencode())

        page_str_list.append(prev)
        for i in range(start_page, end_page + 1):
            self.query_dict.setlist(self.page_param, [i])
            if i == self.page:
                ele = '<li class="active"><a href="?{}">{}</a></li>'.format(self.query_dict.urlencode(), i)
            else:
                ele = '<li><a href="?{}">{}</a></li>'.format(self.query_dict.urlencode(), i)
            page_str_list.append(ele)
        self.query_dict.setlist(self.page_param, [min(self.total_page_count, self.page + 1)])
        nextv = '<li><a href="?{}">下一页</a></li>'.format(self.query_dict.urlencode())
        page_str_list.append(nextv)
        self.query_dict.setlist(self.page_param, [self.total_page_count])
        page_str_list.append('<li><a href="?{}">尾页</a></li>'.format(self.query_dict.urlencode()))
        search_string = """
            <li>
                    <form style="float: left;margin-left: 1px" method="get">
                        <input type="text" name="page"
                               class="form-control" placeholder="页码" style="position:relative;
                               float: left;display: inline-block;width: 80px;border-radius: 0">
                        <button class="btn btn-default" type="submit" style="border-radius: 0">跳转</button>
                        </input>

                    </form>
                </li>"""
        page_str_list.append(search_string)
        page_string = mark_safe("".join(page_str_list))
        return page_string
