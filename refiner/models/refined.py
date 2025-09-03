from datetime import datetime
from sqlalchemy import Column, String, Integer, Float, ForeignKey, DateTime, Text, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

# Base model for SQLAlchemy
Base = declarative_base()

# Zomato specific models
class ZomatoAccount(Base):
    __tablename__ = 'zomato_accounts'
    
    account_id = Column(Integer, primary_key=True, autoincrement=True)
    data_type = Column(String, nullable=False)  # "ZOMATO"
    witnesses = Column(String, nullable=False)
    account_username = Column(String, nullable=False)
    user_id = Column(String, nullable=False)  # Zomato user ID
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    
    orders = relationship("ZomatoOrder", back_populates="account")

class ZomatoOrder(Base):
    __tablename__ = 'zomato_orders'
    
    order_id = Column(String, primary_key=True)
    account_id = Column(Integer, ForeignKey('zomato_accounts.account_id'), nullable=False)
    total_cost = Column(String, nullable=False)
    dish_string = Column(Text, nullable=False)
    restaurant_url = Column(String, nullable=False)
    delivery_address = Column(Text, nullable=False)
    delivery_status = Column(String, nullable=False)
    delivery_message = Column(String, nullable=True)
    delivery_label = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    
    account = relationship("ZomatoAccount", back_populates="orders")

# Uber specific models
class UberAccount(Base):
    __tablename__ = 'uber_accounts'
    
    account_id = Column(Integer, primary_key=True, autoincrement=True)
    data_type = Column(String, nullable=False)  # "UBER"
    witnesses = Column(String, nullable=False)
    account_username = Column(String, nullable=False)
    user_id = Column(String, nullable=False)
    username = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    
    trips = relationship("UberTrip", back_populates="account")

class UberTrip(Base):
    __tablename__ = 'uber_trips'
    
    trip_id = Column(Integer, primary_key=True, autoincrement=True)
    account_id = Column(Integer, ForeignKey('uber_accounts.account_id'), nullable=False)
    begin_trip_time = Column(String, nullable=False)
    dropoff_time = Column(String, nullable=False)
    pickup_address = Column(Text, nullable=False)
    dropoff_address = Column(Text, nullable=False)
    fare = Column(String, nullable=False)
    vehicle_type = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    
    account = relationship("UberAccount", back_populates="trips")

# LinkedIn specific models
class LinkedinAccount(Base):
    __tablename__ = 'linkedin_accounts'
    
    account_id = Column(Integer, primary_key=True, autoincrement=True)
    data_type = Column(String, nullable=False)  # "LINKEDIN"
    witnesses = Column(String, nullable=False)
    account_username = Column(String, nullable=False)
    linkedin_user_data = Column(Text, nullable=False)  # JSON string
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    
    connections = relationship("LinkedinConnection", back_populates="account")

class LinkedinConnection(Base):
    __tablename__ = 'linkedin_connections'
    
    connection_id = Column(Integer, primary_key=True, autoincrement=True)
    account_id = Column(Integer, ForeignKey('linkedin_accounts.account_id'), nullable=False)
    name = Column(String, nullable=False)
    headline = Column(Text, nullable=True)
    url = Column(String, nullable=True)
    pfp = Column(String, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    
    account = relationship("LinkedinAccount", back_populates="connections")

# Spotify specific models
class SpotifyAccount(Base):
    __tablename__ = 'spotify_accounts'
    
    account_id = Column(Integer, primary_key=True, autoincrement=True)
    data_type = Column(String, nullable=False)  # "SPOTIFY"
    witnesses = Column(String, nullable=False)
    account_username = Column(String, nullable=False)
    username = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    
    playlists = relationship("SpotifyPlaylist", back_populates="account")
    recently_played = relationship("SpotifyRecentlyPlayed", back_populates="account")

class SpotifyPlaylist(Base):
    __tablename__ = 'spotify_playlists'
    
    playlist_id = Column(String, primary_key=True)
    account_id = Column(Integer, ForeignKey('spotify_accounts.account_id'), nullable=False)
    playlist_name = Column(String, nullable=False)
    playlist_owner = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    
    account = relationship("SpotifyAccount", back_populates="playlists")
    tracks = relationship("SpotifyTrack", back_populates="playlist")

class SpotifyTrack(Base):
    __tablename__ = 'spotify_tracks'
    
    track_id = Column(String, primary_key=True)
    playlist_id = Column(String, ForeignKey('spotify_playlists.playlist_id'), nullable=False)
    track_name = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    
    playlist = relationship("SpotifyPlaylist", back_populates="tracks")

class SpotifyRecentlyPlayed(Base):
    __tablename__ = 'spotify_recently_played'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    account_id = Column(Integer, ForeignKey('spotify_accounts.account_id'), nullable=False)
    track_name = Column(String, nullable=False)
    track_id = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    
    account = relationship("SpotifyAccount", back_populates="recently_played")

# Netflix specific models
class NetflixAccount(Base):
    __tablename__ = 'netflix_accounts'
    
    account_id = Column(Integer, primary_key=True, autoincrement=True)
    data_type = Column(String, nullable=False)  # "NETFLIX"
    witnesses = Column(String, nullable=False)
    account_username = Column(String, nullable=False)
    profile_name = Column(String, nullable=False)
    user_id = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    
    favorites = relationship("NetflixFavorite", back_populates="account")

class NetflixFavorite(Base):
    __tablename__ = 'netflix_favorites'
    
    favorite_id = Column(Integer, primary_key=True, autoincrement=True)
    account_id = Column(Integer, ForeignKey('netflix_accounts.account_id'), nullable=False)
    favorite_item = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    
    account = relationship("NetflixAccount", back_populates="favorites")

# Prime Video specific models
class PrimeVideoAccount(Base):
    __tablename__ = 'prime_video_accounts'
    
    account_id = Column(Integer, primary_key=True, autoincrement=True)
    data_type = Column(String, nullable=False)  # "AMAZON_PRIME"
    witnesses = Column(String, nullable=False)
    account_username = Column(String, nullable=False)
    profile_name = Column(String, nullable=False)
    user_id = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    
    watch_history = relationship("PrimeVideoWatchHistory", back_populates="account")

class PrimeVideoWatchHistory(Base):
    __tablename__ = 'prime_video_watch_history'
    
    watch_id = Column(Integer, primary_key=True, autoincrement=True)
    account_id = Column(Integer, ForeignKey('prime_video_accounts.account_id'), nullable=False)
    watch_date = Column(String, nullable=False)
    watched_items = Column(JSON, nullable=False)  # List of watched items for that date
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    
    account = relationship("PrimeVideoAccount", back_populates="watch_history")

# Twitch specific models
class TwitchAccount(Base):
    __tablename__ = 'twitch_accounts'
    
    account_id = Column(Integer, primary_key=True, autoincrement=True)
    data_type = Column(String, nullable=False)  # "TWITCH"
    witnesses = Column(String, nullable=False)
    account_username = Column(String, nullable=False)
    username = Column(String, nullable=False)
    followers = Column(Integer, nullable=False)
    pfp_url = Column(String, nullable=True)
    bio = Column(Text, nullable=True)
    socials = Column(JSON, nullable=True)  # List of social links
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

# Twitter specific models
class TwitterAccount(Base):
    __tablename__ = 'twitter_accounts'
    
    account_id = Column(Integer, primary_key=True, autoincrement=True)
    data_type = Column(String, nullable=False)  # "TWITTER"
    witnesses = Column(String, nullable=False)
    account_username = Column(String, nullable=False)
    user_name = Column(String, nullable=False)
    followers = Column(String, nullable=False)
    following = Column(String, nullable=False)
    posts = Column(String, nullable=False)
    user_description = Column(Text, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

# Reddit specific models
class RedditAccount(Base):
    __tablename__ = 'reddit_accounts'
    
    account_id = Column(Integer, primary_key=True, autoincrement=True)
    data_type = Column(String, nullable=False)  # "REDDIT"
    witnesses = Column(String, nullable=False)
    account_username = Column(String, nullable=False)
    username = Column(String, nullable=False)
    pfp = Column(String, nullable=True)
    user_id = Column(String, nullable=False)
    bio = Column(Text, nullable=True)
    social_links = Column(JSON, nullable=True)  # List of social links
    post_karma = Column(Integer, nullable=False)
    comment_karma = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    
    posts = relationship("RedditPost", back_populates="account")

class RedditPost(Base):
    __tablename__ = 'reddit_posts'
    
    post_id = Column(String, primary_key=True)
    account_id = Column(Integer, ForeignKey('reddit_accounts.account_id'), nullable=False)
    title = Column(Text, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    
    account = relationship("RedditAccount", back_populates="posts")

# Steam specific models
class SteamAccount(Base):
    __tablename__ = 'steam_accounts'
    
    account_id = Column(Integer, primary_key=True, autoincrement=True)
    data_type = Column(String, nullable=False)  # "STEAM"
    witnesses = Column(String, nullable=False)
    account_username = Column(String, nullable=False)
    user_id = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    
    games = relationship("SteamGame", back_populates="account")

class SteamGame(Base):
    __tablename__ = 'steam_games'
    
    game_id = Column(Integer, primary_key=True, autoincrement=True)
    account_id = Column(Integer, ForeignKey('steam_accounts.account_id'), nullable=False)
    game_name = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    
    account = relationship("SteamAccount", back_populates="games")
