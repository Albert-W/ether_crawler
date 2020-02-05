#  所有的配置入口

#  入口网页
entry = 'https://etherscan.io/txsPending?ps=100&&m=&p=1'
# firstpage = 'https://etherscan.io/txsPending?ps=100&&m=&p=1'
# lastpage = 'https://etherscan.io/txsPending?ps=100&&m=&p=646'
useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'

# 页码信息获取 的regex 
# 字串符匹配方式 对应 int(pages_search.findall(raw_result)[0])
# regex = r'ellipsis">...</button><button type="button" class="Button PaginationButton Button--plain">(.*?)</button>'
pRegex = r'of <strong class="font-weight-medium">(\d+)</strong></span>'
# r'ellipsis">...</button><button type="button" class="Button PaginationButton Button--plain">(\d+)</button>'

