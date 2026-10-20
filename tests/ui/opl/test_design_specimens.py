"""Real-browser specimen contracts; no model calls or browser installation.

Run: python -B tests/ui/opl/test_design_specimens.py
Set OPL_CHROMIUM_BIN if Chromium is not otherwise discoverable.
Set OPL_UI_EVIDENCE to save review screenshots outside the source tree.
"""
import os
from pathlib import Path
import shutil
import unittest
from urllib.parse import urlencode

from playwright.sync_api import sync_playwright, expect, Error as PlaywrightError

ROOT = Path(__file__).resolve().parents[3]
SPECIMEN = ROOT / "plugins/opl/skills/design-perceptual-interfaces/specimens/index.html"


class DesignSpecimenTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.playwright = sync_playwright().start()
        binary = os.environ.get("OPL_CHROMIUM_BIN") or shutil.which("chromium") or shutil.which("google-chrome")
        options = {"headless": True}
        try:
            if binary:
                cls.browser = cls.playwright.chromium.launch(executable_path=binary, **options)
                return
            if os.name == "nt":
                for channel in ("chrome", "msedge"):
                    try:
                        cls.browser = cls.playwright.chromium.launch(channel=channel, **options)
                        return
                    except PlaywrightError as error:
                        if f"Chromium distribution '{channel}' is not found" not in str(error):
                            raise
            if Path(cls.playwright.chromium.executable_path).is_file():
                cls.browser = cls.playwright.chromium.launch(**options)
                return
            raise RuntimeError("UI gate blocked: set OPL_CHROMIUM_BIN to an installed Chromium executable")
        except (PlaywrightError, RuntimeError):
            cls.playwright.stop()
            raise

    @classmethod
    def tearDownClass(cls):
        cls.browser.close()
        cls.playwright.stop()

    def setUp(self):
        self.context = self.browser.new_context(viewport={"width": 1360, "height": 1150})
        self.addCleanup(self.context.close)
        self.page = self.context.new_page()
        self.errors = []
        self.page.on("pageerror", lambda error: self.errors.append(str(error)))
        self.page.on("console", lambda message: self.errors.append(message.text) if message.type == "error" else None)

    def tearDown(self):
        self.assertEqual(self.errors, [])

    def open(self, scene="regroup", phase="before", **query):
        self.page.goto(SPECIMEN.as_uri() + "?" + urlencode({"scene": scene, "phase": phase, **query}))
        expect(self.page.locator("#cabinet")).to_have_attribute("data-capture-ready", "true")

    def data(self, name):
        return self.page.locator("#cabinet").get_attribute("data-" + name)

    def wait_settled(self, phase="settled"):
        expect(self.page.locator("#cabinet")).to_have_attribute("data-phase", phase)
        expect(self.page.locator("#cabinet")).to_have_attribute("data-capture-ready", "true")

    def capture(self, name):
        if directory := os.environ.get("OPL_UI_EVIDENCE"):
            path = Path(directory)
            path.mkdir(parents=True, exist_ok=True)
            self.page.screenshot(path=str(path / name), full_page=True)

    def test_regroup_preserves_objects_selection_focus_and_readable_frames(self):
        self.open()
        self.page.locator('[data-object-id="c5"]').click()
        self.page.evaluate("window.originalCards = [...document.querySelectorAll('[data-object-id]')]")
        self.page.locator("#apply").click()
        self.page.locator('[data-object-id="c5"]').focus()
        self.wait_settled()
        self.assertTrue(self.page.evaluate("window.originalCards.every(node => node === document.querySelector('[data-object-id=' + node.dataset.objectId + ']'))"))
        self.assertEqual(self.data("selected-id"), "c5")
        expect(self.page.locator('[data-object-id="c5"]')).to_be_focused()
        for phase in ("before", "quarter", "mid", "late", "settled"):
            self.page.locator("#phase").select_option(phase)
            expect(self.page.locator("#cabinet")).to_have_attribute("data-capture-ready", "true")
            boxes = self.page.locator("[data-object-id]").evaluate_all("(nodes) => nodes.map(node => {const r = node.getBoundingClientRect(); return {x:r.x,y:r.y,w:r.width,h:r.height}})")
            for i, a in enumerate(boxes):
                for b in boxes[i + 1:]:
                    self.assertFalse(a["x"] < b["x"] + b["w"] and b["x"] < a["x"] + a["w"] and a["y"] < b["y"] + b["h"] and b["y"] < a["y"] + a["h"])
        self.capture("design-regroup-settled.png")

    def test_live_interruption_retargets_displayed_state_then_reverses(self):
        self.open()
        self.page.locator("#apply").click()
        self.page.wait_for_function("Number(document.querySelector('#cabinet').dataset.progress) > .15")
        self.page.locator("#pause").click()
        expect(self.page.locator("#cabinet")).to_have_attribute("data-phase", "paused")
        paused = float(self.data("progress"))
        self.assertGreater(paused, 0)
        self.assertLess(paused, 1)
        self.page.locator("#retarget").click()
        self.assertAlmostEqual(float(self.data("from-progress")), paused, places=3)
        self.assertEqual(self.data("target"), "0")
        self.wait_settled("reversed")
        self.assertEqual(self.data("selected-id"), "c3")
        self.page.locator("#apply").click()
        self.page.wait_for_function("Number(document.querySelector('#cabinet').dataset.progress) > .15")
        # Reverse is a real control during motion, not a query-string snapshot.
        self.page.locator("#reverse").click()
        self.assertGreater(float(self.data("from-progress")), 0)
        self.wait_settled("reversed")
        self.assertEqual(float(self.data("progress")), 0)

    def test_heading_revision_never_moves_observed_heading_or_fabricates_bearings(self):
        self.open("heading")
        physical = self.page.locator("#physical-heading").get_attribute("transform")
        self.page.locator("#apply").click()
        self.page.wait_for_function("Number(document.querySelector('#cabinet').dataset.progress) > .1")
        self.assertEqual(self.data("observed-heading"), "38")
        self.assertEqual(self.data("inferred-heading"), "82")
        self.assertEqual(self.page.locator("#physical-heading").get_attribute("transform"), physical)
        self.page.locator("#retarget").click()
        self.assertEqual(self.data("inferred-heading"), "58")
        self.wait_settled("reversed")
        self.assertEqual(self.page.locator("#physical-heading").get_attribute("transform"), physical)
        self.page.locator("#phase").select_option("mid")
        self.assertEqual(self.page.locator("#estimate-marker").get_attribute("data-degrees"), "82")
        self.capture("design-heading-mid.png")

    def test_relationship_retains_one_edge_and_endpoints_without_certainty(self):
        self.open("relationship")
        self.page.evaluate("window.savedEdge = document.querySelector('#association')")
        original = self.page.locator("#association").get_attribute("d")
        self.page.locator("#apply").click()
        self.wait_settled()
        self.assertEqual(self.data("support-count"), "7")
        self.assertEqual(self.data("relationship-status"), "provisional")
        self.assertEqual(self.page.locator("[data-edge-id]").count(), 1)
        self.assertTrue(self.page.evaluate("window.savedEdge === document.querySelector('#association')"))
        self.assertEqual(self.page.locator("#association").get_attribute("d"), original)
        expect(self.page.locator("#association")).to_have_attribute("data-from", "a")
        expect(self.page.locator("#association")).to_have_attribute("data-to", "b")
        self.capture("design-relationship-settled.png")
        self.page.locator("#reverse").click()
        self.wait_settled("reversed")
        self.assertEqual(self.data("support-count"), "2")

    def test_reduced_motion_and_keyboard_keep_complete_semantics(self):
        self.page.emulate_media(reduced_motion="reduce")
        for scene in ("regroup", "heading", "relationship"):
            self.open(scene)
            self.assertEqual(self.data("mode"), "reduced")
            self.page.locator("#apply").focus()
            self.page.keyboard.press("Enter")
            self.wait_settled()
            self.assertEqual(float(self.data("progress")), 1)
            self.assertEqual(self.data("running"), "false")
            self.page.locator("#reverse").focus()
            self.page.keyboard.press("Enter")
            self.wait_settled("reversed")
            self.assertEqual(float(self.data("progress")), 0)
        self.open("heading", "mid", reduced="1")
        self.assertEqual(self.data("capture-state"), "heading:mid")
        self.assertEqual(self.data("inferred-heading"), "82")
        self.assertEqual(float(self.data("progress")), 1)

    def test_all_frozen_phases_report_state_and_mobile_has_no_overflow(self):
        phases = ("before", "response", "quarter", "mid", "late", "settled", "interrupted", "reversed")
        for scene in ("regroup", "heading", "relationship"):
            for phase in phases:
                self.open(scene, phase)
                self.assertEqual(self.data("capture-state"), scene + ":" + phase)
                self.assertEqual(self.data("running"), "false")
                self.assertGreaterEqual(int(self.data("time-ms")), 0)
                self.assertTrue(self.page.locator("#selection-detail").inner_text())
        self.page.set_viewport_size({"width": 390, "height": 844})
        self.open("regroup", "settled")
        self.assertTrue(self.page.evaluate("document.documentElement.scrollWidth <= innerWidth"))
        self.capture("design-mobile.png")

    def test_labeled_counterexample_recreates_nodes_and_loses_selection(self):
        self.open(variant="replacement")
        expect(self.page.locator("#variant-note")).to_contain_text("COUNTEREXAMPLE")
        self.page.evaluate("window.originalCard = document.querySelector('[data-object-id=c3]')")
        self.page.locator("#phase").select_option("settled")
        expect(self.page.locator("#cabinet")).to_have_attribute("data-capture-ready", "true")
        self.assertFalse(self.page.evaluate("window.originalCard === document.querySelector('[data-object-id=c3]')"))
        self.assertEqual(self.data("selected-id"), "c1")
        self.capture("design-counterexample.png")


if __name__ == "__main__":
    unittest.main(verbosity=1)

