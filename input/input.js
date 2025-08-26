const contributions = [
    {
        "type": "UBER",
        "claimedDate": "2025-08-18T10:30:00Z",
        "witnesses": "https://example.com/uber-proof",
        "walletAddress": "0x1234abcd5678efgh9012ijkl3456mnop7890qrst",
        "AccountUsername": "john_doe_uber",
        "securedSharedData": {
            "trips": [
                {
                    "beginTripTime": "2025-07-15T08:15:00Z",
                    "dropoffTime": "2025-07-15T08:45:00Z",
                    "pickupAddress": "123 Main St, San Francisco, CA",
                    "dropoffAddress": "456 Market St, San Francisco, CA",
                    "fare": "23.75 USD",
                    "vehicleType": "UberX"
                },
                {
                    "beginTripTime": "2025-07-20T19:10:00Z",
                    "dropoffTime": "2025-07-20T19:40:00Z",
                    "pickupAddress": "789 Pine St, San Francisco, CA",
                    "dropoffAddress": "22 Embarcadero, San Francisco, CA",
                    "fare": "17.50 USD",
                    "vehicleType": "Uber Comfort"
                }
            ],
            "userid": "uber_99123",
            "username": "john_doe_uber"
        }
    },
    {
        "type": "STEAM",
        "claimedDate": "2025-08-15T12:00:00Z",
        "witnesses": "https://example.com/steam-proof",
        "walletAddress": "0xabcd2345efgh6789ijkl0123mnop4567qrst8901",
        "AccountUsername": "gamer_jane",
        "securedSharedData": {
            "ownedGames": [
                "Counter-Strike 2",
                "Elden Ring",
                "Stardew Valley"
            ],
            "userId": "steam_88234"
        }
    },
    {
        "type": "AMAZON_PRIME",
        "claimedDate": "2025-08-10T14:45:00Z",
        "witnesses": "https://example.com/prime-proof",
        "walletAddress": "0x9876abcd5432efgh1098ijkl7654mnop3210qrst",
        "AccountUsername": "prime_alex",
        "securedSharedData": {
            "profileName": "Alex P",
            "watchHistory": {
                "2025-07-01": [
                    "The Boys S04E01",
                    "Invincible S02E03"
                ],
                "2025-07-15": [
                    "Fallout S01E05"
                ]
            }
        }
    },
    {
        "type": "ZOMATO",
        "claimedDate": "2025-08-05T09:20:00Z",
        "witnesses": "https://example.com/zomato-proof",
        "walletAddress": "0xefgh3456ijkl7890mnop1234qrst5678abcd9012",
        "AccountUsername": "foodie_sam",
        "securedSharedData": {
            "userid": "zomato_77231",
            "orders": [
                {
                    "orderId": "ZM123456",
                    "totalCost": "45.30 USD",
                    "dishString": "Paneer Butter Masala, Garlic Naan, Mango Lassi",
                    "deliveryDetails": {
                        "deliveryAddress": "101 Sunset Blvd, Los Angeles, CA",
                        "deliveryStatus": "Delivered",
                        "deliveryMessage": "Leave at doorstep",
                        "deliveryLabel": "Dinner"
                    },
                    "restaurantURL": "https://zomato.com/restaurant/awesome-indian"
                },
                {
                    "orderId": "ZM123789",
                    "totalCost": "18.75 USD",
                    "dishString": "Pepperoni Pizza, Coke",
                    "deliveryDetails": {
                        "deliveryAddress": "101 Sunset Blvd, Los Angeles, CA",
                        "deliveryStatus": "Delivered",
                        "deliveryMessage": "Ring doorbell",
                        "deliveryLabel": "Lunch"
                    },
                    "restaurantURL": "https://zomato.com/restaurant/pizza-heaven"
                }
            ]
        }
    }
];