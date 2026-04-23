from app.database import SessionLocal
from app.models.hcp import HCP
from app.models.rep import Rep


def seed():
    db = SessionLocal()
    try:
        if not db.query(HCP).first():
            hcps = [
                HCP(name="Dr. Smith", specialty="Cardiology", territory="North"),
                HCP(name="Dr. Jones", specialty="Oncology", territory="South"),
                HCP(name="Dr. Patel", specialty="Neurology", territory="East"),
            ]
            db.add_all(hcps)

        if not db.query(Rep).first():
            rep = Rep(name="Alex Chen", email="alex@pharma.com", territory="North")
            db.add(rep)

        db.commit()
        print("Seed data inserted.")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
