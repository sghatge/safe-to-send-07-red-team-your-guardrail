import json
import unittest

from red_team import hardened, naive, score

with open("examples/corpus.json", encoding="utf-8") as fh:
    CORPUS = json.load(fh)


class RedTeamTest(unittest.TestCase):
    def test_hardened_catches_every_write_in_corpus(self):
        _, missed, _ = score(hardened, CORPUS)
        self.assertEqual(missed, [])

    def test_naive_misses_whitespace_unicode_and_functions(self):
        _, missed, _ = score(naive, CORPUS)
        whys = {c["why"] for c in missed}
        self.assertIn("full-width Unicode letters", whys)
        self.assertIn("stored function with side effects", whys)

    def test_hardened_still_over_blocks_unknown_functions(self):
        _, _, over = score(hardened, CORPUS)
        self.assertEqual([c["why"] for c in over], ["unknown but read-only function"])

    def test_string_literals_not_blocked(self):
        self.assertFalse(hardened("SELECT 1 FROM t WHERE x = 'delete'"))


if __name__ == "__main__":
    unittest.main()
