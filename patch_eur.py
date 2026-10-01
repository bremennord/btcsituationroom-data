import pathlib
p = pathlib.Path(r'C:\bitcoin\site-v72\index.html')
s = p.read_text(encoding='utf-8')
if 'const fEk =' in s:
    print("Euro-Anzeige ist schon eingebaut")
    raise SystemExit
R = []
# 1) Hilfsfunktionen
R.append((r"""const fEUR = (v, d = 0) => v == null || !isFinite(v) ? '@E@@M@' : '@E@' + Number(v).toLocaleString('de-DE', { maximumFractionDigits: d });""",
 r"""const fEUR = (v, d = 0) => v == null || !isFinite(v) ? '@E@@M@' : '@E@' + Number(v).toLocaleString('de-DE', { maximumFractionDigits: d });
const fEk = (usd) => { const r = S && S.eurusd; if (!r || usd == null || !isFinite(usd)) return '@E@@M@'; const e = usd / r; return e >= 1e6 ? '@E@' + (e / 1e6).toFixed(2) + ' Mio' : '@E@' + Math.round(e / 1000) + 'k'; };
const eurLine = (lo, hi) => (S && S.eurusd) ? '<div style="font-size:13px;font-weight:500;color:var(--mu);margin-top:2px">' + fEk(lo) + ' @N@ ' + fEk(hi) + '</div>' : '';"""))
# 2) Kopfzeile: Dollar + Euro
R.append((r"""txt('h-px', fUSD(m.usd));""",
 r"""htm('h-px', fUSD(m.usd) + (m.eur ? ' <span style="font-size:13px;font-weight:500;color:var(--mu)">@D@ ' + fEUR(m.eur) + '</span>' : ''));"""))
# 3) Kachel: Euro zuerst in der Unterzeile
R.append((r"""`<span class="${cls(m.chg24)}">${fPct(m.chg24)}</span> @D@ ${fEUR(m.eur)}`""",
 r"""`${fEUR(m.eur)} @D@ <span class="${cls(m.chg24)}">${fPct(m.chg24)}</span>`"""))
# 4) Lage-Satz
R.append((r"""vom ATH ${fUSDk(pr.ATH)}.""", r"""vom ATH ${fUSDk(pr.ATH)} / ${fEk(pr.ATH)}."""))
R.append((r"""<b>${fUSDk(pr.bottom.low)}@N@${fUSDk(pr.bottom.high)}</b> (""", r"""<b>${fUSDk(pr.bottom.low)}@N@${fUSDk(pr.bottom.high)}</b> @D@ ${fEk(pr.bottom.low)}@N@${fEk(pr.bottom.high)} ("""))
R.append((r"""<b>${fUSDk(pr.peak.low)}@N@${fUSDk(pr.peak.high)}</b> (""", r"""<b>${fUSDk(pr.peak.low)}@N@${fUSDk(pr.peak.high)}</b> @D@ ${fEk(pr.peak.low)}@N@${fEk(pr.peak.high)} ("""))
# 5) Prognose-Karten: Boden und Peak
R.append((r"""txt('b-range', `${fUSDk(b.low)} @N@ ${fUSDk(b.high)}`);""", r"""htm('b-range', `${fUSDk(b.low)} @N@ ${fUSDk(b.high)}` + eurLine(b.low, b.high));"""))
R.append((r"""txt('p-range', `${fUSDk(p.low)} @N@ ${fUSDk(p.high)}`);""", r"""htm('p-range', `${fUSDk(p.low)} @N@ ${fUSDk(p.high)}` + eurLine(p.low, p.high));"""))
R.append((r"""`Schwerpunkt ${fUSD(Math.round(b.c / 500) * 500)} um""", r"""`Schwerpunkt ${fUSD(Math.round(b.c / 500) * 500)} (${fEk(b.c)}) um"""))
R.append((r"""`Schwerpunkt ${fUSDk(p.c)} um""", r"""`Schwerpunkt ${fUSDk(p.c)} (${fEk(p.c)}) um"""))
E, D, N, M = chr(0x20ac), chr(0xb7), chr(0x2013), chr(0x2014)
R = [(a.replace('@E@', E).replace('@D@', D).replace('@N@', N).replace('@M@', M), b.replace('@E@', E).replace('@D@', D).replace('@N@', N).replace('@M@', M)) for a, b in R]
n = 0
for old, new in R:
    if old in s:
        s = s.replace(old, new, 1)
        n += 1
    else:
        print("WARNUNG: Stelle nicht gefunden:", old[:60])
p.write_text(s, encoding='utf-8')
print("Euro neben Dollar eingebaut:", n, "von", len(R), "Stellen")
