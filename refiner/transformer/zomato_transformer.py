from typing import Dict, Any, List
from datetime import datetime
from refiner.models.refined import Base, ZomatoAccount, ZomatoOrder
from refiner.transformer.base_transformer import DataTransformer
from refiner.models.unrefined import ZomatoInputData, ZomatoData
from refiner.utils.date import parse_timestamp


class ZomatoTransformer(DataTransformer):
    """
    Transformer for Zomato data.
    """
    
    def transform(self, data: Dict[str, Any]) -> List[Base]:
        """
        Transform raw Zomato data into SQLAlchemy model instances.
        Focus on contribution data in sequential manner.
        
        Args:
            data: Dictionary containing Zomato data
            
        Returns:
            List of SQLAlchemy model instances
        """
        models = []
        
        # Check if data has the new structure with contributions
        if 'contributions' in data:
            # New data structure - process contributions sequentially
            input_data = ZomatoInputData.model_validate(data)
            
            # Process each contribution sequentially
            for contribution in input_data.contributions:
                if contribution.type == "ZOMATO":
                    models.extend(self._process_zomato_contribution(contribution))
        else:
            # Old data structure for backward compatibility
            zomato_data = ZomatoData.model_validate(data)
            models.extend(self._process_legacy_zomato_data(zomato_data))
        
        return models
    
    def _process_zomato_contribution(self, contribution_data) -> List[Base]:
        """
        Process a single Zomato contribution sequentially.
        
        Args:
            contribution_data: Zomato contribution data
            
        Returns:
            List of SQLAlchemy model instances for this contribution
        """
        models = []
        
        # Create Zomato account instance (without redundant date/wallet fields)
        account = ZomatoAccount(
            data_type=contribution_data.type,
            witnesses=contribution_data.witnesses,
            account_username=contribution_data.AccountUsername,
            user_id=contribution_data.securedSharedData.userid
        )
        models.append(account)
        
        # Create order instances for each order sequentially
        for order_data in contribution_data.securedSharedData.orders:
            order = ZomatoOrder(
                order_id=order_data.orderId,
                account_id=None,  # Will be set after account is saved
                total_cost=order_data.totalCost,
                dish_string=order_data.dishString,
                restaurant_url=order_data.restaurantURL,
                delivery_address=order_data.deliveryDetails.deliveryAddress,
                delivery_status=order_data.deliveryDetails.deliveryStatus,
                delivery_message=order_data.deliveryDetails.deliveryMessage,
                delivery_label=order_data.deliveryDetails.deliveryLabel
            )
            # Set the relationship
            order.account = account
            models.append(order)
        
        return models
    
    def _process_legacy_zomato_data(self, zomato_data: ZomatoData) -> List[Base]:
        """
        Process legacy Zomato data structure (for backward compatibility).
        
        Args:
            zomato_data: Legacy Zomato data
            
        Returns:
            List of SQLAlchemy model instances
        """
        models = []
        
        # Create Zomato account instance (without redundant date/wallet fields)
        account = ZomatoAccount(
            data_type=zomato_data.type,
            witnesses=zomato_data.witnesses,
            account_username=zomato_data.AccountUsername,
            user_id=zomato_data.securedSharedData.userid
        )
        models.append(account)
        
        # Create order instances for each order sequentially
        for order_data in zomato_data.securedSharedData.orders:
            order = ZomatoOrder(
                order_id=order_data.orderId,
                account_id=None,  # Will be set after account is saved
                total_cost=order_data.totalCost,
                dish_string=order_data.dishString,
                restaurant_url=order_data.restaurantURL,
                delivery_address=order_data.deliveryDetails.deliveryAddress,
                delivery_status=order_data.deliveryDetails.deliveryStatus,
                delivery_message=order_data.deliveryDetails.deliveryMessage,
                delivery_label=order_data.deliveryDetails.deliveryLabel
            )
            # Set the relationship
            order.account = account
            models.append(order)
        
        return models
