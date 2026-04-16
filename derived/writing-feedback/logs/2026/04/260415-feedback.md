# Writing Feedback

Source: `resources/raws/logs/2026/04/260415.tex`

## Overview

This entry works well as a math research log because it records both the day's workflow problems and your current understanding of the bundle-theoretic viewpoint in the paper. The main English issues are article usage, awkward verb patterns, spelling, and a few sentences that mix several ideas at once. In the mathematical part, the biggest improvements come from keeping notation consistent and marking more clearly when you are stating your own interpretation rather than a fully settled claim.

## Grammar Corrections

<div align="left"><strong>Original</strong></div>

<div align="left">After daily exercise and recording **playing drum**, we checked the feedback file for the yesterday diary.</div>

<div align="left"><strong>Polished</strong></div>

<div align="left">After **my daily exercise and drum practice**, we checked the feedback file for yesterday's diary.</div>

> **Reason**
> "Playing drum" is not idiomatic in English. The revised phrase sounds natural and also fixes the article in "the yesterday diary."

<br>
<br>

<div align="left"><strong>Original</strong></div>

<div align="left">The main feedback was **as following**:</div>

<div align="left"><strong>Polished</strong></div>

<div align="left">The main feedback was **as follows**:</div>

> **Reason**
> The fixed expression is "as follows," not "as following."

<br>
<br>

<div align="left"><strong>Original</strong></div>

<div align="left">As there was a DNS error again, we decided to fix **this problem**.</div>

<div align="left"><strong>Polished</strong></div>

<div align="left">Because there was another DNS error, we decided to fix **the problem**.</div>

> **Reason**
> "Another DNS error" is more natural than "a DNS error again," and "the problem" refers back to the issue already under discussion.

<br>
<br>

<div align="left"><strong>Original</strong></div>

<div align="left">The cause of DNS failure was that a sandbox executing Codex's automation was not allowed for **networ access**.</div>

<div align="left"><strong>Polished</strong></div>

<div align="left">The cause of **the DNS failure** was that the sandbox running Codex's automation was not allowed **network access**.</div>

> **Reason**
> This fixes the spelling error, adds the needed article, and uses a more natural verb phrase than "executing Codex's automation."

<br>
<br>

<div align="left"><strong>Original</strong></div>

<div align="left">What's **dissapointing** was that we spent too much time on debugging.</div>

<div align="left"><strong>Polished</strong></div>

<div align="left">What was **disappointing** was that we spent too much time debugging.</div>

> **Reason**
> The spelling should be "disappointing," and "spent too much time debugging" is the natural English pattern.

<br>
<br>

<div align="left"><strong>Original</strong></div>

<div align="left">We wondered for figuring out what is **real problem**, and how to fix it.</div>

<div align="left"><strong>Polished</strong></div>

<div align="left">We spent time trying to figure out what **the real problem** was and how to fix it.</div>

> **Reason**
> "Wondered for figuring out" is not idiomatic. The revision expresses the intended meaning clearly and fixes the missing article.

<br>
<br>

<div align="left"><strong>Original</strong></div>

<div align="left">After having **break by chatting with other PostDoc in our university**, we continued to reading McPhail-Snyder's paper from the second section.</div>

<div align="left"><strong>Polished</strong></div>

<div align="left">After **taking a break and chatting with another postdoc at our university**, we continued reading McPhail--Snyder's paper from the second section.</div>

> **Reason**
> The original phrase is ungrammatical and too literal. The revision uses natural English and fixes "continued to reading" to "continued reading."

<br>
<br>

<div align="left"><strong>Original</strong></div>

<div align="left">The author **persuade readers** that, the quantum invariant constructed in his paper is a vector bundle, and that it seems like the quantization of the CS invariant.</div>

<div align="left"><strong>Polished</strong></div>

<div align="left">The author **persuades the reader** that the quantum invariant constructed in his paper is a vector bundle, and that it seems to be a quantization of the CS invariant.</div>

> **Reason**
> This fixes subject-verb agreement, removes the unnecessary comma, and makes the final clause more idiomatic.

<br>
<br>

## Style and English Feedback

- The first half of the entry reads best when each paragraph has one job: feedback summary, automation/debugging story, or paper-reading progress. A few sentences currently combine diagnosis, frustration, and process details too tightly.
- You alternate between `we` and `I`. That can work in a diary, but it is better to do it deliberately. Use `I` for your own reactions and interpretations, and `we` only when you mean a joint workflow with Codex or another person.
- Several phrases sound translated rather than idiomatic, such as "recording playing drum," "wondered for figuring out," and "after having break." Simpler verb patterns usually improve the prose immediately.
- The sentence about the paper's viewpoint is carrying too much at once: classical Chern--Simons, line bundle, quantum invariant, vector bundle, and quantization. Splitting that into two sentences makes the exposition easier to scan.
- When you describe technical understanding in a log, phrases like "my current understanding is" or "one way to view this is" help the reader distinguish settled statements from working interpretations.

## Mathematical Writing Feedback

- The notation should stay consistent. You introduce `\mathcal{M}` and `\mathcal{X}`, but the diagram and later sentences switch to `M` and `X`. In a mathematical explanation, that makes it look as if new spaces have appeared.
- The sentence "one might regard a section of this bundle as a functional on `\mathcal{M}`" is reasonable, but it becomes clearer if you say explicitly that a section of the trivial bundle is identified with a function on `\mathcal{M}`.
- In the quotient-bundle paragraph, it helps to separate the geometric construction from the consequence for sections. Right now the explanation moves from the action, to the quotient, to the diagram, to pullback sections in one continuous block.
- "For any (holomorphic) section ... then we have" is grammatically awkward and mathematically compressed. It is better to say directly that any section of the quotient bundle pulls back to a function on `\mathcal{M}` satisfying the equivariance condition.
- Since this is a research log, it is good to keep the interpretation modest. The revised version preserves that tone by presenting the quasi-periodicity relation as part of your current understanding rather than as a finalized exposition.

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


\title{April 15, 2026}


\begin{document}
\maketitle

After my daily exercise and drum practice, we checked the feedback file for yesterday's diary.
The main feedback was as follows:
\begin{itemize}
    \item article usage,
    \item tense consistency,
    \item using simpler verb phrases,
    \item separating bibliographic context from the mathematical idea,
    \item making the surrounding sentences clearer,
    \item using ``my understanding is'' for tentative mathematical interpretations.
\end{itemize}

\par\vspace{1em}
After lunch, we tested the skill \texttt{arXiv-review-routine}.
Because there was another DNS error, we decided to fix the problem.
The cause of the DNS failure was that the sandbox running Codex's automation was not allowed network access.
What was disappointing was that we spent too much time debugging.
We spent time trying to figure out what the real problem was and how to fix it.
Even though I only gave an order to Codex, time was still consumed while waiting for its report.

\par\vspace{1em}
After taking a break and chatting with another postdoc at our university, we continued reading McPhail--Snyder's paper from the second section.
This section focuses on the viewpoint that the classical Chern--Simons invariant can be seen as a line bundle.
The author persuades the reader that the quantum invariant constructed in his paper is a vector bundle, and that it seems to be a quantization of the Chern--Simons invariant.
Here I record my current understanding.

\par\vspace{1em}

Let $\mathcal{M} := \mathbb{C}^2$, which is the universal cover of $\mathcal{X} := (\mathbb{C}^{\times})^2$, with projection given by the exponential map.
Consider the trivial bundle $\mathcal{M} \times \mathbb{C}$.
Since this bundle is trivial, a section can be identified with a function on $\mathcal{M}$.
If the action of $\mathbb{Z}^2 \cong \pi_1(\mathcal{X})$ on $\mathcal{M}$ extends to an action on the total space $\mathcal{M} \times \mathbb{C}$, then we obtain a quotient bundle
\[
    (\mathcal{M} \times \mathbb{C})/\mathbb{Z}^2 \to \mathcal{X}.
\]
In other words, we have the following commutative diagram:
\[
    \begin{tikzcd}
    \mathcal{M} \times \mathbb{C} \arrow[r, two heads] \arrow[d, two heads]
    & (\mathcal{M} \times \mathbb{C})/\mathbb{Z}^2 \arrow[d] \\
    \mathcal{M} \arrow[r, two heads]
    & \mathcal{X}
    \end{tikzcd}
\]
and we may regard $\mathcal{M} \times \mathbb{C}$ as the pullback of the quotient bundle.

Any (holomorphic) section of $(\mathcal{M} \times \mathbb{C})/\mathbb{Z}^2$ pulls back to a (holomorphic) section of $\mathcal{M} \times \mathbb{C}$.
Equivalently, it pulls back to a function on $\mathcal{M}$ satisfying the restriction induced by the $\mathbb{Z}^2$-action.

In particular, the action considered in the reference is
\[
    (a,b) \cdot (x, y, z) = (x+a, y+b, e^{2\pi i(bx - ay)} z),
\]
so the corresponding section $f$ satisfies
\[
    f(x+a, y+b) = e^{2\pi i(bx - ay)} f(x,y),
\]
which is called the \emph{quasi-periodicity relation}.



\bibliographystyle{amsalpha}
% \nocite{*}
\bibliography{bibliography}
\end{document}
```

## Next-Time Checklist

- Use idiomatic verb patterns such as "spent time debugging" and "continued reading."
- Keep `I` and `we` distinct so the reader can tell whether a sentence reports your own reflection or a joint workflow.
- When summarizing a paper, split conceptual background from your own interpretation into separate sentences.
- Keep notation consistent once a symbol such as `\mathcal{M}` or `\mathcal{X}` has been introduced.
- In math logs, state explicitly when a sentence is your current understanding rather than a settled formal claim.
