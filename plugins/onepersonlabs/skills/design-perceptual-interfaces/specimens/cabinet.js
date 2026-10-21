/* A local specimen, not a production navigation system or a comprehension result.
   Geometry has one owner: displayed progress. Retargeting samples that value,
   so a new animation never restarts from an obsolete endpoint. */
"use strict";
(() => {
  const $ = (selector) => document.querySelector(selector);
  const root = $("#cabinet");
  const stage = $("#stage");
  const DURATION = 1200;
  const frames = { before: 0, response: 16 / DURATION, quarter: .25, mid: .5,
    late: .75, settled: 1, interrupted: .5, reversed: 0 };
  const scenes = {
    regroup: {
      kicker: "01 / OBJECT CONSTANCY", title: "A different arrangement. The same conversations.",
      apply: "Group by topic", invariant: "Six conversations keep their IDs, content and selected object. Position changes; identity does not. Times and topic labels remain readable in every frame.",
      hypothesis: "After a regrouping or interruption, can a person locate the selected conversation and tell that no conversation was added or lost?"
    },
    heading: {
      kicker: "02 / OBSERVATION & INFERENCE", title: "The estimate changes. The vessel does not.",
      apply: "Revise estimate", invariant: "The measured physical heading stays at 038°. An inferred useful heading is revised from 058° to 082°. The estimate snaps to the supported value; only the obsolete mark fades.",
      hypothesis: "Can a person distinguish an estimator revision from a physical turn, without watching the transition or knowing the legend in advance?"
    },
    relationship: {
      kicker: "03 / EVIDENCE STRENGTH", title: "A stronger case. Still an inference.",
      apply: "Add observations", invariant: "The same A–B association and endpoints remain. Support changes from 2 to 7 of 9 observations. This is provisional association, not certainty or established causation.",
      hypothesis: "Does the stronger link read as increased support for an existing relationship, without implying a new relationship or a proven cause?"
    }
  };
  const conversations = [
    { id: "c1", title: "Reading at a glance", time: "09:12", topic: "Interfaces" },
    { id: "c2", title: "Sensor notes", time: "09:28", topic: "Field notes" },
    { id: "c3", title: "Calm is a state", time: "09:44", topic: "Interfaces" },
    { id: "c4", title: "A sea trial", time: "10:03", topic: "Field notes" },
    { id: "c5", title: "More evidence", time: "10:26", topic: "Field notes" },
    { id: "c6", title: "Stable frames", time: "10:51", topic: "Interfaces" }
  ];
  const params = new URLSearchParams(location.search);
  const media = matchMedia("(prefers-reduced-motion: reduce)");
  const state = {
    scene: Object.hasOwn(scenes, params.get("scene")) ? params.get("scene") : "regroup",
    phase: "before", p: 0, target: 0, from: 0, selected: "c3", running: false,
    reduced: params.get("reduced") === "true" || params.get("reduced") === "1" || media.matches,
    variant: params.get("variant") === "replacement" ? "replacement" : "preserve",
    elapsed: 0, start: 0, duration: DURATION, replaced: false, readyVersion: 0
  };
  let raf = 0;
  const fmt = (n) => n.toFixed(4);
  const ease = (t) => t * t * (3 - 2 * t);
  function acknowledgeStableRender() {
    const version = ++state.readyVersion;
    root.dataset.captureReady = "false";
    requestAnimationFrame(() => requestAnimationFrame(() => {
      if (version === state.readyVersion && !state.running) root.dataset.captureReady = "true";
    }));
  }
  function createCards() {
    $("#objects").innerHTML = conversations.map((item) =>
      '<button class="conversation" data-object-id="' + item.id + '" aria-pressed="false">' +
      '<span class="object-id">' + item.id.toUpperCase() + '</span><span><strong>' + item.title +
      '</strong><small>' + item.time + ' · ' + item.topic + '</small></span><span class="selected-mark" aria-hidden="true"></span></button>'
    ).join("");
    stage.querySelectorAll("[data-object-id]").forEach((card) => {
      card.addEventListener("click", () => { state.selected = card.dataset.objectId; render(); acknowledgeStableRender(); });
    });
  }
  function buildScene() {
    const meta = scenes[state.scene];
    $("#scene-kicker").textContent = meta.kicker;
    $("#scene-title").textContent = meta.title;
    $("#apply").innerHTML = meta.apply + ' <span aria-hidden="true">→</span>';
    $("#invariant").textContent = meta.invariant;
    $("#hypothesis").textContent = meta.hypothesis;
    document.querySelectorAll("[data-scene]").forEach((button) =>
      button.setAttribute("aria-pressed", String(button.dataset.scene === state.scene)));
    const counterexample = state.variant === "replacement" && state.scene === "regroup";
    $("#variant-note").hidden = !counterexample;
    $("#variant-note").textContent = "COUNTEREXAMPLE · Fade and rebuild. Objects are recreated and selection resets at the midpoint. This handcrafted alternative exposes an identity failure; it is not a baseline-versus-skill experiment.";
    if (state.scene === "regroup") {
      stage.innerHTML = '<div class="stage-title"><strong id="arrangement"></strong><span>6 conversations · persistent IDs</span></div>' +
        '<span class="group-label" style="left:25%">INTERFACES</span><span class="group-label" style="left:75%">FIELD NOTES</span>' +
        '<div id="objects" role="group" aria-label="Conversations"></div>' +
        '<div class="legend"><span><i style="background:var(--accent)"></i> Selected conversation</span><span>Time + topic stay attached to each object</span></div>';
      createCards();
    } else if (state.scene === "heading") {
      stage.innerHTML = '<div class="stage-title"><strong>Fixed north-up reference</strong><span>Synthetic readings · current sample</span></div>' +
        '<svg class="diagram" viewBox="0 0 540 340" role="img" aria-label="Measured heading and separate inferred useful heading">' +
        '<circle cx="270" cy="164" r="114" fill="none" stroke="#c5cfc2"/><circle cx="270" cy="164" r="83" fill="none" stroke="#dce2d6" stroke-dasharray="2 8"/>' +
        '<path d="M270 39v12 M395 164h-12 M270 289v-12 M145 164h12" stroke="#89998a"/>' +
        '<text class="dial-label" x="270" y="29" text-anchor="middle">N / 000°</text><text class="dial-label" x="412" y="168">E</text>' +
        '<text class="dial-label" x="270" y="309" text-anchor="middle">S</text><text class="dial-label" x="122" y="168">W</text>' +
        '<g id="previous-estimate" class="ghost"><path d="M270 164V55"/><circle cx="270" cy="55" r="5"/></g>' +
        '<g id="estimate-marker" class="estimated"><path d="M270 164V55"/><circle cx="270" cy="55" r="7" fill="#f4f5ef"/></g>' +
        '<g id="physical-heading" class="observed" transform="rotate(38 270 164)" data-degrees="38"><path d="M270 184V78"/><path d="M262 91L270 74L278 91Z"/></g>' +
        '<circle cx="270" cy="164" r="5" fill="#24322d"/><rect x="20" y="247" width="125" height="69" rx="5" fill="#fefefa"/>' +
        '<text class="small" x="34" y="266">MEASURED HEADING</text><text class="readout" x="33" y="305">038°</text>' +
        '<rect x="365" y="247" width="155" height="69" rx="5" fill="#fefefa"/><text class="small" x="379" y="266">INFERRED USEFUL HEADING</text>' +
        '<text id="estimate-value" class="readout" x="379" y="305" style="fill:#9d3c23"></text></svg>' +
        '<div class="legend"><span><i></i> Observed physical heading</span><span><i class="inferred"></i> Inferred estimate</span><span><i class="previous"></i> Obsolete estimate, fading</span></div>';
    } else {
      stage.innerHTML = '<div class="stage-title"><strong>One association · A → B</strong><span>Fixed endpoints · synthetic evidence</span></div>' +
        '<svg class="diagram" viewBox="0 0 540 340" role="img" aria-label="One provisional association from interruptions to repeat glances">' +
        '<path id="association" class="association" data-edge-id="a-b" data-from="a" data-to="b" d="M154 164C228 95 312 95 386 164"/>' +
        '<circle class="node" cx="109" cy="192" r="54" data-node-id="a"/><circle class="node" cx="431" cy="192" r="54" data-node-id="b"/>' +
        '<text class="small" x="109" y="182" text-anchor="middle">A / OBSERVED</text><text class="node-label" x="109" y="205" text-anchor="middle">Interruptions</text>' +
        '<text class="small" x="431" y="182" text-anchor="middle">B / OBSERVED</text><text class="node-label" x="431" y="205" text-anchor="middle">Repeat glances</text>' +
        '<rect x="175" y="65" width="190" height="54" rx="5" fill="#fefefa" stroke="#d2dacd"/><text id="support-value" class="support-label" x="270" y="86" text-anchor="middle"></text>' +
        '<text class="small" x="270" y="104" text-anchor="middle">PROVISIONAL ASSOCIATION</text>' +
        '<text id="support-strength" class="small" x="270" y="271" text-anchor="middle"></text>' +
        '<text class="small" x="270" y="292" text-anchor="middle">Association does not establish causation.</text></svg>' +
        '<div class="legend"><span><i class="inferred"></i> Inferred relationship</span><span>Weight reinforces support; text gives the evidence</span></div>';
    }
  }
  function render() {
    root.dataset.scene = state.scene;
    root.dataset.phase = state.phase;
    root.dataset.captureState = state.scene + ":" + state.phase;
    root.dataset.mode = state.reduced ? "reduced" : "full";
    root.dataset.variant = state.variant;
    root.dataset.timeMs = String(Math.round(state.elapsed));
    root.dataset.clock = Object.hasOwn(frames, state.phase) ? "frozen-scenario" : "live-segment";
    root.dataset.progress = fmt(state.p);
    root.dataset.target = String(state.target);
    root.dataset.fromProgress = fmt(state.from);
    root.dataset.running = String(state.running);
    $("#frame-badge").textContent = state.phase.charAt(0).toUpperCase() + state.phase.slice(1);
    $("#frame-readout").textContent = Math.round(state.elapsed) + " ms · " + (state.running ? "live" : "frozen") + " · " + (state.reduced ? "reduced motion" : "full motion");
    $("#pause").textContent = state.running ? "Pause" : "Resume";
    $("#pause").disabled = !state.running && state.p === state.target;
    $("#reduced").checked = state.reduced;
    if (Object.hasOwn(frames, state.phase)) $("#phase").value = state.phase;
    if (state.scene === "regroup") {
      const replacement = state.variant === "replacement";
      const useAfter = state.p >= .5;
      if (replacement && useAfter !== state.replaced) {
        state.replaced = useAfter;
        state.selected = "c1";
        createCards();
      }
      const p = replacement ? (useAfter ? 1 : 0) : state.p;
      $("#arrangement").textContent = state.running || (state.p > 0 && state.p < 1)
        ? "Rearranging · target: " + (state.target ? "topic" : "chronology")
        : (state.p === 1 ? "Grouped by topic" : "Chronological order");
      stage.querySelectorAll(".group-label").forEach((label) => { label.style.visibility = p > .1 ? "visible" : "hidden"; });
      conversations.forEach((item, index) => {
        const card = stage.querySelector('[data-object-id="' + item.id + '"]');
        const x = 50 + ((item.topic === "Interfaces" ? 25 : 75) - 50) * p;
        const y = 88 + index * 55; // Retain the time axis: separated rows stay readable during regrouping.
        card.style.left = x + "%"; card.style.top = y + "px"; card.style.width = (68 - 24 * p) + "%";
        card.style.opacity = replacement ? String(Math.max(.12, Math.abs(1 - state.p * 2))) : "1";
        card.dataset.x = fmt(x); card.dataset.y = fmt(y);
        card.setAttribute("aria-pressed", String(item.id === state.selected));
        card.querySelector(".selected-mark").textContent = item.id === state.selected ? "●" : "";
      });
      const selected = conversations.find((item) => item.id === state.selected);
      $("#selection-detail").innerHTML = '<strong>Selected ' + selected.id.toUpperCase() + ' · ' + selected.title + '</strong> — ' +
        (replacement ? "counterexample rebuild can lose selection and focus." : "same object, same content, continuous position.");
      root.dataset.selectedId = state.selected;
    } else if (state.scene === "heading") {
      const estimate = state.target ? 82 : 58;
      const previous = state.target ? 58 : 82;
      // Never interpolate a bearing: the new inference is a discrete supported claim.
      $("#estimate-marker").setAttribute("transform", "rotate(" + estimate + " 270 164)");
      $("#estimate-marker").dataset.degrees = String(estimate);
      $("#estimate-value").textContent = String(estimate).padStart(3, "0") + "°";
      $("#previous-estimate").setAttribute("transform", "rotate(" + previous + " 270 164)");
      $("#previous-estimate").style.opacity = String(Math.abs(state.target - state.p) * .5);
      $("#selection-detail").innerHTML = "<strong>Observed 038° · inferred " + String(estimate).padStart(3, "0") + "°.</strong> Estimate valid for this synthetic sample; no physical turn is shown.";
      root.dataset.observedHeading = "38"; root.dataset.inferredHeading = String(estimate);
    } else {
      const support = state.target ? 7 : 2;
      $("#association").setAttribute("stroke-width", String(1.5 + state.p * 2.5));
      $("#association").setAttribute("opacity", String(.48 + state.p * .4));
      $("#support-value").textContent = support + " of 9 observations support A–B";
      $("#support-strength").textContent = state.target ? "Better supported · uncertainty remains" : "Weak support · uncertainty remains";
      $("#selection-detail").innerHTML = "<strong>Same association A–B · " + support + "/9 support.</strong> Synthetic sample count, not a calibrated probability.";
      root.dataset.supportCount = String(support); root.dataset.relationshipStatus = "provisional";
    }
  }
  function freeze(phase) {
    cancelAnimationFrame(raf);
    state.running = false; state.phase = phase; state.p = ease(frames[phase]);
    state.target = ["before", "reversed", "interrupted"].includes(phase) ? 0 : 1;
    state.from = phase === "interrupted" ? .5 : phase === "reversed" ? 1 : 0;
    state.elapsed = phase === "reversed" ? DURATION : frames[phase] * DURATION;
    // Reduced-motion captures show the semantic endpoint, not an animated intermediate.
    if (state.reduced) { state.p = state.target; state.elapsed = 0; }
    render(); acknowledgeStableRender();
  }
  function tick(now) {
    if (!state.running) return;
    const t = Math.min(1, (now - state.start) / state.duration);
    const eased = ease(t);
    state.p = state.from + (state.target - state.from) * eased;
    state.elapsed = Math.min(state.duration, now - state.start);
    if (t >= 1) {
      state.running = false; state.p = state.target;
      state.phase = state.target ? "settled" : "reversed";
      render(); acknowledgeStableRender();
      $("#announcement").textContent = state.target ? "Change complete." : "Original state restored.";
    } else { render(); raf = requestAnimationFrame(tick); }
  }
  function animateTo(target) {
    cancelAnimationFrame(raf);
    ++state.readyVersion; root.dataset.captureReady = "false";
    state.from = state.p; state.target = target; state.elapsed = 0;
    state.duration = DURATION; state.start = performance.now();
    state.running = !state.reduced && state.p !== target;
    state.phase = state.running ? "playing" : target ? "settled" : "reversed";
    if (!state.running) state.p = target;
    render();
    if (state.running) raf = requestAnimationFrame(tick);
    else acknowledgeStableRender();
  }
  $("#apply").addEventListener("click", () => animateTo(1));
  $("#reverse").addEventListener("click", () => animateTo(0));
  $("#retarget").addEventListener("click", () => animateTo(1 - state.target));
  $("#pause").addEventListener("click", () => {
    if (!state.running) { animateTo(state.target); return; }
    cancelAnimationFrame(raf); state.running = false; state.phase = "paused";
    render(); acknowledgeStableRender();
  });
  $("#phase").addEventListener("change", (event) => freeze(event.target.value));
  function setReduced(reduced) {
    state.reduced = reduced;
    if (reduced) {
      cancelAnimationFrame(raf); state.running = false; state.p = state.target;
      state.phase = state.target ? "settled" : "reversed";
    }
    render(); acknowledgeStableRender();
  }
  $("#reduced").addEventListener("change", (event) => setReduced(event.target.checked));
  media.addEventListener("change", (event) => setReduced(event.matches));
  document.querySelectorAll("[data-scene]").forEach((button) => button.addEventListener("click", () => {
    state.scene = button.dataset.scene; state.selected = "c3"; state.replaced = false;
    buildScene(); freeze("before");
  }));
  buildScene();
  freeze(Object.hasOwn(frames, params.get("phase")) ? params.get("phase") : "before");
})();



