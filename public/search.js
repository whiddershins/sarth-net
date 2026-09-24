// Search for sarth.net.
//
// Three jobs, all optional. The footer form works without any of this: it is
// a plain GET to /search/, so a browser with JavaScript off still searches.
//
//   1. On /search/, match against search-index.json and render results.
//   2. On a long index page, filter the cards already on screen. No index is
//      fetched for this: the text is in the DOM.
//   3. Anywhere, the / key focuses the footer box.
//
// The index is 80KB gzipped and only fetched when someone actually searches,
// so nobody pays for a search they did not run.

(function () {
  'use strict';

  var INDEX_URL = '/search-index.json';
  var indexPromise = null;

  function loadIndex() {
    if (!indexPromise) {
      indexPromise = fetch(INDEX_URL).then(function (r) {
        if (!r.ok) throw new Error('search index ' + r.status);
        return r.json();
      });
    }
    return indexPromise;
  }

  function tokenize(text) {
    return (text.toLowerCase().match(/[a-z0-9]+/g) || []).filter(function (t) {
      return t.length > 1;
    });
  }

  // Exact hits count fully; a word someone is still typing counts for less,
  // so results settle rather than jump as the query grows.
  function score(data, query) {
    var totals = Object.create(null);
    var terms = tokenize(query);
    if (!terms.length) return [];

    var tokens = Object.keys(data.index);

    terms.forEach(function (term) {
      var matches = [];
      if (data.index[term]) {
        matches.push([term, 1]);
      } else {
        for (var i = 0; i < tokens.length; i++) {
          if (tokens[i].indexOf(term) === 0) matches.push([tokens[i], 0.5]);
          if (matches.length >= 60) break;
        }
      }
      matches.forEach(function (pair) {
        data.index[pair[0]].forEach(function (posting) {
          totals[posting[0]] = (totals[posting[0]] || 0) + posting[1] * pair[1];
        });
      });
    });

    return Object.keys(totals)
      .map(function (id) {
        return { doc: data.docs[id], score: totals[id] };
      })
      .sort(function (a, b) {
        return b.score - a.score;
      });
  }

  function renderResults(container, results, query) {
    container.innerHTML = '';

    if (!query) {
      container.className = 'search-results';
      return;
    }

    if (!results.length) {
      var none = document.createElement('p');
      none.textContent = 'Nothing for “' + query + '”.';
      container.appendChild(none);
      return;
    }

    var count = document.createElement('p');
    count.className = 'search-count';
    count.textContent =
      results.length + (results.length === 1 ? ' page' : ' pages') + ' for “' + query + '”';
    container.appendChild(count);

    var list = document.createElement('ol');
    list.className = 'cards';
    results.slice(0, 40).forEach(function (hit) {
      var li = document.createElement('li');
      var a = document.createElement('a');
      a.href = hit.doc.r;

      var strong = document.createElement('strong');
      strong.textContent = hit.doc.t;
      a.appendChild(strong);

      if (hit.doc.d) {
        var span = document.createElement('span');
        span.textContent = hit.doc.d;
        a.appendChild(span);
      }

      li.appendChild(a);
      list.appendChild(li);
    });
    container.appendChild(list);
  }

  function searchPage() {
    var input = document.querySelector('[data-search-input]');
    var container = document.querySelector('[data-search-results]');
    if (!input || !container) return;

    var current = '';

    function run(query, pushState) {
      current = query;
      if (!query) {
        renderResults(container, [], '');
        return;
      }
      container.setAttribute('aria-busy', 'true');
      loadIndex().then(
        function (data) {
          // A later keystroke may have overtaken this one.
          if (current !== query) return;
          container.removeAttribute('aria-busy');
          renderResults(container, score(data, query), query);
        },
        function () {
          container.removeAttribute('aria-busy');
          container.textContent = 'The search index did not load. Every page is listed on the sitemap.';
        }
      );
      if (pushState) {
        var url = query ? '?q=' + encodeURIComponent(query) : location.pathname;
        history.replaceState(null, '', url);
      }
    }

    var timer = null;
    input.addEventListener('input', function () {
      clearTimeout(timer);
      var value = input.value.trim();
      timer = setTimeout(function () {
        run(value, true);
      }, 120);
    });

    // The form still submits without JavaScript; here it would only reload.
    var form = input.closest('form');
    if (form) {
      form.addEventListener('submit', function (e) {
        e.preventDefault();
        run(input.value.trim(), true);
      });
    }

    var initial = new URLSearchParams(location.search).get('q') || '';
    if (initial) {
      input.value = initial;
      run(initial, false);
    }
    input.focus();
  }

  // Narrowing a list that is already on the page. Nothing is fetched.
  function listFilter() {
    var input = document.querySelector('[data-list-filter]');
    if (!input) return;

    var lists = document.querySelectorAll('main ol.cards, main ul.press');
    if (!lists.length) return;

    var items = [];
    Array.prototype.forEach.call(lists, function (list) {
      Array.prototype.forEach.call(list.children, function (li) {
        items.push({ el: li, text: (li.textContent || '').toLowerCase() });
      });
    });

    var status = document.querySelector('[data-list-filter-status]');

    input.addEventListener('input', function () {
      var query = input.value.trim().toLowerCase();
      var shown = 0;

      items.forEach(function (item) {
        var match = !query || item.text.indexOf(query) !== -1;
        item.el.hidden = !match;
        if (match) shown++;
      });

      // A group whose every card is hidden goes too, heading and all,
      // otherwise a filter leaves a column of headings with nothing under
      // them. The heading may be a sibling rather than a wrapper: these
      // pages run h2, list, h2, list with no section elements.
      Array.prototype.forEach.call(lists, function (list) {
        var any = Array.prototype.some.call(list.children, function (li) {
          return !li.hidden;
        });
        var section = list.closest('section');
        if (section) {
          section.hidden = !any;
          return;
        }
        list.hidden = !any;
        var previous = list.previousElementSibling;
        if (previous && /^H[1-6]$/.test(previous.tagName)) {
          previous.hidden = !any;
        }
      });

      if (status) {
        status.textContent = query ? shown + ' of ' + items.length : '';
      }
    });
  }

  // Press / anywhere to reach the footer box.
  function slashShortcut() {
    document.addEventListener('keydown', function (e) {
      if (e.key !== '/' || e.metaKey || e.ctrlKey || e.altKey) return;
      var tag = (e.target.tagName || '').toLowerCase();
      if (tag === 'input' || tag === 'textarea' || e.target.isContentEditable) return;

      var box = document.querySelector('[data-list-filter]') ||
                document.querySelector('[data-search-input]') ||
                document.querySelector('.site-search input');
      if (!box) return;
      e.preventDefault();
      box.focus();
      box.select();
    });
  }

  function start() {
    searchPage();
    listFilter();
    slashShortcut();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', start);
  } else {
    start();
  }
})();
