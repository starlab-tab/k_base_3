import functools

from flask import request
from flask_redis import FlaskRedis

from app.exceptions import FakeCode200, Code404
from app.models import MalIp, db

redis_client = FlaskRedis()


def ip_limiter(max_num=32, ex=1800):
    def wrapper(func):
        @functools.wraps(func)
        def _wrapper(*args, **kwargs):
            ip = request.remote_addr
            msg = get_ci_kv(request.headers, ['X-Real-Ip', 'X-Forwarded-For', 'User-Agent'])
            msg['X-Real-Ip'] = ip
            msg['comment'] = "You’re gonna be banned for a while"
            mal_ip = MalIp.query.filter_by(ip=ip).first()
            handle_mal_ip(mal_ip, msg)
            try:
                if redis_client.exists(ip):
                    redis_client.setrange(ip, 0, int(redis_client.get(ip)) + 1)
                else:
                    redis_client.set(ip, 1, ex=ex)
            except Exception as e:
                raise Code404()
            num = int(redis_client.get(ip))
            if num > max_num:
                redis_client.set(ip, num, ex=3600)
                if not handle_mal_ip(mal_ip, msg):
                    mal_ip = MalIp(ip=ip, num=1, xffs=[msg['X-Forwarded-For'][:16]], agents=[msg['User-Agent'][:128]])
                    with db.auto_commit():
                        db.session.add(mal_ip)
                raise FakeCode200(msg=msg)
            return func(*args, **kwargs)

        return _wrapper

    return wrapper


def handle_mal_ip(mal_ip, msg):
    if mal_ip:
        if mal_ip.num > 8:
            msg['comment'] = "byebye..."
            redis_client.delete(mal_ip.ip)
            raise FakeCode200(msg=msg)
        else:
            with db.auto_commit():
                xff = msg['X-Forwarded-For']
                agent = msg['User-Agent']
                if xff not in mal_ip.xffs and len(xff) > 7:
                    mal_ip.xffs.append(xff)
                if agent not in mal_ip.agents and len(agent) > 10:
                    mal_ip.agents.append(agent)
                mal_ip.num = mal_ip.num + 1
            return True
    return False


def get_ci_kv(input_dict, keys):
    msg = {}
    for key in keys:
        msg[key] = next((value for dict_key, value in input_dict.items() if dict_key.lower() == key.lower()), "")[:160]
    return msg