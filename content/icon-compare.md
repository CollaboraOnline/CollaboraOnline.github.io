+++
title = "Icon Compare"
description = "Compare Collabora Online icon SVGs before and after a change"
date = "2026-06-08"
+++

<div class="icon-diff">
  <p class="lede">Compare an icon's <strong>before</strong> and <strong>after</strong> SVG, on light and dark backgrounds.</p>

  <div class="tip">
    Reviewing a whole Gerrit change? Run this in your <code>online</code> checkout to diff every icon at once, with usage info:
    <pre>./scripts/icon-before-after.py &lt;gerrit-change-url-or-number&gt;</pre>
  </div>

  <div class="inputs">
    <fieldset class="grp">
      <legend>Light <code>images/</code></legend>
      <div class="two">
        <div class="field">
          <label for="light-before">Before SVG</label>
          <textarea id="light-before" placeholder="&lt;svg ...&gt;...&lt;/svg&gt;" spellcheck="false"></textarea>
        </div>
        <div class="field">
          <label for="light-after">After SVG</label>
          <textarea id="light-after" placeholder="&lt;svg ...&gt;...&lt;/svg&gt;" spellcheck="false"></textarea>
        </div>
      </div>
    </fieldset>
    <fieldset class="grp">
      <legend>Dark <code>images/dark/</code></legend>
      <div class="two">
        <div class="field">
          <label for="dark-before">Before SVG</label>
          <textarea id="dark-before" placeholder="&lt;svg ...&gt;...&lt;/svg&gt;" spellcheck="false"></textarea>
        </div>
        <div class="field">
          <label for="dark-after">After SVG</label>
          <textarea id="dark-after" placeholder="&lt;svg ...&gt;...&lt;/svg&gt;" spellcheck="false"></textarea>
        </div>
      </div>
    </fieldset>
  </div>

  <div class="cards">
    <div class="card light">
      <h2>Light theme</h2>
      <div class="pair">
        <div class="slot">
          <div class="tag">Before</div>
          <span class="ico empty" id="lb"></span>
          <div class="sizes" id="lb-sizes"></div>
        </div>
        <div class="slot">
          <div class="tag">After</div>
          <span class="ico empty" id="la"></span>
          <div class="sizes" id="la-sizes"></div>
        </div>
      </div>
    </div>
    <div class="card dark">
      <h2>Dark theme</h2>
      <div class="pair">
        <div class="slot">
          <div class="tag">Before</div>
          <span class="ico empty" id="db"></span>
          <div class="sizes" id="db-sizes"></div>
        </div>
        <div class="slot">
          <div class="tag">After</div>
          <span class="ico empty" id="da"></span>
          <div class="sizes" id="da-sizes"></div>
        </div>
      </div>
    </div>
  </div>

  <section class="lookup">
    <h2 class="lookup-h">Find where this icon is used in the code</h2>
    <p class="lookup-sub">Separate from the diff above: enter the icon's name to locate its references in the Collabora Online sources.</p>
    <div class="field full">
      <label for="name">Icon name</label>
      <input type="text" id="name" placeholder="lc_autosum.svg  (or just: autosum)" autocomplete="off" spellcheck="false">
    </div>
    <p class="usage" id="usage"><span class="muted">Type an icon name to look up its usages.</span></p>
  </section>

  <p class="priv">Everything stays in your browser. No uploads, no network calls.</p>
</div>

<style>
  .icon-diff { font-family: system-ui, -apple-system, "Segoe UI", Roboto, sans-serif; color: #1a1a1a; }
  .icon-diff * { box-sizing: border-box; }
  .icon-diff .lede { color: #555; font-size: 0.95rem; margin: 0 0 1.5rem; line-height: 1.5; }
  .icon-diff code { font-family: ui-monospace, "SF Mono", Menlo, Consolas, monospace; }
  .icon-diff .lede code { background: #eee; padding: 0.05rem 0.3rem; border-radius: 4px; font-size: 0.85em; }

  .icon-diff .inputs { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-bottom: 1rem; }
  .icon-diff .grp { border: 1px solid #ddd; border-radius: 10px; padding: 0.75rem 1rem 1rem; margin: 0; }
  .icon-diff .grp legend { font-size: 0.8rem; font-weight: 600; opacity: 0.7; padding: 0 0.4rem; width: auto; border: 0; margin: 0; }
  .icon-diff .grp legend code { background: #eee; padding: 0.05rem 0.3rem; border-radius: 4px; font-size: 0.85em; font-weight: 400; }
  .icon-diff .two { display: grid; grid-template-columns: 1fr 1fr; gap: 0.75rem; }
  .icon-diff .field { display: flex; flex-direction: column; }
  .icon-diff .field.full { grid-column: 1 / -1; }
  .icon-diff label { font-size: 0.8rem; font-weight: 600; opacity: 0.7; margin-bottom: 0.3rem; }
  .icon-diff input[type=text], .icon-diff textarea {
    font-family: ui-monospace, "SF Mono", Menlo, Consolas, monospace;
    font-size: 0.82rem; padding: 0.55rem 0.7rem;
    border: 1px solid #ccc; border-radius: 8px; background: #fff; color: #1a1a1a; width: 100%;
  }
  .icon-diff textarea { min-height: 8.5rem; resize: vertical; line-height: 1.4; }
  .icon-diff input:focus, .icon-diff textarea:focus { outline: 2px solid #5c2983; border-color: #5c2983; }

  .icon-diff .tip { background: #efe7f3; border: 1px solid #d7c4e6; border-left: 4px solid #5c2983;
    border-radius: 8px; padding: 1rem 1.1rem; margin: 0 0 1.5rem; font-size: 0.92rem; line-height: 1.55; }
  /* !important: the Hugo theme's Bootstrap base styles `pre` with a light background, which would
     leave the light text unreadable. Force our dark-purple code block to win. */
  .icon-diff .tip pre { background: #2e1a47 !important; color: #efe7f3 !important; border: 0; border-radius: 6px;
    padding: 0.6rem 0.8rem; overflow-x: auto; font-size: 0.8rem; line-height: 1.4; margin: 0.5rem 0 0.2rem; }
  .icon-diff .tip pre code { background: none; color: inherit; padding: 0; }

  /* The "find usage" block is a concern separate from the SVG diff: a labelled,
     bordered box so it does not read as another diff input. */
  .icon-diff .lookup { border: 1px solid #ddd; border-radius: 10px; padding: 1.1rem 1.2rem; margin: 2.5rem 0 0; background: #fff; }
  .icon-diff .lookup-h { font-size: 1rem; font-weight: 700; margin: 0 0 0.25rem; color: #1a1a1a; }
  .icon-diff .lookup-sub { font-size: 0.85rem; color: #777; margin: 0 0 0.9rem; line-height: 1.45; }
  .icon-diff .usage { margin: 0.8rem 0 0; font-size: 0.9rem; }
  .icon-diff .usage a { color: #5c2983; text-decoration: none; font-weight: 600; }
  .icon-diff .usage a:hover { text-decoration: underline; }
  .icon-diff .usage .muted { color: #888; font-weight: 400; font-style: italic; }

  .icon-diff .cards { display: grid; grid-template-columns: 1fr 1fr; gap: 1.25rem; }
  .icon-diff .card { border-radius: 12px; padding: 1.25rem; }
  .icon-diff .card.light { background: #ffffff; border: 1px solid #e3e3e3; }
  .icon-diff .card.dark  { background: #1f1f1f; color: #f0f0f0; border: 1px solid #333; }
  .icon-diff .card h2 { margin: 0 0 1rem; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.05em; opacity: 0.6; }
  .icon-diff .pair { display: flex; gap: 1.5rem; align-items: flex-start; }
  .icon-diff .slot { flex: 1; text-align: center; }
  .icon-diff .slot .tag { font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.05em; opacity: 0.55; margin-bottom: 0.5rem; }
  .icon-diff .ico { display: inline-flex; align-items: center; justify-content: center; width: 48px; height: 48px; }
  .icon-diff .ico img { width: 100%; height: 100%; object-fit: contain; }
  .icon-diff .ico.empty { width: 48px; height: 48px; border: 1px dashed currentColor; border-radius: 6px; opacity: 0.25; }
  .icon-diff .sizes { margin-top: 1rem; display: flex; gap: 1rem; justify-content: center; align-items: flex-end; opacity: 0.9; }
  .icon-diff .sizes .s { text-align: center; }
  .icon-diff .sizes .s small { display: block; font-size: 0.6rem; opacity: 0.5; margin-top: 0.2rem; }

  .icon-diff .priv { margin-top: 2.5rem; font-size: 0.78rem; color: #999; line-height: 1.5; }

  @media (max-width: 720px) {
    .icon-diff .inputs, .icon-diff .cards, .icon-diff .two { grid-template-columns: 1fr; }
  }
</style>

<script>
  // Derive the command-ish stem from a pasted name, mirroring the CLI:
  //   browser/images/lc_autosum.svg -> autosum ; lc_autosum -> autosum
  function stemFromName(raw) {
    if (!raw) return '';
    var name = raw.trim().split(/[\\/]/).pop();         // drop any path
    name = name.replace(/\.(svg|png|jpe?g|gif)$/i, ''); // drop extension
    name = name.replace(/^(lc_|sc_|cmd_)/, '');         // drop theme/cmd prefix
    return name.trim();
  }

  // Render pasted SVG safely: as an <img> data URL it cannot run scripts or
  // fetch external resources, unlike injecting the markup into the DOM.
  function svgImg(text) {
    var t = (text || '').trim();
    if (!t || t.indexOf('<svg') === -1) return null;
    var img = document.createElement('img');
    img.src = 'data:image/svg+xml;charset=utf-8,' + encodeURIComponent(t);
    img.alt = '';
    return img;
  }

  function fillSlot(id, text) {
    var host = document.getElementById(id);
    var sizes = document.getElementById(id + '-sizes');
    host.innerHTML = '';
    sizes.innerHTML = '';
    var img = svgImg(text);
    if (!img) { host.classList.add('empty'); return; }
    host.classList.remove('empty');
    host.appendChild(img);
    // Also show the icon at the sizes it actually appears in the UI.
    [16, 24, 32].forEach(function (px) {
      var s = document.createElement('div'); s.className = 's';
      var ico = document.createElement('span'); ico.className = 'ico';
      ico.style.width = px + 'px'; ico.style.height = px + 'px';
      var i2 = svgImg(text); ico.appendChild(i2);
      var cap = document.createElement('small'); cap.textContent = px + 'px';
      s.appendChild(ico); s.appendChild(cap); sizes.appendChild(s);
    });
  }

  function updateUsage() {
    var stem = stemFromName(document.getElementById('name').value);
    var el = document.getElementById('usage');
    if (!stem) {
      el.innerHTML = '<span class="muted">Type an icon name above to look up its usages.</span>';
      return;
    }
    // Mirror the CLI scoping: browser/ sources only, minus the translation
    // catalogues (which mention every command label) and the icon files themselves.
    var q = 'repo:CollaboraOnline/online path:browser/ -path:browser/po/ -path:browser/images/ ' + stem;
    var url = 'https://github.com/search?type=code&q=' + encodeURIComponent(q);
    el.innerHTML = '🔍 Find where <strong>' + stem +
      '</strong> is used in <code>CollaboraOnline/online</code>: ' +
      '<a href="' + url + '" target="_blank" rel="noopener">search the browser/ sources on GitHub</a>';
  }

  function render() {
    fillSlot('lb', document.getElementById('light-before').value);
    fillSlot('la', document.getElementById('light-after').value);
    fillSlot('db', document.getElementById('dark-before').value);
    fillSlot('da', document.getElementById('dark-after').value);
    updateUsage();
  }

  ['name', 'light-before', 'light-after', 'dark-before', 'dark-after'].forEach(function (id) {
    document.getElementById(id).addEventListener('input', render);
  });
  render();
</script>
