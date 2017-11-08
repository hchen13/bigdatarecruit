# -*- coding: utf-8 -*-

# 用于md5加密
# @param str 字符串
# @return str 字符串
# @author WuXiaokun
# @DateTime 2017-08-17
def md5(src):
    import hashlib
    hash = hashlib.md5()
    if isinstance(src,str):
        src = src.encode('utf-8')
    hash.update(src)
    return hash.hexdigest()

# 用于给redis添加数据
# @param type 1,str 2,list 添加数据类型
# @param key
# @param value 数据值
# @return boolean
# @author WuXiaokun
# @DateTime 2017-11-07
def redisAddValue(type, key, value, host='127.0.0.1', port=6379):
    import redis
    r = redis.Redis(host=host,port=port)
    r.flushall()
    if type == 1:
        res = r.set(key, value)
    elif type == 2:
        res = r.lpush(key, value)
    return res

if __name__ == '__main__':
    res = redisAddValue(1, 'a', '1')
    print(res)