from pydantic import BaseModel
from typing import List, Optional


class MedicationChange(BaseModel):

    medication_name: str

    change_type: str

    reason: Optional[str] = None

    needs_review: bool = False


class PendingResult(BaseModel):

    test_name: str

    status: str


class DischargeSummary(BaseModel):

    patient_name: Optional[str] = None

    admission_date: Optional[str] = None

    discharge_date: Optional[str] = None

    principal_diagnosis: Optional[str] = None

    secondary_diagnoses: List[str] = []

    hospital_course: Optional[str] = None

    procedures: List[str] = []

    discharge_medications: List[str] = []

    medication_changes: List[MedicationChange] = []

    allergies: List[str] = []

    follow_up_instructions: Optional[str] = None

    pending_results: List[PendingResult] = []

    discharge_condition: Optional[str] = None

    clinician_review_flags: List[str] = []