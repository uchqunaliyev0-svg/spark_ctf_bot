import time
from aiogram import BaseMiddleware
from aiogram.types import Message

class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, limit=1.0): # 1 sekund ichida limit
        self.limit = limit
        self.users = {}
        super().__init__()

    async def __call__(self, handler, event: Message, data):
        user_id = event.from_user.id
        now = time.time()

        if user_id in self.users:
            # 1 sekund ichida 10 tadan ko'p xabar yuborsa
            last_time, count = self.users[user_id]
            if now - last_time < self.limit:
                if count >= 10:
                    return # Xabarni tashlab yuboramiz, javob bermaymiz
                self.users[user_id] = (last_time, count + 1)
            else:
                self.users[user_id] = (now, 1)
        else:
            self.users[user_id] = (now, 1)

        return await handler(event, data)
