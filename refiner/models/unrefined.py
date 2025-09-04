from typing import List, Dict, Union, Optional
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

class ZomatoSecuredSharedData(BaseModel):
    userid: str
    orders: List[ZomatoOrder]

# Uber specific models
class UberTrip(BaseModel):
    beginTripTime: str
    dropoffTime: str
    pickupAddress: str
    dropoffAddress: str
    fare: str
    vehicleType: str

class UberSecuredSharedData(BaseModel):
    trips: List[UberTrip]
    userid: str
    username: str

# LinkedIn specific models
class LinkedInConnection(BaseModel):
    name: str
    headline: str
    url: str
    pfp: str

class LinkedInSecuredSharedData(BaseModel):
    linkedinUserData: str
    connectionsList: List[LinkedInConnection]

# Spotify specific models
class SpotifyTrack(BaseModel):
    trackName: str
    trackId: str

class SpotifyPlaylist(BaseModel):
    playlistId: str
    playlistName: str
    playlistOwner: str
    tracks: List[SpotifyTrack]

class SpotifyRecentlyPlayed(BaseModel):
    trackName: str
    trackId: str

class SpotifySecuredSharedData(BaseModel):
    username: str
    userPlaylists: List[SpotifyPlaylist]
    recentlyPlayed: List[SpotifyRecentlyPlayed]

# Netflix specific models
class NetflixSecuredSharedData(BaseModel):
    profileName: str
    favorites: List[str]
    userId: str

# Prime Video specific models
class PrimeVideoSecuredSharedData(BaseModel):
    profileName: str
    userId: str
    watchHistory: Dict[str, List[str]]

# Twitch specific models
class TwitchSecuredSharedData(BaseModel):
    username: str
    followers: int
    pfpUrl: str
    bio: str
    socials: List[str]

# Twitter specific models
class TwitterSecuredSharedData(BaseModel):
    userName: str
    followers: str
    following: str
    posts: str
    userDescription: Optional[str]

# Reddit specific models
class RedditKarma(BaseModel):
    postKarma: int
    commentKarma: int

class RedditPost(BaseModel):
    title: str
    id: str

class RedditSecuredSharedData(BaseModel):
    username: str
    pfp: str
    userid: str
    bio: str
    socialLinks: List[str]
    karma: RedditKarma
    posts: List[RedditPost]

# Steam specific models
class SteamSecuredSharedData(BaseModel):
    ownedGames: List[str]
    userId: str

# Union type for all secured shared data types
SecuredSharedDataUnion = Union[
    ZomatoSecuredSharedData,
    UberSecuredSharedData,
    LinkedInSecuredSharedData,
    SpotifySecuredSharedData,
    NetflixSecuredSharedData,
    PrimeVideoSecuredSharedData,
    TwitchSecuredSharedData,
    TwitterSecuredSharedData,
    RedditSecuredSharedData,
    SteamSecuredSharedData
]

# Generic contribution model
class Contribution(BaseModel):
    type: str  # EContributionType
    claimedDate: str
    witnesses: str
    walletAddress: str
    AccountUsername: str
    securedSharedData: SecuredSharedDataUnion

# Main input data model
class MultiProviderInputData(BaseModel):
    walletAddress: str
    claimDate: str
    contributions: List[Contribution]

# Legacy models for backward compatibility
class SecuredSharedData(BaseModel):
    userid: str
    orders: List[ZomatoOrder]

class ZomatoContribution(BaseModel):
    type: str
    claimedDate: str
    witnesses: str
    walletAddress: str
    AccountUsername: str
    securedSharedData: ZomatoSecuredSharedData

class ZomatoInputData(BaseModel):
    walletAddress: str
    claimDate: str
    contributions: List[ZomatoContribution]

class ZomatoData(BaseModel):
    type: str
    claimedDate: str
    witnesses: str
    walletAddress: str
    AccountUsername: str
    securedSharedData: ZomatoSecuredSharedData