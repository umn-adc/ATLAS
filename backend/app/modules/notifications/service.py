from uuid import UUID
from app.modules.notifications.schemas import(Notification, NotificationCreate, NotificationType, NotificationUpdate)

from app.modules.notifications.repository import NotificationRepository
class NotificationService():

    def __init__(self, repository: NotificationRepository) -> None:
        self.repository = repository

    async def create_notification( self, notification_data: NotificationCreate) -> Notification:
        
        await self.repository.create(
            owner_id= notification_data.owner_id,
            title=notification_data.title,
            message=notification_data.message,
            data=notification_data.data
            )
        # return What should this return??owner_id:UUID, 
                # type:NotificationType, 
                # title:str, 
                # message:str, 
                # data:dict
    

    #
    def get_notification(self, page: int, limit: int, unread_filter = False):
        return self.repository.get_notification(self, page, limit, unread_filter)


    def get_notification_count(self):
        raise NotImplementedError ## return paginated results???

    def read_all_notifications(self):
        raise NotImplementedError 

    def read_notification_by_id(self, owner_id: UUID, notification_id: UUID):
        #get notificaiton
        #check ownership
        # if correct: user datetime.func.now()

        raise NotImplementedError

