# Unix时间戳转正常时间
def unixToTime(unix_time):
    from datetime import datetime
    dtime = datetime.fromtimestamp(unix_time)
    res = dtime.strftime("%Y-%m-%d %H:%M:%S")
    return res

# 常见的编程语言
def getProgramingLanguage():
    programing_language_list = ['javascript', 'python', 'java', 'ruby', 'php', 'c\\+\\+', 'css', 'c\\#', 'go', 'typescript', 'shell', 'swift', 'scala', 'ios', 'DBA', 'matlab']
    return programing_language_list