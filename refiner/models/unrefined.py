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

class ZomatoContribution(BaseModel):
    type: str
    claimedDate: str  # We'll ignore this in storage but keep for validation
    witnesses: str
    walletAddress: str  # We'll ignore this in storage but keep for validation
    AccountUsername: str
    securedSharedData: SecuredSharedData

class ZomatoInputData(BaseModel):
    walletAddress: str  # We'll ignore this in storage but keep for validation
    claimDate: str  # We'll ignore this in storage but keep for validation
    contributions: List[ZomatoContribution]

# Keep the old ZomatoData for backward compatibility
class ZomatoData(BaseModel):
    type: str
    claimedDate: str  # We'll ignore this in storage but keep for validation
    witnesses: str
    walletAddress: str  # We'll ignore this in storage but keep for validation
    AccountUsername: str
    securedSharedData: SecuredSharedData