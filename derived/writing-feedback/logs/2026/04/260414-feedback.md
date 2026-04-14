# Writing Feedback

Source: `resources/raws/logs/2026/04/260414.tex`

## Overview

This entry has strong research-log value because it records concrete workflow issues, reading progress, and mathematical connections that came up during the day. The main writing problems are article usage, tense consistency, awkward verb phrases, and several sentences that pack too many ideas together. Since this is a math research log, the revision should keep the exploratory tone while making the chronology, references, and technical observations easier to follow.

## Grammar Corrections

<div align="left"><strong>Original</strong></div>

<div align="left">The automation works with unchecked **arxiv review file** generated yesterday.</div>

<div align="left"><strong>Polished</strong></div>

<div align="left">The automation works with **the unchecked arXiv review file** generated yesterday.</div>

> **Reason**
> The noun phrase needs an article, and "arXiv" should keep its standard capitalization.

<br>
<br>

<div align="left"><strong>Original</strong></div>

<div align="left">Open VScode and checkout the branch for the corresponding branch, then VScode will open **new repository**.</div>

<div align="left"><strong>Polished</strong></div>

<div align="left">Open VS Code and check out the corresponding branch, then VS Code will open **the new repository**.</div>

> **Reason**
> Fix capitalization, use the verb form "check out," remove repetition, and add the article needed before "new repository."

<br>
<br>

<div align="left"><strong>Original</strong></div>

<div align="left">Using the **opend** editor, the user(I) checked generated review file, and then, ask codex to merge the branch and remove the worktree after committing.</div>

<div align="left"><strong>Polished</strong></div>

<div align="left">Using the **opened** editor, **I** checked the generated review file and then **asked Codex** to merge the branch and remove the worktree after committing.</div>

> **Reason**
> Correct the spelling of "opened," make the subject natural, add the missing article, and keep the verb tense consistent in a past-tense narrative.

<br>
<br>

<div align="left"><strong>Original</strong></div>

<div align="left">It was first written in 2023, but it was updated in 2026. There are familiar names in **the author list**.</div>

<div align="left"><strong>Polished</strong></div>

<div align="left">It was first written in 2023, but it was updated in 2026. There are familiar names in **the list of authors**.</div>

> **Reason**
> "The list of authors" sounds more natural than "the author list" in this context.

<br>
<br>

<div align="left"><strong>Original</strong></div>

<div align="left">By writing the review paper, I spent time **for adapting** 'margin cite' style of McPhail-Snyder's paper.</div>

<div align="left"><strong>Polished</strong></div>

<div align="left">While writing the review paper, I spent time **adapting the** 'margin cite' style of McPhail-Snyder's paper.</div>

> **Reason**
> "Spent time adapting" is the natural verb pattern here, and "while writing" fits the intended time relation better.

<br>
<br>

<div align="left"><strong>Original</strong></div>

<div align="left">However, he uses his custom .cls class for this function, and **that I give-up** to implement it since I didn't want to make my writing system more complicated.</div>

<div align="left"><strong>Polished</strong></div>

<div align="left">However, he uses his own custom `.cls` file for this function, and **I gave up trying** to implement it because I did not want to make my writing system more complicated.</div>

> **Reason**
> "That I give-up" is ungrammatical here. "I gave up trying to implement it" expresses the idea clearly and idiomatically.

<br>
<br>

<div align="left"><strong>Original</strong></div>

<div align="left">Then, I realized that we should review from the recent one to the past one since the newer paper contains information of older ones.</div>

<div align="left"><strong>Polished</strong></div>

<div align="left">Then I realized that we should review the papers from the most recent one to the oldest one, since the newer papers contain information **about** the older ones.</div>

> **Reason**
> This revision makes the comparison structure clearer and uses the correct preposition in "information about."

<br>
<br>

<div align="left"><strong>Original</strong></div>

<div align="left">As I reviewed that paper, now I can understand that it is a relation between the double cross product which results in a bialgebra, and the cross product which results in an just algebra.</div>

<div align="left"><strong>Polished</strong></div>

<div align="left">As I reviewed that paper, I came to understand that it describes a relation between the double cross product, which yields a bialgebra, and the cross product, which yields **just** an algebra.</div>

> **Reason**
> The original sentence mixes time frames and has awkward wording. The revision clarifies the claim and fixes the article in "just an algebra."

<br>
<br>

## Style and English Feedback

- The entry becomes clearer when each paragraph focuses on one purpose: workflow issue, reading progress, or mathematical reflection. A few paragraphs currently mix several functions.
- Imperative sentences such as "Open VS Code and check out the branch..." read more like instructions than a diary-style record. In a daily log, past-tense narration is usually easier to follow.
- Several phrases sound slightly literal rather than idiomatic, especially "spent time for adapting," "review from the recent one to the past one," and "results in an just algebra." Simpler verb patterns make the prose more natural.
- When a sentence contains both bibliographic context and a mathematical idea, splitting it into two sentences usually improves readability.
- You use references well, but the surrounding prose should state more explicitly whether a sentence is reporting the paper's content, your own interpretation, or a question that arose while reading.

## Mathematical Writing Feedback

- The passage about the Heisenberg double and the Drinfel'd double has interesting mathematical content, but the logical status of each statement is not fully separated. It would help to distinguish: "this idea came to mind," "Kashaev investigates X," and "my current understanding is Y."
- In "which seems like the coproduct," the referent of "which" is unclear. It is hard to tell whether you mean the homomorphism, one of the doubles, or the overall relation.
- The phrase "the other quantum invariants constructed via ideal triangulation" would be easier to follow if you named the invariants or at least specified whether you mean a class of state-sum invariants or a particular construction.
- "Used decorations are eigenvalues of peripheral subgroups" is mathematically suggestive but compressed. Expanding it into a full sentence would make the relation to the $A$-polynomial setting much clearer.
- For research logs, it is useful to mark uncertain interpretations explicitly with phrases like "my current reading is" or "it seems that," especially when summarizing a paper's conceptual structure.

## Polished Revision

```tex
\documentclass[11pt]{amsart}

\usepackage{amsmath, amssymb, amsthm}
\usepackage{mathtools}
\usepackage{thmtools}
\usepackage{enumitem}
\usepackage{tikz-cd}
\usepackage{hyperref}
\usepackage[nameinlink]{cleveref}

% % Theorem environments
\declaretheorem[numberwithin=section]{theorem}
\declaretheorem[style=plain, sibling=theorem]{lemma, proposition, corollary}
\declaretheorem[style=definition]{definition, example, condition}
\declaretheorem[style=remark]{remark, note, observation, todo}


\title{April 14, 2026}


\begin{document}
\maketitle

After my daily exercise, I checked the result of the automation for the skill \texttt{arXiv-review-routine}. The automation works with the unchecked arXiv review file generated the previous day. The problem was that checking boxes in the VS Code preview does not modify the original file, so none of the checkboxes were actually recorded.

\par\vspace{1em}
We tried to set up a daily workflow with \texttt{arXiv-review-routine}. Currently, Codex performs the skill at a fixed time (12:00 PM) by creating a new worktree. I opened VS Code, checked out the corresponding branch, and then worked in the newly opened repository. Using that editor, I checked the generated review file and then asked Codex to merge the branch and remove the worktree after committing.

Additionally, we modified the format of the review file and the folder structure.

\par\vspace{1em}

While checking the updated papers on arXiv, we found a paper dealing with Reidemeister torsion: \cite{Benard-Tange-Tran-Ueki-2026-nonacyclic_L_functions_Whiteheadlink}. It was first written in 2023, but it was updated in 2026. There are familiar names in the list of authors.

\par\vspace{1em}

We started reading the introductions of eight papers written by McPhail--Snyder. While writing the review paper, I spent time adapting the `margin cite' style from one of McPhail--Snyder's papers. However, he uses his own custom \texttt{.cls} file for that feature, and I gave up trying to implement it because I did not want to make my writing system more complicated.

First, I read \cite{McPhailSnyder_Miller-2020-planar_diagrams}, which attempts to generalize the Reshetikhin--Turaev invariant to \textit{virtual graphs}, which seem to be equivalence classes of ribbon graphs on a surface. Then I realized that we should review the papers from the most recent one to the oldest one, since the newer papers contain information about the older ones.

While reading the part of the paper that describes the relation between the quantum invariant constructed there and other quantum invariants constructed via ideal triangulations, I started thinking about the relation between the Heisenberg double and the Drinfel'd double. This was investigated by Kashaev in \cite{Kashaev-1996-Heisenberg_double}. After reviewing that paper, my current understanding is that the relation is between the double cross product, which yields a bialgebra, and the cross product, which yields just an algebra. In other words, Kashaev claimed that there is an algebra homomorphism between the two doubles that seems to play the role of the coproduct.

\par \vspace{1em}
Continuing through the first two sections of \cite{McPhailSnyder_Miller-2020-planar_diagrams}, I saw that the authors treat TQFT invariants as holomorphic sections of line or vector bundles over the \textit{decorated} representation variety. The decorations used are eigenvalues of peripheral subgroups, so this seems highly related to the setting of $A$-polynomials.


\bibliographystyle{amsalpha}
% \nocite{*}
\bibliography{bibliography}
\end{document}
```

## Next-Time Checklist

- Keep daily-log narration in the past tense unless you are describing a tool's general behavior.
- Split long research sentences into "paper summary," "my interpretation," and "next thought" when those are different moves.
- Use explicit articles in technical noun phrases such as "the unchecked file" or "the corresponding branch."
- Mark tentative mathematical interpretations with phrases like "my current understanding is."
- When describing workflow problems, write the observed behavior first and the inferred cause second.
