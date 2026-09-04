/* Next community call, in the reader's own timezone. The schedule comes from
 * data/meetings.yaml through the community-calls-data partial. Zones resolve
 * through Intl, so Europe/Berlin follows CET and CEST on its own.
 */
window.CommunityCalls = (function () {
  'use strict';

  var DAY = 86400000;

  function calls() {
    var node = document.getElementById('community-calls-data');
    if (!node) {
      return [];
    }
    try {
      var parsed = JSON.parse(node.textContent);
      return Array.isArray(parsed) ? parsed : [];
    } catch (e) {
      if (window.console) {
        console.error('community-calls: could not parse the schedule', e);
      }
      return [];
    }
  }

  function zoneOffset(utcMs, tz) {
    var parts = new Intl.DateTimeFormat('en-US', {
      timeZone: tz, hour12: false,
      year: 'numeric', month: '2-digit', day: '2-digit',
      hour: '2-digit', minute: '2-digit', second: '2-digit'
    }).formatToParts(new Date(utcMs));
    var p = {};
    parts.forEach(function (part) { p[part.type] = part.value; });
    var asIfUTC = Date.UTC(+p.year, p.month - 1, +p.day,
                           (+p.hour) % 24, +p.minute, +p.second);
    return asIfUTC - utcMs;
  }

  /* One correction pass covers the daylight-saving boundaries. */
  function wallToUTC(year, month, day, hh, mm, tz) {
    var guess = Date.UTC(year, month, day, hh, mm);
    return guess - zoneOffset(guess - zoneOffset(guess, tz), tz);
  }

  function dateKeyInZone(ms, tz) {
    var p = {};
    new Intl.DateTimeFormat('en-CA', {
      timeZone: tz, year: 'numeric', month: '2-digit', day: '2-digit'
    }).formatToParts(new Date(ms)).forEach(function (part) {
      p[part.type] = part.value;
    });
    return p.year + '-' + p.month + '-' + p.day;
  }

  function occurrences(days) {
    var list = calls();
    var out = [];
    var now = Date.now();
    for (var offset = -1; offset < (days || 9); offset++) {
      var probe = new Date(now + offset * DAY);
      for (var i = 0; i < list.length; i++) {
        var call = list[i];
        if (!call.time || !call.tz || !call.days) { continue; }
        var hhmm = String(call.time).split(':');
        var at = wallToUTC(probe.getUTCFullYear(), probe.getUTCMonth(),
                           probe.getUTCDate(), +hhmm[0], +hhmm[1], call.tz);
        var weekday = new Date(at + zoneOffset(at, call.tz)).getUTCDay();
        if (call.days.indexOf(weekday) === -1) { continue; }
        var key = dateKeyInZone(at, call.tz);
        if (call.from && key < call.from) { continue; }
        if (call.to && key > call.to) { continue; }
        var seen = false;
        for (var j = 0; j < out.length; j++) {
          if (out[j].at === at && out[j].name === call.name) { seen = true; break; }
        }
        if (!seen) {
          out.push({ at: at, name: call.name, url: call.url,
                     minutes: call.minutes || 60 });
        }
      }
    }
    out.sort(function (a, b) { return a.at - b.at; });
    return out;
  }

  /* `only` restricts the search to calls whose name contains that string. */
  function nextOrLive(list, only) {
    var now = Date.now();
    for (var i = 0; i < list.length; i++) {
      var occ = list[i];
      if (only && occ.name.indexOf(only) === -1) { continue; }
      if (now >= occ.at && now < occ.at + occ.minutes * 60000) {
        return { live: true, occ: occ };
      }
      if (occ.at > now) {
        return { live: false, occ: occ };
      }
    }
    return null;
  }

  function pad(n) { return n < 10 ? '0' + n : '' + n; }

  function countdown(ms) {
    var mins = Math.round((ms - Date.now()) / 60000);
    if (mins < 1) { return 'about to start'; }
    if (mins < 60) { return 'in ' + mins + ' min'; }
    if (mins < 1440) {
      return 'in ' + Math.floor(mins / 60) + ' h ' + pad(mins % 60) + ' min';
    }
    var days = Math.floor(mins / 1440);
    return 'in ' + days + (days === 1 ? ' day ' : ' days ')
      + Math.floor((mins % 1440) / 60) + ' h';
  }

  function localZone() {
    try { return Intl.DateTimeFormat().resolvedOptions().timeZone; }
    catch (e) { return ''; }
  }

  function shortWhen(ms) {
    return new Intl.DateTimeFormat(undefined, {
      weekday: 'short', hour: '2-digit', minute: '2-digit'
    }).format(new Date(ms));
  }

  function longWhen(ms) {
    return new Intl.DateTimeFormat(undefined, {
      weekday: 'long', day: 'numeric', month: 'long',
      hour: '2-digit', minute: '2-digit'
    }).format(new Date(ms));
  }

  return {
    occurrences: occurrences,
    nextOrLive: nextOrLive,
    countdown: countdown,
    localZone: localZone,
    shortWhen: shortWhen,
    longWhen: longWhen,
    DAY: DAY
  };
}());
