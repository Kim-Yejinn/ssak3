import socketio


class ControlHandler(socketio.AsyncNamespace):

    async def on_connect(self, sid, environ):
        print("control connected")

    async def on_disconnect(self, sid):
        print("control disconnected")
    # 세탁물 정보 확인
    async def on_result(self, data):
        print(data)

    # 세탁 시작
    async def emit_laundry_start(self, data):
        # 수거해야 할 목록도 보내야 함.
        await self.emit("laundry_start", data)
