import socketio


class AuthHandler(socketio.AsyncNamespace):
    async def on_connect(self, sid, environ):
        print("auth connected")

    async def on_disconnect(self, sid):
        print("auth disconnected")

    async def on_authenticate(self, sid, data):
        # 등록된 터틀봇 번호인지 확인
        # data로 turtlebotNo가 번호가 들어감
        print("try turtlebot auth")
        print(data)

        # 테스트용 데이터
        # 보낼때 int로 보내면 int로 옴.
        auth_data = 123

        if data == auth_data:
            print("auth success")
            self.enter_room(sid, data)

        else:
            print("auth fail")




