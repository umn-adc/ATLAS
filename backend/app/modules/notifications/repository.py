from uuid import UUID
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.notifications.models import NotificationModel, NotificationType


class NotificationRepository():

    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        pass
    

    async def create(
        self,
        owner_id:UUID, 
        type:NotificationType, 
        title:str, 
        message:str, 
        data:dict
        ) -> Notification: #TODO dict for data???
        notification = NotificationModel(
            owner_id=owner_id, 
            type=type,
            title=title,
            message=message,
            data=data,
        )

        self.session.add(notification)
        await self.session.flush()
        await self.session.refresh(notification)

        return notification
    
    #TODO make udpate by id
    async def update_by_id():
            raise NotImplementedError

    #TODO make get count
    async def get_count():
            raise NotImplementedError
