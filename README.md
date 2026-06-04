# Discharge Summary Agent

## Objective

AI agent that extracts structured discharge summaries from scanned hospital PDFs.

## Features

- PDF text extraction
- OCR fallback for scanned documents
- Diagnosis extraction
- Hospital course extraction
- Pending lab detection
- Medication reconciliation
- Clinician review flags
- Safe agent workflow
- Retry handling

## Architecture

PDF
 ↓
 OCR
 ↓
 Section Splitter
 ↓
 Agent Workflow
 ↓
 Structured Discharge Summary

## Safety Features

- Retry mechanism
- Missing data detection
- Low confidence diagnosis flags
- Human review escalation

## Current Performance

Sample scanned discharge summary:

- Principal diagnosis extracted ✓
- Secondary diagnoses extracted ✓
- Pending labs detected ✓
- Medications extracted ✓
- Medication reconciliation ✓
- OCR fallback ✓

Known limitations:

- OCR noise may affect extraction quality
- Patient demographics not yet extracted
- Follow-up instructions may require clinician review

## Run

```bash
python test_agent.py
```