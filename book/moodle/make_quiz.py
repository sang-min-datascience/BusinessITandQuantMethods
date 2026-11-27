"""Build a small Moodle XML sample of calculated questions (Session 1)."""
import random, html
random.seed(1)

def ds(name, lo, hi, dec, n=20):
    vals = [round(random.uniform(lo, hi), dec) for _ in range(n)]
    items = "".join(f"<dataset_item><number>{i+1}</number><value>{v}</value></dataset_item>" for i, v in enumerate(vals))
    return f"""<dataset_definition><status><text>private</text></status><name><text>{name}</text></name>
<type>calculated</type><distribution><text>uniform</text></distribution>
<minimum><text>{lo}</text></minimum><maximum><text>{hi}</text></maximum><decimals><text>{dec}</text></decimals>
<itemcount>{n}</itemcount><dataset_items>{items}</dataset_items><number_of_items>{n}</number_of_items></dataset_definition>"""

def q(name, text, formula, datasets, feedback, tol=0.01, decimals=2):
    return f"""<question type="calculated">
<name><text>{html.escape(name)}</text></name>
<questiontext format="html"><text><![CDATA[{text}]]></text></questiontext>
<generalfeedback format="html"><text><![CDATA[{feedback}]]></text></generalfeedback>
<defaultgrade>1</defaultgrade><penalty>0</penalty><hidden>0</hidden>
<synchronize>0</synchronize><single>0</single><answernumbering>abc</answernumbering><shuffleanswers>0</shuffleanswers>
<correctfeedback format="html"><text></text></correctfeedback>
<partiallycorrectfeedback format="html"><text></text></partiallycorrectfeedback>
<incorrectfeedback format="html"><text></text></incorrectfeedback>
<answer fraction="100"><text>{formula}</text><tolerance>{tol}</tolerance><tolerancetype>2</tolerancetype>
<correctanswerformat>1</correctanswerformat><correctanswerlength>{decimals}</correctanswerlength>
<feedback format="html"><text></text></feedback></answer>
<unitgradingtype>0</unitgradingtype><unitpenalty>0.1</unitpenalty><showunits>3</showunits><unitsleft>0</unitsleft>
<dataset_definitions>{"".join(datasets)}</dataset_definitions>
</question>"""

qs = [
 q("S1 VAT gross price",
   "<p>A tune-up costs €{net} net. VAT is 19&nbsp;%. What is the gross price in euros? Round to cents.</p>",
   "{net}*1.19", [ds("net", 20, 90, 0)],
   "<p>Gross = net × 1.19. See the chapter <em>Percentages</em>.</p>"),
 q("S1 Net from gross",
   "<p>A customer paid €{gross} including 19&nbsp;% VAT. What is the net price in euros? Round to cents.</p>",
   "{gross}/1.19", [ds("gross", 100, 900, 2)],
   "<p>Net = gross ÷ 1.19. Taking 19&nbsp;% off the gross price is wrong, because VAT is calculated on the net price.</p>"),
 q("S1 Two price changes",
   "<p>A price rises by {up}&nbsp;% and later falls by {down}&nbsp;%. By how many percent has it changed in total? Give a percentage (negative for a fall), rounded to two decimals, without the % sign.</p>",
   "((1+{up}/100)*(1-{down}/100)-1)*100", [ds("up", 5, 30, 0), ds("down", 5, 30, 0)],
   "<p>Multiply the growth factors: (1 + up) × (1 − down), then subtract 1.</p>"),
 q("S1 Average growth rate",
   "<p>Sales grew from €{start} to €{end} in {n} years. What was the average growth rate per year in percent? Round to two decimals, without the % sign.</p>",
   "(pow({end}/{start}, 1/{n})-1)*100", [ds("start", 40000, 60000, 0), ds("end", 65000, 90000, 0), ds("n", 2, 5, 0)],
   "<p>Average growth rate = (end ÷ start)<sup>1/n</sup> − 1.</p>"),
]

xml = '<?xml version="1.0" encoding="UTF-8"?>\n<quiz>\n<question type="category"><category><text>$course$/top/IBL103 Mathematics/Entry quiz 1 (sample)</text></category></question>\n' + "\n".join(qs) + "\n</quiz>\n"
import sys; open(sys.argv[1], "w", encoding="utf-8").write(xml)
