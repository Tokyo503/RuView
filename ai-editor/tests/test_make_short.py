"""Unit tests for the pure parts of scripts/make_short.py (no Whisper, no ffmpeg).
Run from ai-editor/: python3 -m unittest discover -s tests"""
import io, os, sys, tempfile, unittest
from contextlib import redirect_stderr

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
import make_short as ms  # noqa: E402


def sent(words):
    """words: [(start, end, text)] -> sentence dict like transcribe() returns."""
    return {"start": words[0][0], "end": words[-1][1], "words": words}


WHISPER = [sent([(0.0, 0.4, "غوجو"), (0.4, 0.9, "ساتورو"), (0.9, 1.3, "ما"), (1.3, 1.8, "يتضرب")]),
           sent([(2.0, 2.5, "مو"), (2.5, 3.0, "لأنه"), (3.0, 3.6, "سريع")])]


class ApplyScript(unittest.TestCase):
    def test_keeps_timeline_and_uses_script_words(self):
        out = ms.apply_script(WHISPER, "غوجو ساتورو ما يتضرب.\nمو لأنه سريع؟")
        self.assertEqual(len(out), 2)
        self.assertEqual([w for _, _, w in out[1]["words"]], ["مو", "لأنه", "سريع"])
        self.assertAlmostEqual(out[0]["start"], 0.0)
        self.assertAlmostEqual(out[-1]["end"], 3.6)

    def test_word_times_never_go_backwards_or_zero(self):
        out = ms.apply_script(WHISPER, "كلمة " * 20)  # more script words than heard words
        ws = [w for s in out for w in s["words"]]
        self.assertEqual(len(ws), 20)
        for st, en, _ in ws:
            self.assertGreaterEqual(en - st, 0.12 - 1e-9)
        starts = [st for st, _, _ in ws]
        self.assertEqual(starts, sorted(starts))

    def test_empty_script_falls_back_to_whisper(self):
        with redirect_stderr(io.StringIO()):
            self.assertIs(ms.apply_script(WHISPER, "  \n "), WHISPER)


class PlanShots(unittest.TestCase):
    def test_cuts_on_sentence_starts_and_covers_all(self):
        sents = [sent([(t, t + 0.8, "x")]) for t in (0.0, 1.0, 2.0, 3.0, 4.0, 5.0)]
        shots = ms.plan_shots(sents, 3, 6.2)
        self.assertEqual(shots, [(0.0, 2.0), (2.0, 4.0), (4.0, 6.2)])

    def test_more_images_than_sentences(self):
        shots = ms.plan_shots(WHISPER, 6, 4.0)
        self.assertEqual(shots, [(0.0, 2.0), (2.0, 4.0)])


class Ass(unittest.TestCase):
    def test_time_format(self):
        self.assertEqual(ms.ass_time(0), "0:00:00.00")
        self.assertEqual(ms.ass_time(-1), "0:00:00.00")
        self.assertEqual(ms.ass_time(75.5), "0:01:15.50")

    def test_escape_strips_override_braces(self):
        self.assertEqual(ms.esc("{\\b1}x"), "(/b1)x")

    def test_build_ass_one_event_per_word_plus_title_and_sig(self):
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "s.ass")
            ms.build_ass(p, WHISPER, "عنوان", 4.0)
            with open(p, encoding="utf-8") as f:
                txt = f.read()
        caps = [l for l in txt.splitlines() if l.startswith("Dialogue: 2,")]
        self.assertEqual(len(caps), 7)
        self.assertIn(",Title,", txt)
        self.assertIn("Tokyo 503", txt)
        self.assertIn("Style: Cap,Tajawal ExtraBold,96", txt)

    def test_caption_box_style(self):
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "s.ass")
            ms.build_ass(p, WHISPER, "", 4.0, box=True)
            with open(p, encoding="utf-8") as f:
                txt = f.read()
        self.assertIn("Style: Cap,Tajawal ExtraBold,88", txt)
        self.assertNotIn(",Title,,", txt)


if __name__ == "__main__":
    unittest.main()
