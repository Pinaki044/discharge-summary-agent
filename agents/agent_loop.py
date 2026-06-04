from schemas.discharge_schema import DischargeSummary
from tools.retry_handler import safe_execute

from agents.extractors import (
    extract_diagnoses,
    extract_hospital_course,
    extract_pending_results,
    extract_discharge_medications,
    reconcile_medications,
)


MAX_STEPS = 10


def run_agent(sections):

    summary = DischargeSummary()

    trace = []

    current_step = 1

    while current_step <= MAX_STEPS:

        # STEP 1 — Diagnoses
        if not summary.principal_diagnosis:

            trace.append({
                "step": current_step,
                "reasoning": "Need to extract diagnoses",
                "action": "extract_diagnoses"
            })

            result = safe_execute(
                extract_diagnoses,
                sections,
                summary
            )

            if result is None:

                trace.append({
                    "step": current_step,
                    "reasoning": "Diagnosis extraction failed",
                    "action": "escalate_to_clinician",
                    "result": "Manual review required"
                })

                break

            summary = result

            trace[-1]["result"] = (
                summary.principal_diagnosis
            )

            current_step += 1

            continue


        # STEP 2 — Hospital Course
        if not summary.hospital_course:

            trace.append({
                "step": current_step,
                "reasoning": "Need hospital course",
                "action": "extract_hospital_course"
            })

            result = safe_execute( 
                extract_hospital_course, 
                sections, 
                summary 
            ) 
            if result is None: 
                trace.append({ 
                    "step": current_step, 
                    "reasoning": "Hospital course extraction failed", 
                    "action": "escalate_to_clinician", 
                    "result": "Manual review required" 
                }) 
                break 
            summary = result

            trace[-1]["result"] = (
                "Hospital course extracted"
            )

            current_step += 1

            continue


        # STEP 3 — Pending Results
        if not summary.pending_results:

            trace.append({
                "step": current_step,
                "reasoning": "Need pending lab detection",
                "action": "extract_pending_results"
            })

            result = safe_execute( 
                extract_pending_results, 
                sections, 
                summary 
            ) 
            if result is None: 
                trace.append({ 
                    "step": current_step, 
                    "reasoning": "Pending result extraction failed", 
                    "action": "escalate_to_clinician", 
                    "result": "Manual review required" 
                }) 
                break 
            summary = result

            trace[-1]["result"] = (
                f"{len(summary.pending_results)} pending results found"
            )

            current_step += 1

            continue


        # STEP 4 — Medications
        if not summary.discharge_medications:

            trace.append({
                "step": current_step,
                "reasoning": "Need medication extraction",
                "action": "extract_discharge_medications"
            })

            result = safe_execute( 
                extract_discharge_medications, 
                sections, 
                summary 
            ) 
            if result is None: 
                trace.append({ 
                    "step": current_step, 
                    "reasoning": "Medication extraction failed", 
                    "action": "escalate_to_clinician", 
                    "result": "Manual review required" 
                }) 
                break 
            summary = result

            trace[-1]["result"] = (
                f"{len(summary.discharge_medications)} meds extracted"
            )

            current_step += 1

            continue


        # STEP 5 — Reconciliation
        if not summary.medication_changes:

            trace.append({
                "step": current_step,
                "reasoning": "Need medication reconciliation",
                "action": "reconcile_medications"
            })

            result = safe_execute( 
                reconcile_medications, 
                summary 
            ) 
            if result is None: 
                trace.append({ 
                    "step": current_step, 
                    "reasoning": "Medication reconciliation failed", 
                    "action": "escalate_to_clinician", 
                    "result": "Manual review required" 
                }) 
                break 
            summary = result

            trace[-1]["result"] = (
                f"{len(summary.medication_changes)} med changes flagged"
            )

            current_step += 1

            continue

        # FINAL VALIDATION
        trace.append({
            "step": current_step,
            "reasoning": "All major sections extracted",
            "action": "finalize_summary",
            "result": "Agent completed safely"
        })

        break

    return summary, trace