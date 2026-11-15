---
publish_time: 1790211189
link: https://www.marktechpost.com/2026/09/23/a-coding-guide-to-typesafe-ai-jev/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: true
digest: |
  MarkTechPost 发布 TypeSafe AI 的 Jev 使用指南：Jev 是其首个 System One 模型，不生成文本，而是对程序状态返回类型化判断（Choice、Score、Noul）。文章演示如何用 Python SDK 做置信度门控路由、复合打分、类型化函数调用与异步扇出，把模型输出当可组合决策单元，适合需要低延迟、可验证 Agent 决策的系统。
---

# TypeSafe AI 发布 Jev：面向 Agent 的类型化 System One 模型与编码指南

> 原文链接：https://www.marktechpost.com/2026/09/23/a-coding-guide-to-typesafe-ai-jev/
> 来源：MarkTechPost

In this tutorial, we work with Jev, TypeSafe AI&#8217;s first System One model, which does not generate text at all: we send it a piece of program state and a set of typed questions, and it returns choices, scores, and yes/no probabilities that our code can branch on directly. We install the official Python SDK, make a first call that uses all three question primitives at once, and look at how the shape of the state changes what the model can know. We then recompute the published confidence statistic from the returned probabilities, measure what batching ten questions into one call buys over ten separate calls, and build the patterns the API is designed for: confidence-gated routing, composite scoring with the weights kept in code, typed function calling, and counting done the way the model can actually do it. We close with the production shape: Pydantic response models, an async client fanned out with asyncio, retry policies, typed errors, and a running ledger that prices the whole notebook.

Copy CodeCopiedUse a different Browser

import os
import sys
import json
import time
import asyncio
import traceback
import subprocess
from getpass import getpass

RESULTS = {}
LEDGER = {"calls": 0, "input_tokens": 0, "output_tokens": 0}
USD_PER_MILLION_INPUT_TOKENS = 0.042          # Jev list price; output tokens are free

def banner(title):
    print("\n" + "=" * 78)
    print(title)
    print("=" * 78)

def section(name):
    def wrap(fn):
        def run(*a, **kw):
            banner(name)
            try:
                out = fn(*a, **kw)
                RESULTS[name] = out if isinstance(out, str) else "ok"
                return out
            except Exception as e:
                RESULTS[name] = f"SKIPPED / FAILED -> {type(e).__name__}: {e}"
                print(f"\n[!] {name} did not complete: {type(e).__name__}: {e}")
                traceback.print_exc(limit=3)
                return None
        return run
    return wrap

banner("0. Install the SDK, load the API key, list the models")
subprocess.run([sys.executable, "-m", "pip", "install", "-q", "typesafe-sdk==0.7.0"], check=True)
import typesafe_sdk
from typesafe_sdk import Choice, Noul, Score, TypeSafeClient

def load_api_key():
    key = os.environ.get("TYPESAFE_API_KEY", "").strip()
    if not key:
        try:
            from google.colab import userdata          # Colab: key stored under the Secrets tab
            key = (userdata.get("TYPESAFE_API_KEY") or "").strip()
        except Exception:
            key = ""
    return key or getpass("TypeSafe API key (console.typesafe.ai/keys): ").strip()

os.environ["TYPESAFE_API_KEY"] = load_api_key()
client = TypeSafeClient()                              # reads TYPESAFE_API_KEY, defaults to jev-latest

print(f"  typesafe-sdk {typesafe_sdk.__version__}  |  Python {sys.version.split()[0]}")
print("  models available to this key:")
for m in client.models.list().models:
    print(f"    {m.name:<14s} released {m.release_date}   {m.description}")

def ask(state, questions, **kw):
    """One System One call, timed, with its tokens added to the running ledger."""
    t0 = time.perf_counter()
    response = client.system_one(state, questions, **kw)
    ms = (time.perf_counter() - t0) * 1e3
    LEDGER["calls"] += 1
    LEDGER["input_tokens"] += response.usage.input_tokens or 0
    LEDGER["output_tokens"] += response.usage.output_tokens or 0
    return response, ms

We install typesafe-sdk, pinned to the version this notebook was written against, and load the API key from the environment, from Colab&#8217;s Secrets tab, or from a hidden prompt, so it never appears in the notebook. TypeSafeClient reads TYPESAFE_API_KEY on its own and defaults to the jev-latest alias; listing the models shows which names and pinned versions the key can use. The small ask helper wraps system_one so that every call in the rest of the notebook is timed and its token usage lands in a ledger we total at the end.

Copy CodeCopiedUse a different Browser

TICKET = {
    "ticket": {
        "subject": "Duplicate charge",
        "messages": [
            {"from": "customer", "text": "I was charged twice for order A-104. This is the second time "
                                         "this year. Please refund the duplicate today."},
            {"from": "support", "text": "We are checking the charges."},
        ],
    },
    "order": {"id": "A-104", "charges": [{"amount_usd": 49, "status": "captured"},
                                         {"amount_usd": 49, "status": "captured"}]},
    "refund_policy": "Duplicate charges are eligible for a full refund within 30 days.",
}

@section("1. Three primitives, one call: Choice, Score, Noul")
def three_primitives():
    response, ms = ask(TICKET, {
        "department": Choice(
            instructions="Which team should handle this ticket",
            criteria={"billing": "Payment, refund or subscription issues",
                      "technical": "Bugs, outages or integration problems",
                      "sales": "Pricing, plans or account upgrades"},
        ),
        "frustration": Score(
            instructions="How frustrated the customer appears in `ticket.messages[0].text`",
            criteria=["Calm, just stating facts", "Frustrated but civil", "Very angry, strong language"],
        ),
        "refund_requested": Noul(instructions="The customer is explicitly asking for a refund"),
        "policy_supports": Noul(instructions="The stated `refund_policy` covers this situation"),
    })

    dept = response.choices["department"]
    print(f"  department       -> {dept.choice!r}   confidence {dept.confidence:.3f}")
    print(f"     probabilities    {({k: round(v, 3) for k, v in dept.probabilities.items()})}")
    fr = response.scores["frustration"]
    print(f"  frustration      -> score {fr.score:.3f} on 0..{len(fr.legend) - 1}   confidence {fr.confidence:.3f}")
    for level, text in fr.legend.items():
        print(f"     {level}: p={fr.probabilities[level]:.3f}  {text}")
    print(f"  refund_requested -> noul {response.nouls['refund_requested'].noul:.3f}")
    print(f"  policy_supports  -> noul {response.nouls['policy_supports'].noul:.3f}")
    print(f"\n  answered by {response.model} in {ms:.0f} ms   "
          f"input tokens {response.usage.input_tokens}, output tokens {response.usage.output_tokens}")
    return f"{dept.choice}, frustration {fr.score:.2f}, refund {response.nouls['refund_requested'].noul:.2f}"

three_primitives()

A System One request has two parts: state, which is any text, JSON object or array describing the situation, and a dictionary of named questions. Choice selects one label from the criteria we define and returns a probability for every label; Score places the state on an ordered rubric and returns the probability-weighted level, so it can land between two levels; Noul returns a single probability that a statement is true. The question names are ours and never reach the model, which is why the instructions carry the full meaning and can point at nested fields with backticked paths. All four questions are evaluated in one request, in parallel and in isolation from one another, and the response reports the pinned model version that answered and the tokens it billed.

Copy CodeCopiedUse a different Browser

@section("2. State is program state: the same question over a string and over named fields")
def state_shapes():
    question = {"eligible": Noul(
        instructions="The customer is eligible for a refund under the company's written policy",
        criteria={"true": "A policy is present and it covers the customer's situation",
                  "false": "No policy is given, or the policy does not cover the situation"},
    )}
    bare = "I was charged twice for order A-104. Please refund the duplicate."
    as_list = [m["text"] for m in TICKET["ticket"]["messages"]]
    shapes = [("string: the message only", bare),
              ("array : the conversation", as_list),
              ("object: ticket + order + policy", TICKET)]
    print(f"  {'state shape':<34s} {'noul':>6s}   input tokens      ms")
    seen = {}
    for label, state in shapes:
        response, ms = ask(state, question)
        seen[label] = response.nouls["eligible"].noul
        print(f"  {label:<34s} {seen[label]:6.3f}   {response.usage.input_tokens:12d}   {ms:5.0f}")
    print("\n  Only the object carries the policy and the two captured charges; the question")
    print("  is identical in all three calls, so any movement comes from the state.")
    return "noul by state shape: " + ", ".join(f"{v:.2f}" for v in seen.values())

state_shapes()

State is the only thing the model knows, so we ask one question, whether the customer is eligible for a refund under the company&#8217;s written policy, over three shapes of state. A bare string contains the complaint and nothing else; an array adds the conversation; the JSON object adds the order with its two captured charges and the refund policy itself. The question never changes, so whatever difference appears in the returned probability is attributable to the state, and the token column shows what the extra context costs. Named fields are the documented recommendation whenever the context has several parts, because the instructions can then refer to them by name.

Copy CodeCopiedUse a different Browser

def confidence_from(probabilities):
    """TypeSafe's published statistic: (count x peak - 1) / (count - 1)."""
    p = list(probabilities.values())
    return (len(p) * max(p) - 1) / (len(p) - 1)

@section("3. Confidence is a statistic of the distribution, and you can recompute it")
def confidence_math():
    tone = Choice(instructions="What is the tone of the message",
                  criteria={"angry": "Upset or hostile", "calm": "Neutral or polite", "excited": "Enthusiastic or eager"})
    urgency = Score(instructions="How soon this needs attention",
                    criteria=["Can wait", "Needs attention this week", "Needs attention today"])
    messages = {
        "clear    ": "This is the third outage this week and nobody answers. Fix it NOW or I cancel today.",
        "ambiguous": "Well. That was certainly an experience. Let me know when you get a chance.",
    }
    print(f"  {'message':<10s} {'choice':<8s} {'API conf':>8s} {'recomputed':>11s}   "
          f"{'score':>6s} {'sum(level*p)':>13s} {'API conf':>9s}")
    worst = 1.0
    for label, text in messages.items():
        response, _ = ask(text, {"tone": tone, "urgency": urgency})
        t, u = response.choices["tone"], response.scores["urgency"]
        expected = sum(level * p for level, p in u.probabilities.items())
        print(f"  {label:<10s} {t.choice:<8s} {t.confidence:8.3f} {confidence_from(t.probabilities):11.3f}   "
              f"{u.score:6.3f} {expected:13.3f} {u.confidence:9.3f}")
        worst = min(worst, t.confidence)
    print("\n  A Noul has no confidence field: its value already is the probability of yes,")
    print("  so 0.5 means undecided, not medium.")
    return f"lowest tone confidence {worst:.2f}"

confidence_math()

TypeSafe documents confidence as a statistic computed from the distribution that the answer already contains: the number of options times the peak probability, minus one, divided by the number of options minus one. We recompute it from a Choice&#8217;s probabilities and compare it with the confidence field, and we recompute the Score as the sum of each level times its probability. Running a blunt message and a deliberately vague one through the same two questions shows how the distribution, and therefore the confidence, responds to ambiguity. A Noul carries no confidence field at all, since its value already is the probability of yes, and a value near 0.5 means undecided rather than moderate.

Copy CodeCopiedUse a different Browser

POSTMORTEM = """Incident 2291 - checkout latency, 14 March. At 09:12 UTC the payments gateway began timing out
for roughly 18 percent of checkout requests in the EU region. The on-call engineer was paged at 09:15 and
acknowledged at 09:21. Initial suspicion fell on the new fraud-scoring service deployed the previous evening,
and it was rolled back at 09:40 with no improvement. At 10:05 the database team found that a connection pool
limit had been lowered from 400 to 40 by an automated configuration sync, which had silently overwritten a
manual override. The limit was restored at 10:11 and error rates returned to baseline by 10:19. Customer
impact: 3,420 failed checkouts and an estimated 61,000 USD in delayed revenue; no data was lost and no
customer data was exposed. Customers were not notified during the incident; the status page was updated at
10:30, after recovery. Follow-ups: alert on pool saturation, require review for configuration-sync overrides,
and add the status page update to the first fifteen minutes of the on-call checklist."""

FANOUT = {
    "root_cause": Choice(instructions="What was the root cause of the incident",
                         criteria={"bad_deploy": "A faulty code or service deployment",
                                   "config_change": "An incorrect configuration value",
                                   "capacity": "Organic traffic exceeded provisioned capacity",
                                   "third_party": "A failure at an external vendor",
                                   "unknown": "The text does not establish a cause"}),
    "detected_by": Choice(instructions="How the incident was first detected",
                          criteria={"alerting": "Automated monitoring or paging", "customer": "Customer reports",
                                    "employee": "An employee noticed by chance", "unclear": "Not stated"}),
    "severity": Score(instructions="Severity of customer impact",
                      criteria=["No customer-visible impact", "Minor degradation for a few customers",
                                "A core flow failed for a meaningful share of customers",
                                "Full outage of a core flow for most customers"]),
    "comms_quality": Score(instructions="Quality of customer communication during the incident",
                           criteria=["Customers were informed promptly while it was happening",
                                     "Customers were informed, but late",
                                     "Customers were only informed after recovery, or never"]),
    "data_exposed": Noul(instructions="Customer data was exposed or leaked"),
    "rollback_helped": Noul(instructions="Rolling back the fraud-scoring service resolved the incident"),
    "human_error": Noul(instructions="A person making a manual mistake directly caused the incident"),
    "has_followups": Noul(instructions="The text lists concrete follow-up actions"),
    "revenue_lost": Noul(instructions="Revenue was permanently lost, as opposed to delayed"),
    "eu_only": Noul(instructions="The impact was limited to the EU region"),
}

def value_of(answer):
    for field in ("choice", "score", "noul"):              # a score of 0.0 is a real value, not a miss
        if hasattr(answer, field):
            return getattr(answer, field)

@section("4. Speculative fan-out: ten questions in one call versus ten calls")
def fan_out():
    batched, batched_ms = ask({"postmortem": POSTMORTEM}, FANOUT)
    batched_tokens = batched.usage.input_tokens
    seq_ms, seq_tokens, agree = 0.0, 0, 0
    print(f"  {'question':<16s} {'one call':>10s} {'own call':>10s}")
    for name, q in FANOUT.items():
        single, ms = ask({"postmortem": POSTMORTEM}, {name: q})
        seq_ms, seq_tokens = seq_ms + ms, seq_tokens + single.usage.input_tokens
        a, b = value_of(batched.answers[name]), value_of(single.answers[name])
        same = a == b if isinstance(a, str) else abs(a - b) < 0.05
        agree += same
        fmt = (lambda v: f"{v:>10s}") if isinstance(a, str) else (lambda v: f"{v:10.3f}")
        print(f"  {name:<16s} {fmt(a)} {fmt(b)}   {'same' if same else 'differs'}")
    print(f"\n  one call : {batched_ms:7.0f} ms   {batched_tokens:6d} input tokens")
    print(f"  ten calls: {seq_ms:7.0f} ms   {seq_tokens:6d} input tokens")
    print(f"  -> {seq_ms / batched_ms:.1f}x faster and {seq_tokens / batched_tokens:.1f}x fewer tokens; "
          f"{agree}/{len(FANOUT)} answers agree, because questions never see each other")
    return f"{seq_ms / batched_ms:.1f}x faster, {seq_tokens / batched_tokens:.1f}x cheaper, {agree}/{len(FANOUT)} agree"

fan_out()

Because questions in a request cannot see each other, we can ask everything we might need up front, including questions that only matter on one branch, and read only the relevant answers afterwards. We put ten questions about an incident postmortem, two Choices, two Scores and six Nouls, into one call, then ask each of them again in a call of its own, and compare wall time, input tokens and the answers. The state is sent once instead of ten times, which is where both the latency and the token savings come from, and the agreement column checks the isolation claim directly: a question should receive the same answer whether or not it travels with others.

Copy CodeCopiedUse a different Browser

INTENT = Choice(
    instructions="What the user wants the banking assistant to do",
    criteria={"check_balance": "See a balance or recent transactions",
              "approve_transfer": "Send or approve a transfer of money",
              "dispute_charge": "Contest a charge they do not recognise",
              "close_account": "Close the account permanently",
              "other": "Anything else, or not clear enough to act on"},
)
STAKES = {"check_balance": 0.50, "dispute_charge": 0.70, "approve_transfer": 0.85, "close_account": 0.90}

def route(answer):
    if answer.choice == "other" or answer.confidence < 0.50:
        return "-> human"
    bar = STAKES[answer.choice]
    return f"-> run {answer.choice}" if answer.confidence >= bar else f"-> confirm first (needs {bar:.2f})"

@section("5. Confidence-gated routing: the bar rises with the stakes")
def gated_routing():
    inbox = ["how much is in my checking account",
             "send 2,000 to my landlord like last month",
             "i guess maybe move some money around? not sure",
             "there's a 89.99 charge from a gym i never joined",
             "shut everything down, i'm done with this bank",
             "what's the weather like in lisbon"]
    print(f"  {'message':<50s} {'intent':<17s} {'conf':>5s}  decision")
    acted = 0
    for text in inbox:
        response, _ = ask(text, {"intent": INTENT})
        a = response.choices["intent"]
        decision = route(a)
        acted += decision.startswith("-> run")
        print(f"  {text[:50]:<50s} {a.choice:<17s} {a.confidence:5.2f}  {decision}")
    print(f"\n  thresholds live in code: {STAKES}")
    return f"{acted}/{len(inbox)} messages acted on automatically"

gated_routing()

Typed answers only matter if the code around them encodes how much certainty an action requires. We classify each message into an intent and route on two things: the intent itself and whether its confidence clears a bar that rises with the stakes, from 0.5 for reading a balance to 0.9 for closing an account. Anything classified as other, or below 0.5, goes to a person; an intent that is recognised but under its bar is confirmed with the user first. The thresholds are ordinary Python values, so risk tolerance is reviewed, versioned and tested like any other code rather than buried in a prompt.

Copy CodeCopiedUse a different Browser

DIMENSIONS = {
    "python_depth": Score(instructions="Depth of hands-on Python engineering experience", criteria=[
        "No Python mentioned", "Scripts or notebooks only", "Ships production Python services",
        "Designs Python libraries or frameworks used by others"]),
    "ml_systems": Score(instructions="Experience running machine learning systems in production", criteria=[
        "None mentioned", "Trained models offline only", "Deployed and monitored models in production",
        "Owned large-scale training or serving infrastructure"]),
    "leadership": Score(instructions="Evidence of leading people or projects", criteria=[
        "None mentioned", "Mentored individuals", "Led a project or a small team",
        "Managed several teams or an organisation"]),
    "communication": Score(instructions="Evidence of clear written or public communication", criteria=[
        "None mentioned", "Internal docs only", "Public posts or talks", "Widely read writing or major conference talks"]),
}
CANDIDATES = {
    "Asha":  "Eight years of Python; maintains an open-source data validation library with 4k stars. "
             "Deployed fraud models at a bank and ran their monitoring. Mentors two juniors. Writes a technical blog.",
    "Bruno": "Engineering manager for three teams (22 people). Wrote Java for a decade, some Python scripting. "
             "Sponsored the company's ML platform but did not build it. Keynoted two industry conferences.",
    "Chen":  "PhD in statistics; trains models in notebooks, no production deployments. Python for analysis. "
             "Teaching assistant for two courses. Several internal reports.",
    "Dara":  "Built and owned the serving infrastructure for a recommender at 40k requests per second in Python "
             "and C++. Led a five-person platform team. Internal design docs only.",
}
WEIGHTS = {"senior IC": {"python_depth": .40, "ml_systems": .40, "leadership": .05, "communication": .15},
           "team lead": {"python_depth": .15, "ml_systems": .25, "leadership": .45, "communication": .15}}

@section("6. Composite scoring: atomic judgments from the model, weights from code")
def composite_scoring():
    table = {}
    for name, bio in CANDIDATES.items():
        response, _ = ask({"candidate_bio": bio}, DIMENSIONS)
        table[name] = {d: response.scores[d].score / (len(q.criteria) - 1) for d, q in DIMENSIONS.items()}
    print(f"  {'':<7s}" + "".join(f"{d:>15s}" for d in DIMENSIONS) + "   (each normalised to 0..1)")
    for name, row in table.items():
        print(f"  {name:<7s}" + "".join(f"{row[d]:15.2f}" for d in DIMENSIONS))
    winners = {}
    for role, w in WEIGHTS.items():
        ranked = sorted(table, key=lambda n: -sum(w[d] * table[n][d] for d in w))
        winners[role] = ranked[0]
        print(f"\n  ranking for {role:<10s}: " +
              "  >  ".join(f"{n} {sum(w[d] * table[n][d] for d in w):.2f}" for n in ranked))
    print("\n  Two rankings, four model calls: changing the weights re-ran no inference.")
    return ", ".join(f"{role}: {who}" for role, who in winners.items())

composite_scoring()

Composite scoring keeps the model&#8217;s job narrow and the policy explicit. For each candidate we ask four Score questions, each describing concrete situations rather than degrees, normalise every score by its top level, and store the resulting table. The ranking is then plain arithmetic: one weight vector for a senior individual contributor, another for a team lead. Because the judgments are stored separately from the weights, changing what we value instantly re-ranks the candidates and requires no inference. You can trace every position in the ranking back to the dimension that produced it.

Copy CodeCopiedUse a different Browser

ROOMS = {"living_room": None, "bedroom": None, "kitchen": None, "office": None}

def set_lights(room, state):
    return f"lights in {room} -> {state}"

def set_thermostat(room, mode):
    return f"thermostat in {room} -> {mode}"

def play_music(room, genre):
    return f"playing {genre} in {room}"

TOOLS = {"set_lights": (set_lights, "state"), "set_thermostat": (set_thermostat, "mode"),
         "play_music": (play_music, "genre")}
CALL_SPEC = {
    "tool": Choice(instructions="Which smart-home function the command asks for",
                   criteria={"set_lights": "Turn lights on, off, or dim them",
                             "set_thermostat": "Make a room warmer, cooler, or set eco mode",
                             "play_music": "Play music or audio",
                             "none": "Not a smart-home command this system supports"}),
    "room": Choice(instructions="Which room the command refers to", criteria=ROOMS),
    "state": Choice(instructions="If this is a lights command: the requested light state",
                    criteria={"on": None, "off": None, "dim": None}),
    "mode": Choice(instructions="If this is a thermostat command: the requested mode",
                   criteria={"heat": "Warmer", "cool": "Cooler", "eco": "Energy saving"}),
    "genre": Choice(instructions="If this is a music command: the requested genre",
                    criteria={"jazz": None, "classical": None, "rock": None, "ambient": None}),
}

@section("7. Typed function calling, and counting the way Jev can do it")
def function_calling():
    commands = ["it's freezing in the office, warm it up", "kill the lights in the bedroom",
                "put on something mellow and jazzy in the kitchen", "order me a pizza"]
    dispatched = 0
    for text in commands:
        response, ms = ask(text, CALL_SPEC)                # every argument asked speculatively, one call
        c = response.choices
        tool = c["tool"].choice
        if tool == "none":
            print(f"  {text!r:<52s} -> no tool (confidence {c['tool'].confidence:.2f})")
            continue
        fn, arg = TOOLS[tool]
        weakest = min(c["tool"].confidence, c["room"].confidence, c[arg].confidence)
        print(f"  {text!r:<52s} -> {tool}(room={c['room'].choice!r}, {arg}={c[arg].choice!r})  "
              f"weakest judgment {weakest:.2f}, {ms:.0f} ms")
        print(f"  {'':<52s}    {fn(c['room'].choice, c[arg].choice)}")
        dispatched += 1

    basket = ["mango", "spanner", "kiwi", "router", "plum", "stapler", "fig", "lychee"]
    response, _ = ask({"items": basket},
                      {f"item_{i}": Noul(instructions=f"`items[{i}]` is the name of a fruit") for i in range(len(basket))})
    probs = [response.nouls[f"item_{i}"].noul for i in range(len(basket))]
    print("\n  counting: one Noul per item, summed in code (Jev does not count reliably in one question)")
    print("  " + "  ".join(f"{item}={p:.2f}" for item, p in zip(basket, probs)))
    count = sum(p > 0.5 for p in probs)
    print(f"  fruits counted: {count} of {len(basket)}")
    return f"{dispatched}/{len(commands)} commands dispatched from typed answers; counted {count} fruits"

function_calling()

Function calling becomes a set of closed-set questions: one Choice selects the tool, including an explicit none option for commands we do not support, and one Choice per argument is asked speculatively in the same request. The code reads only the arguments that belong to the selected tool, reports the weakest judgment as the confidence of the whole call, and then executes an ordinary Python function with validated, enumerated values. The second half applies a documented workaround: Jev does not count reliably inside a single question, so we ask one Noul per item in one request and do the sum in code.

Copy CodeCopiedUse a different Browser

import concurrent.futures
from typesafe_sdk import (AsyncTypeSafeClient, ChoiceAnswer, NoulAnswer, RetryPolicy, ScoreAnswer,
                          SystemOneResponse, TypeSafeAPIError, TypeSafeError)

class TicketDecision(SystemOneResponse):
    """Declare the answers you expect and read them as attributes, validated by Pydantic."""
    department: ChoiceAnswer
    frustration: ScoreAnswer
    refund_requested: NoulAnswer

TRIAGE = {
    "department": Choice(instructions="Which team should handle this ticket",
                         criteria={"billing": "Payment, refund or subscription issues",
                                   "technical": "Bugs, outages or integration problems",
                                   "sales": "Pricing, plans or account upgrades"}),
    "frustration": Score(instructions="How frustrated the customer appears",
                         criteria=["Calm, just stating facts", "Frustrated but civil", "Very angry, strong language"]),
    "refund_requested": Noul(instructions="The customer is explicitly asking for a refund"),
}
QUEUE = ["My invoice shows two seats but I only have one user.", "The export button does nothing in Safari.",
         "Can I get a discount if I pay annually?", "Your API returns 500 on every request since this morning!!",
         "I want my money back for last month, the product never worked.", "How do I add a teammate?",
         "Webhooks stopped firing after your update.", "Do you offer a plan for nonprofits?",
         "Charged after I cancelled. Refund this immediately.", "The dashboard is slow but usable.",
         "Is there an on-prem version?", "Login emails never arrive."]

def run_async(coro):
    """Works in a plain script and inside Jupyter/Colab, where an event loop is already running."""
    try:
        asyncio.get_running_loop()
    except RuntimeError:
        return asyncio.run(coro)
    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as pool:
        return pool.submit(asyncio.run, coro).result()

async def triage_all(tickets):
    retry = RetryPolicy(max_retries=3, backoff_initial=0.5, backoff_max=4.0, timeout=20.0)
    async with AsyncTypeSafeClient(retry=retry, timeout=10.0) as aclient:
        t0 = time.perf_counter()
        results = await asyncio.gather(*(aclient.system_one(t, TRIAGE, response_model=TicketDecision)
                                         for t in tickets))
        return results, (time.perf_counter() - t0) * 1e3

@section("8. Production shape: typed response models, async fan-out, retries, errors")
def production():
    results, wall_ms = run_async(triage_all(QUEUE))
    for r in results:
        LEDGER["calls"] += 1
        LEDGER["input_tokens"] += r.usage.input_tokens or 0
        LEDGER["output_tokens"] += r.usage.output_tokens or 0
    print(f"  {len(QUEUE)} tickets triaged concurrently in {wall_ms:.0f} ms wall time "
          f"({wall_ms / len(QUEUE):.0f} ms per ticket amortised)\n")
    print(f"  {'ticket':<58s} {'department':<10s} {'frustr.':>7s} {'refund':>7s}")
    for text, r in zip(QUEUE, results):                    # attribute access, no dict lookups, no parsing
        print(f"  {text[:58]:<58s} {r.department.choice:<10s} {r.frustration.score:7.2f} {r.refund_requested.noul:7.2f}")

    print("\n  errors are typed too:")
    try:
        client.system_one("anything", {})
    except TypeSafeError as e:
        print(f"    empty questions, caught before any request : {type(e).__name__}: {e}")
    try:
        client.system_one("anything", {"q": Noul(instructions="Is this a test")}, model="jev-does-not-exist",
                          retry=RetryPolicy(max_retries=0))
    except TypeSafeAPIError as e:
        print(f"    unknown model, rejected by the API         : {type(e).__name__} (HTTP {e.status})")
    refunds = sum(r.refund_requested.noul > 0.5 for r in results)
    return f"{len(QUEUE)} tickets in {wall_ms:.0f} ms; {refunds} refund requests flagged"

production()

Four details turn the examples into a decision service. Subclassing SystemOneResponse and declaring the answers we expect gives attribute access validated by Pydantic, so the typed decision stays typed all the way into the application rather than becoming a dictionary lookup. Because every request is independent, a queue of tickets is a queue of independent decisions: AsyncTypeSafeClient with asyncio.gather sends them concurrently, and the run_async helper makes the same code work in a script and inside a notebook, where an event loop is already running. RetryPolicy bounds the retries, the backoff and the total time budget per call. Errors are typed as well: an empty question set is rejected before any request is made, and an unknown model name comes back from the API as a TypeSafeAPIError subclass carrying the HTTP status.

Copy CodeCopiedUse a different Browser

banner("SUMMARY")
for name, res in RESULTS.items():
    print(f"  {name:<86s} {res}")
cost = LEDGER["input_tokens"] / 1e6 * USD_PER_MILLION_INPUT_TOKENS
client.close()
print(f"\n  whole tutorial: {LEDGER['calls']} calls, {LEDGER['input_tokens']:,} input tokens, "
      f"{LEDGER['output_tokens']:,} output tokens (free)  ->  about ${cost:.5f}")
print("""
Where to go next
 - Patterns: docs.typesafe.ai/patterns  (fan-out, confidence routing, composite scoring, intent routing)
 - Cookbooks: re-ranking, RAG passage filtering, citation checks, LLM guardrails, hierarchical classification
 - Known rough edges of jev-1.13: docs.typesafe.ai/model-jaggedness/jev-1.13  (literal reading, arithmetic,
   counting, date comparison, large irrelevant state)
 - Compare against an LLM on the same questions: github.com/typesafe-ai/system-one-adapter-python
 - Pin a version for production: TypeSafeClient(model="jev-1.13.0"); response.model reports what answered
""")

The summary prints the one-line result each section returned, then totals the ledger that every call has been feeding: the number of requests, the input and output tokens, and the cost at the published input price, with output tokens free.

In conclusion, we used Jev the way it is meant to be used: as a source of small, typed judgments that code composes, not as a text generator to be prompted and parsed. Every answer arrived as a label, a level, or a probability with its distribution attached, letting us set thresholds, weights, and routing rules in Python where they can be tested. Batching questions over a shared state reduces both latency and tokens because the state travels once per item; Nouls replace a count the model cannot be trusted to make, and closed-set Choices turn natural-language commands into validated function calls. The production pieces, typed response models, the async client, retry policies, and typed errors, are small, and the ledger prices the whole notebook. What remains is the part no SDK can do for us: evaluating the questions, criteria, and thresholds on our own data before trusting them with real actions.

Check out the FULL CODES here. All credit goes to the researcher of this project. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post A Coding Guide to TypeSafe AI Jev: Typed Decisions, Calibrated Confidence, and Speculative Fan-Out with a System One Model appeared first on MarkTechPost.