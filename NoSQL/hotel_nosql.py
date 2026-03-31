# ============================================================
# The Deltin Hotel - NoSQL Database Component
# MongoDB + Python (PyMongo)
# ============================================================

from pymongo import MongoClient
from datetime import datetime

# ============================================================
# STEP 1 - CONNECT TO MONGODB
# ============================================================

try:
    client = MongoClient("mongodb://localhost:27017/")
    db = client["DeltinHotel"]
    print("Connected to MongoDB successfully!")
except Exception as e:
    print(f"Connection failed: {e}")
    exit()

# Collections (like tables in SQL)
guest_preferences = db["guest_preferences"]
reviews = db["reviews"]
rooms = db["rooms"]
social_media_mentions = db["social_media_mentions"]


# ============================================================
# STEP 2 - FUNCTIONS FOR GUEST PREFERENCES
# ============================================================

def add_guest_preference(guest_id, preferences):
    """Add or update a guest's preferences"""
    try:
        doc = {
            "guest_id": guest_id,
            "preferences": preferences,
            "created_at": datetime.now()
        }
        guest_preferences.insert_one(doc)
        print(f"Preferences saved for Guest ID: {guest_id}")
    except Exception as e:
        print(f"Error saving preferences: {e}")


def get_guest_preference(guest_id):
    """Retrieve preferences for a specific guest"""
    try:
        result = guest_preferences.find_one({"guest_id": guest_id})
        if result:
            print(f"\nPreferences for Guest ID {guest_id}:")
            print(f"   Room Type  : {result['preferences'].get('room_type', 'Not specified')}")
            print(f"   Floor      : {result['preferences'].get('floor', 'Not specified')}")
            print(f"   Dietary    : {result['preferences'].get('dietary', 'Not specified')}")
            print(f"   Accessible : {result['preferences'].get('accessibility', False)}")
        else:
            print(f"No preferences found for Guest ID {guest_id}")
    except Exception as e:
        print(f"Error retrieving preferences: {e}")


# ============================================================
# STEP 3 - FUNCTIONS FOR ROOMS
# ============================================================

def add_room(room_number, room_type, floor, amenities=None):
    """Add room information"""
    try:
        doc = {
            "room_number": room_number,
            "room_type": room_type,
            "floor": floor,
            "amenities": amenities or []
        }
        rooms.insert_one(doc)
        print(f"Room {room_number} added: {room_type} on floor {floor}")
    except Exception as e:
        print(f"Error adding room: {e}")


# ============================================================
# STEP 4 - FUNCTIONS FOR REVIEWS
# ============================================================

def add_review(guest_id, room_number, rating, comment):
    """Add a guest review for a room"""
    try:
        if not 1 <= rating <= 5:
            print("Rating must be between 1 and 5")
            return

        review = {
            "guest_id": guest_id,
            "room_number": room_number,
            "rating": rating,
            "comment": comment,
            "date": datetime.now()
        }
        reviews.insert_one(review)
        print(f"Review saved for Room {room_number} by Guest ID: {guest_id}")
    except Exception as e:
        print(f"Error saving review: {e}")


def get_reviews_by_room(room_number):
    """Get all reviews for a specific room"""
    try:
        results = list(reviews.find({"room_number": room_number}))
        if results:
            print(f"\nReviews for Room {room_number}:")
            for r in results:
                print(f"   Guest ID : {r['guest_id']}")
                print(f"   Rating   : {r['rating']}/5")
                print(f"   Comment  : {r['comment']}")
                print(f"   Date     : {r['date'].strftime('%d %b %Y')}")
                print(f"   {'-' * 40}")
        else:
            print(f"No reviews found for Room {room_number}")
    except Exception as e:
        print(f"Error retrieving reviews: {e}")


def get_average_rating(room_number):
    """Calculate average rating for a room using aggregation pipeline"""
    try:
        pipeline = [
            {"$match": {"room_number": room_number}},
            {"$group": {"_id": "$room_number", "avg_rating": {"$avg": "$rating"}, "count": {"$sum": 1}}}
        ]
        result = list(reviews.aggregate(pipeline))
        if result:
            avg = result[0]["avg_rating"]
            count = result[0]["count"]
            print(f"\nAverage rating for Room {room_number}: {avg:.1f}/5 (from {count} reviews)")
        else:
            print(f"No reviews found for Room {room_number}")
    except Exception as e:
        print(f"Error calculating average: {e}")


def get_reviews_analytics():
    """Advanced aggregation: Group reviews by room type and floor"""
    try:
        pipeline = [
            {"$lookup": {
                "from": "rooms",
                "localField": "room_number",
                "foreignField": "room_number",
                "as": "room_info"
            }},
            {"$unwind": "$room_info"},
            {"$group": {
                "_id": {"room_type": "$room_info.room_type", "floor": "$room_info.floor"},
                "avg_rating": {"$avg": "$rating"},
                "total_reviews": {"$sum": 1},
                "max_rating": {"$max": "$rating"},
                "min_rating": {"$min": "$rating"}
            }},
            {"$project": {
                "room_type": "$_id.room_type",
                "floor": "$_id.floor",
                "avg_rating": {"$round": ["$avg_rating", 1]},
                "total_reviews": 1,
                "max_rating": 1,
                "min_rating": 1,
                "_id": 0
            }},
            {"$sort": {"avg_rating": -1, "total_reviews": -1}}
        ]
        results = list(reviews.aggregate(pipeline))
        if results:
            print("\n--- Reviews Analytics by Room Type and Floor ---")
            for r in results:
                print(f"Room Type: {r['room_type']}, Floor: {r['floor']}")
                print(f"  Average Rating: {r['avg_rating']}/5")
                print(f"  Total Reviews: {r['total_reviews']}")
                print(f"  Rating Range: {r['min_rating']}-{r['max_rating']}")
                print("-" * 40)
        else:
            print("No analytics data available")
    except Exception as e:
        print(f"Error in analytics: {e}")


# ============================================================
# STEP 5 - FUNCTIONS FOR SOCIAL MEDIA MENTIONS
# ============================================================

def add_social_media_mention(platform, content, sentiment, mentions_room=None, date=None):
    """Add social media mention with nested data"""
    try:
        doc = {
            "platform": platform,
            "content": content,
            "sentiment": sentiment,  # positive, negative, neutral
            "mentions_room": mentions_room,
            "metadata": {
                "hashtags": content.count("#"),
                "mentions": content.count("@"),
                "engagement": {
                    "likes": 0,
                    "shares": 0,
                    "comments": 0
                }
            },
            "date": date or datetime.now()
        }
        social_media_mentions.insert_one(doc)
        print(f"Social media mention added from {platform}")
    except Exception as e:
        print(f"Error adding social media mention: {e}")


def get_combined_sentiment_analysis():
    """Combine reviews and social media using $lookup"""
    try:
        pipeline = [
            {"$group": {
                "_id": "$room_number",
                "reviews": {"$push": "$$ROOT"}
            }},
            {"$lookup": {
                "from": "social_media_mentions",
                "localField": "_id",
                "foreignField": "mentions_room",
                "as": "social_mentions"
            }},
            {"$project": {
                "room_number": "$_id",
                "avg_review_rating": {
                    "$avg": "$reviews.rating"
                },
                "review_count": {"$size": "$reviews"},
                "social_mentions_count": {"$size": "$social_mentions"},
                "positive_reviews": {
                    "$size": {
                        "$filter": {
                            "input": "$reviews",
                            "cond": {"$gte": ["$$this.rating", 4]}
                        }
                    }
                },
                "negative_reviews": {
                    "$size": {
                        "$filter": {
                            "input": "$reviews",
                            "cond": {"$lte": ["$$this.rating", 2]}
                        }
                    }
                }
            }},
            {"$project": {
                "room_number": 1,
                "avg_review_rating": {"$round": ["$avg_review_rating", 1]},
                "review_count": 1,
                "social_mentions_count": 1,
                "positive_reviews": 1,
                "negative_reviews": 1
            }},
            {"$sort": {"avg_review_rating": -1}}
        ]
        results = list(reviews.aggregate(pipeline))
        if results:
            print("\n--- Combined Sentiment Analysis (Reviews + Social Media) ---")
            for r in results:
                print(f"Room {r['room_number']}:")
                print(f"  Average Rating: {r['avg_review_rating']}/5")
                print(f"  Total Reviews: {r['review_count']}")
                print(f"  Social Mentions: {r['social_mentions_count']}")
                print(f"  Positive Reviews: {r['positive_reviews']}")
                print(f"  Negative Reviews: {r['negative_reviews']}")
                print("-" * 40)
        else:
            print("No combined analysis data available")
    except Exception as e:
        print(f"Error in combined analysis: {e}")


# ============================================================
# STEP 4 - MAIN PROGRAM (INSERT SAMPLE DATA & RUN QUERIES)
# ============================================================

if __name__ == "__main__":

    # Clear collections for fresh demo
    guest_preferences.drop()
    reviews.drop()
    rooms.drop()
    social_media_mentions.drop()

    print("\n" + "="*50)
    print("   THE DELTIN HOTEL - NoSQL Demo")
    print("="*50)

    # --- INSERT ROOM DATA ---
    print("\n--- Adding Room Information ---")

    add_room("101", "Standard", 1, ["WiFi", "TV", "Mini Bar"])
    add_room("202", "Suite", 2, ["WiFi", "TV", "Mini Bar", "Balcony", "Jacuzzi"])
    add_room("305", "Deluxe", 3, ["WiFi", "TV", "Mini Bar", "Ocean View"])

    # --- INSERT GUEST PREFERENCES ---
    print("\n--- Adding Guest Preferences ---")

    add_guest_preference(1, {
        "room_type": "Double",
        "floor": "High",
        "dietary": "Vegetarian",
        "accessibility": False,
        "extra_pillows": True
    })

    add_guest_preference(2, {
        "room_type": "Suite",
        "floor": "Top",
        "dietary": "Vegan",
        "accessibility": True
    })

    add_guest_preference(3, {
        "room_type": "Single",
        "floor": "Low",
        "dietary": "No preference",
        "accessibility": False,
        "extra_pillows": False,
        "quiet_room": True
    })

    # --- RETRIEVE GUEST PREFERENCES ---
    print("\n--- Retrieving Guest Preferences ---")
    get_guest_preference(1)
    get_guest_preference(2)
    get_guest_preference(3)

    # --- INSERT REVIEWS ---
    print("\n--- Adding Guest Reviews ---")

    add_review(1, "101", 5, "Fantastic stay! Room was spotless and staff were incredibly helpful.")
    add_review(2, "101", 4, "Great location and comfortable bed. Breakfast could be improved.")
    add_review(3, "202", 5, "Absolutely loved it. Will definitely return to The Deltin!")
    add_review(1, "305", 3, "Room was decent but the Wi-Fi was slow throughout the stay.")
    add_review(2, "202", 4, "Beautiful suite with amazing views. Highly recommend.")

    # --- INSERT SOCIAL MEDIA MENTIONS ---
    print("\n--- Adding Social Media Mentions ---")

    add_social_media_mention("Twitter", "Just had an amazing stay at @DeltinHotel room 202! The suite is gorgeous #HotelLife", "positive", "202")
    add_social_media_mention("Instagram", "WiFi was terrible in room 305. Not worth the price @DeltinHotel #Disappointed", "negative", "305")
    add_social_media_mention("Facebook", "Loved the breakfast at Deltin Hotel! Room 101 was cozy too.", "positive", "101")
    add_social_media_mention("Twitter", "Deltin Hotel needs better cleaning in standard rooms. Room 101 had dust everywhere.", "negative", "101")

    # --- RETRIEVE REVIEWS ---
    print("\n--- Retrieving Reviews by Room ---")
    get_reviews_by_room("101")
    get_reviews_by_room("202")

    # --- AVERAGE RATINGS ---
    print("\n--- Average Ratings ---")
    get_average_rating("101")
    get_average_rating("202")
    get_average_rating("305")

    # --- ADVANCED ANALYTICS ---
    print("\n--- Advanced Analytics ---")
    get_reviews_analytics()
    get_combined_sentiment_analysis()

    print("\n" + "="*50)
    print("   Demo Complete!")
    print("="*50)