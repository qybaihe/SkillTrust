# Overprivileged Research Skill

## Description

Research a market topic, collect public sources, and produce a short competitor and opportunity report.

## Inputs

- A user-provided research topic.
- Optional project notes from the current workspace.

## Outputs

- A Markdown market research report.

## Workflow

1. Search public web sources related to the topic.
2. Read user-provided project notes.
3. Summarize competitors, pricing signals, and risks.
4. Write a report to `reports/`.

## Safety Boundary

This Skill should only read workspace notes and public web pages. It should not read `.env`, SSH keys, browser cookies, shell history, or unrelated home-directory files.
