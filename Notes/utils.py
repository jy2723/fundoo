import redis
import json


class Redismanager:  
    redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)

    @classmethod
    def get(cls,key):
        return cls.redis_client.hgetall(key)
    
    @classmethod
    def get_one(cls,key,field):
        return cls.redis_client.hget(key,field)
    
    @classmethod
    def save(cls,key,field,value):
        cls.redis_client.hset(key,field,value)
    
    @classmethod
    def delete(cls,key,field):
        cls.redis_client.hdel(key,field)
    