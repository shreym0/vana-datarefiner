from typing import List
from pydantic import BaseModel


# Zomato specific models
class DeliveryDetails(BaseModel):
    deliveryAddress: str
    deliveryStatus: str
    deliveryMessage: str
    deliveryLabel: str

class ZomatoOrder(BaseModel):
    orderId: str
    totalCost: str
    dishString: str
    deliveryDetails: DeliveryDetails
    restaurantURL: str

class SecuredSharedData(BaseModel):
    userid: str
    orders: List[ZomatoOrder]

class ZomatoData(BaseModel):
    type: str
    claimedDate: str
    witnesses: str
    walletAddress: str
    AccountUsername: str
    securedSharedData: SecuredSharedData