# The judgement calls — what the agent fixes after the scripts run

`SKILL.md` step 5 covers the mechanical tiers. This file is step 6: the findings
that need someone to read the pages. Read it when a report hands you `anchor`,
`stale`, `gone`, `templated` or low-confidence `renamed`, or when a tier's verifier
refused a fix because the anchor did not exist.

## Who fixes what

**Read this before you tell anyone that the rest "needs a person".** It almost
never does. When the script stops, most of what is left is work for YOU — open the
pages, read them, decide, and fix. Do not hand a human a list of 3,000 findings and
call that a result.

There are three kinds of work here, and only the third belongs to a human:

| | who | example | how much of it |
|---|---|---|---|
| One correct answer, computable | the script | this link needs one more `../` | ~15,800 of 20,800 |
| Needs reading the pages | **YOU, the agent** | which heading did this link mean? is this the right screenshot? | ~4,300 |
| Needs a product or policy decision nobody can read off the page | a human | was this page dropped on purpose? how should shared blocks address things? what is `{{envoy_path}}` supposed to be? | a few hundred, and mostly one decision each rather than N fixes |

The line between rows two and three is *"could someone find the answer by reading
what is in front of them?"* If yes, it is yours. "Needs someone to read the page"
means **you** read the page.

**Route your decisions through `fix_links.py`, do not edit pages by hand.** Write a
plan of the same shape and apply it with `--tier agent`:

```bash
cat > /tmp/agent-fixes.json <<'JSON'
{"scope": "api-manager/4.6.0", "tiers": {"agent": [
  {"file": "api-manager/4.6.0/administer/x.md",
   "link": "../y/#Old-Heading-Name",
   "suggested": "../y/#the-real-heading",
   "is_html": false,
   "evidence": {
     "sentence": "For details, see [Configuring the gateway](../y/#Old-Heading-Name).",
     "matched": "## The real heading"}}
]}}
JSON
python3 scripts/fix_links.py en/docs --plan /tmp/agent-fixes.json --tier agent
python3 scripts/fix_links.py en/docs --plan /tmp/agent-fixes.json --tier agent \
    --apply --journal /tmp/agent-journal.json
```

That is not bureaucracy. It buys three things a hand edit does not: every rewrite
is checked against the files before it is written, a wrong choice is refused rather
than applied, and the journal records what changed and why. Record `is_html` — it
decides which base the path is checked against.

**`evidence` is required on every `agent` entry, and the script enforces it.**
Two fields, both quoted from the files:

- `sentence` — the sentence containing the link, **verbatim**. It must appear on the
  page character for character; a paraphrase is refused. This is the field that says
  where the reader was being sent.
- `matched` — the heading, page title or filename you chose, quoted from the target.

The reason it is enforced rather than encouraged: **a correct judgement and a wrong
guess produce the same diff.** Both have valid syntax and point at a real heading.
The difference is that the wrong one silently drops the reader in a section about
something else, and nothing will ever flag it again — not `mkdocs build`, not
`check_links.py`, not the next person to read the page. Quoting the two lines you
based the decision on is what lets a reviewer check twenty and trust the rest,
instead of taking "fixed 2,949 anchors" on faith. If you cannot fill in the two
fields honestly, that finding is not ready to fix — leave it and say why.

**What to work, and what evidence justifies a fix:**

- **`anchor`** — the heading was reworded. Open the target page, read its headings,
  and read *the sentence containing the link* — that says what the reader was being
  sent to. Only act when the sentence and one heading clearly agree. "Probably that
  one" is not enough: a wrong anchor drops the reader in a section about something
  else and nothing will ever flag it.
- **`dir_style` and `renamed` refusals** — the path was right and the *anchor* did
  not exist on the new target, so the whole fix was refused. Supply the path AND
  the anchor together and the refusal goes away.
- **`renamed` at low confidence** — several files share the name. The plan lists
  them in `alternatives`. Read the linking sentence and pick; if two are equally
  plausible, leave it and say which two.
- **`stale`** — the old-site path does not exist under this version, so the
  mechanical mapping could not fire. Search the version for the content by title
  and by heading, not by filename.
- **`gone`** — no page or file of that name anywhere. Four situations, and only
  reading tells them apart:
  1. the content moved → repoint the link;
  2. **the file was never copied over** → copy it (see *Copying files the migration
     left behind*, below). This is the largest slice and it is fully yours;
  3. the content was dropped for this version → the sentence has to be rewritten or
     removed, which changes what the page says — **ask a human**;
  4. the page was missed in the migration → **ask a human**, it is a content
     decision, not a link fix.
- **`templated`** — same as `gone`, with a `{{base_path}}` on the front.

## Images and screenshots — open them and look

 You can read an image, so an
image finding is not automatically someone else's problem:

- *A missing screenshot, and a file of the same name exists in another version* —
  open both the sibling version's image and the page that wants it. Reuse it only
  if the screen it shows still matches what the surrounding steps describe. A
  4.5.0 screenshot of a redesigned page is worse than no screenshot, because the
  reader trusts it.
- *Two candidates with similar names* — `create-api.png` and `create-api-new.png`.
  Open both, read the linking sentence, and pick the one that shows what the
  sentence describes. Put the reason in `evidence.matched`.
- *An image that resolves but is wrong* — the text says "click **Deploy**" and the
  screenshot shows the Publish screen. **No script in this skill can catch this**,
  and no build warning will ever fire. It is worth opening the images on any page
  you are already editing, and worth a deliberate pass on the pages a release
  touches. Report these separately: the fix is a new screenshot, which needs a
  human with the product running.
- *An animated GIF or a 3 MB PNG* (`IMG_ANIMATED_GIF`, size findings) — a judgement
  about whether it earns its weight. Look at it before saying.

## Copying files the migration left behind

 253 findings name a file — `.zip`,
`.jar`, a screenshot — that still exists in `wso2/docs-apim` and was never copied.
That is not a link problem and the link must NOT be edited: the address is right,
the file is absent. Do the copy instead.

```bash
git clone --depth 1 --branch 4.6.0 https://github.com/wso2/docs-apim /tmp/docs-apim
# for each finding, the old path is the same path under en/docs
cp /tmp/docs-apim/en/docs/<same/path/file.png> en/docs/<same/path/file.png>
```

Rules for this, in order:

1. **Copy from the matching version branch**, not from `master`. An attachment on
   the 4.6.0 branch belongs to 4.6.0.
2. **Verify each file after copying** — non-zero size, and it actually opens as
   what it claims to be. A 0-byte or HTML-error-page PNG passes a "file exists"
   check and fails for every reader.
3. **Re-run `report_links.py` afterwards.** The findings should disappear on their
   own. If one does not, the path was wrong, not the file.
4. **Ask before committing a bulk copy.** ~219 files is a change to the repo's
   contents, not a link fix — show the list and the total size and wait for a yes.

## When the old repo is worth opening

 `wso2/docs-apim` keeps
one branch per version (`3.0.0` … `4.7.0`), so the pre-migration page is still
there at the path a broken link names. Measured, so nobody spends a week building
cross-repo recovery that does not pay:

| | worth it? |
|---|---|
| A missing file — `.zip`, `.jar`, an image | **Yes.** 253 findings name a file that still exists in docs-apim and was never copied. The action is to copy the file, not to edit the link. |
| A missing anchor | **No.** Of 3,017 anchor findings whose target page still exists in docs-apim, only **23** had that heading in the old page. **2,994 were already broken before the migration** — inherited debt, not migration damage. The old repo cannot answer them, and neither can a lookup: read the page. |

That second row is worth saying out loud in any report. The largest "needs a
person" group is mostly pre-existing breakage carried over from the old site, so it
is not a regression the migration introduced and it does not have to block it.

**Leave alone:** `partial` needs a decision about how shared blocks should address
things at all, which is one human decision rather than N fixes. Do not paper over
it with a relative path.

**Report as you go.** For each group say how many you fixed, how many you left,
and why. A run that says "fixed all 98 anchors" is less trustworthy than one that
says "fixed 61, left 37 because the sentence did not name a section clearly enough".

## How to actually work through it

When someone asks you to fix the broken links and images, this is the loop. Do not
stop at the report — the report is the input to this section, not the output.

1. **Take one scope at a time**, the same scope the mechanical run used —
   `api-manager/4.6.0`, not the whole repo. A repo-wide agent pass cannot be
   reviewed by anyone and cannot be handed back if it is wrong.
2. **Sort the group by target page, not by source page.** Twenty links across the
   repo often point at the *same* page whose heading was reworded. Read that page
   once and you have twenty answers; go source-page-by-source-page and you read it
   twenty times and risk answering it differently each time.
3. **Work in batches of about 25**, and after each batch: dry-run the plan, then
   `--apply`, then `git diff` the batch and read it. Refusals are information —
   if the script refuses several in a row, your reading is off, so stop and
   re-read rather than adjusting the plan until it passes.
4. **Regenerate the report after each batch.** Fixing one link changes what others
   resolve to.
5. **Leave what you cannot justify.** Two headings equally plausible, a sentence
   that names no section, a page that does not obviously correspond to anything —
   leave it, and list it. Target roughly two thirds fixed per group; a claim of
   100% on `anchor` means guessing happened.
6. **Stop and ask** the moment a fix would change what a page *says* rather than
   where it points — removing a sentence, dropping a step, rewording a heading.
   That is a content decision.
7. **Verify at the end the way `SKILL.md` step 7 says** — a real `mkdocs build`, and links
   resolved against the built HTML, not against your own report. Quote the
   before/after, and say how many you left.

A finished agent pass reads like: *"`anchor`, api-manager/4.6.0: 87 findings, read
41 target pages, fixed 58, left 29 (19 where the sentence named no section, 10
where two headings were equally plausible — listed below). Built the site: links
landing on a missing heading went 87 → 29, nothing newly broken."* That is a
result. "Needs a person" is not.

