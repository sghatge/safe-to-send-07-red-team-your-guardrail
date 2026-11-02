# safe-to-send-07 · Red-Team Your Guardrail

![Safe to Send, Episode 07](docs/episode.png)

**Safe to Send · Episode 07** — Week 1 retrospective of a 28-day learn-in-public series on governing AI in CRM operations.

> A guardrail you haven't attacked is a guardrail you're guessing about.

## The real-world scenario

Your AI gate blocks SQL writes by looking for `DELETE`, `UPDATE` and friends. It passes every demo. Then an agent writes `delete` followed by a newline, or calls a stored function that purges recipients, or (because it learned from messy data) uses full-width Unicode letters. Does your detector notice?

## Run it

```bash
python red_team.py examples/corpus.json
```

## Real example output

```
naive     caught 2/7 writes, over-blocked 1 safe reads
   MISSED   DELETE followed by a newline
   MISSED   stored function with side effects
   MISSED   UPDATE followed by a tab
   MISSED   full-width Unicode letters
   MISSED   write hidden inside a CTE
   BLOCKED  the word delete inside a string (safe)

hardened  caught 7/7 writes, over-blocked 1 safe reads
   BLOCKED  unknown but read-only function (safe)
```

## What this teaches

1. **A naive keyword check missed 5 of 7 writes** in a 12-query corpus. Whitespace, Unicode and stored functions are enough.
2. **The hardened version catches all 7** by normalising Unicode, stripping comments and strings, and treating any unknown function as a possible write.
3. **It still over-blocks**, on purpose. A false positive costs one human click. A false negative costs a market.
4. **No pattern detector is complete.** That's why the database operator's own rights must be the outer boundary. The gate is defence in depth, not the only wall.

Add your own attacks to `examples/corpus.json`. If you find one the hardened detector misses, open an issue.

## Where this fits

[ACC Agent Gate](https://github.com/sghatge/acc-agent-gate) documents the same limitation: its analysers are pattern-based and tuned to over-block.

Independent project, not affiliated with Adobe. MIT · [Sangram Ghatge](https://www.linkedin.com/in/sangram-g-2369705b) · #SafeToSend
