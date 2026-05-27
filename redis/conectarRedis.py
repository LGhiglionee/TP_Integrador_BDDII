import redis

def conectarRedis():

    try:

        redis_db = redis.Redis(
            host='localhost',
            port=6379,
            decode_responses=True
        )

        redis_db.ping()

        print("Conexión exitosa con Redis.")

        return redis_db

    except Exception as e:

        print(f"Se produjo un error al conectar con Redis: {e}")