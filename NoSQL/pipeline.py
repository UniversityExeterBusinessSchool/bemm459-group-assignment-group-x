# ============================================================
# The Deltin Hotel — Polyglot Persistence Pipeline
# Connects University SQL Server + Local MongoDB
# ============================================================

import sys
import pyodbc
from pymongo import MongoClient
import matplotlib
matplotlib.use("Agg")  # non-GUI backend for scripts
import matplotlib.pyplot as plt


# ============================================================
# STEP 1 — DATABASE CONNECTIONS
# ============================================================

def connect_sql_server():
    """Connect to University SQL Server"""
    try:
        conn = pyodbc.connect(
            "DRIVER={SQL Server};"
            "SERVER=mcruebs04.isad.isadroot.ex.ac.uk;"
            "DATABASE=BEMM459_2026_Group_X;"
            "UID=Group_X_2026;"
            "PWD=XusA274+Vi;"
            "TrustServerCertificate=yes;"
        )
        print("✅ Connected to SQL Server successfully!")
        return conn
    except Exception as e:
        print(f"❌ SQL Server connection failed: {e}")
        sys.exit(1)


def connect_mongodb():
    """Connect to local MongoDB"""
    try:
        client = MongoClient("mongodb://localhost:27017/")
        db = client["DeltinHotel"]
        print("✅ Connected to MongoDB successfully!")
        return client, db
    except Exception as e:
        print(f"❌ MongoDB connection failed: {e}")
        sys.exit(1)


# ============================================================
# STEP 2 — FETCH FROM SQL SERVER
# ============================================================

def get_guest_from_sql(sql_cursor, guest_id):
    """Fetch guest details from SQL Server"""
    try:
        sql_cursor.execute("""
            SELECT guest_Id, first_name, last_name
            FROM dbo.guest
            WHERE guest_Id = ?
        """, guest_id)
        row = sql_cursor.fetchone()

        if row:
            return {
                "guest_id": row[0],
                "first_name": row[1],
                "last_name": row[2],
                "email": None,
                "phone": None
            }

        print(f"⚠️ No guest found with ID {guest_id}")
        return None

    except Exception as e:
        print(f"❌ Error fetching guest: {e}")
        return None


def get_bookings_from_sql(sql_cursor, guest_id):
    """Fetch all bookings for a guest from SQL Server"""
    try:
        # fallback safe query for university schema (if dbo.booking exists)
        sql_cursor.execute("""
            SELECT TOP 0 1
            FROM INFORMATION_SCHEMA.TABLES
            WHERE TABLE_NAME = 'booking'
        """)
        has_booking = sql_cursor.fetchone() is not None

        if not has_booking:
            print("⚠️ Booking table not present; skipping booking history")
            return []

        sql_cursor.execute("""
            SELECT b.booking_Id, r.room_number, r.room_type,
                   b.checkin_date, b.checkout_date, b.total_price
            FROM dbo.booking b
            JOIN dbo.room r ON b.room_Id = r.room_Id
            WHERE b.guest_Id = ?
            ORDER BY b.checkin_date DESC
        """, guest_id)

        rows = sql_cursor.fetchall()
        bookings = []

        for row in rows:
            bookings.append({
                "booking_id": row[0],
                "room_number": row[1],
                "room_type": row[2],
                "check_in": str(row[3]),
                "check_out": str(row[4]),
                "total_price": float(row[5]),
                "payment_method": None
            })

        return bookings

    except Exception as e:
        print(f"❌ Error fetching bookings: {e}")
        return []


# ============================================================
# STEP 3 — FETCH FROM MONGODB
# ============================================================

def get_preferences_from_mongo(mongo_db, guest_id):
    """Fetch guest preferences from MongoDB"""
    try:
        result = mongo_db.guest_preferences.find_one({"guest_id": guest_id})
        if result:
            return result.get("preferences", {})
        return {}
    except Exception as e:
        print(f"❌ Error fetching preferences: {e}")
        return {}


def get_reviews_from_mongo(mongo_db, guest_id):
    """Fetch all reviews written by a guest from MongoDB"""
    try:
        results = list(mongo_db.reviews.find({"guest_id": guest_id}))
        reviews = []

        for r in results:
            reviews.append({
                "room_number": r.get("room_number"),
                "rating": r.get("rating", 0),
                "comment": r.get("comment", ""),
                "date": str(r.get("date", ""))[:10]
            })

        return reviews

    except Exception as e:
        print(f"❌ Error fetching reviews: {e}")
        return []


# ============================================================
# STEP 4 — BUILD UNIFIED GUEST PROFILE
# ============================================================

def build_guest_profile(sql_cursor, mongo_db, guest_id):
    """
    Combines SQL Server data + MongoDB data
    into one unified guest profile.
    """
    print(f"\n{'=' * 55}")
    print(f"  Building Unified Profile for Guest ID: {guest_id}")
    print(f"{'=' * 55}")

    guest = get_guest_from_sql(sql_cursor, guest_id)
    bookings = get_bookings_from_sql(sql_cursor, guest_id)

    if not guest:
        return

    preferences = get_preferences_from_mongo(mongo_db, guest_id)
    reviews = get_reviews_from_mongo(mongo_db, guest_id)

    print(f"\n👤 GUEST DETAILS (from SQL Server)")
    print(f"   Name  : {guest['first_name']} {guest['last_name']}")
    print(f"   Email : {guest['email']}")
    print(f"   Phone : {guest['phone']}")

    print(f"\n🛎️ PREFERENCES (from MongoDB)")
    if preferences:
        for key, val in preferences.items():
            print(f"   {key.replace('_', ' ').title():<20}: {val}")
    else:
        print("   No preferences recorded.")

    print(f"\n📅 BOOKING HISTORY (from SQL Server)")
    if bookings:
        for b in bookings:
            print(
                f"   Booking #{b['booking_id']} | "
                f"Room {b['room_number']} ({b['room_type']}) | "
                f"{b['check_in']} → {b['check_out']} | "
                f"£{b['total_price']:.2f} | {b['payment_method']}"
            )
    else:
        print("   No bookings found.")

    print(f"\n⭐ REVIEWS WRITTEN (from MongoDB)")
    if reviews:
        for r in reviews:
            stars = "⭐" * int(r["rating"])
            print(
                f"   Room {r['room_number']} | "
                f"{stars} ({r['rating']}/5) | "
                f"{r['comment']} | {r['date']}"
            )
    else:
        print("   No reviews written.")

    print(f"\n{'=' * 55}")
    print("  Profile Complete!")
    print(f"{'=' * 55}\n")


# ============================================================
# STEP 5 — OPTIONAL CHART
# ============================================================

def plot_ratings_chart(mongo_db):
    """Generate and save ratings chart without opening GUI"""
    try:
        reviews = list(mongo_db.reviews.find({}, {"room_number": 1, "rating": 1, "_id": 0}))

        if not reviews:
            print("⚠️ No reviews found. Chart not created.")
            return

        room_numbers = [str(r.get("room_number", "Unknown")) for r in reviews]
        ratings = [float(r.get("rating", 0)) for r in reviews]

        plt.figure(figsize=(10, 6))
        plt.bar(room_numbers, ratings)
        plt.xlabel("Room Number")
        plt.ylabel("Rating")
        plt.title("Hotel Room Ratings")
        plt.ylim(0, 5)
        plt.tight_layout()
        plt.savefig("ratings_chart.png", dpi=300, bbox_inches="tight")
        plt.close()

        print("✅ Chart saved as ratings_chart.png")

    except Exception as e:
        print(f"❌ Error generating ratings chart: {e}")


# ============================================================
# STEP 6 — RUN THE PIPELINE
# ============================================================

def main():
    sql_conn = None
    sql_cursor = None
    mongo_client = None

    try:
        sql_conn = connect_sql_server()
        sql_cursor = sql_conn.cursor()

        mongo_client, mongo_db = connect_mongodb()

        print("\n" + "=" * 55)
        print("  THE DELTIN HOTEL — Polyglot Pipeline Demo")
        print("=" * 55)

        build_guest_profile(sql_cursor, mongo_db, 1)
        build_guest_profile(sql_cursor, mongo_db, 2)
        build_guest_profile(sql_cursor, mongo_db, 3)

        plot_ratings_chart(mongo_db)

    finally:
        if sql_cursor:
            sql_cursor.close()
        if sql_conn:
            sql_conn.close()
        if mongo_client:
            mongo_client.close()

        print("✅ All connections closed.")


if __name__ == "__main__":
    main()