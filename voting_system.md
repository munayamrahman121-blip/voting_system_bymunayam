# Voting System: Selected Features and Plan

A console project for the DSA Level 2 module, built with dictionaries, sets, lists, tuples, searching and a frequency counter. No functions.

---

## 1. Problem Statement

> *"Our batch needs to elect a Class Representative. Right now we raise hands, so people copy each other, some people vote twice, and nobody trusts the count. I want a console program for election day. The admin registers the candidates and the eligible voters before voting starts. Each voter identifies themselves with their roll number and can vote only once. The program must never reveal who voted for whom. Voters can also choose NOTA (None of the above). When the admin closes the election, the program shows the full result: votes and percentage for each candidate, the turnout, and the winner. If two candidates tie, it must say so."*

### Project at a Glance

| Aspect | Decision |
|---|---|
| Users | Admin (sets up and closes), Voter (casts one vote) |
| Election | One election per program run |
| Voter identity | Roll number, registered by the admin, age 18 or above |
| Candidates | Registered by the admin, numbered automatically |
| Special choice | NOTA, always available as candidate number `0`. It is counted and shown in the results, but it never wins |
| Ballot | Secret: the vote is stored separately from the voter's identity |
| Result | Votes and percentage per candidate, turnout, winner or tie |
| Out of scope | Saving to files, multiple posts, voter passwords, recounts |

---

## 2. Selected Features

| # | Feature | Status | Why |
|---|---|---|---|
| F1 | Register candidates (no empty or duplicate names) | Core | Needed for any election |
| F2 | Register voters with roll number and age check (18+) | Core | Eligibility rule |
| F3 | View candidates | Core | Voters must see their choices |
| F4 | Cast one vote per voter | Core | The main purpose |
| F5 | Secret ballot (who voted and what was chosen are stored separately) | Core | The key data-structure lesson |
| F6 | Results with votes, percentage, turnout and winner | Core | The outcome |
| F7 | Messages when no candidate received a vote | Core | Edge case |
| F8 | NOTA option (counted and shown, never wins) | Selected | Realistic, and a good edge case |
| F9 | Admin PIN (3 attempts) to close the election | Selected | Protects the result |
| F10 | Registration locked after the first vote | Selected | Prevents changing the rules mid-election |
| F11 | Tie detection | Selected | Uses a set of leaders |
| F12 | Vote bars in the results | **Dropped** | Not needed |
| F13 | Voter passwords, recount, turnout log, saving to a file | Stretch | Only if time allows |

**Defaults used:** F8 to F11 are included. To shorten the program, drop F9 (admin PIN) first.

---

## 3. Menu

| Key | Menu item | Who | When allowed |
|---|---|---|---|
| `1` | Register candidate | Admin | Only before the first vote is cast |
| `2` | Register voter | Admin | Only before the first vote is cast |
| `3` | View candidates | Anyone | Always |
| `4` | Cast vote | Voter | Only while the election is open |
| `5` | Close election and show results | Admin (PIN required) | Needs at least one registered candidate and one registered voter |
| `q` | Exit | Anyone | Always |

---

## 4. Rules

### 4.1 Registration

| # | Rule |
|---|---|
| R1 | A candidate name cannot be empty or already registered (names are compared ignoring case and extra spaces) |
| R2 | A voter needs a roll number and an age. The roll number must be a whole number and not already registered |
| R3 | The voter must be 18 or older, otherwise registration is refused with a reason |
| R4 | Registration of candidates and voters is locked as soon as the first vote is cast |

### 4.2 Voting

| # | Rule |
|---|---|
| V1 | The voter enters their roll number, which must be registered |
| V2 | A voter who has already voted is refused ("already voted") |
| V3 | The program shows the candidates, including NOTA, and asks for a number |
| V4 | An invalid choice is rejected and the voter is asked again, without losing their turn |
| V5 | After a vote, the program only says "Vote recorded". It never shows the choice or links it to the voter |
| V6 | No votes are accepted once the election is closed |

### 4.3 Closing and Results

| # | Rule |
|---|---|
| C1 | Closing requires the admin PIN, with 3 attempts |
| C2 | Results show, for each candidate and NOTA: votes and percentage of all votes cast (no bars) |
| C3 | Turnout is shown as voted out of registered, with a percentage |
| C4 | The winner is the **candidate** with the most votes. NOTA is shown in the table but is never picked as the winner |
| C5 | If two or more candidates share the top count, declare a tie and list them |
| C6 | If no ballots were cast, say "No votes were cast." If ballots were cast but every one was NOTA, say "No candidate received any votes." In both cases show no winner |

---

## 5. Data Design

| Real-life need | Structure | Why this one |
|---|---|---|
| Candidates by number | Dictionary `{1: "Nadia", 2: "Rahim"}` | Look up a name by the number the voter types |
| Registered voters | Dictionary `{roll: age}` | "Is this roll registered?" in one step |
| Who has already voted | Set `voted` | Fast duplicate-vote check, each roll stored once |
| The secret ballot box | List `ballots` of candidate numbers | Holds votes only, with no names attached |
| Counting votes | Frequency counter (dictionary) | Built from `ballots` when the election closes |
| Result ranking | List of tuples `(votes, name)`, sorted | Tuples sort by the first item, so the highest votes come first |
| Tie detection | Set of candidate names with the top count (NOTA left out) | Holds one or more leaders cleanly |
| Fixed settings | Constants (admin PIN, voting age 18, NOTA is `0`) | Change in one place |

### Design Decision to Discuss with the Class

| Question | Answer |
|---|---|
| Why two structures, `voted` and `ballots`? | They are not connected, so nobody (including the admin) can find out how a person voted |
| What would break the secrecy? | A single dictionary like `{roll: choice}` |
| Why count at closing time instead of adding to a counter on every vote? | It is a deliberate use of the frequency-counter pattern, and it keeps the ballot box simple |
| How does NOTA stay out of the winner? | It is counted like everyone else, but skipped when choosing the leaders |

---

## 6. Expected Result Screen

```
ELECTION RESULT: Class Representative

Candidate        Votes       %
Nadia                5   50.0%
Rahim                3   30.0%
Sadia                1   10.0%
NOTA                 1   10.0%

Turnout: 10 of 12 registered voters (83%)
Winner: Nadia with 5 votes
```