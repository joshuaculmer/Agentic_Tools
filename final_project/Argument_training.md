# Reasoning Improvement Tool — Design Document

*Status: Pre-architecture design phase*

---

## 1. Product Direction

### What This Is

A personal reasoning improvement tool. The primary use case is **personal belief examination** — helping users articulate not just what they believe, but why. The tool surfaces the structure of a user's reasoning, identifies unexamined assumptions, spots weak inferences, and introduces genuine counterarguments.

This is not a formal logic checker, a debate trainer, or an academic argument mapper. Those products exist. This is closer to a Socratic interlocutor: an AI that asks "what's your evidence for that?" without judgment, but with genuine intellectual pressure.

### What Success Looks Like

A successful session leaves the user with something concrete they didn't have when they arrived: a clearer articulation of their position, a gap they can now see, an assumption they've named, or a counterargument they've actually engaged with. Not all of those — one or two. Comprehensiveness is a failure mode.

A successful tool over time shifts the user's default reasoning habits — they start examining their own assumptions before the tool has to ask.

### What This Is Not Optimizing For

- Winning arguments
- Identifying all fallacies in a piece of text
- Producing formally valid syllogisms
- Validating whatever the user already thinks

---

## 2. Core Interaction Design

### Session as the Primary Unit

Individual conversations are the primary product unit. Each session is a focused deep-dive on a single belief, argument, or question the user wants to examine. Sessions are bounded — the goal is depth on one thread, not coverage of everything.

Users can return across multiple sessions. Longitudinal data enriches the system's behavior over time but does not drive the experience. The tool gets better at asking the right questions for a specific user; this is disclosed in general terms during onboarding without being foregrounded as a feature.

### Session Structure

**Opening — Premise Declaration**

Before reasoning examination begins, the user declares the premises they want to treat as given for this session. These are the starting assumptions the argument will be built on.

The system does light probing of declared premises — not to challenge them, but to ensure the user understands what they're committing to. Example probe: "You've listed X as a starting assumption. Are you treating that as always true, true in most cases, or true specifically in the context you're discussing?" This is clarification, not interrogation. It frequently surfaces vagueness the user didn't notice.

Premises are then held as anchors for the session. The primary agent and red team agent both operate within them.

**Middle — Reasoning Examination**

The user states the belief or conclusion they want to examine and articulates their reasoning in their own words. This act alone — before any AI response — is productive. People discover gaps when they try to write them out.

The system reflects the structure back: "Here's what I'm hearing — you believe X because of Y and Z, and you're assuming A." This reflection step is not evaluation; it's making the structure legible so the user can confirm or correct it.

The system then identifies multiple interesting threads in the reasoning (empirical claims, value assumptions, inference structure, conspicuous omissions) and surfaces two or three for the user to prioritize. This gives the user ownership of direction while making visible what the system actually found. The session goes deep on one thread rather than touching all of them shallowly.

The red team agent generates the strongest case against the user's position, constrained to not require rejecting any declared premises. The primary agent introduces one piece of this as a question — "One consideration some people raise is X — how does that interact with your reasoning?" — and draws on more of the red team output as the conversation develops. If the only strong objection requires challenging a declared premise, the system surfaces that explicitly: "The strongest counterargument I can find actually requires questioning your premise about X."

**Close — Session Summary**

The session ends with the system summarizing: what was examined, what gaps or tensions were found, what counterarguments the user engaged with, and where the user's reasoning held up well. This summary is the primary longitudinal data feed — labeled reasoning moves extracted from a coherent session.

### Affirming Sound Reasoning

The system must be able to tell a user their reasoning is solid. If the conclusion follows well from the premises, the inferences are valid, and the user has genuinely engaged with the main counterargument, the system says so. This affirmation is only valuable if it's not the default — it has to be earned. The system should also note when this means residual uncertainty lives in the premises themselves rather than the argument structure.

### Handling Simple Arguments

When a user's premises and reasoning are too straightforward to generate meaningful examination — the argument is trivially valid, the premises do all the work, or the conclusion is uncontested — the system can note this and invite the user to go deeper: identify a more contentious premise, consider edge cases, or examine a more specific version of the claim. Early users will rarely trigger this; it's a ceiling rather than a floor.

---

## 3. Design Principles

### The System Is an Interlocutor, Not a Judge

The system surfaces counterarguments; it does not endorse them. It asks "how does X interact with your reasoning?" not "but have you considered that you might be wrong?" The user remains the epistemic agent throughout. The system's job is illumination, not steering.

### Improvement-Focused Without Introducing Bias

The tool has a concept of reasoning quality — better-supported claims, examined assumptions, genuine engagement with counterarguments — but it does not have positions on substantive questions. The risk of an improvement-focused tool is that "better reasoning" smuggles in the system's own values or priors. Mitigations:

- The premise system isolates substantive starting points from reasoning structure. The tool evaluates how well the reasoning follows from the premises, not whether the premises are correct.
- The system distinguishes "your reasoning has a gap here" from "I disagree with your conclusion." These are different interventions and conflating them is how the tool starts steering.
- Prompt design and interaction logs should be monitored for asymmetry — if the system consistently asks harder questions about certain types of claims, that's bias to address.

### Depth Over Breadth in Every Session

The temptation toward comprehensiveness is where these tools die. One thread pursued well is more valuable than five threads touched lightly. The session structure enforces this.

### Longitudinal Adaptation

The system tracks reasoning patterns across sessions — recurring appeals to authority, consistent avoidance of base rates, habitual conflation of correlation and causation — and uses these to calibrate future sessions. This is disclosed to users in general terms during onboarding ("the tool gets better at asking the right questions for you over time") but not surfaced as a dashboard or score. Full transparency kills the effect; full opacity crosses a line. The goal is for users to experience well-calibrated conversations, not to see their own reasoning grade.

Patterns are surfaced explicitly only when the user asks.

---

## 4. Agent Architecture

### Two-Agent Structure

**Primary Agent** — the conversational interlocutor. Maintains session state, reflects reasoning structure back to the user, asks targeted questions, manages tone. Warm and curious, not adversarial. Introduces counterarguments as questions, not challenges.

**Red Team Agent** — internal only, never talks to the user directly. Given the user's full articulated position and the declared premises, its only job is to find the strongest objection that doesn't require rejecting any premise. Prompted to be aggressive internally. Its output is filtered and translated by the primary agent.

The separation serves two purposes: the red team can generate adversarial content that would damage rapport if delivered directly, and the primary agent can calibrate how much pressure to apply based on where the conversation is.

### Agent Interaction Pattern

1. User declares premises → both agents receive them as constraints
2. User articulates position → primary agent reflects structure back
3. Red team generates strongest constrained objection → not shown to user
4. Primary agent selects one piece of red team output, introduces it as a question
5. Conversation continues; primary agent can draw on more red team output or leave it
6. Session close: primary agent generates summary with labeled reasoning moves

### What the System Needs to Track Per Session

- Declared premises (structured, not free text)
- User's stated conclusion
- Reasoning chain as articulated by the user
- Assumptions identified (stated vs. unstated)
- Counterarguments introduced and how the user engaged with them
- Reasoning verdict (sound / gaps identified / premise-dependent)

---

## 5. Technical Notes

### Where Complexity Earns Its Place

**Prompt engineering** is the crux. The difference between a system that genuinely challenges reasoning and one that performs challenge lives almost entirely here. The primary agent's tendency toward agreeableness is the central problem to solve. This deserves more iteration than any architectural decision.

**Session state management** is necessary. The primary agent needs the full conversation context plus the structured premise list and reasoning chain. This is standard context management, not a novel architecture problem.

**Longitudinal pattern storage** warrants a structured approach. Raw conversation summaries are insufficient — you need labeled reasoning moves (e.g., "appeal to authority without examining underlying evidence," "conflated correlation and causation") that can be aggregated across sessions. The extraction of these labels from session summaries is itself an LLM task and should be designed carefully.

### Where Complexity Does Not Earn Its Place

**RAG** does not belong in the core reasoning loop. The Socratic dialogue doesn't benefit from retrieval — it needs to track the user's specific reasoning chain. RAG might belong in a secondary feature (surfacing related empirical evidence after a session), but that's a different product and should be built separately and evaluated carefully. It shifts the tool from reasoning examination to information provision.

**Vector databases** are only warranted when longitudinal pattern storage reaches a scale or retrieval complexity that a structured database doesn't handle. Don't start there.

**Multi-agent beyond the two-agent structure** is not warranted at launch. Get the primary/red-team loop right before adding complexity.

### Data Architecture Consideration

The session summary and labeled reasoning moves are the most valuable data the system produces. The storage schema for these should be designed before the conversation schema, because it determines what the conversation needs to surface. Work backward from "what do we need to know about this user's reasoning patterns?" to "what does the session summary need to contain?" to "what does the conversation need to track?"

---

## 6. Open Questions

- **Onboarding flow**: How does the user learn to declare premises well? First-time users will likely declare conclusions as premises, or declare premises that are doing more argumentative work than they realize. The light probing helps, but the onboarding experience needs to teach the distinction.

- **Session length**: No explicit decision made. Worth defining a natural stopping point — either a time/turn limit or a signal that the session has done its work.

- **User-facing summary format**: The close-of-session summary is the most tangible artifact the user takes away. Its format matters for whether users feel the session was valuable. This is a design decision with UX implications.

- **Confidence calibration**: The tool examines reasoning structure, but users also frequently have miscalibrated confidence in their conclusions. Whether and how to address confidence (vs. just argument structure) is unresolved.

- **Premise revisitation**: If the user wants to revisit a declared premise mid-session, what's the protocol? Allowing it freely could let users escape pressure by retreating to first principles; never allowing it could make sessions feel rigid.