import os
import sys
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

# Add the backend root directory to the python path so we can import 'app'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from app.db.session import engine, SessionLocal
from app.db.base_class import Base
from app import models

# Real Odisha district coordinates
ODISHA_DISTRICTS = [
    {"name": "Koraput", "level": "district", "lat": 18.8135, "lon": 82.7123},
    {"name": "Gajapati", "level": "district", "lat": 19.2167, "lon": 84.1333},
    {"name": "Kandhamal", "level": "district", "lat": 20.4681, "lon": 84.2441},
    {"name": "Mayurbhanj", "level": "district", "lat": 21.9375, "lon": 86.7333},
    {"name": "Puri", "level": "district", "lat": 19.8135, "lon": 85.8312},
    {"name": "Cuttack", "level": "district", "lat": 20.4625, "lon": 85.8828},
    {"name": "Sambalpur", "level": "district", "lat": 21.4669, "lon": 83.9812},
    {"name": "Bhubaneswar", "level": "district", "lat": 20.2961, "lon": 85.8245},
]


def seed_db():
    print("Resetting and seeding database with Odisha data...")

    # Drop and recreate all tables
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    # ── 1. Seed AdminUnits (Odisha districts) ──
    admin_units = {}
    for d in ODISHA_DISTRICTS:
        au = models.AdminUnit(name=d["name"], level=d["level"], lat=d["lat"], lon=d["lon"])
        db.add(au)
        db.commit()
        db.refresh(au)
        admin_units[d["name"]] = au
    print(f"  [OK] Seeded {len(admin_units)} admin units")

    # ── 2. Seed Assets + AccountabilityRecords ──
    projects = [
        {
            "name": "New School Building",
            "type": "Education",
            "district": "Koraput",
            "lat": 18.8200, "lon": 82.7200,
            "source_system": "IIG",
            "contractor": "Bansal Builders",
            "sanctioned_cost": 45000000.0,
            "actual_cost": 42000000.0,
            "planned_completion": datetime(2025, 12, 31),
            "actual_completion": None,
            "official": "District Education Officer",
            "department": "School & Mass Education",
        },
        {
            "name": "Rural Road Construction",
            "type": "Road",
            "district": "Gajapati",
            "lat": 19.2200, "lon": 84.1400,
            "source_system": "PMGSY",
            "contractor": "Shree Infra Pvt. Ltd.",
            "sanctioned_cost": 24000000.0,
            "actual_cost": 24000000.0,
            "planned_completion": datetime(2024, 12, 31),
            "actual_completion": datetime(2024, 12, 15),
            "official": "Block Development Officer",
            "department": "Rural Development",
        },
        {
            "name": "PHC Upgradation",
            "type": "Health",
            "district": "Kandhamal",
            "lat": 20.4700, "lon": 84.2500,
            "source_system": "IIG",
            "contractor": "Odisha Buildcon Ltd.",
            "sanctioned_cost": 38000000.0,
            "actual_cost": 35000000.0,
            "planned_completion": datetime(2025, 2, 28),
            "actual_completion": None,
            "official": "District Medical Officer",
            "department": "Health & Family Welfare",
        },
        {
            "name": "Water Supply Project",
            "type": "Water",
            "district": "Mayurbhanj",
            "lat": 21.9400, "lon": 86.7400,
            "source_system": "IIG",
            "contractor": "Jai Maa Construction",
            "sanctioned_cost": 12000000.0,
            "actual_cost": 14500000.0,
            "planned_completion": datetime(2025, 5, 31),
            "actual_completion": None,
            "official": "Executive Engineer, RWSS",
            "department": "Water Resources",
        },
        {
            "name": "Street Light Installation",
            "type": "Electricity",
            "district": "Puri",
            "lat": 19.8100, "lon": 85.8300,
            "source_system": "eSAKSHI",
            "contractor": "Bright Power Solutions",
            "sanctioned_cost": 5500000.0,
            "actual_cost": 5200000.0,
            "planned_completion": datetime(2024, 9, 30),
            "actual_completion": datetime(2024, 10, 15),
            "official": "Municipal Engineer",
            "department": "Urban Local Body",
        },
        {
            "name": "Community Drain Construction",
            "type": "Sanitation",
            "district": "Cuttack",
            "lat": 20.4600, "lon": 85.8800,
            "source_system": "PMGSY",
            "contractor": "Clean City Infra",
            "sanctioned_cost": 8500000.0,
            "actual_cost": None,
            "planned_completion": datetime(2025, 8, 31),
            "actual_completion": None,
            "official": "Executive Engineer, PHD",
            "department": "Housing & Urban Development",
        },
        {
            "name": "Bridge Repair on NH-55",
            "type": "Road",
            "district": "Sambalpur",
            "lat": 21.4700, "lon": 83.9800,
            "source_system": "IIG",
            "contractor": "National Highways Builders",
            "sanctioned_cost": 95000000.0,
            "actual_cost": 110000000.0,
            "planned_completion": datetime(2025, 3, 31),
            "actual_completion": None,
            "official": "Superintending Engineer, NHAI",
            "department": "Works Department",
        },
    ]

    assets_by_name = {}
    for proj in projects:
        asset = models.Asset(
            name=proj["name"],
            type=proj["type"],
            lat=proj["lat"],
            lon=proj["lon"],
            admin_unit_id=admin_units[proj["district"]].id,
            source_system=proj["source_system"],
        )
        db.add(asset)
        db.commit()
        db.refresh(asset)
        assets_by_name[proj["name"]] = asset

        record = models.AccountabilityRecord(
            asset_id=asset.id,
            contractor_name=proj["contractor"],
            sanctioned_cost=proj["sanctioned_cost"],
            actual_cost=proj["actual_cost"],
            planned_completion_date=proj["planned_completion"],
            actual_completion_date=proj["actual_completion"],
            responsible_official=proj["official"],
            department=proj["department"],
        )
        db.add(record)

    db.commit()
    print(f"  [OK] Seeded {len(projects)} assets + accountability records")

    # ── 3. Seed sample Consent + Feedback ──
    feedbacks_data = [
        {
            "category": "Road",
            "description": "Pothole on main road near bus stand causing accidents daily. Two wheelers have fallen multiple times.",
            "language": "en",
            "district": "Puri",
            "lat": 19.8100, "lon": 85.8350,
            "status": "new",
        },
        {
            "category": "Water",
            "description": "Handpump broken for 3 weeks. No drinking water for 50 families. Please repair urgently.",
            "language": "en",
            "district": "Cuttack",
            "lat": 20.4650, "lon": 85.8850,
            "status": "new",
        },
        {
            "category": "Sanitation",
            "description": "Severe water logging on main street after every rain. Drainage is completely blocked.",
            "language": "en",
            "district": "Bhubaneswar",
            "lat": 20.2950, "lon": 85.8200,
            "status": "triaged",
        },
        {
            "category": "Electricity",
            "description": "Street light not working on NH road for past 2 months. Very dangerous at night.",
            "language": "en",
            "district": "Sambalpur",
            "lat": 21.4680, "lon": 83.9850,
            "status": "new",
        },
        {
            "category": "Road",
            "description": "Bridge railing broken on village bridge. Children walk to school over it. Very unsafe.",
            "language": "en",
            "district": "Koraput",
            "lat": 18.8150, "lon": 82.7100,
            "status": "in_progress",
        },
        {
            "category": "Health",
            "description": "PHC has no doctor since last month. Nearest hospital 40 km away. Pregnant women suffering.",
            "language": "en",
            "district": "Kandhamal",
            "lat": 20.4690, "lon": 84.2450,
            "status": "new",
        },
        {
            "category": "Education",
            "description": "School roof leaking badly during monsoon. Students sitting in water. No fans working.",
            "language": "en",
            "district": "Gajapati",
            "lat": 19.2180, "lon": 84.1350,
            "status": "triaged",
        },
        {
            "category": "Water",
            "description": "Piped water supply project completed but water not reaching last 3 wards. Pipeline leaking.",
            "language": "en",
            "district": "Mayurbhanj",
            "lat": 21.9380, "lon": 86.7350,
            "status": "new",
        },
        {
            "category": "Road",
            "description": "Road to weekly market completely washed out in last flood. No vehicle can pass.",
            "language": "en",
            "district": "Koraput",
            "lat": 18.8180, "lon": 82.7150,
            "status": "new",
        },
        {
            "category": "Sanitation",
            "description": "Open drain overflowing near school. Children falling sick. Mosquito breeding ground.",
            "language": "en",
            "district": "Cuttack",
            "lat": 20.4610, "lon": 85.8810,
            "status": "new",
        },
    ]

    for i, fb_data in enumerate(feedbacks_data):
        # Create consent first (as per consent-flow.md)
        import hashlib, uuid
        unique_string = f"citizen-feedback-web-{uuid.uuid4()}"
        consent = models.Consent(
            purpose="citizen-feedback",
            language=fb_data["language"],
            channel="web",
            timestamp=datetime.utcnow() - timedelta(hours=i * 2),
            consent_hash=hashlib.sha256(unique_string.encode()).hexdigest(),
        )
        db.add(consent)
        db.commit()
        db.refresh(consent)

        fb = models.Feedback(
            consent_id=consent.id,
            category=fb_data["category"],
            description_text=fb_data["description"],
            language=fb_data["language"],
            lat=fb_data["lat"],
            lon=fb_data["lon"],
            admin_unit_id=admin_units.get(fb_data["district"], admin_units["Puri"]).id,
            status=fb_data["status"],
            media_urls=[],
            created_at=datetime.utcnow() - timedelta(hours=i * 2),
        )
        db.add(fb)

    db.commit()
    print(f"  [OK] Seeded {len(feedbacks_data)} consent + feedback records")

    db.close()
    print("Database seeding completed successfully!")


if __name__ == "__main__":
    seed_db()
