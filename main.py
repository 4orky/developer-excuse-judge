# Make the AI Judge Laugh: Developer Excuses — make.fun bounty
# u-motasimfuad-make-the-ai-judge-laugh-developer-49386be3
#
# The program writes one funny single-line excuse a developer gives
# when code breaks in production (a single line of at most 200
# characters) to /output/entry.txt.
# Candidates were drafted against the judge's brief, in order of weight:
#   1. a funny single-line excuse a developer gives when code breaks
#      in production, on the subject or it loses outright
#   2. turns on a twist a developer recognises, revealing what really
#      happened rather than stating the obvious
#   3. sounds like something a developer would actually say out loud,
#      with the jargon used right
#   4. lands fast in one line, every word earning its place
#   5. feels fresh: avoids the worn excuses ("it worked on my
#      machine") or turns one in a way nobody has before
# Each candidate carries a hand-scored craft score (0-10 per criterion,
# summed below); selection is deterministic: highest score wins, ties go
# to the shorter text. The output is byte-identical on every run.

CANDIDATES = [
    # score: on-subject 10, twist 10, dev-voice 10, fast 9,
    #   fresh 8 = 47. The staging-vs-production gap every developer
    #   recognises: staging is a toy, production is the real world.
    #   The punch lands on the last two words, and the excuse is one
    #   a developer would genuinely offer in an incident call.
    ("It worked in staging because staging has no users, no data "
     "and no consequences \u2014 production has all three.",
     47),
    # score: on-subject 10, twist 9, dev-voice 9, fast 9,
    #   fresh 8 = 45. The stale-cache confession: a classic production
    #   failure mode, told as the cache finally owning up. The twist
    #   reveals what really happened, but "since March" is a beat
    #   slower than the winner's closer.
    ("Production didn't break \u2014 the cache just finally admitted "
     "it had been lying to us since March.",
     45),
    # score: on-subject 10, twist 8, dev-voice 9, fast 8,
    #   fresh 7 = 42. Real users clicking in the wrong order is a
    #   truth every developer knows, but the line states the failure
    #   more than it turns it.
    ("The code didn't break in production. Production just finally "
     "met a user who clicks things in the wrong order.",
     42),
    # score: on-subject 9, twist 8, dev-voice 8, fast 8,
    #   fresh 7 = 40. "Surprise load test" is a likeable reframing,
    #   but it reads as a quip about the incident rather than an
    #   excuse a developer would actually give for it.
    ("It's not a bug, it's a surprise load test the users "
     "volunteered for without signing anything.",
     40),
    # score: on-subject 9, twist 7, dev-voice 8, fast 8,
    #   fresh 7 = 39. Stage fright is a cute image, yet the excuse
    #   explains itself and the twist is thin.
    ("The deploy was fine. Production just read the release notes "
     "and got stage fright.",
     39),
    # score: on-subject 9, twist 7, dev-voice 7, fast 8,
    #   fresh 6 = 37. Personifying the database is familiar ground;
    #   the disagreement lands softly and the line is a touch long
    #   for what it delivers.
    ("I didn't break production \u2014 I just introduced it to the "
     "database, and they had a disagreement.",
     37),
]

# The gate requires 1-200 characters of non-whitespace UTF-8 text.
MAX_CHARS = 200


def pick(candidates):
    best = None
    for text, score in candidates:
        assert 1 <= len(text) <= MAX_CHARS, \
            f"candidate over gate: {len(text)} chars"
        assert text.strip(), "candidate is blank"
        assert "\n" not in text, "candidate must be a single line"
        key = (score, -len(text))  # highest score, then shortest
        if best is None or key > best[0]:
            best = (key, text)
    return best[1]


def main():
    import hashlib
    import os
    import sys

    excuse = pick(CANDIDATES)
    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8") as f:
        f.write(excuse)
    os.chmod("/output/entry.txt", 0o644)
    # Verify the written output: read it back byte-for-byte, print its
    # SHA-256 so the run is auditable, and re-check the gate (1-200
    # characters, single line, non-blank). A truncated or altered file
    # must fail loudly instead of shipping a bad entry.
    with open("/output/entry.txt", "rb") as f:
        raw = f.read()
    written = raw.decode("utf-8")
    digest = hashlib.sha256(raw).hexdigest()
    if written != excuse:
        print("error: /output/entry.txt does not match selected excuse",
              file=sys.stderr)
        sys.exit(1)
    if not (1 <= len(written) <= MAX_CHARS and written.strip()
            and "\n" not in written):
        print("error: /output/entry.txt fails gate: "
              f"{len(written)} chars", file=sys.stderr)
        sys.exit(1)
    print(f"sha256: {digest}")
    print(f"chars: {len(written)}")
    print(excuse)


if __name__ == "__main__":
    main()
