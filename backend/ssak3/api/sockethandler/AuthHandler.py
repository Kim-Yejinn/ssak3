import socketio


class AuthHandler(socketio.AsyncNamespace):
    async def on_connect(self, sid, environ):
        print("auth connected")


    async def on_disconnect(self, sid):
        print("auth disconnected")

    async def on_authenticate(self, sid, data):
        # 등록된 터틀봇 번호인지 확인
        # data로 turtlebotNo가 번호가 들어감
        print(data)

        # 테스트용 데이터
        auth_data = '123'

        if data == auth_data:
            print("auth success")
        else:
            print("auth fail")
            await self.disconnect(sid)




