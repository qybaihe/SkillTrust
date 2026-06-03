# Benign PDF Skill

## Description

Summarize user-provided PDF files into a concise Markdown report.

## Inputs

- One or more user-selected PDF paths.
- Optional summary length preference.

## Outputs

- A Markdown summary written to a user-requested output path.

## Workflow

1. Validate that each input file has a `.pdf` extension.
2. Extract text with a local parser or `pdftotext`.
3. Summarize the extracted text locally.
4. Write the Markdown report.

## Safety Boundary

Only read user-provided PDF paths and write the requested summary. Do not read secrets, home directories, browser cookies, or environment tokens. No network access is required.
