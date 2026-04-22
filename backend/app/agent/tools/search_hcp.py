from sqlalchemy.orm import Session
from app.models.hcp import HCP
from langchain_core.tools import tool


def search_hcp_by_name(name: str, db: Session) -> dict:
    hcp = db.query(HCP).filter(HCP.name.ilike(f"%{name}%")).first()
    if not hcp:
        return {"found": False, "hcp": None}
    return {
        "found": True,
        "hcp": {
            "id": hcp.id,
            "name": hcp.name,
            "specialty": hcp.specialty,
            "territory": hcp.territory,
        },
    }


def make_search_hcp_tool(db: Session):
    @tool
    def search_hcp(name: str) -> dict:
        """Search for an HCP by name. Returns HCP id and details if found."""
        return search_hcp_by_name(name, db)

    return search_hcp
