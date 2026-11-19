---
name: smart-delegation
description: Judge each part of a request and hand mechanical, bulky work (reading or transcribing PDFs, extraction, locating, conversion, running tests, browser click-through checks, boilerplate code) to cheaper helper models while the main model keeps the reasoning and the final answer. Includes ready-made breakdowns for common jobs: testing or auditing an app, auditing a body of content, adding items from PDFs or photos, bulk reformatting, and building documents. Use on any multi-step or multi-part request, any request involving large or many files, any request to test, check, verify or audit, and any task with a mechanical phase before a thinking phase, even when the user does not mention models, cost or delegation.
---

# Smart delegation

The goal is the lowest long-run cost without losing answer quality. Installing this skill is standing permission to delegate: do not ask before doing it, and do not explain the mechanics unless asked.

You cannot change the model you are running on. What you can do is hand a piece of work to a helper (the Agent tool) and choose its model. You stay the orchestrator: you judge the work, write the briefs, check what comes back, and write the final answer yourself.

If no helper tool exists in the session, do all the work yourself and say nothing about it. The three habits in the next section still apply.

## Where the cost actually goes

In long sessions on a top-tier model, most of the spend is re-reading, not writing: every tool call makes the main model re-read the whole conversation so far. A session with 200 test runs, searches and browser checks is expensive because of what piles up in the main conversation, even if each step is small. So three habits matter as much as the choice of model:

- **Script before model.** If a check can be a script (does this file exist, does this code parse, is every record's answer one of its options), write the script once, save it with the project, and run it. A script costs nothing to rerun; a model checking the same things item by item costs every time.
- **Loops go to helpers.** Any phase made of many tool calls with long outputs (running suites, clicking through an app, searching dozens of files, extracting many PDFs) runs in a helper, so the pile-up happens in a cheap context that is thrown away afterwards.
- **Output goes to files; only failures come back.** Send logs and reports to a file, then read the summary and the failing items. Never print a full passing test log into the main conversation.

For long jobs, keep a short progress note in the project's outputs folder (what is done, what is left, which files hold the results). Follow-ups are often just "continue", sometimes in a new session; starting from the note is far cheaper than rediscovering the project.

## Step 1: Split the request into parts

Before doing anything, list the parts of the request and label each one:

- **Mechanical**: the result can be checked against a source and needs no judgment. Transcribing, extracting, locating, listing, converting formats, renaming, running a known script, filling a fixed template, gathering sources.
- **Thinking**: the result depends on reasoning, subject knowledge, the user's preferences, or decisions with consequences. Answering questions, explaining, diagnosing a bug, designing, reviewing for correctness, writing anything the user will read as the final product.

## Step 2: Decide whether delegating actually saves money

A helper starts with no context, so every delegation has a fixed overhead (the brief, the helper's own setup, your check of its output). Delegate a mechanical part only when all three hold:

1. **It is bulky.** Roughly: more than about 10 pages, more than a few files, or more than a handful of tool calls. Below that, do it yourself; the overhead costs more than it saves.
2. **It is self-contained.** You can describe it fully in a short brief without the conversation history.
3. **You will not need to re-read all of its output.** The saving comes from you reading only an index plus the parts you need. If you would have to read every word back anyway and the source is already cheap text, there is nothing to gain.

PDFs, scans and slide decks nearly always pass this test: pages are expensive for you to read directly, and a helper can turn them into a text file you read selectively.

Keep thinking parts for yourself. The one exception is going up: if this session is running on a smaller model and a part needs deep reasoning, hand that part to a stronger model with a complete brief and relay its result faithfully.

## Step 3: Pick the cheapest tier that will do the job reliably

| Tier | Give it |
|---|---|
| Smallest (Haiku) | Locating pages or files, listing headings or items, extraction from clean text, file conversion and renaming, running test suites and checker scripts and reporting only the failures |
| Middle (Sonnet) | Word-for-word transcription of PDFs with tables, columns, figures or handwriting; structured extraction into JSON or CSV; routine or boilerplate code from a precise spec (including checker scripts); browser click-through checks; rearranging existing text into a fixed format without adding facts; proposing matches (for example recording to document) with the evidence quoted; web source gathering |
| Top (the session model) | Everything labelled thinking, all verification, and the final answer |

When unsure between two tiers for transcription or anything feeding a high-stakes answer (medical, legal, financial, exam), choose the higher one. A wrong transcription that leads to a wrong answer costs far more than the tier difference.

## Step 4: Write a brief the helper can follow cold

Every brief contains:

- The exact file paths or inputs.
- The exact task, in one or two sentences.
- **The fidelity rule** (below), stated explicitly.
- The output format and the file path to save it to.
- What to send back: a short index only (for example page ranges, item numbers, headings, and the saved file path), never the full content.

### The fidelity rule

Helpers transcribe and extract **word for word**. They never summarize, paraphrase, correct, reorder or fill in gaps, unless the user explicitly asked for a summary. Specifically:

- Keep the original wording, numbers, units, answer-choice letters and ordering exactly.
- Tag every block with its source page or slide, for example `[p. 14]`.
- Reproduce tables as tables.
- For figures and images write `[FIGURE p. 14: one-line description]` so the orchestrator knows to look at that page itself.
- Mark anything unreadable as `[UNREADABLE p. 14]` rather than guessing.

The reason: answers must match their source documents exactly. A helper's summary silently drops the details that matter, and the orchestrator cannot see what was lost.

## Step 5: Run it efficiently

- Launch independent helpers in the same turn so they run in parallel. Split a very large file into page ranges across several helpers.
- While helpers run, start on thinking parts that do not depend on them.
- Have helpers save results to files. Read the index, then open only the sections you need.

## Step 6: Check before relying on it

- Spot-check each helper's output against the source: compare one or two pages or items directly. Check more when the content feeds a high-stakes answer.
- Look at flagged figures and unreadable pages yourself.
- If the check fails, do not retry the same tier with the same brief. Either move up a tier or do that part yourself.

## Step 7: Write the final answer yourself

The final answer follows the user's own detail and format preferences, which the helpers never saw. Build it from the verified material. Do not paste helper output to the user as the answer unless the request was purely mechanical (for example "transcribe this").

End with one short line saying what was handed off and to which tier, for example: `Handed off: PDF transcription (Sonnet), page lookup (Haiku).` Skip the line if nothing was delegated.

## Breakdowns for common jobs

When a request matches one of these, use its breakdown instead of planning from scratch. Match on intent, not wording: "test it", "make sure everything is set up correctly" and "continue" all count. Adapt the details to the project; if the project keeps its own notes or map of conventions, those win.

General rules for work on a user's project:

- Change it through small, reversible steps, after a backup of what is touched.
- Never test against the user's live data. Use a separate copy.
- Check free disk space before making backups or test copies, and delete your own test files when done.
- Write a short report of what was checked and changed to the project's outputs folder.

### "Test the app" / "check for broken links or code" / "make sure everything works"

Scripted checks are nearly free, so they always cover the whole project. Browser checks and anything you read yourself cover what changed since the last audit, unless the user says everything.

1. **You, briefly:** find the last audit report and what changed since (modification times). Write the two briefs below. Launch both helpers in the same turn.
2. **Haiku helper, scripted checks on everything.** Runs the test suites plus a static checker saved in the project's tests folder. The checker verifies whatever can be verified mechanically, for example: every script and stylesheet the entry page names exists and parses; every local file the data points to exists on disk; every internal reference resolves; every record has a unique id and its required fields. It writes a report file and returns counts plus the first 20 failures per category. If the checker does not exist yet, a Sonnet helper writes it once and saves it there.
3. **Sonnet helper, browser smoke run.** On the test copy, at desktop and phone width: open every main view and one item of each kind. Collect console errors, failed requests, buttons that do nothing and sideways overflow. Return failures only, each with steps to reproduce and a screenshot path.
4. **Outside links** are checked by script for a response. A link behind a sign-in is reported as could not verify, not as broken.
5. **You:** read the two failure reports and nothing else. Group failures by root cause, diagnose, fix, then have a helper rerun only the failed checks plus the suites.
6. **Tell the user:** how much was checked, what was broken, what you fixed, and what needs their decision.

### Auditing a body of content for correctness

Judging correctness stays with you; a missed error costs more than any saving. The saving comes from scope and from compact input.

1. **Haiku helper:** dump the content to plain text with ids kept and markup stripped, and extract the source documents to page-tagged text. Reuse an existing extraction if one is already saved.
2. **Script:** format checks (required parts present, truncated labels, duplicates, spelling conventions).
3. **You:** read only items that are new or changed since the last audit, recorded in an audit log in the outputs folder. On a first audit, read everything. When a claim needs checking, read that source page from the extracted text.
4. Fixes go in one change; a helper runs the suites; you log what was audited.

### Adding items from PDFs, photos or other documents

1. **Sonnet helpers, in parallel by page range:** transcribe word for word under the fidelity rule. A script then removes duplicates across overlapping sources and lists conflicts.
2. **You:** do the part that needs judgment (for example solving each question independently instead of trusting a printed key, and writing explanations in the project's established format, read from its format spec rather than from memory). For large sets, write in batches saved to files so progress survives the session.
3. **Sonnet helper:** convert to the project's data format and wire it in. **Haiku helper:** run the suites.
4. **You:** compare about 1 in 10 against the source, and look at every figure.

### Bulk reformatting and linking

- Rearranging what is already written, with no new claims, goes to Sonnet helpers in parallel batches. The brief says: add no facts; where a part has nothing to draw on, write `[NEEDS CONTENT]`. You write those parts yourself and compare about 1 in 20 per batch against the original.
- For matching one set of things to another, score by script first. A Sonnet helper proposes matches with the evidence quoted and a confidence. You review only the low-confidence ones.

### Building documents from source material

1. **Sonnet helper:** transcribe the sources, page-tagged. Check for a saved transcript first; the same source often feeds several documents.
2. **You:** write the content to the user's format spec, if one is saved.
3. **Sonnet helper:** build the file with the project's existing build script, render the pages to images, check for missing-glyph boxes and overflow, and return the page count and any problems. You look at two pages yourself.

### Small scripts and tools

You design and write the logic and deliver the complete file every time, never a partial snippet. A helper runs the test harness and returns only failures. A small fix is not worth a helper.

### Not worth delegating

Settings and quick system tasks, single questions, short explanations, and anything under about 10 tool calls. Do these yourself.

## Examples

**"Read this 120-slide PDF and answer these 15 questions in my usual format."**
Sonnet helpers transcribe the deck word for word into a page-tagged text file (split into ranges, in parallel) and return a heading index. You read the sections each question needs, view any flagged figures yourself, and write all 15 answers.

**"Add the items from this document to my app and fix the scoring bug."**
A Sonnet helper converts the document word for word into the app's data format and saves it. You diagnose and fix the bug yourself, spot-check the converted items against the document, and review the content for correctness before adding it.

**"Which of these 30 files mention heparin?"**
A Haiku helper searches and returns the file names with page numbers. You report the list.

**"Read this 3-page handout and explain the mechanism."**
Too small to delegate. Do it all yourself.

**"Rename these 5 files and tell me what you think of my plan."**
Both parts are small. Do it all yourself.
