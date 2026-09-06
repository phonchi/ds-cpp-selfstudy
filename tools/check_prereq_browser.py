#!/usr/bin/env python3
"""Browser acceptance for P1–P9 (requires Playwright and installed Chromium).

Uses local file URLs and blocks external requests. Screenshots are optional.
Checks real controls, quiz feedback, cards, navigation and narrow-screen layout.
"""
import argparse
import json
from pathlib import Path
import re

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
CONTROLS = {
    "p1": ("play", "step", "reset", "status"),
    "p2": ("play", "step", "reset", "status"),
    "p3": ("play", "step", "reset", "status"),
    "p4": ("ptrPlay", "ptrNext", "ptrReset", "ptrNarration"),
    "p5": ("listPlay", "listNext", "listReset", "listNote"),
    "p6": ("mapPlay", "mapNext", "mapReset", "mapNote"),
    "p7": ("p7Play", "p7Step", "p7Reset", "p7Out"),
    "p8": ("p8Play", "p8Step", "p8Reset", "p8Out"),
    "p9": ("p9Play", "p9Step", "p9Reset", "p9Out"),
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--screenshots", type=Path)
    parser.add_argument("--pages", nargs="+", choices=list(CONTROLS))
    args = parser.parse_args()
    if args.screenshots:
        args.screenshots.mkdir(parents=True, exist_ok=True)
    reports = []
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True, timeout=15000,
                                     args=["--no-sandbox", "--disable-dev-shm-usage"])
        for chapter in args.pages or CONTROLS:
            path = next(ROOT.glob(f"{chapter}_*.html"))
            report = {"page": path.name, "errors": []}
            page = browser.new_page(viewport={"width": 1440, "height": 960})
            page.set_default_timeout(4000)
            page.on("pageerror", lambda error, r=report: r["errors"].append(str(error)))
            page.route(re.compile(r"^https?://"), lambda route: route.abort())
            # Accelerate only lesson intervals; still use actual browser timers.
            page.add_init_script("""(() => {
                const interval = window.setInterval.bind(window);
                window.setInterval = (fn, ms, ...args) =>
                    interval(fn, Math.min(ms, 120), ...args);
            })();""")
            try:
                page.goto(path.as_uri(), wait_until="load")
                play_id, step_id, reset_id, state_id = CONTROLS[chapter]
                play, step, reset = [page.locator("#" + key)
                                     for key in (play_id, step_id, reset_id)]
                state = page.locator("#" + state_id)
                initial = state.inner_text()
                assert "播放" in play.inner_text(), "initial play label"
                step.click()
                assert state.inner_text() != initial, "single step did not advance"
                reset.click()
                assert state.inner_text() == initial, "reset did not restore initial state"
                play.click()
                assert "暫停" in play.inner_text(), "playing button does not say pause"
                play.click()
                assert "播放" in play.inner_text(), "paused button does not say play"
                paused = state.inner_text()
                page.wait_for_timeout(300)
                assert state.inner_text() == paused, "paused animation keeps advancing"
                play.click()
                step.click()
                assert "暫停" not in play.inner_text(), "single step did not pause playback"
                reset.click()
                play.click()
                page.wait_for_function("id => document.getElementById(id).textContent.includes('重播')",
                                       arg=play_id)
                completed = state.inner_text()
                page.wait_for_timeout(300)
                assert state.inner_text() == completed, "completed animation keeps advancing"
                play.click()
                assert "暫停" in play.inner_text(), "completed playback did not restart"
                reset.click()
                page.wait_for_timeout(300)
                assert state.inner_text() == initial, "reset failed to cancel active timer"
                assert "播放" in play.inner_text(), "reset retained completed/playback label"
                if chapter == "p3":
                    for mode, expected in (("modeValue", "score = 20"), ("modeRef", "score = 30")):
                        page.locator("#" + mode).click()
                        play.click()
                        page.wait_for_function("() => document.getElementById('play').textContent.includes('重播')")
                        assert expected in state.inner_text(), f"{mode}: wrong caller value"
                    page.locator("#modeValue").click()
                    assert "播放" in play.inner_text(), "mode change retained completed label"
                report["player"] = "passed"

                questions = page.locator(".sq-item")
                assert questions.count(), "no quiz questions"
                correct_positions = []
                for number in range(questions.count()):
                    question = questions.nth(number)
                    buttons = question.locator('.sq-opt')
                    for option in range(buttons.count()):
                        button = buttons.nth(option)
                        correct = button.get_attribute("data-c") == "1"
                        cls = "correct" if correct else "wrong"
                        if correct:
                            correct_positions.append(option + 1)
                        button.click()
                        assert cls in (button.get_attribute("class") or ""), "quiz marking failed"
                        feedback = question.locator(".sq-fb")
                        assert feedback.is_visible(), "quiz feedback hidden"
                        assert feedback.inner_text() == button.get_attribute("data-fb"), "wrong feedback"
                report["quiz"] = questions.count()
                report["correct_positions"] = correct_positions
                cards = page.locator(".fc-card")
                count = cards.count()
                assert count, "flashcards missing"
                cards.first.click()
                assert "flipped" in cards.first.get_attribute("class"), "card did not flip"
                page.locator("#fcUnflip").click()
                assert page.locator(".fc-card.flipped").count() == 0, "cards did not turn front"
                page.locator("#fcFlipAll").click()
                assert page.locator(".fc-card.flipped").count() == count, "flip all failed"
                page.locator("#fcShuffle").click()
                assert cards.count() == count, "shuffle lost cards"
                report["cards"] = count
                assert page.locator(".chapter-nav a").count() >= 2, "chapter navigation missing"
                assert page.locator('.toc a[href="#reference"], .toc a[href="#quickref"]').count(), "REF missing from TOC"
                for width in (1440, 390):
                    page.set_viewport_size({"width": width, "height": 960})
                    page.wait_for_timeout(100)
                    overflow = page.evaluate("document.documentElement.scrollWidth > innerWidth + 2")
                    assert not overflow, f"page overflows {width}px viewport"
                    page.evaluate("window.scrollTo({top: 0, behavior: 'instant'})")
                    if args.screenshots:
                        page.screenshot(path=str(args.screenshots / f"{chapter}-{width}.png"))
                report["layout"] = "1440px and 390px passed"
            except Exception as exc:
                report["errors"].append(str(exc))
            page.close()
            reports.append(report)
            print(json.dumps(report, ensure_ascii=False), flush=True)
        browser.close()
    return any(report["errors"] for report in reports)


if __name__ == "__main__":
    raise SystemExit(main())
