import socketio


class EnvHandler(socketio.AsyncNamespace):
    async def on_connect(self, sid, environ):
        print("env connected")

    async def on_disconnect(self, sid):
        print("env disconnected")

    # 시간 정보
    # format : month(1~12)/day(1~31)/hour(1~12)/minute(0~60)
    async def on_turtlebot_time(self, sid, data):
        print(data)

    # 온도 정보
    # format : String (0~100)
    async def on_turtlebot_temp(self, sid, data):
        print(data)

    # 날시 정보
    # format : String ("Sunny", "Cloudy", "Foggu", "Stormy", "Rainy", "Snowy")
    async def on_turtlebot_weather(self, sid, data):
        print(data)
