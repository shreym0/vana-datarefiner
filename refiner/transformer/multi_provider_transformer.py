from typing import Dict, Any, List
from datetime import datetime
from refiner.models.refined import (
    Base, ZomatoAccount, ZomatoOrder, UberAccount, UberTrip,
    LinkedinAccount, LinkedinConnection, SpotifyAccount, SpotifyPlaylist,
    SpotifyTrack, SpotifyRecentlyPlayed, NetflixAccount, NetflixFavorite,
    PrimeVideoAccount, PrimeVideoWatchHistory, TwitchAccount,
    TwitterAccount, RedditAccount, RedditPost, SteamAccount, SteamGame
)
from refiner.transformer.base_transformer import DataTransformer
from refiner.models.unrefined import (
    MultiProviderInputData, ZomatoInputData, ZomatoData,
    ZomatoSecuredSharedData, UberSecuredSharedData, LinkedInSecuredSharedData,
    SpotifySecuredSharedData, NetflixSecuredSharedData, PrimeVideoSecuredSharedData,
    TwitchSecuredSharedData, TwitterSecuredSharedData, RedditSecuredSharedData,
    SteamSecuredSharedData
)
import json


class MultiProviderTransformer(DataTransformer):
    """
    Transformer for multi-provider data that can handle different types of contributions.
    """
    
    def transform(self, data: Dict[str, Any]) -> List[Base]:
        """
        Transform raw multi-provider data into SQLAlchemy model instances.
        
        Args:
            data: Dictionary containing multi-provider data
            
        Returns:
            List of SQLAlchemy model instances
        """
        models = []
        
        # Check if data has the new multi-provider structure
        if 'contributions' in data:
            # Check if it's the legacy Zomato-only structure
            if self._is_legacy_zomato_structure(data):
                input_data = ZomatoInputData.model_validate(data)
                for contribution in input_data.contributions:
                    if contribution.type == "ZOMATO":
                        models.extend(self._process_zomato_contribution(contribution))
            else:
                # New multi-provider structure
                input_data = MultiProviderInputData.model_validate(data)
                for contribution in input_data.contributions:
                    models.extend(self._process_contribution_by_type(contribution))
        else:
            # Legacy single contribution structure
            zomato_data = ZomatoData.model_validate(data)
            models.extend(self._process_legacy_zomato_data(zomato_data))
        
        return models
    
    def _is_legacy_zomato_structure(self, data: Dict[str, Any]) -> bool:
        """Check if the data structure is the legacy Zomato-only format."""
        if 'contributions' not in data:
            return False
        
        # Check if ALL contributions are Zomato type and have the legacy structure
        zomato_count = 0
        total_contributions = len(data['contributions'])
        
        for contribution in data['contributions']:
            if contribution.get('type') == 'ZOMATO':
                if 'securedSharedData' in contribution:
                    secured_data = contribution['securedSharedData']
                    # Legacy Zomato structure has 'userid' and 'orders'
                    if 'userid' in secured_data and 'orders' in secured_data:
                        zomato_count += 1
        
        # Only consider it legacy if ALL contributions are Zomato
        return zomato_count == total_contributions and total_contributions > 0
    
    def _process_contribution_by_type(self, contribution) -> List[Base]:
        """Process a contribution based on its type."""
        contribution_type = contribution.type
        
        if contribution_type == "ZOMATO":
            return self._process_zomato_contribution_new(contribution)
        elif contribution_type == "UBER":
            return self._process_uber_contribution(contribution)
        elif contribution_type == "LINKEDIN":
            return self._process_linkedin_contribution(contribution)
        elif contribution_type == "SPOTIFY":
            return self._process_spotify_contribution(contribution)
        elif contribution_type == "NETFLIX":
            return self._process_netflix_contribution(contribution)
        elif contribution_type == "AMAZON_PRIME":
            return self._process_prime_video_contribution(contribution)
        elif contribution_type == "TWITCH":
            return self._process_twitch_contribution(contribution)
        elif contribution_type == "TWITTER":
            return self._process_twitter_contribution(contribution)
        elif contribution_type == "REDDIT":
            return self._process_reddit_contribution(contribution)
        elif contribution_type == "STEAM":
            return self._process_steam_contribution(contribution)
        else:
            # Unknown contribution type, skip
            return []
    
    def _process_zomato_contribution_new(self, contribution) -> List[Base]:
        """Process Zomato contribution with new structure."""
        models = []
        secured_data = ZomatoSecuredSharedData.model_validate(contribution.securedSharedData)
        
        account = ZomatoAccount(
            data_type=contribution.type,
            witnesses=contribution.witnesses,
            account_username=contribution.AccountUsername,
            user_id=secured_data.userid
        )
        models.append(account)
        
        for order_data in secured_data.orders:
            order = ZomatoOrder(
                order_id=order_data.orderId,
                account_id=None,
                total_cost=order_data.totalCost,
                dish_string=order_data.dishString,
                restaurant_url=order_data.restaurantURL,
                delivery_address=order_data.deliveryDetails.deliveryAddress,
                delivery_status=order_data.deliveryDetails.deliveryStatus,
                delivery_message=order_data.deliveryDetails.deliveryMessage,
                delivery_label=order_data.deliveryDetails.deliveryLabel
            )
            order.account = account
            models.append(order)
        
        return models
    
    def _process_uber_contribution(self, contribution) -> List[Base]:
        """Process Uber contribution."""
        models = []
        secured_data = UberSecuredSharedData.model_validate(contribution.securedSharedData)
        
        account = UberAccount(
            data_type=contribution.type,
            witnesses=contribution.witnesses,
            account_username=contribution.AccountUsername,
            user_id=secured_data.userid,
            username=secured_data.username
        )
        models.append(account)
        
        for trip_data in secured_data.trips:
            trip = UberTrip(
                account_id=None,
                begin_trip_time=trip_data.beginTripTime,
                dropoff_time=trip_data.dropoffTime,
                pickup_address=trip_data.pickupAddress,
                dropoff_address=trip_data.dropoffAddress,
                fare=trip_data.fare,
                vehicle_type=trip_data.vehicleType
            )
            trip.account = account
            models.append(trip)
        
        return models
    
    def _process_linkedin_contribution(self, contribution) -> List[Base]:
        """Process LinkedIn contribution."""
        models = []
        secured_data = LinkedInSecuredSharedData.model_validate(contribution.securedSharedData)
        
        account = LinkedinAccount(
            data_type=contribution.type,
            witnesses=contribution.witnesses,
            account_username=contribution.AccountUsername,
            linkedin_user_data=secured_data.linkedinUserData
        )
        models.append(account)
        
        for connection_data in secured_data.connectionsList:
            connection = LinkedinConnection(
                account_id=None,
                name=connection_data.name,
                headline=connection_data.headline,
                url=connection_data.url,
                pfp=connection_data.pfp
            )
            connection.account = account
            models.append(connection)
        
        return models
    
    def _process_spotify_contribution(self, contribution) -> List[Base]:
        """Process Spotify contribution."""
        models = []
        secured_data = SpotifySecuredSharedData.model_validate(contribution.securedSharedData)
        
        account = SpotifyAccount(
            data_type=contribution.type,
            witnesses=contribution.witnesses,
            account_username=contribution.AccountUsername,
            username=secured_data.username
        )
        models.append(account)
        
        # Process playlists
        for playlist_data in secured_data.userPlaylists:
            playlist = SpotifyPlaylist(
                playlist_id=playlist_data.playlistId,
                account_id=None,
                playlist_name=playlist_data.playlistName,
                playlist_owner=playlist_data.playlistOwner
            )
            playlist.account = account
            models.append(playlist)
            
            # Process tracks in playlist
            for track_data in playlist_data.tracks:
                track = SpotifyTrack(
                    track_id=track_data.trackId,
                    playlist_id=playlist_data.playlistId,
                    track_name=track_data.trackName
                )
                track.playlist = playlist
                models.append(track)
        
        # Process recently played tracks
        for recent_track in secured_data.recentlyPlayed:
            recently_played = SpotifyRecentlyPlayed(
                account_id=None,
                track_name=recent_track.trackName,
                track_id=recent_track.trackId
            )
            recently_played.account = account
            models.append(recently_played)
        
        return models
    
    def _process_netflix_contribution(self, contribution) -> List[Base]:
        """Process Netflix contribution."""
        models = []
        secured_data = NetflixSecuredSharedData.model_validate(contribution.securedSharedData)
        
        account = NetflixAccount(
            data_type=contribution.type,
            witnesses=contribution.witnesses,
            account_username=contribution.AccountUsername,
            profile_name=secured_data.profileName,
            user_id=secured_data.userId
        )
        models.append(account)
        
        for favorite_item in secured_data.favorites:
            favorite = NetflixFavorite(
                account_id=None,
                favorite_item=favorite_item
            )
            favorite.account = account
            models.append(favorite)
        
        return models
    
    def _process_prime_video_contribution(self, contribution) -> List[Base]:
        """Process Prime Video contribution."""
        models = []
        secured_data = PrimeVideoSecuredSharedData.model_validate(contribution.securedSharedData)
        
        account = PrimeVideoAccount(
            data_type=contribution.type,
            witnesses=contribution.witnesses,
            account_username=contribution.AccountUsername,
            profile_name=secured_data.profileName,
            user_id=secured_data.userId
        )
        models.append(account)
        
        for date, watched_items in secured_data.watchHistory.items():
            watch_history = PrimeVideoWatchHistory(
                account_id=None,
                watch_date=date,
                watched_items=watched_items
            )
            watch_history.account = account
            models.append(watch_history)
        
        return models
    
    def _process_twitch_contribution(self, contribution) -> List[Base]:
        """Process Twitch contribution."""
        models = []
        secured_data = TwitchSecuredSharedData.model_validate(contribution.securedSharedData)
        
        account = TwitchAccount(
            data_type=contribution.type,
            witnesses=contribution.witnesses,
            account_username=contribution.AccountUsername,
            username=secured_data.username,
            followers=secured_data.followers,
            pfp_url=secured_data.pfpUrl,
            bio=secured_data.bio,
            socials=secured_data.socials
        )
        models.append(account)
        
        return models
    
    def _process_twitter_contribution(self, contribution) -> List[Base]:
        """Process Twitter contribution."""
        models = []
        secured_data = TwitterSecuredSharedData.model_validate(contribution.securedSharedData)
        
        account = TwitterAccount(
            data_type=contribution.type,
            witnesses=contribution.witnesses,
            account_username=contribution.AccountUsername,
            user_name=secured_data.userName,
            followers=secured_data.followers,
            following=secured_data.following,
            posts=secured_data.posts,
            user_description=secured_data.userDescription
        )
        models.append(account)
        
        return models
    
    def _process_reddit_contribution(self, contribution) -> List[Base]:
        """Process Reddit contribution."""
        models = []
        secured_data = RedditSecuredSharedData.model_validate(contribution.securedSharedData)
        
        account = RedditAccount(
            data_type=contribution.type,
            witnesses=contribution.witnesses,
            account_username=contribution.AccountUsername,
            username=secured_data.username,
            pfp=secured_data.pfp,
            user_id=secured_data.userid,
            bio=secured_data.bio,
            social_links=secured_data.socialLinks,
            post_karma=secured_data.karma.postKarma,
            comment_karma=secured_data.karma.commentKarma
        )
        models.append(account)
        
        for post_data in secured_data.posts:
            post = RedditPost(
                post_id=post_data.id,
                account_id=None,
                title=post_data.title
            )
            post.account = account
            models.append(post)
        
        return models
    
    def _process_steam_contribution(self, contribution) -> List[Base]:
        """Process Steam contribution."""
        models = []
        secured_data = SteamSecuredSharedData.model_validate(contribution.securedSharedData)
        
        account = SteamAccount(
            data_type=contribution.type,
            witnesses=contribution.witnesses,
            account_username=contribution.AccountUsername,
            user_id=secured_data.userId
        )
        models.append(account)
        
        for game_name in secured_data.ownedGames:
            game = SteamGame(
                account_id=None,
                game_name=game_name
            )
            game.account = account
            models.append(game)
        
        return models
    
    # Legacy methods for backward compatibility
    def _process_zomato_contribution(self, contribution_data) -> List[Base]:
        """Process a single Zomato contribution (legacy method)."""
        models = []
        
        account = ZomatoAccount(
            data_type=contribution_data.type,
            witnesses=contribution_data.witnesses,
            account_username=contribution_data.AccountUsername,
            user_id=contribution_data.securedSharedData.userid
        )
        models.append(account)
        
        for order_data in contribution_data.securedSharedData.orders:
            order = ZomatoOrder(
                order_id=order_data.orderId,
                account_id=None,
                total_cost=order_data.totalCost,
                dish_string=order_data.dishString,
                restaurant_url=order_data.restaurantURL,
                delivery_address=order_data.deliveryDetails.deliveryAddress,
                delivery_status=order_data.deliveryDetails.deliveryStatus,
                delivery_message=order_data.deliveryDetails.deliveryMessage,
                delivery_label=order_data.deliveryDetails.deliveryLabel
            )
            order.account = account
            models.append(order)
        
        return models
    
    def _process_legacy_zomato_data(self, zomato_data) -> List[Base]:
        """Process legacy Zomato data structure."""
        models = []
        
        account = ZomatoAccount(
            data_type=zomato_data.type,
            witnesses=zomato_data.witnesses,
            account_username=zomato_data.AccountUsername,
            user_id=zomato_data.securedSharedData.userid
        )
        models.append(account)
        
        for order_data in zomato_data.securedSharedData.orders:
            order = ZomatoOrder(
                order_id=order_data.orderId,
                account_id=None,
                total_cost=order_data.totalCost,
                dish_string=order_data.dishString,
                restaurant_url=order_data.restaurantURL,
                delivery_address=order_data.deliveryDetails.deliveryAddress,
                delivery_status=order_data.deliveryDetails.deliveryStatus,
                delivery_message=order_data.deliveryDetails.deliveryMessage,
                delivery_label=order_data.deliveryDetails.deliveryLabel
            )
            order.account = account
            models.append(order)
        
        return models
