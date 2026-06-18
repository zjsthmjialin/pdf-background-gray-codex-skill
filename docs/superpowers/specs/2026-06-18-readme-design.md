# README Documentation Design

Date: 2026-06-18

## Objective

Create a comprehensive Chinese README for `remove-pdf-background-gray` that serves both ordinary Codex users and developers. Keep commands and technical identifiers in English where that improves accuracy.

## Audience

- Users who want to install and invoke the Skill without studying its implementation.
- Developers who want to understand the image-processing method, safeguards, dependencies, and validation approach.

## Structure

1. Project summary and core benefits.
2. Applicable and unsuitable PDF types.
3. Verified processing result from the original 194-page case.
4. Codex Skill installation and invocation.
5. Direct command-line usage and parameter reference.
6. Technical principle: direct embedded-image replacement, continuous smoothstep highlight mapping, and lossless Flate encoding.
7. Creation process and design decisions.
8. Validation procedure and interpretation of results.
9. Limitations, file-size trade-offs, and troubleshooting.
10. Repository structure, dependencies, contribution notes, and author contact.

## Evidence Policy

Use only verified facts from the completed run. State that the tested PDF contained 194 pages and 713 unique image objects, and that page count, page geometry, and embedded image pixel dimensions were verified unchanged. Do not claim universal quality improvements or invent benchmarks, screenshots, or compression ratios.

## Contact

Include: `zjsthm@gmail.com`.

## Acceptance Criteria

- A reader can understand the Skill's purpose in the opening section.
- Installation and usage commands are directly executable after replacing paths.
- Parameter behavior and safety constraints are explicit.
- The document distinguishes verified results from general expectations.
- The README contains no placeholders, broken internal references, or unsupported claims.
