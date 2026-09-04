from fastapi import APIRouter, Request, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Any

from database import SessionLocal
from rule_checks import run_owasp_checks, find_phi_fields

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class DeviceSubmission(BaseModel):
    name: str
    api_spec: dict[str, Any]


@router.post("/scans/audit")
async def run_audit(submission: DeviceSubmission, request: Request):
    user_id = request.session.get("user_id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Not logged in")

    owasp_findings = run_owasp_checks(submission.api_spec)
    phi_findings = find_phi_fields(submission.api_spec.get("sample_response", {}))

    return {
        "device_name": submission.name,
        "owasp_findings": owasp_findings,
        "phi_findings": phi_findings,
        "total_findings": len(owasp_findings) + len(phi_findings),
    }