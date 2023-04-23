import pymysql


class SQLManager():
    __instance = None
    __flag = False

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self):
        if not SQLManager.__flag:
            self.connect()
            SQLManager.__flag = True

    # 进入with语句自动执行
    def __enter__(self):
        return self

    # 退出with语句自动执行
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()

    # 连接数据库
    def connect(self):
        try:
            self.conn = pymysql.connect(host='localhost',
                                        port=15030,
                                        user='root',
                                        password='123456',
                                        database='spiders')
            self.cursor = self.conn.cursor()
        except Exception as e:
            print(e)

    def test(self):
        # 使用 execute()  方法执行 SQL 查询
        self.cursor.execute("SELECT VERSION()")

        # 使用 fetchone() 方法获取单条数据.
        data = self.cursor.fetchone()

        print("Database version : %s " % data)


if __name__ == '__main__':
    with SQLManager() as query:
        query.test()
