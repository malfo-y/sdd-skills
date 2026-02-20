# Adaptive Questions Guide

Criteria for determining input completeness level and question strategies per level.

---

## Input Completeness Level Assessment

### HIGH (Detailed Input)

**All** of the following conditions are met:
- Feature name or improvement target is clear
- Description is specific (what needs to be done is clear)
- Acceptance Criteria are present or can be inferred
- Priority is stated or clear from context

**Example**:
> "Add real-time notification feature (High priority). Send Slack webhook notification on download completion.
> Acceptance criteria: Slack webhook configurable, message template customizable, retry on error."

**Response**: Proceed directly without questions. Only confirm by summarizing collected information.

---

### MEDIUM (Partial Input)

Only **some** of the following are met:
- Feature name or target is present but
- Acceptance criteria are insufficient or
- Priority is missing or
- Technical context is lacking

**Example**:
> "I want to add a feature that sends notifications via Slack."

**Response**: Ask only 1-3 key questions.

**MEDIUM level question list** (select only what's missing):

1. **Priority** (when missing):
   ```json
   {
     "question": "What is the priority of this feature?",
     "header": "Priority",
     "options": [
       {"label": "High", "description": "Must be included in the next release"},
       {"label": "Medium", "description": "Planned improvement"},
       {"label": "Low", "description": "Nice to have"}
     ],
     "multiSelect": false
   }
   ```

2. **Acceptance Criteria** (when missing):
   - "What conditions would indicate this feature is complete? (at least 2)"

3. **Technical Constraints** (when unclear):
   - "Are there any technical considerations? (libraries to use, architecture constraints, etc.)"

---

### LOW (Vague Input)

Applies when:
- Request is at the vague idea level
- No specific feature name
- "I want something like this" level

**Example**:
> "Add some notification feature"
> "Need performance improvements"

**Response**: Confirm type first → then ask type-specific required questions.

---

## LOW Level: Type Confirmation Question

First, confirm the requirement type:

```json
{
  "question": "What kind of item is this?",
  "header": "Type",
  "options": [
    {"label": "New Feature", "description": "Adding entirely new functionality"},
    {"label": "Improvement", "description": "Enhancing existing functionality"},
    {"label": "Bug Report", "description": "Reporting a discovered issue"},
    {"label": "Component Change", "description": "Adding or modifying a component"}
  ],
  "multiSelect": false
}
```

---

## LOW Level: Type-Specific Required Questions

### New Feature

| Order | Question | Required |
|-------|----------|----------|
| 1 | What is the feature name? | Required |
| 2 | What is the priority? (High/Medium/Low) | Required |
| 3 | What should this feature do? (description) | Required |
| 4 | What are the completion criteria? (Acceptance Criteria, at least 2) | Required |
| 5 | Which components are involved? | Optional |
| 6 | Are there any technical constraints or notes? | Optional |

### Improvement

| Order | Question | Required |
|-------|----------|----------|
| 1 | What do you want to improve? (target) | Required |
| 2 | How does it currently work? (current state) | Required |
| 3 | How should it be improved? (proposal) | Required |
| 4 | Why is this improvement needed? (reason) | Required |
| 5 | What is the priority? | Optional |

### Bug Report

| Order | Question | Required |
|-------|----------|----------|
| 1 | Describe the bug in one sentence (name) | Required |
| 2 | What is the severity? (High/Medium/Low) | Required |
| 3 | What is the problem? (description) | Required |
| 4 | How can it be reproduced? (reproduction steps) | Required |
| 5 | What should the correct behavior be? (expected behavior) | Required |
| 6 | Do you know the location? (file:line) | Optional |
| 7 | Is there a workaround? | Optional |

### Component Change

**Adding a new component**:

| Order | Question | Required |
|-------|----------|----------|
| 1 | What is the component name? | Required |
| 2 | What is the purpose of this component? | Required |
| 3 | What are the inputs and outputs? | Required |
| 4 | What are the main methods/functions? | Optional |

**Modifying an existing component**:

| Order | Question | Required |
|-------|----------|----------|
| 1 | Which component is being modified? | Required |
| 2 | What kind of change is it? (Enhancement/Refactor/Fix) | Required |
| 3 | What specific changes are needed? | Required |
| 4 | Does it affect backward compatibility? | Optional |

### Configuration Change

| Order | Question | Required |
|-------|----------|----------|
| 1 | What is the configuration item name? | Required |
| 2 | What type is it? (environment variable/config file/CLI argument) | Required |
| 3 | What does this setting control? (description) | Required |
| 4 | Is it required? What is the default? | Optional |

---

## Question Efficiency Tips

### Using AskUserQuestion

- Bundle multiple questions into a single AskUserQuestion call (up to 4 questions)
- Use options for choice-based questions (minimize typing)
- Collect free-text answers through conversation

### Question Order Optimization

1. Choice-based questions first (quick via AskUserQuestion)
2. Free-text questions later (naturally through conversation)

### Avoiding Unnecessary Questions

- Don't re-ask information already mentioned in conversation
- Only confirm information that can be inferred from existing spec
- Ask optional questions only when user provides additional information
