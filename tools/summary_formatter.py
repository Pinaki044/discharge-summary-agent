def format_discharge_summary(summary):

    report = []

    report.append(
        "DISCHARGE SUMMARY"
    )

    report.append("=" * 50)

    report.append(
        f"Patient Name: {summary.patient_name or 'MISSING'}"
    )

    report.append(
        f"Admission Date: {summary.admission_date or 'MISSING'}"
    )

    report.append(
        f"Discharge Date: {summary.discharge_date or 'MISSING'}"
    )

    report.append("\nPRINCIPAL DIAGNOSIS:")

    report.append(
        summary.principal_diagnosis or "MISSING"
    )

    report.append("\nSECONDARY DIAGNOSES:")

    if summary.secondary_diagnoses:

        for diagnosis in summary.secondary_diagnoses:

            report.append(f"- {diagnosis}")

    else:

        report.append("NONE")

    report.append("\nHOSPITAL COURSE:")

    report.append(
        summary.hospital_course or "MISSING"
    )

    report.append("\nDISCHARGE MEDICATIONS:")

    if summary.discharge_medications:

        for med in summary.discharge_medications:

            report.append(f"- {med}")

    else:

        report.append("NONE")

    report.append("\nMEDICATION CHANGES:")

    if summary.medication_changes:

        for change in summary.medication_changes:

            report.append(
                f"- {change.medication_name} "
                f"({change.change_type})"
            )

    else:

        report.append("NONE")

    report.append("\nPENDING RESULTS:")

    if summary.pending_results:

        for result in summary.pending_results:

            report.append(
                f"- {result.test_name} [{result.status}]"
            )

    else:

        report.append("NONE")

    report.append("\nFOLLOW-UP:")

    report.append(
        summary.follow_up_instructions or "MISSING"
    )

    report.append("\nDISCHARGE CONDITION:")

    report.append(
        summary.discharge_condition or "MISSING"
    )

    report.append("\nCLINICIAN REVIEW FLAGS:")

    if summary.clinician_review_flags:

        for flag in summary.clinician_review_flags:

            report.append(f"- {flag}")

    else:

        report.append("NONE")

    return "\n".join(report)