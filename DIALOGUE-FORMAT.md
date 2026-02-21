# Dialogue Format Guide

Complete guide to formatting dialogues for the TTS Tool.

## Basic Format

The tool uses this simple format:

```
[SPEAKER_NAME] Text spoken by the speaker
[OTHER_SPEAKER] Their response
[SPEAKER_NAME] More dialogue
```

### Example

```
[JOHN] Hello, how are you today?
[SARAH] Hi John! I'm doing great, thanks for asking.
[JOHN] That's wonderful! What did you do this morning?
[SARAH] I went to the market and bought some fresh fruits.
```

## Speaker Names

### Rules

1. **Must be in [BRACKETS]**
   - `[JOHN]` ✓
   - `JOHN:` ✗

2. **Must be UPPERCASE or Mixed Case**
   - `[JOHN]` ✓
   - `[john]` ✗ (might not detect)
   - `[John Smith]` ~ (spaces can be problematic)

3. **Can contain:**
   - Letters: A-Z, a-z
   - Numbers: 0-9
   - Underscores: _
   
   Examples:
   - `[JOHN]` ✓
   - `[JOHN_SMITH]` ✓
   - `[PERSON_1]` ✓
   - `[JOHN123]` ✓

4. **Cannot contain:**
   - Spaces (without underscore): `[JOHN SMITH]` ✗
   - Special characters: `[JOHN!]` ✗
   - Hyphens: `[JOHN-DOE]` ✗ (might work, but not recommended)

### Name Examples

Good names:
```
[JOHN]
[SARAH]
[DOCTOR]
[PATIENT]
[PERSON_1]
[INTERVIEWER]
[CANDIDATE]
[WAITER]
[CUSTOMER]
[MANAGER]
[DEVELOPER]
[TEACHER]
[STUDENT]
```

Avoid these:
```
[john]              # lowercase
[John Doe]          # spaces
[JOHN-SMITH]        # hyphens
[JOHN!]             # special chars
[José]              # accented characters (may not work)
```

## Text Guidelines

### Sentence Structure

Write natural English dialogue:

```
[JOHN] Hello, how are you today?
[SARAH] I'm doing well, thanks for asking.
[JOHN] That's great! What have you been up to?
[SARAH] I've been working on a new project.
```

### Punctuation

Use proper punctuation:
- **Periods** (.) for statements
- **Question marks** (?) for questions
- **Exclamation marks** (!) for excitement
- **Commas** (,) for pauses

```
[ALICE] Hi there!
[BOB] How are you?
[ALICE] I'm great, thanks for asking.
[BOB] That's wonderful!
```

### Line Breaks

Each speaker's line should start with [SPEAKER_NAME]:

```
[JOHN] Hello, how are you today?
[SARAH] I'm doing well, thanks for asking.
```

If you need multiple sentences per speaker, use periods:

```
[JOHN] Hello! How are you today? I hope you're having a great morning.
[SARAH] I'm doing well. Thanks for asking. How about you?
```

## Format Examples

### 2-Speaker Dialogue

```
[ALICE] Good morning! How are you?
[BOB] Hi Alice! I'm doing great.
[ALICE] That's wonderful! Want to get coffee?
[BOB] Sure! Let's go to our favorite cafe.
```

### 3-Speaker Dialogue

```
[PERSON1] Hey everyone! Ready for the meeting?
[PERSON2] Yes, I've prepared the presentation.
[PERSON3] Great! Let's get started.
[PERSON1] First, let's review the agenda.
[PERSON2] Good idea. I have the slides ready.
```

### Multi-Turn Dialogue

```
[DOCTOR] Good morning. How are you feeling today?
[PATIENT] I'm not feeling well. I have a headache.
[DOCTOR] I see. When did it start?
[PATIENT] It started yesterday morning.
[DOCTOR] Have you taken any medication?
[PATIENT] No, I haven't taken anything yet.
[DOCTOR] Let me check your blood pressure. Can you sit here?
[PATIENT] Okay, I'm ready.
[DOCTOR] Everything looks normal. Try drinking water and rest.
[PATIENT] Thank you, doctor. I'll do that.
```

### Business Dialogue

```
[MANAGER] Good morning, team. Let's start our weekly standup.
[DEVELOPER] Hi! I completed the API integration yesterday.
[DESIGNER] And I finished the UI mockups for the new dashboard.
[MANAGER] Excellent work! What are your plans for this week?
[DEVELOPER] I'm starting on the testing phase and bug fixes.
[DESIGNER] I'll be refining the mobile version of the UI.
[MANAGER] Sounds good. Keep up the great work!
```

## Common Mistakes & Fixes

### ❌ Mistake 1: Wrong Name Format

```
JOHN: Hello there  ← Wrong (no brackets)
john: Hello there  ← Wrong (no brackets)
[john] Hello there ← Wrong (lowercase)
```

**Fix:**
```
[JOHN] Hello there  ← Correct
```

### ❌ Mistake 2: Missing Space After Bracket

```
[JOHN]Hello there  ← Wrong (no space)
```

**Fix:**
```
[JOHN] Hello there  ← Correct (space after bracket)
```

### ❌ Mistake 3: Spaces in Names

```
[JOHN SMITH] Hello  ← Wrong (spaces in name)
```

**Fix:**
```
[JOHN_SMITH] Hello  ← Use underscores
```

### ❌ Mistake 4: Special Characters

```
[DR. JOHN] Hello     ← Wrong (period in name)
[JOHN-SMITH] Hello   ← Wrong (hyphen)
[JOHN!] Hello        ← Wrong (exclamation)
```

**Fix:**
```
[DR_JOHN] Hello      ← Use underscore
[JOHNSMITH] Hello    ← Or just concatenate
[JOHN] Hello         ← Or use first name only
```

### ❌ Mistake 5: Inconsistent Naming

```
[JOHN] Hello there
[john] How are you?
[John] I'm great
```

**Problem:** Tool might see these as different speakers!

**Fix:**
```
[JOHN] Hello there
[JOHN] How are you?
[JOHN] I'm great
```

### ❌ Mistake 6: No Text After Speaker Name

```
[JOHN]
[SARAH] Hi there!
```

**Problem:** Empty line skipped

**Fix:**
```
[JOHN] I'm ready to listen.
[SARAH] Hi there!
```

## Advanced Formatting

### Named Characters in Longer Scenes

```
[SCENE: Morning at a café]

[WAITER] Good morning! Welcome to our cafe.
[CUSTOMER1] Hi! Can we get a table for two?
[WAITER] Of course! Right this way.
[CUSTOMER2] This place looks nice.
[CUSTOMER1] It really does! I heard they have great coffee.
[WAITER] Here are your menus. I'll be right back to take your order.
[CUSTOMER1] Thank you!
```

### Stage Directions (Optional)

Some tools support actions in parentheses (TTS Tool ignores them):

```
[JOHN] (excited) I just got the job!
[SARAH] (happy) That's amazing! Congratulations!
[JOHN] (grateful) Thank you so much for your support!
```

**Note:** The tool will read everything, including the description. For cleaner audio, remove parenthetical actions.

### Natural Pauses

Use ellipsis (...) for pauses:

```
[JOHN] Well... I'm not sure what to say.
[SARAH] Take your time!
```

## Best Practices

### 1. Keep It Natural

Write like people actually talk:

✓ **Good:**
```
[ALICE] Hey, how was your day?
[BOB] Pretty good! How about yours?
```

✗ **Awkward:**
```
[ALICE] Greetings. How did your diurnal period progress?
[BOB] My diurnal period was satisfactory.
```

### 2. Use Contractions

English speakers use contractions naturally:

✓ **Good:**
```
[JOHN] I'm not sure about that.
[SARAH] It's not a big deal.
```

✗ **Awkward:**
```
[JOHN] I am not sure about that.
[SARAH] It is not a big deal.
```

### 3. Vary Sentence Length

Mix short and long sentences:

✓ **Good:**
```
[ALICE] Hi! How are you?
[BOB] I'm doing well, thanks for asking. I've had a really good day at work.
[ALICE] That's wonderful!
```

✗ **Monotonous:**
```
[ALICE] How are you doing today?
[BOB] I am doing fine and I have had a good day.
[ALICE] That is wonderful to hear.
```

### 4. Use Proper Punctuation

It helps the TTS engine:

✓ **Good:**
```
[JOHN] Hello! How are you today?
[SARAH] I'm doing great, thanks!
```

✗ **No punctuation:**
```
[JOHN] Hello how are you today
[SARAH] Im doing great thanks
```

### 5. Avoid Ambiguous Abbreviations

TTS might mispronounce:

✓ **Good:**
```
[DOCTOR] Your blood pressure is one-twenty over eighty.
[PATIENT] That's good, right?
```

✗ **With abbreviations:**
```
[DOCTOR] Your BP is 120/80.
[PATIENT] That's good, right?
```

## File Encoding

### Required Encoding

Files must be saved as **UTF-8** (most modern editors default to this).

### How to Check/Fix

**In most text editors:**
1. File → Encoding → UTF-8 (or Save with Encoding)
2. Save file

**On command line:**
```bash
# Convert to UTF-8
iconv -f ISO-8859-1 -t UTF-8 input.txt > output.txt

# Verify
file -i dialogue.txt  # Should show "utf-8"
```

## Length Guidelines

### Dialogue Length

Typical lengths and generation times:

| Lines | Duration | Gen Time |
|-------|----------|----------|
| 5 | 20 sec | 1-2 sec |
| 10 | 1 min | 2-3 sec |
| 20 | 2-3 min | 5-8 sec |
| 50 | 5-8 min | 15-20 sec |
| 100+ | 10+ min | 30+ sec |

### Maximum Recommended

- **Short dialogues:** 5-10 exchanges (best)
- **Medium dialogues:** 20-30 exchanges (good)
- **Long dialogues:** 50+ exchanges (works, but slower)

For very long content, split into multiple files.

## Validation Checklist

Before generating, check:

- [ ] All speaker names in [UPPERCASE_BRACKETS]
- [ ] Space after closing bracket
- [ ] No spaces in speaker names (use underscore)
- [ ] No special characters in names
- [ ] Text isn't empty
- [ ] File is UTF-8 encoded
- [ ] At least 2 different speakers
- [ ] Proper punctuation in dialogue

## Testing Your Format

### Quick Test

Try with this simple dialogue:

```
[TEST1] Hello world
[TEST2] How are you
[TEST1] I am fine
```

If this works, your format is correct!

### Common Test Issues

```
[test] lowercase names    ← Might not detect
[T EST] space in name    ← Might not detect
[TEST]no space           ← Might cause issues
TEST: brackets wrong     ← Won't detect
```

---

**Remember: Simple, clear, natural-sounding dialogue works best! 🎙️**
