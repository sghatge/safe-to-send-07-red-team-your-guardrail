Safe to Send · Ep 07 — I attacked my own guardrail

Week 1 retro. Instead of listing what my AI gate does, I tried to break it.

I wrote 12 SQL queries an agent might produce, 7 of them writes, and ran them through a naive "block DELETE/UPDATE" check.

It missed 5 of 7.
→ "delete" followed by a newline
→ UPDATE followed by a tab
→ full-width Unicode letters
→ a write hidden inside a CTE
→ a stored function that purges recipients

The hardened version (Unicode normalising, comment and string stripping, unknown functions treated as writes) caught 7 of 7. It also blocks one perfectly safe query, deliberately. A false positive costs a click. A false negative costs a market.

The real lesson: no pattern detector is complete. Your database permissions must be the outer wall. The AI gate is defence in depth, not the only control.

Find an attack the hardened detector misses? Open an issue in the repo.

Repo: https://github.com/sghatge/safe-to-send-07-red-team-your-guardrail

#SafeToSend #AISecurity #RedTeam #LearnInPublic
