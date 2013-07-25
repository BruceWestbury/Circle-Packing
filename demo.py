
"""

Most of this section is taken up with knots and braids.
However the functions in this package have been designed to
work with general ribbon graphs. First we have some ribbon graphs
which are not knots or braids.

>>> g = spider.RibbonGraph.vertex(4)
>>> g.show('Tk')


.. raw:: html

    <html>
    <body>
    <svg xmlns="http://www.w3.org/2000/svg" version="1.1" width="500" height="500">
    <title>A Link Diagram</title>
    <desc>A link diagram produced using circle packing.</desc>
    <defs>
      <marker id="Arrow" markerWidth="5" markerHeight="10"
        refX="5" refY="5" orient="auto">
        <path d="M 0 0 5 5 0 10 Z" style="fill: blue;"/>
      </marker>
    </defs>
    <line x1="449.583671" y1="50.407486" x2="349.953028" y2="50.271204" style = "stroke: black ;"/>
    <line x1="450.000000" y1="449.916802" x2="449.949475" y2="349.951217" style = "stroke: black ;"/>
    <line x1="250.030093" y1="449.988658" x2="250.024952" y2="349.992442" style = "stroke: red ;"/>
    <line x1="50.123062" y1="50.000005" x2="50.071806" y2="149.975259" style = "stroke: black ;"/>
    <line x1="250.078309" y1="50.128512" x2="250.028956" y2="150.055558" style = "stroke: red ;"/>
    <line x1="50.031275" y1="249.969904" x2="150.027490" y2="249.985012" style = "stroke: red ;"/>
    <line x1="449.987405" y1="249.924637" x2="349.964380" y2="250.039878" style = "stroke: red ;"/>
    <line x1="250.023395" y1="250.035480" x2="250.024952" y2="349.992442" style = "stroke: red ;"/>
    <line x1="250.030093" y1="449.988658" x2="350.024742" y2="449.958094" style = "stroke: black ;"/>
    <line x1="250.078309" y1="50.128512" x2="150.135754" y2="50.010765" style = "stroke: black ;"/>
    <line x1="50.031275" y1="249.969904" x2="50.009970" y2="349.975807" style = "stroke: black ;"/>
    <line x1="250.023395" y1="250.035480" x2="150.027490" y2="249.985012" style = "stroke: red ;"/>
    <line x1="449.987405" y1="249.924637" x2="449.788168" y2="149.963420" style = "stroke: black ;"/>
    <line x1="250.023395" y1="250.035480" x2="349.964380" y2="250.039878" style = "stroke: red ;"/>
    <line x1="250.023395" y1="250.035480" x2="250.028956" y2="150.055558" style = "stroke: red ;"/>
    <line x1="50.000000" y1="449.999995" x2="150.024188" y2="449.999995" style = "stroke: black ;"/>
    <line x1="250.078309" y1="50.128512" x2="349.953028" y2="50.271204" style = "stroke: black ;"/>
    <line x1="449.987405" y1="249.924637" x2="449.949475" y2="349.951217" style = "stroke: black ;"/>
    <line x1="50.031275" y1="249.969904" x2="50.071806" y2="149.975259" style = "stroke: black ;"/>
    <line x1="450.000000" y1="449.916802" x2="350.024742" y2="449.958094" style = "stroke: black ;"/>
    <line x1="50.123062" y1="50.000005" x2="150.135754" y2="50.010765" style = "stroke: black ;"/>
    <line x1="50.000000" y1="449.999995" x2="50.009970" y2="349.975807" style = "stroke: black ;"/>
    <line x1="449.583671" y1="50.407486" x2="449.788168" y2="149.963420" style = "stroke: black ;"/>
    <line x1="250.030093" y1="449.988658" x2="150.024188" y2="449.999995" style = "stroke: black ;"/>
    </svg>
    </body>
    </html>

>>> g = spider.RibbonGraph.polygon(5)
>>> g.show('Tk')

.. raw:: html

    <html>
    <body>

    <svg xmlns="http://www.w3.org/2000/svg" version="1.1" width="500" height="500">

    <title>A Link Diagram</title>
    <desc>A link diagram produced using circle packing.</desc>

    <defs>
      <marker id="Arrow" markerWidth="5" markerHeight="10"
        refX="5" refY="5" orient="auto">
        <path d="M 0 0 5 5 0 10 Z" style="fill: blue;"/>
      </marker>
    </defs>
    <line x1="250.077882" y1="440.381251" x2="317.460995" y2="440.366983" style = "stroke: black ;"/>
    <line x1="88.187499" y1="322.733040" x2="109.011366" y2="386.856244" style = "stroke: black ;"/>
    <line x1="150.095800" y1="132.358021" x2="95.547580" y2="172.010495" style = "stroke: black ;"/>
    <line x1="350.553328" y1="132.627890" x2="296.069979" y2="92.783164" style = "stroke: black ;"/>
    <line x1="411.808436" y1="322.838711" x2="432.525580" y2="258.881236" style = "stroke: black ;"/>
    <line x1="250.077882" y1="440.381251" x2="250.086460" y2="375.314598" style = "stroke: red ;"/>
    <line x1="88.187499" y1="322.733040" x2="150.100700" y2="302.631635" style = "stroke: red ;"/>
    <line x1="150.095800" y1="132.358021" x2="188.352768" y2="185.042057" style = "stroke: red ;"/>
    <line x1="350.553328" y1="132.627890" x2="312.135953" y2="185.257357" style = "stroke: red ;"/>
    <line x1="411.808436" y1="322.838711" x2="350.030733" y2="302.755155" style = "stroke: red ;"/>
    <line x1="287.684431" y1="218.623208" x2="250.199349" y2="217.295313" style = "stroke: red ;"/>
    <line x1="310.723168" y1="289.956335" x2="300.422674" y2="253.948566" style = "stroke: red ;"/>
    <line x1="189.475533" y1="289.851233" x2="150.100700" y2="302.631635" style = "stroke: red ;"/>
    <line x1="287.684431" y1="218.623208" x2="312.135953" y2="185.257357" style = "stroke: red ;"/>
    <line x1="250.097780" y1="333.931965" x2="250.086460" y2="375.314598" style = "stroke: red ;"/>
    <line x1="310.723168" y1="289.956335" x2="350.030733" y2="302.755155" style = "stroke: red ;"/>
    <line x1="250.097780" y1="333.931965" x2="219.042988" y2="312.937886" style = "stroke: red ;"/>
    <line x1="189.475533" y1="289.851233" x2="199.838188" y2="253.815944" style = "stroke: red ;"/>
    <line x1="212.689089" y1="218.545853" x2="250.199349" y2="217.295313" style = "stroke: red ;"/>
    <line x1="287.684431" y1="218.623208" x2="300.422674" y2="253.948566" style = "stroke: red ;"/>
    <line x1="212.689089" y1="218.545853" x2="188.352768" y2="185.042057" style = "stroke: red ;"/>
    <line x1="310.723168" y1="289.956335" x2="281.173959" y2="312.977549" style = "stroke: red ;"/>
    <line x1="250.097780" y1="333.931965" x2="281.173959" y2="312.977549" style = "stroke: red ;"/>
    <line x1="189.475533" y1="289.851233" x2="219.042988" y2="312.937886" style = "stroke: red ;"/>
    <line x1="212.689089" y1="218.545853" x2="199.838188" y2="253.815944" style = "stroke: red ;"/>
    <line x1="126.399943" y1="440.386567" x2="182.681436" y2="440.386567" style = "stroke: black ;"/>
    <line x1="50.000000" y1="205.071414" x2="67.372569" y2="258.606935" style = "stroke: black ;"/>
    <line x1="250.317111" y1="59.613433" x2="204.724993" y2="92.703221" style = "stroke: black ;"/>
    <line x1="450.000000" y1="205.739608" x2="404.872380" y2="172.560928" style = "stroke: black ;"/>
    <line x1="373.694223" y1="440.350966" x2="391.049527" y2="386.872627" style = "stroke: black ;"/>
    <line x1="373.694223" y1="440.350966" x2="317.460995" y2="440.366983" style = "stroke: black ;"/>
    <line x1="126.399943" y1="440.386567" x2="109.011366" y2="386.856244" style = "stroke: black ;"/>
    <line x1="50.000000" y1="205.071414" x2="95.547580" y2="172.010495" style = "stroke: black ;"/>
    <line x1="250.317111" y1="59.613433" x2="296.069979" y2="92.783164" style = "stroke: black ;"/>
    <line x1="450.000000" y1="205.739608" x2="432.525580" y2="258.881236" style = "stroke: black ;"/>
    <line x1="250.077882" y1="440.381251" x2="182.681436" y2="440.386567" style = "stroke: black ;"/>
    <line x1="88.187499" y1="322.733040" x2="67.372569" y2="258.606935" style = "stroke: black ;"/>
    <line x1="150.095800" y1="132.358021" x2="204.724993" y2="92.703221" style = "stroke: black ;"/>
    <line x1="350.553328" y1="132.627890" x2="404.872380" y2="172.560928" style = "stroke: black ;"/>
    <line x1="411.808436" y1="322.838711" x2="391.049527" y2="386.872627" style = "stroke: black ;"/>
    </svg>

    </body>
    </html>

>>> f = spider.RibbonGraph.vertex(4)
>>> g = spider.RibbonGraph.vertex(3)
>>> spider.glue(f,g,0).show('Tk')

.. raw:: html

    <html>
    <body>

    <svg xmlns="http://www.w3.org/2000/svg" version="1.1" width="500" height="500">

    <title>A Link Diagram</title>
    <desc>A link diagram produced using circle packing.</desc>

    <defs>
      <marker id="Arrow" markerWidth="5" markerHeight="10"
        refX="5" refY="5" orient="auto">
        <path d="M 0 0 5 5 0 10 Z" style="fill: blue;"/>
      </marker>
    </defs>
    <line x1="399.287455" y1="229.156889" x2="420.420570" y2="224.339301" style = "stroke: red ;"/>
    <line x1="138.102237" y1="288.660427" x2="174.422674" y2="329.480853" style = "stroke: red ;"/>
    <line x1="138.102237" y1="288.660427" x2="153.169345" y2="236.144594" style = "stroke: red ;"/>
    <line x1="399.287455" y1="229.156889" x2="398.550008" y2="255.347897" style = "stroke: red ;"/>
    <line x1="138.102237" y1="288.660427" x2="94.605302" y2="270.945712" style = "stroke: red ;"/>
    <line x1="399.287455" y1="229.156889" x2="387.276337" y2="205.879928" style = "stroke: red ;"/>
    <line x1="115.925226" y1="391.534290" x2="140.515609" y2="391.534290" style = "stroke: black ;"/>
    <line x1="50.000000" y1="308.690359" x2="61.239030" y2="322.812957" style = "stroke: black ;"/>
    <line x1="73.632415" y1="205.555449" x2="68.502297" y2="227.953652" style = "stroke: black ;"/>
    <line x1="275.595805" y1="108.460687" x2="215.973364" y2="137.125731" style = "stroke: black ;"/>
    <line x1="434.337168" y1="185.026279" x2="420.819015" y2="178.506779" style = "stroke: black ;"/>
    <line x1="450.000000" y1="253.752901" x2="446.889058" y2="240.114436" style = "stroke: black ;"/>
    <line x1="340.101907" y1="391.539313" x2="379.528315" y2="342.105749" style = "stroke: black ;"/>
    <line x1="199.375768" y1="391.534675" x2="273.941087" y2="391.536649" style = "stroke: black ;"/>
    <line x1="80.899578" y1="347.518337" x2="101.597051" y2="373.528251" style = "stroke: black ;"/>
    <line x1="61.084733" y1="260.336942" x2="54.034470" y2="291.102514" style = "stroke: black ;"/>
    <line x1="148.787943" y1="169.425659" x2="95.762403" y2="194.915986" style = "stroke: black ;"/>
    <line x1="384.299045" y1="160.893223" x2="332.544767" y2="135.930297" style = "stroke: black ;"/>
    <line x1="442.161851" y1="219.382655" x2="437.442403" y2="198.665917" style = "stroke: black ;"/>
    <line x1="415.357864" y1="297.183429" x2="440.641107" y2="265.485747" style = "stroke: black ;"/>
    <line x1="138.102237" y1="288.660427" x2="106.545499" y2="323.448355" style = "stroke: red ;"/>
    <line x1="199.375768" y1="391.534675" x2="174.422674" y2="329.480853" style = "stroke: red ;"/>
    <line x1="80.899578" y1="347.518337" x2="106.545499" y2="323.448355" style = "stroke: red ;"/>
    <line x1="61.084733" y1="260.336942" x2="94.605302" y2="270.945712" style = "stroke: red ;"/>
    <line x1="148.787943" y1="169.425659" x2="153.169345" y2="236.144594" style = "stroke: red ;"/>
    <line x1="384.299045" y1="160.893223" x2="387.276337" y2="205.879928" style = "stroke: red ;"/>
    <line x1="442.161851" y1="219.382655" x2="420.420570" y2="224.339301" style = "stroke: red ;"/>
    <line x1="415.357864" y1="297.183429" x2="398.550008" y2="255.347897" style = "stroke: red ;"/>
    <line x1="199.375768" y1="391.534675" x2="140.515609" y2="391.534290" style = "stroke: black ;"/>
    <line x1="80.899578" y1="347.518337" x2="61.239030" y2="322.812957" style = "stroke: black ;"/>
    <line x1="61.084733" y1="260.336942" x2="68.502297" y2="227.953652" style = "stroke: black ;"/>
    <line x1="148.787943" y1="169.425659" x2="215.973364" y2="137.125731" style = "stroke: black ;"/>
    <line x1="384.299045" y1="160.893223" x2="420.819015" y2="178.506779" style = "stroke: black ;"/>
    <line x1="442.161851" y1="219.382655" x2="446.889058" y2="240.114436" style = "stroke: black ;"/>
    <line x1="415.357864" y1="297.183429" x2="379.528315" y2="342.105749" style = "stroke: black ;"/>
    <line x1="340.101907" y1="391.539313" x2="273.941087" y2="391.536649" style = "stroke: black ;"/>
    <line x1="115.925226" y1="391.534290" x2="101.597051" y2="373.528251" style = "stroke: black ;"/>
    <line x1="50.000000" y1="308.690359" x2="54.034470" y2="291.102514" style = "stroke: black ;"/>
    <line x1="73.632415" y1="205.555449" x2="95.762403" y2="194.915986" style = "stroke: black ;"/>
    <line x1="275.595805" y1="108.460687" x2="332.544767" y2="135.930297" style = "stroke: black ;"/>
    <line x1="434.337168" y1="185.026279" x2="437.442403" y2="198.665917" style = "stroke: black ;"/>
    <line x1="450.000000" y1="253.752901" x2="440.641107" y2="265.485747" style = "stroke: black ;"/>
    </svg>

    </body>
    </html>

Next we come to knots.

This illustrates the construction of a link diagram
as the link closure of a braid.

>>> knots.LinkDiagram.from_braid([1,1,1]).show('Tk')

.. raw:: html

    <html>
    <body>

    <svg xmlns="http://www.w3.org/2000/svg" version="1.1" width="500" height="500">

    <title>A Link Diagram</title>
    <desc>A link diagram produced using circle packing.</desc>

    <defs>
      <marker id="Arrow" markerWidth="5" markerHeight="10"
        refX="5" refY="5" orient="auto">
        <path d="M 0 0 5 5 0 10 Z" style="fill: blue;"/>
      </marker>
    </defs>
    <line x1="354.818493" y1="215.516288" x2="234.948213" y2="236.349613" style = "stroke: blue ; marker-end: url(\#Arrow);"/>
    <line x1="137.614440" y1="236.349613" x2="234.948213" y2="236.349613" style = "stroke: blue ;"/>
    <line x1="342.659432" y1="236.597312" x2="294.023188" y2="320.921407" style = "stroke: blue ;"/>
    <line x1="239.953556" y1="414.089934" x2="191.212000" y2="329.782317" style = "stroke: blue ;"/>
    <line x1="113.280996" y1="236.349613" x2="191.212000" y2="329.782317" style = "stroke: blue ; marker-end: url(\#Arrow);"/>
    <line x1="100.624797" y1="274.767017" x2="50.000000" y2="428.436631" style = "stroke: blue ; marker-end: url(\#Arrow);"/>
    <line x1="327.883134" y1="185.379663" x2="220.141698" y2="64.833162" style = "stroke: blue ; marker-end: url(\#Arrow);"/>
    <line x1="252.138945" y1="435.166838" x2="294.023188" y2="320.921407" style = "stroke: blue ; marker-end: url(\#Arrow);"/>
    <line x1="291.711156" y1="426.905254" x2="450.000000" y2="393.858920" style = "stroke: blue ; marker-end: url(\#Arrow);"/>
    <line x1="252.138945" y1="435.166838" x2="50.000000" y2="428.436631" style = "stroke: blue ;"/>
    <line x1="113.280996" y1="236.349613" x2="220.141698" y2="64.833162" style = "stroke: blue ;"/>
    <line x1="354.818493" y1="215.516288" x2="450.000000" y2="393.858920" style = "stroke: blue ;"/>
    </svg>

    </body>
    </html>

A knot can also be constructed from a
Dowker-Thistlewaite code. Here are some
examples:

>>> g = knots.LinkDiagram.from_DT(knots.DT([4,6,2]))
>>> g.show('Tk')

.. raw:: html

    <html>
    <body>

    <svg xmlns="http://www.w3.org/2000/svg" version="1.1" width="500" height="500">

    <title>A Link Diagram</title>
    <desc>A link diagram produced using circle packing.</desc>

    <defs>
      <marker id="Arrow" markerWidth="5" markerHeight="10"
        refX="5" refY="5" orient="auto">
        <path d="M 0 0 5 5 0 10 Z" style="fill: blue;"/>
      </marker>
    </defs>
    <line x1="398.481837" y1="262.356014" x2="267.268689" y2="50.000000" style = "stroke: blue ; marker-end: url(\#Arrow);"/>
    <line x1="101.518163" y1="236.651360" x2="233.293066" y2="236.651360" style = "stroke: blue ; marker-end: url(\#Arrow);"/>
    <line x1="249.934165" y1="249.946232" x2="231.215140" y2="260.144616" style = "stroke: blue ;"/>
    <line x1="398.481837" y1="262.356014" x2="266.387898" y2="263.082074" style = "stroke: blue ;"/>
    <line x1="246.605945" y1="247.287258" x2="233.293066" y2="236.651360" style = "stroke: blue ;"/>
    <line x1="101.518163" y1="236.651360" x2="231.603644" y2="450.000000" style = "stroke: blue ;"/>
    <line x1="249.934165" y1="249.946232" x2="268.624639" y2="239.731242" style = "stroke: blue ; marker-end: url(\#Arrow);"/>
    <line x1="253.224912" y1="252.573401" x2="266.387898" y2="263.082074" style = "stroke: blue ; marker-end: url(\#Arrow);"/>
    <line x1="372.510397" y1="257.831060" x2="268.624639" y2="239.731242" style = "stroke: blue ;"/>
    <line x1="127.457559" y1="241.350011" x2="231.215140" y2="260.144616" style = "stroke: blue ; marker-end: url(\#Arrow);"/>
    <line x1="134.668268" y1="199.321088" x2="267.268689" y2="50.000000" style = "stroke: blue ;"/>
    <line x1="365.106198" y1="299.884812" x2="231.603644" y2="450.000000" style = "stroke: blue ; marker-end: url(\#Arrow);"/>
    </svg>

    </body>
    </html>


>>> g = knots.LinkDiagram.from_DT(knots.DT([4,6,8,2]))
>>> g.show('Tk')

.. raw:: html

    <html>
    <body>

    <svg xmlns="http://www.w3.org/2000/svg" version="1.1" width="500" height="500">

    <title>A Link Diagram</title>
    <desc>A link diagram produced using circle packing.</desc>

    <defs>
      <marker id="Arrow" markerWidth="5" markerHeight="10"
        refX="5" refY="5" orient="auto">
        <path d="M 0 0 5 5 0 10 Z" style="fill: blue;"/>
      </marker>
    </defs>
    <line x1="270.030266" y1="450.000000" x2="433.676012" y2="450.000000" style = "stroke: blue ;"/>
    <line x1="270.866718" y1="304.272075" x2="251.280251" y2="273.741442" style = "stroke: blue ;"/>
    <line x1="404.478572" y1="255.776242" x2="318.419603" y2="296.532649" style = "stroke: blue ;"/>
    <line x1="170.882540" y1="199.333093" x2="66.323988" y2="325.867148" style = "stroke: blue ;"/>
    <line x1="276.892737" y1="319.589420" x2="281.410350" y2="350.328164" style = "stroke: blue ; marker-end: url(\#Arrow);"/>
    <line x1="197.022178" y1="167.699579" x2="251.280251" y2="273.741442" style = "stroke: blue ; marker-end: url(\#Arrow);"/>
    <line x1="219.632652" y1="176.369857" x2="310.074549" y2="211.050968" style = "stroke: blue ; marker-end: url(\#Arrow);"/>
    <line x1="413.760845" y1="206.469713" x2="364.830965" y2="50.000000" style = "stroke: blue ; marker-end: url(\#Arrow);"/>
    <line x1="229.118830" y1="450.000000" x2="281.410350" y2="350.328164" style = "stroke: blue ;"/>
    <line x1="232.879123" y1="427.799647" x2="247.920295" y2="338.998235" style = "stroke: blue ; marker-end: url(\#Arrow);"/>
    <line x1="275.763334" y1="311.904733" x2="247.920295" y2="338.998235" style = "stroke: blue ;"/>
    <line x1="425.993314" y1="245.587141" x2="310.074549" y2="211.050968" style = "stroke: blue ;"/>
    <line x1="275.763334" y1="311.904733" x2="318.419603" y2="296.532649" style = "stroke: blue ; marker-end: url(\#Arrow);"/>
    <line x1="425.993314" y1="245.587141" x2="433.676012" y2="450.000000" style = "stroke: blue ; marker-end: url(\#Arrow);"/>
    <line x1="229.118830" y1="450.000000" x2="66.323988" y2="325.867148" style = "stroke: blue ; marker-end: url(\#Arrow);"/>
    <line x1="197.022178" y1="167.699579" x2="364.830965" y2="50.000000" style = "stroke: blue ;"/>
    </svg>

    </body>
    </html>
    
>>> g = knots.LinkDiagram.from_DT(knots.DT([4,8,10,2,6]))
>>> g.show('Tk')

.. raw:: html

    <html>
    <body>

    <svg xmlns="http://www.w3.org/2000/svg" version="1.1" width="500" height="500">

    <title>A Link Diagram</title>
    <desc>A link diagram produced using circle packing.</desc>

    <defs>
      <marker id="Arrow" markerWidth="5" markerHeight="10"
        refX="5" refY="5" orient="auto">
        <path d="M 0 0 5 5 0 10 Z" style="fill: blue;"/>
      </marker>
    </defs>
    <line x1="246.576925" y1="237.448481" x2="245.697960" y2="246.626232" style = "stroke: blue ;"/>
    <line x1="248.179855" y1="249.774807" x2="249.757014" y2="246.092886" style = "stroke: blue ;"/>
    <line x1="249.646823" y1="262.077469" x2="235.459185" y2="267.628476" style = "stroke: blue ;"/>
    <line x1="249.025822" y1="260.341236" x2="246.541820" y2="253.396303" style = "stroke: blue ;"/>
    <line x1="243.553690" y1="237.068798" x2="231.460749" y2="235.550068" style = "stroke: blue ;"/>
    <line x1="368.309669" y1="233.636971" x2="260.674783" y2="231.647397" style = "stroke: blue ;"/>
    <line x1="395.218390" y1="234.134364" x2="264.737354" y2="264.240346" style = "stroke: blue ;"/>
    <line x1="248.654498" y1="250.368096" x2="250.553070" y2="252.741253" style = "stroke: blue ;"/>
    <line x1="130.917125" y1="267.628476" x2="235.459185" y2="267.628476" style = "stroke: blue ; marker-end: url(\#Arrow);"/>
    <line x1="104.781610" y1="267.628476" x2="231.460749" y2="235.550068" style = "stroke: blue ; marker-end: url(\#Arrow);"/>
    <line x1="247.212943" y1="239.177362" x2="249.757014" y2="246.092886" style = "stroke: blue ; marker-end: url(\#Arrow);"/>
    <line x1="252.664929" y1="262.510044" x2="264.737354" y2="264.240346" style = "stroke: blue ; marker-end: url(\#Arrow);"/>
    <line x1="246.576925" y1="237.448481" x2="260.674783" y2="231.647397" style = "stroke: blue ; marker-end: url(\#Arrow);"/>
    <line x1="247.683476" y1="249.145092" x2="245.697960" y2="246.626232" style = "stroke: blue ; marker-end: url(\#Arrow);"/>
    <line x1="395.218390" y1="234.134364" x2="221.281144" y2="50.000000" style = "stroke: blue ; marker-end: url(\#Arrow);"/>
    <line x1="248.179855" y1="249.774807" x2="246.541820" y2="253.396303" style = "stroke: blue ; marker-end: url(\#Arrow);"/>
    <line x1="104.781610" y1="267.628476" x2="271.139424" y2="450.000000" style = "stroke: blue ;"/>
    <line x1="249.646823" y1="262.077469" x2="250.553070" y2="252.741253" style = "stroke: blue ; marker-end: url(\#Arrow);"/>
    <line x1="128.081517" y1="224.102781" x2="221.281144" y2="50.000000" style = "stroke: blue ;"/>
    <line x1="370.402597" y1="277.307492" x2="271.139424" y2="450.000000" style = "stroke: blue ; marker-end: url(\#Arrow);"/>
    </svg>

    </body>
    </html>


>>> g = knots.LinkDiagram.from_DT(knots.DT([8,10,2,12,4,6]))
>>> g.show('Tk')

.. raw:: html

    <html>
    <body>

    <svg xmlns="http://www.w3.org/2000/svg" version="1.1" width="500" height="500">

    <title>A Link Diagram</title>
    <desc>A link diagram produced using circle packing.</desc>

    <defs>
      <marker id="Arrow" markerWidth="5" markerHeight="10"
        refX="5" refY="5" orient="auto">
        <path d="M 0 0 5 5 0 10 Z" style="fill: blue;"/>
      </marker>
    </defs>
    <line x1="180.116594" y1="254.759457" x2="180.047596" y2="231.020272" style = "stroke: blue ; marker-end: url(\#Arrow);"/>
    <line x1="210.113710" y1="365.898218" x2="192.895325" y2="288.507220" style = "stroke: blue ; marker-end: url(\#Arrow);"/>
    <line x1="192.013450" y1="210.530767" x2="162.880632" y2="201.290311" style = "stroke: blue ;"/>
    <line x1="180.116594" y1="254.759457" x2="192.895325" y2="288.507220" style = "stroke: blue ;"/>
    <line x1="88.146490" y1="201.290311" x2="162.880632" y2="201.290311" style = "stroke: blue ; marker-end: url(\#Arrow);"/>
    <line x1="189.620279" y1="214.628668" x2="180.047596" y2="231.020272" style = "stroke: blue ;"/>
    <line x1="183.334897" y1="250.873617" x2="196.208108" y2="235.330258" style = "stroke: blue ;"/>
    <line x1="65.570363" y1="234.003705" x2="50.000000" y2="364.857282" style = "stroke: blue ;"/>
    <line x1="392.906971" y1="287.410793" x2="324.296867" y2="210.367436" style = "stroke: blue ;"/>
    <line x1="244.754748" y1="398.190863" x2="366.100516" y2="449.970441" style = "stroke: blue ;"/>
    <line x1="404.325576" y1="256.498884" x2="450.000000" y2="132.851248" style = "stroke: blue ;"/>
    <line x1="373.359770" y1="294.015939" x2="295.170966" y2="320.436522" style = "stroke: blue ; marker-end: url(\#Arrow);"/>
    <line x1="197.568092" y1="205.952084" x2="219.786663" y2="187.637354" style = "stroke: blue ; marker-end: url(\#Arrow);"/>
    <line x1="255.955107" y1="101.577837" x2="134.679100" y2="50.029559" style = "stroke: blue ;"/>
    <line x1="286.274108" y1="114.464907" x2="219.786663" y2="187.637354" style = "stroke: blue ;"/>
    <line x1="174.148470" y1="253.438181" x2="150.275970" y2="248.153078" style = "stroke: blue ; marker-end: url(\#Arrow);"/>
    <line x1="293.878660" y1="133.645413" x2="324.296867" y2="210.367436" style = "stroke: blue ; marker-end: url(\#Arrow);"/>
    <line x1="69.462954" y1="201.290311" x2="150.275970" y2="248.153078" style = "stroke: blue ;"/>
    <line x1="214.418306" y1="385.245968" x2="295.170966" y2="320.436522" style = "stroke: blue ;"/>
    <line x1="192.013450" y1="210.530767" x2="196.208108" y2="235.330258" style = "stroke: blue ; marker-end: url(\#Arrow);"/>
    <line x1="214.418306" y1="385.245968" x2="50.000000" y2="364.857282" style = "stroke: blue ; marker-end: url(\#Arrow);"/>
    <line x1="392.906971" y1="287.410793" x2="366.100516" y2="449.970441" style = "stroke: blue ; marker-end: url(\#Arrow);"/>
    <line x1="286.274108" y1="114.464907" x2="450.000000" y2="132.851248" style = "stroke: blue ; marker-end: url(\#Arrow);"/>
    <line x1="69.462954" y1="201.290311" x2="134.679100" y2="50.029559" style = "stroke: blue ; marker-end: url(\#Arrow);"/>
    </svg>

    </body>
    </html>

There are two ways this diagram can be embellished with information
about the knot diagram. First we can draw the diagram with the arcs
of the diagram in different colours:

>>> g = knots.LinkDiagram.from_DT(knots.DT([8,10,2,12,4,6]))
>>> g.witharcs().show('SVG')

.. raw:: html

    <html>
    <body>

    <svg xmlns="http://www.w3.org/2000/svg" version="1.1" width="500" height="500">

    <title>A Link Diagram</title>
    <desc>A link diagram produced using circle packing.</desc>

    <defs>
      <marker id="Arrow" markerWidth="5" markerHeight="10"
        refX="5" refY="5" orient="auto">
        <path d="M 0 0 5 5 0 10 Z" style="fill: blue;"/>
      </marker>
    </defs>
    <line x1="245.090505" y1="244.507483" x2="251.429447" y2="222.959863" style = "stroke: green ;"/>
    <line x1="360.954562" y1="104.310382" x2="50.000000" y2="106.301687" style = "stroke: brown ; marker-end: url(\#Arrow);"/>
    <line x1="145.318281" y1="395.689618" x2="450.000000" y2="395.689618" style = "stroke: orange ; marker-end: url(\#Arrow);"/>
    <line x1="145.318281" y1="395.689618" x2="226.777988" y2="256.270228" style = "stroke: orange ;"/>
    <line x1="166.960020" y1="372.248657" x2="253.526977" y2="278.484811" style = "stroke: red ; marker-end: url(\#Arrow);"/>
    <line x1="265.677199" y1="259.324090" x2="265.530309" y2="255.801338" style = "stroke: purple ; marker-end: url(\#Arrow);"/>
    <line x1="266.347127" y1="258.910058" x2="269.026841" y2="257.253928" style = "stroke: blue ; marker-end: url(\#Arrow);"/>
    <line x1="269.708608" y1="249.857499" x2="260.859856" y2="246.585959" style = "stroke: blue ; marker-end: url(\#Arrow);"/>
    <line x1="257.843484" y1="265.890287" x2="253.526977" y2="278.484811" style = "stroke: red ;"/>
    <line x1="265.677199" y1="259.324090" x2="264.717731" y2="263.076627" style = "stroke: purple ;"/>
    <line x1="269.708608" y1="249.857499" x2="269.026841" y2="257.253928" style = "stroke: blue ;"/>
    <line x1="264.978520" y1="259.501834" x2="262.183806" y2="260.212809" style = "stroke: red ;"/>
    <line x1="360.954562" y1="104.310382" x2="280.491722" y2="242.048611" style = "stroke: brown ;"/>
    <line x1="268.872948" y1="251.046267" x2="265.530309" y2="255.801338" style = "stroke: purple ;"/>
    <line x1="339.049539" y1="128.040278" x2="251.429447" y2="222.959863" style = "stroke: green ; marker-end: url(\#Arrow);"/>
    <line x1="245.090505" y1="244.507483" x2="252.157573" y2="258.556682" style = "stroke: green ; marker-end: url(\#Arrow);"/>
    <line x1="257.843484" y1="265.890287" x2="262.183806" y2="260.212809" style = "stroke: red ; marker-end: url(\#Arrow);"/>
    <line x1="256.706302" y1="264.423566" x2="252.157573" y2="258.556682" style = "stroke: green ;"/>
    <line x1="248.244375" y1="244.923178" x2="260.859856" y2="246.585959" style = "stroke: blue ;"/>
    <line x1="259.218333" y1="265.327555" x2="264.717731" y2="263.076627" style = "stroke: purple ; marker-end: url(\#Arrow);"/>
    <line x1="241.428002" y1="246.860032" x2="226.777988" y2="256.270228" style = "stroke: orange ; marker-end: url(\#Arrow);"/>
    <line x1="271.865231" y1="248.295722" x2="280.491722" y2="242.048611" style = "stroke: brown ; marker-end: url(\#Arrow);"/>
    <line x1="126.254625" y1="337.812032" x2="50.000000" y2="106.301687" style = "stroke: brown ;"/>
    <line x1="378.763650" y1="162.586229" x2="450.000000" y2="395.689618" style = "stroke: orange ;"/>
    </svg>

    </body>
    </html>
Second we can draw the diagram with the
`Seifert circles <http://mathworld.wolfram.com/SeifertCircle.html>`_ of the diagram in different colours:


>>> g = knots.LinkDiagram.from_DT(knots.DT([8,10,2,12,4,6]))
>>> g.withseifert().show('SVG')

.. raw:: html

    <html>
    <body>

    <svg xmlns="http://www.w3.org/2000/svg" version="1.1" width="500" height="500">

    <title>A Link Diagram</title>
    <desc>A link diagram produced using circle packing.</desc>

    <defs>
      <marker id="Arrow" markerWidth="5" markerHeight="10"
        refX="5" refY="5" orient="auto">
        <path d="M 0 0 5 5 0 10 Z" style="fill: blue;"/>
      </marker>
    </defs>
    <line x1="370.301330" y1="256.018779" x2="267.243465" y2="237.785664" style = "stroke: blue ; marker-end: url(\#Arrow);"/>
    <line x1="251.390813" y1="245.210194" x2="255.318267" y2="254.601734" style = "stroke: green ;"/>
    <line x1="396.065796" y1="260.577058" x2="266.904587" y2="265.950077" style = "stroke: blue ;"/>
    <line x1="248.485101" y1="263.351960" x2="245.467443" y2="264.214762" style = "stroke: blue ;"/>
    <line x1="240.688624" y1="260.555537" x2="246.462673" y2="261.255137" style = "stroke: green ; marker-end: url(\#Arrow);"/>
    <line x1="256.818686" y1="262.006708" x2="251.321517" y2="264.581426" style = "stroke: blue ;"/>
    <line x1="249.052384" y1="263.597853" x2="251.321517" y2="264.581426" style = "stroke: blue ; marker-end: url(\#Arrow);"/>
    <line x1="255.656958" y1="261.938478" x2="251.010043" y2="261.665560" style = "stroke: green ;"/>
    <line x1="248.080616" y1="262.932595" x2="246.462673" y2="261.255137" style = "stroke: green ;"/>
    <line x1="241.252267" y1="259.157537" x2="243.506838" y2="253.565534" style = "stroke: green ;"/>
    <line x1="250.408950" y1="242.862309" x2="243.506838" y2="253.565534" style = "stroke: green ; marker-end: url(\#Arrow);"/>
    <line x1="256.818686" y1="262.006708" x2="255.318267" y2="254.601734" style = "stroke: green ; marker-end: url(\#Arrow);"/>
    <line x1="240.688624" y1="260.555537" x2="230.119508" y2="262.697289" style = "stroke: blue ;"/>
    <line x1="241.644388" y1="261.287382" x2="245.467443" y2="264.214762" style = "stroke: blue ; marker-end: url(\#Arrow);"/>
    <line x1="103.934204" y1="234.912638" x2="234.725330" y2="234.912638" style = "stroke: blue ;"/>
    <line x1="258.835866" y1="262.795382" x2="266.904587" y2="265.950077" style = "stroke: blue ; marker-end: url(\#Arrow);"/>
    <line x1="250.408950" y1="242.862309" x2="267.243465" y2="237.785664" style = "stroke: blue ;"/>
    <line x1="396.065796" y1="260.577058" x2="267.372331" y2="50.000000" style = "stroke: red ; marker-end: url(\#Arrow);"/>
    <line x1="248.485101" y1="263.351960" x2="251.010043" y2="261.665560" style = "stroke: green ; marker-end: url(\#Arrow);"/>
    <line x1="129.171265" y1="240.469568" x2="230.119508" y2="262.697289" style = "stroke: blue ; marker-end: url(\#Arrow);"/>
    <line x1="103.934204" y1="234.912638" x2="234.178723" y2="450.000000" style = "stroke: red ; marker-end: url(\#Arrow);"/>
    <line x1="247.272226" y1="241.272375" x2="234.725330" y2="234.912638" style = "stroke: blue ; marker-end: url(\#Arrow);"/>
    <line x1="136.621829" y1="197.930110" x2="267.372331" y2="50.000000" style = "stroke: red ;"/>
    <line x1="363.688381" y1="298.461646" x2="234.178723" y2="450.000000" style = "stroke: red ;"/>
    </svg>

    </body>
    </html>

The other options for drawing show auxilliary information which
comes from the circle packing method which is used to construct
the drawing.

The first option shows the circles in the circle packing:

>>> g = knots.LinkDiagram.from_DT(knots.DT([4,6,2]))
>>> g.show('Tk',withcircles=True)
>>> g = knots.LinkDiagram.from_DT(knots.DT([4,6,8,2]))
>>> g.show('Tk',withcircles=True)
>>> g = knots.LinkDiagram.from_DT(knots.DT([4,8,10,2,6]))
>>> g.show('Tk',withcircles=True)
>>> g = knots.LinkDiagram.from_DT(knots.DT([8,10,2,12,4,6]))
>>> g.show('Tk',withcircles=True)

The second option shows the triangulation of the oriented surface.
The first stage of the circle packing algorithm is to construct
this as a combinatorial triangulation.

>>> g = knots.LinkDiagram.from_DT(knots.DT([4,6,2]))
>>> g.show('Tk',withtriangles=True)
>>> g = knots.LinkDiagram.from_DT(knots.DT([4,6,8,2]))
>>> g.show('Tk',withtriangles=True)
>>> g = knots.LinkDiagram.from_DT(knots.DT([4,8,10,2,6]))
>>> g.show('Tk',withtriangles=True)
>>> g = knots.LinkDiagram.from_DT(knots.DT([8,10,2,12,4,6]))
>>> g.show('Tk',withtriangles=True)

The third option draws a polygon in each face. This is for
illustrative purposes only.

>>> g = knots.LinkDiagram.from_DT(knots.DT([4,6,2]))
>>> g.show('Tk',medial=True)
>>> g = knots.LinkDiagram.from_DT(knots.DT([4,6,8,2]))
>>> g.show('Tk',medial=True)
>>> g = knots.LinkDiagram.from_DT(knots.DT([4,8,10,2,6]))
>>> g.show('Tk',medial=True)
>>> g = knots.LinkDiagram.from_DT(knots.DT([8,10,2,12,4,6]))
>>> g.show('Tk',medial=True)

The fourth option shows the radical circles. Each triangle
determines three circles with no two concentric. This determines
a radical centre whose centre is the radical centre of the three
circles. The default is for each pair of circles to be tangent.
In this case the radical circle is the incircle of the triangle.

>>> g = knots.LinkDiagram.from_DT(knots.DT([4,6,2]))
>>> g.show('Tk',withradicalcircles=True)
>>> g = knots.LinkDiagram.from_DT(knots.DT([4,6,8,2]))
>>> g.show('Tk',withradicalcircles=True)
>>> g = knots.LinkDiagram.from_DT(knots.DT([4,8,10,2,6]))
>>> g.show('Tk',withradicalcircles=True)
>>> g = knots.LinkDiagram.from_DT(knots.DT([8,10,2,12,4,6]))
>>> g.show('Tk',withradicalcircles=True)

Next we come to braids. First we illustrate the basic construction
of braids.

>>> s1 = pivotal.Artin_generator(3,1)
>>> s1.show('Tk')

.. raw:: html

    <html>
    <body>

    <svg xmlns="http://www.w3.org/2000/svg" version="1.1" width="500" height="500">

    <title>A Link Diagram</title>
    <desc>A link diagram produced using circle packing.</desc>

    <defs>
      <marker id="Arrow" markerWidth="5" markerHeight="10"
        refX="5" refY="5" orient="auto">
        <path d="M 0 0 5 5 0 10 Z" style="fill: blue;"/>
      </marker>
    </defs>
    <line x1="269.387582" y1="316.193086" x2="305.365706" y2="316.178241" style = "stroke: black ;"/>
    <line x1="300.570199" y1="256.060938" x2="281.998003" y2="279.700832" style = "stroke: blue ;"/>
    <line x1="269.090351" y1="184.205556" x2="225.139456" y2="184.402736" style = "stroke: black ;"/>
    <line x1="50.676175" y1="316.215123" x2="115.036518" y2="316.215123" style = "stroke: black ;"/>
    <line x1="305.213249" y1="250.150964" x2="281.879014" y2="220.652670" style = "stroke: blue ; marker-end: url(\#Arrow);"/>
    <line x1="309.869147" y1="244.250753" x2="328.492741" y2="220.649907" style = "stroke: blue ; marker-end: url(\#Arrow);"/>
    <line x1="170.927054" y1="184.650555" x2="171.658178" y2="232.753264" style = "stroke: blue ;"/>
    <line x1="341.551566" y1="316.146240" x2="386.525425" y2="316.088459" style = "stroke: black ;"/>
    <line x1="171.762157" y1="250.441550" x2="171.748535" y2="268.129344" style = "stroke: blue ;"/>
    <line x1="341.318535" y1="184.026191" x2="328.492741" y2="220.649907" style = "stroke: blue ;"/>
    <line x1="305.213249" y1="250.150964" x2="328.600140" y2="279.566910" style = "stroke: blue ;"/>
    <line x1="449.758103" y1="183.784877" x2="386.288764" y2="183.923243" style = "stroke: black ;"/>
    <line x1="170.927054" y1="184.650555" x2="114.649196" y2="184.934400" style = "stroke: black ;"/>
    <line x1="50.000000" y1="185.264150" x2="50.337495" y2="250.870587" style = "stroke: black ;"/>
    <line x1="171.276444" y1="316.212670" x2="171.748535" y2="268.129344" style = "stroke: blue ; marker-end: url(\#Arrow);"/>
    <line x1="171.276444" y1="316.212670" x2="225.455650" y2="316.203897" style = "stroke: black ;"/>
    <line x1="450.000000" y1="315.999979" x2="449.901520" y2="249.906370" style = "stroke: black ;"/>
    <line x1="269.090351" y1="184.205556" x2="281.879014" y2="220.652670" style = "stroke: blue ;"/>
    <line x1="269.387582" y1="316.193086" x2="281.998003" y2="279.700832" style = "stroke: blue ; marker-end: url(\#Arrow);"/>
    <line x1="341.551566" y1="316.146240" x2="328.600140" y2="279.566910" style = "stroke: blue ; marker-end: url(\#Arrow);"/>
    <line x1="341.318535" y1="184.026191" x2="305.083078" y2="184.050084" style = "stroke: black ;"/>
    <line x1="171.762157" y1="250.441550" x2="171.658178" y2="232.753264" style = "stroke: blue ; marker-end: url(\#Arrow);"/>
    <line x1="341.551566" y1="316.146240" x2="305.365706" y2="316.178241" style = "stroke: black ;"/>
    <line x1="170.927054" y1="184.650555" x2="225.139456" y2="184.402736" style = "stroke: black ;"/>
    <line x1="171.276444" y1="316.212670" x2="115.036518" y2="316.215123" style = "stroke: black ;"/>
    <line x1="450.000000" y1="315.999979" x2="386.525425" y2="316.088459" style = "stroke: black ;"/>
    <line x1="341.318535" y1="184.026191" x2="386.288764" y2="183.923243" style = "stroke: black ;"/>
    <line x1="50.000000" y1="185.264150" x2="114.649196" y2="184.934400" style = "stroke: black ;"/>
    <line x1="50.676175" y1="316.215123" x2="50.337495" y2="250.870587" style = "stroke: black ;"/>
    <line x1="269.387582" y1="316.193086" x2="225.455650" y2="316.203897" style = "stroke: black ;"/>
    <line x1="449.758103" y1="183.784877" x2="449.901520" y2="249.906370" style = "stroke: black ;"/>
    <line x1="269.090351" y1="184.205556" x2="305.083078" y2="184.050084" style = "stroke: black ;"/>
    </svg>

    </body>
    </html>


>>> s2 = pivotal.Artin_generator(3,2)
>>> s2.show('Tk')

.. raw:: html

    <html>
    <body>

    <svg xmlns="http://www.w3.org/2000/svg" version="1.1" width="500" height="500">

    <title>A Link Diagram</title>
    <desc>A link diagram produced using circle packing.</desc>

    <defs>
      <marker id="Arrow" markerWidth="5" markerHeight="10"
        refX="5" refY="5" orient="auto">
        <path d="M 0 0 5 5 0 10 Z" style="fill: blue;"/>
      </marker>
    </defs>
    <line x1="449.848248" y1="184.673415" x2="385.374280" y2="184.441966" style = "stroke: black ;"/>
    <line x1="158.521430" y1="183.911774" x2="171.435620" y2="220.553852" style = "stroke: blue ;"/>
    <line x1="329.035056" y1="184.242178" x2="328.429411" y2="232.394045" style = "stroke: blue ;"/>
    <line x1="199.431042" y1="244.133933" x2="218.068753" y2="220.519676" style = "stroke: blue ; marker-end: url(\#Arrow);"/>
    <line x1="230.781350" y1="183.990680" x2="218.068753" y2="220.519676" style = "stroke: blue ;"/>
    <line x1="329.035056" y1="184.242178" x2="274.777127" y2="184.101250" style = "stroke: black ;"/>
    <line x1="158.501609" y1="316.121026" x2="171.414566" y2="279.504511" style = "stroke: blue ; marker-end: url(\#Arrow);"/>
    <line x1="230.781350" y1="183.990680" x2="194.748188" y2="183.949478" style = "stroke: black ;"/>
    <line x1="450.000000" y1="315.826656" x2="449.909098" y2="250.145934" style = "stroke: black ;"/>
    <line x1="328.936054" y1="315.985716" x2="385.277612" y2="315.913407" style = "stroke: black ;"/>
    <line x1="50.019990" y1="183.874062" x2="50.006354" y2="249.999991" style = "stroke: black ;"/>
    <line x1="50.000000" y1="316.125938" x2="113.505645" y2="316.125938" style = "stroke: black ;"/>
    <line x1="230.700907" y1="316.096002" x2="218.048743" y2="279.576782" style = "stroke: blue ; marker-end: url(\#Arrow);"/>
    <line x1="158.521430" y1="183.911774" x2="113.525594" y2="183.893260" style = "stroke: black ;"/>
    <line x1="328.345189" y1="250.129329" x2="328.388723" y2="267.837678" style = "stroke: blue ;"/>
    <line x1="328.345189" y1="250.129329" x2="328.429411" y2="232.394045" style = "stroke: blue ; marker-end: url(\#Arrow);"/>
    <line x1="194.771614" y1="250.037498" x2="218.048743" y2="279.576782" style = "stroke: blue ;"/>
    <line x1="158.501609" y1="316.121026" x2="194.697745" y2="316.110335" style = "stroke: black ;"/>
    <line x1="230.700907" y1="316.096002" x2="274.683964" y2="316.048686" style = "stroke: black ;"/>
    <line x1="190.100205" y1="255.930900" x2="171.414566" y2="279.504511" style = "stroke: blue ;"/>
    <line x1="194.771614" y1="250.037498" x2="171.435620" y2="220.553852" style = "stroke: blue ; marker-end: url(\#Arrow);"/>
    <line x1="328.936054" y1="315.985716" x2="328.388723" y2="267.837678" style = "stroke: blue ; marker-end: url(\#Arrow);"/>
    <line x1="329.035056" y1="184.242178" x2="385.374280" y2="184.441966" style = "stroke: black ;"/>
    <line x1="230.781350" y1="183.990680" x2="274.777127" y2="184.101250" style = "stroke: black ;"/>
    <line x1="158.521430" y1="183.911774" x2="194.748188" y2="183.949478" style = "stroke: black ;"/>
    <line x1="449.848248" y1="184.673415" x2="449.909098" y2="250.145934" style = "stroke: black ;"/>
    <line x1="450.000000" y1="315.826656" x2="385.277612" y2="315.913407" style = "stroke: black ;"/>
    <line x1="50.000000" y1="316.125938" x2="50.006354" y2="249.999991" style = "stroke: black ;"/>
    <line x1="158.501609" y1="316.121026" x2="113.505645" y2="316.125938" style = "stroke: black ;"/>
    <line x1="50.019990" y1="183.874062" x2="113.525594" y2="183.893260" style = "stroke: black ;"/>
    <line x1="230.700907" y1="316.096002" x2="194.697745" y2="316.110335" style = "stroke: black ;"/>
    <line x1="328.936054" y1="315.985716" x2="274.683964" y2="316.048686" style = "stroke: black ;"/>
    </svg>

    </body>
    </html>

The following illustrates composition of braids.

>>> s1 = pivotal.Artin_generator(3,1)
>>> s2 = pivotal.Artin_generator(3,2)
>>> s1.compose(s2).show('Tk')

.. raw:: html

    <html>
    <body>

    <svg xmlns="http://www.w3.org/2000/svg" version="1.1" width="500" height="500">

    <title>A Link Diagram</title>
    <desc>A link diagram produced using circle packing.</desc>

    <defs>
      <marker id="Arrow" markerWidth="5" markerHeight="10"
        refX="5" refY="5" orient="auto">
        <path d="M 0 0 5 5 0 10 Z" style="fill: blue;"/>
      </marker>
    </defs>
    <line x1="215.445578" y1="230.423195" x2="227.106068" y2="203.525073" style = "stroke: blue ; marker-end: url(\#Arrow);"/>
    <line x1="283.466839" y1="270.269731" x2="271.731355" y2="297.188539" style = "stroke: blue ;"/>
    <line x1="50.011101" y1="174.981415" x2="50.003907" y2="249.974683" style = "stroke: black ;"/>
    <line x1="212.530456" y1="237.147725" x2="184.410778" y2="210.411846" style = "stroke: blue ; marker-end: url(\#Arrow);"/>
    <line x1="50.000000" y1="326.777942" x2="124.887689" y2="326.777942" style = "stroke: black ;"/>
    <line x1="286.400710" y1="263.540029" x2="249.445622" y2="250.331674" style = "stroke: blue ; marker-end: url(\#Arrow);"/>
    <line x1="183.503471" y1="326.774066" x2="195.352378" y2="275.740146" style = "stroke: blue ; marker-end: url(\#Arrow);"/>
    <line x1="450.000000" y1="326.365028" x2="449.781257" y2="250.522020" style = "stroke: black ;"/>
    <line x1="449.510824" y1="173.222058" x2="374.203906" y2="173.464511" style = "stroke: black ;"/>
    <line x1="212.530456" y1="237.147725" x2="249.445622" y2="250.331674" style = "stroke: blue ;"/>
    <line x1="168.450195" y1="174.297494" x2="121.201956" y2="174.568920" style = "stroke: black ;"/>
    <line x1="233.073866" y1="173.931658" x2="204.334212" y2="174.093002" style = "stroke: black ;"/>
    <line x1="330.487030" y1="326.693265" x2="314.536812" y2="290.409435" style = "stroke: blue ; marker-end: url(\#Arrow);"/>
    <line x1="168.450195" y1="174.297494" x2="184.410778" y2="210.411846" style = "stroke: blue ;"/>
    <line x1="315.375442" y1="173.660205" x2="265.872444" y2="173.795350" style = "stroke: black ;"/>
    <line x1="265.642881" y1="326.754252" x2="294.405703" y2="326.740738" style = "stroke: black ;"/>
    <line x1="315.375442" y1="173.660205" x2="303.592633" y2="224.858213" style = "stroke: blue ;"/>
    <line x1="330.487030" y1="326.693265" x2="377.998382" y2="326.565868" style = "stroke: black ;"/>
    <line x1="265.642881" y1="326.754252" x2="271.731355" y2="297.188539" style = "stroke: blue ; marker-end: url(\#Arrow);"/>
    <line x1="183.503471" y1="326.774066" x2="232.875681" y2="326.763971" style = "stroke: black ;"/>
    <line x1="286.400710" y1="263.540029" x2="314.536812" y2="290.409435" style = "stroke: blue ;"/>
    <line x1="233.073866" y1="173.931658" x2="227.106068" y2="203.525073" style = "stroke: blue ;"/>
    <line x1="212.530456" y1="237.147725" x2="195.352378" y2="275.740146" style = "stroke: blue ;"/>
    <line x1="286.400710" y1="263.540029" x2="303.592633" y2="224.858213" style = "stroke: blue ; marker-end: url(\#Arrow);"/>
    <line x1="50.000000" y1="326.777942" x2="50.003907" y2="249.974683" style = "stroke: black ;"/>
    <line x1="183.503471" y1="326.774066" x2="124.887689" y2="326.777942" style = "stroke: black ;"/>
    <line x1="449.510824" y1="173.222058" x2="449.781257" y2="250.522020" style = "stroke: black ;"/>
    <line x1="315.375442" y1="173.660205" x2="374.203906" y2="173.464511" style = "stroke: black ;"/>
    <line x1="50.011101" y1="174.981415" x2="121.201956" y2="174.568920" style = "stroke: black ;"/>
    <line x1="168.450195" y1="174.297494" x2="204.334212" y2="174.093002" style = "stroke: black ;"/>
    <line x1="233.073866" y1="173.931658" x2="265.872444" y2="173.795350" style = "stroke: black ;"/>
    <line x1="330.487030" y1="326.693265" x2="294.405703" y2="326.740738" style = "stroke: black ;"/>
    <line x1="450.000000" y1="326.365028" x2="377.998382" y2="326.565868" style = "stroke: black ;"/>
    <line x1="265.642881" y1="326.754252" x2="232.875681" y2="326.763971" style = "stroke: black ;"/>
    </svg>

    </body>
    </html>

>>> s1 = pivotal.Artin_generator(3,1)
>>> t1 = pivotal.Artin_generator(3,-1)
>>> t1.show('Tk')

.. raw:: html

    <html>
    <body>

    <svg xmlns="http://www.w3.org/2000/svg" version="1.1" width="500" height="500">

    <title>A Link Diagram</title>
    <desc>A link diagram produced using circle packing.</desc>

    <defs>
      <marker id="Arrow" markerWidth="5" markerHeight="10"
        refX="5" refY="5" orient="auto">
        <path d="M 0 0 5 5 0 10 Z" style="fill: blue;"/>
      </marker>
    </defs>
    <line x1="170.927054" y1="184.636616" x2="114.649196" y2="184.920461" style = "stroke: black ;"/>
    <line x1="449.795759" y1="183.798816" x2="386.340430" y2="183.903779" style = "stroke: black ;"/>
    <line x1="171.276444" y1="316.198731" x2="171.748535" y2="268.115405" style = "stroke: blue ; marker-end: url(\#Arrow);"/>
    <line x1="309.890627" y1="256.020214" x2="328.600140" y2="279.552971" style = "stroke: blue ;"/>
    <line x1="269.090351" y1="184.191617" x2="225.139456" y2="184.388797" style = "stroke: black ;"/>
    <line x1="305.213249" y1="250.137025" x2="281.998003" y2="279.686893" style = "stroke: blue ;"/>
    <line x1="171.762157" y1="250.427611" x2="171.658178" y2="232.739325" style = "stroke: blue ; marker-end: url(\#Arrow);"/>
    <line x1="269.387582" y1="316.179147" x2="281.998003" y2="279.686893" style = "stroke: blue ; marker-end: url(\#Arrow);"/>
    <line x1="341.363576" y1="183.972112" x2="328.521815" y2="220.621968" style = "stroke: blue ;"/>
    <line x1="450.000000" y1="315.986040" x2="449.901520" y2="249.892431" style = "stroke: black ;"/>
    <line x1="170.927054" y1="184.636616" x2="171.658178" y2="232.739325" style = "stroke: blue ;"/>
    <line x1="341.551566" y1="316.132301" x2="328.600140" y2="279.552971" style = "stroke: blue ; marker-end: url(\#Arrow);"/>
    <line x1="171.762157" y1="250.427611" x2="171.748535" y2="268.115405" style = "stroke: blue ;"/>
    <line x1="300.546402" y1="244.237366" x2="281.879014" y2="220.638731" style = "stroke: blue ; marker-end: url(\#Arrow);"/>
    <line x1="50.000000" y1="185.250211" x2="50.337495" y2="250.856648" style = "stroke: black ;"/>
    <line x1="305.213249" y1="250.137025" x2="328.521815" y2="220.621968" style = "stroke: blue ; marker-end: url(\#Arrow);"/>
    <line x1="269.387582" y1="316.179147" x2="305.365706" y2="316.164302" style = "stroke: black ;"/>
    <line x1="341.363576" y1="183.972112" x2="305.119420" y2="184.043262" style = "stroke: black ;"/>
    <line x1="269.090351" y1="184.191617" x2="281.879014" y2="220.638731" style = "stroke: blue ;"/>
    <line x1="341.551566" y1="316.132301" x2="386.525425" y2="316.074520" style = "stroke: black ;"/>
    <line x1="50.676175" y1="316.201184" x2="115.036518" y2="316.201184" style = "stroke: black ;"/>
    <line x1="171.276444" y1="316.198731" x2="225.455650" y2="316.189958" style = "stroke: black ;"/>
    <line x1="50.000000" y1="185.250211" x2="114.649196" y2="184.920461" style = "stroke: black ;"/>
    <line x1="341.363576" y1="183.972112" x2="386.340430" y2="183.903779" style = "stroke: black ;"/>
    <line x1="170.927054" y1="184.636616" x2="225.139456" y2="184.388797" style = "stroke: black ;"/>
    <line x1="449.795759" y1="183.798816" x2="449.901520" y2="249.892431" style = "stroke: black ;"/>
    <line x1="50.676175" y1="316.201184" x2="50.337495" y2="250.856648" style = "stroke: black ;"/>
    <line x1="341.551566" y1="316.132301" x2="305.365706" y2="316.164302" style = "stroke: black ;"/>
    <line x1="269.090351" y1="184.191617" x2="305.119420" y2="184.043262" style = "stroke: black ;"/>
    <line x1="450.000000" y1="315.986040" x2="386.525425" y2="316.074520" style = "stroke: black ;"/>
    <line x1="171.276444" y1="316.198731" x2="115.036518" y2="316.201184" style = "stroke: black ;"/>
    <line x1="269.387582" y1="316.179147" x2="225.455650" y2="316.189958" style = "stroke: black ;"/>
    </svg>

    </body>
    </html>

>>> s1.compose(t1).show('Tk')

.. raw:: html

    <html>
    <body>

    <svg xmlns="http://www.w3.org/2000/svg" version="1.1" width="500" height="500">

    <title>A Link Diagram</title>
    <desc>A link diagram produced using circle packing.</desc>

    <defs>
      <marker id="Arrow" markerWidth="5" markerHeight="10"
        refX="5" refY="5" orient="auto">
        <path d="M 0 0 5 5 0 10 Z" style="fill: blue;"/>
      </marker>
    </defs>
    <line x1="310.938945" y1="266.509663" x2="317.929376" y2="250.138673" style = "stroke: blue ; marker-end: url(\#Arrow);"/>
    <line x1="309.255748" y1="229.588511" x2="300.484051" y2="250.123743" style = "stroke: blue ;"/>
    <line x1="305.567409" y1="225.912696" x2="290.814051" y2="211.209438" style = "stroke: blue ; marker-end: url(\#Arrow);"/>
    <line x1="277.272530" y1="320.104123" x2="290.745900" y2="288.954811" style = "stroke: blue ; marker-end: url(\#Arrow);"/>
    <line x1="449.949747" y1="319.979077" x2="449.888905" y2="250.255947" style = "stroke: black ;"/>
    <line x1="50.021632" y1="179.855742" x2="50.006873" y2="249.999983" style = "stroke: black ;"/>
    <line x1="277.272530" y1="320.104123" x2="309.280343" y2="320.086074" style = "stroke: black ;"/>
    <line x1="309.255748" y1="229.588511" x2="327.796527" y2="211.320240" style = "stroke: blue ; marker-end: url(\#Arrow);"/>
    <line x1="341.426096" y1="320.065109" x2="327.708026" y2="288.873420" style = "stroke: blue ; marker-end: url(\#Arrow);"/>
    <line x1="178.956359" y1="179.902150" x2="179.745568" y2="231.097033" style = "stroke: blue ;"/>
    <line x1="305.502250" y1="274.272891" x2="290.745900" y2="288.954811" style = "stroke: blue ;"/>
    <line x1="341.681849" y1="180.146915" x2="327.796527" y2="211.320240" style = "stroke: blue ;"/>
    <line x1="178.935167" y1="320.137610" x2="235.769671" y2="320.120673" style = "stroke: black ;"/>
    <line x1="341.681849" y1="180.146915" x2="309.386231" y2="180.077984" style = "stroke: black ;"/>
    <line x1="179.816133" y1="250.032275" x2="179.731801" y2="268.967484" style = "stroke: blue ;"/>
    <line x1="277.360105" y1="180.029462" x2="235.830934" y2="179.973323" style = "stroke: black ;"/>
    <line x1="277.360105" y1="180.029462" x2="290.814051" y2="211.209438" style = "stroke: blue ;"/>
    <line x1="309.191338" y1="270.602411" x2="300.484051" y2="250.123743" style = "stroke: blue ; marker-end: url(\#Arrow);"/>
    <line x1="450.000000" y1="180.766487" x2="384.138942" y2="180.388436" style = "stroke: black ;"/>
    <line x1="178.935167" y1="320.137610" x2="179.731801" y2="268.967484" style = "stroke: blue ; marker-end: url(\#Arrow);"/>
    <line x1="309.191338" y1="270.602411" x2="327.708026" y2="288.873420" style = "stroke: blue ;"/>
    <line x1="310.990474" y1="233.698543" x2="317.929376" y2="250.138673" style = "stroke: blue ;"/>
    <line x1="179.816133" y1="250.032275" x2="179.745568" y2="231.097033" style = "stroke: blue ; marker-end: url(\#Arrow);"/>
    <line x1="50.000000" y1="320.144258" x2="119.059885" y2="320.144258" style = "stroke: black ;"/>
    <line x1="341.426096" y1="320.065109" x2="383.848170" y2="320.033250" style = "stroke: black ;"/>
    <line x1="178.956359" y1="179.902150" x2="119.081436" y2="179.877039" style = "stroke: black ;"/>
    <line x1="450.000000" y1="180.766487" x2="449.888905" y2="250.255947" style = "stroke: black ;"/>
    <line x1="50.000000" y1="320.144258" x2="50.006873" y2="249.999983" style = "stroke: black ;"/>
    <line x1="341.426096" y1="320.065109" x2="309.280343" y2="320.086074" style = "stroke: black ;"/>
    <line x1="277.272530" y1="320.104123" x2="235.769671" y2="320.120673" style = "stroke: black ;"/>
    <line x1="277.360105" y1="180.029462" x2="309.386231" y2="180.077984" style = "stroke: black ;"/>
    <line x1="178.956359" y1="179.902150" x2="235.830934" y2="179.973323" style = "stroke: black ;"/>
    <line x1="341.681849" y1="180.146915" x2="384.138942" y2="180.388436" style = "stroke: black ;"/>
    <line x1="178.935167" y1="320.137610" x2="119.059885" y2="320.144258" style = "stroke: black ;"/>
    <line x1="449.949747" y1="319.979077" x2="383.848170" y2="320.033250" style = "stroke: black ;"/>
    <line x1="50.021632" y1="179.855742" x2="119.081436" y2="179.877039" style = "stroke: black ;"/>
    </svg>

    </body>
    </html>

The following is intended to illustrate the implementation
of Vogel's algorithm for converting a knot diagram to the
closure of a link diagram. Here are the previous implementations
of this algorithm that we are aware of:

 - `Dan Roozemond <http://www.mathdox.org/new-web/scripts/vogel.php>`_
 - `Andrew Bartholomew <http://www.layer8.co.uk/maths/>`_
 - `Dan Carney <http://katlas.org/wiki/Braid_Representatives>`_


Unfortunately this is not working.

>>> c = knots.DT([4,6,2])
>>> g = knots.LinkDiagram.from_DT(c)

g.braid #doctest: +ELLIPSIS
<pivotal.Morphism instance at 0x...>
g.braid.show('Tk')

>>> c = knots.DT([4,6,8,2])
>>> g = knots.LinkDiagram.from_DT(c)

g.braid #doctest: +ELLIPSIS
<pivotal.Morphism instance at 0x...>
g.braid.show('Tk')

>>> c = knots.DT([4,8,10,2,6])
>>> g = knots.LinkDiagram.from_DT(c)

g.braid #doctest: +ELLIPSIS
<pivotal.Morphism instance at 0x...>
g.braid.show('Tk')

>>> c = knots.DT([8,10,2,12,4,6])
>>> g = knots.LinkDiagram.from_DT(c)

g.braid #doctest: +ELLIPSIS
<pivotal.Morphism instance at 0x...>
g.braid.show('Tk')

The functions illustrated so far draw the diagram in a window.
The next functions produce the same diagrams but the diagrams are
first written to a file and then this file is opened in the web
browser.

>>> g = knots.LinkDiagram.from_DT(knots.DT([8,10,2,12,4,6]))
>>> g.show('SVG')


>>> g = knots.LinkDiagram.from_DT(knots.DT([8,10,2,12,4,6]))
>>> g.show('SVG',graph=True,withcircles=True)

.. raw:: html

    <html>
    <body>

    <svg xmlns="http://www.w3.org/2000/svg" version="1.1" width="500" height="500">

    <title>A Link Diagram</title>
    <desc>A link diagram produced using circle packing.</desc>

    <defs>
      <marker id="Arrow" markerWidth="5" markerHeight="10"
        refX="5" refY="5" orient="auto">
        <path d="M 0 0 5 5 0 10 Z" style="fill: blue;"/>
      </marker>
    </defs>
    <line x1="289.777338" y1="383.386772" x2="450.000000" y2="256.367993" style = "stroke: blue ; marker-end: url(\#Arrow);"/>
    <line x1="320.065155" y1="96.719357" x2="120.412440" y2="54.805066" style = "stroke: blue ;"/>
    <line x1="249.462666" y1="240.386173" x2="262.274516" y2="226.530450" style = "stroke: blue ;"/>
    <line x1="240.660204" y1="245.402733" x2="218.262202" y2="251.613249" style = "stroke: blue ; marker-end: url(\#Arrow);"/>
    <line x1="50.000000" y1="246.273347" x2="162.427868" y2="246.273347" style = "stroke: blue ; marker-end: url(\#Arrow);"/>
    <line x1="284.169863" y1="361.025334" x2="261.739960" y2="271.579581" style = "stroke: blue ;"/>
    <line x1="188.477938" y1="269.184281" x2="156.372329" y2="279.564932" style = "stroke: blue ; marker-end: url(\#Arrow);"/>
    <line x1="192.443030" y1="275.624553" x2="208.303400" y2="301.385642" style = "stroke: blue ; marker-end: url(\#Arrow);"/>
    <line x1="246.259704" y1="243.850104" x2="261.739960" y2="271.579581" style = "stroke: blue ; marker-end: url(\#Arrow);"/>
    <line x1="71.274466" y1="252.931664" x2="156.372329" y2="279.564932" style = "stroke: blue ;"/>
    <line x1="188.477938" y1="269.184281" x2="218.262202" y2="251.613249" style = "stroke: blue ;"/>
    <line x1="183.267924" y1="264.602094" x2="162.427868" y2="246.273347" style = "stroke: blue ;"/>
    <line x1="320.065155" y1="96.719357" x2="280.308518" y2="198.637722" style = "stroke: blue ; marker-end: url(\#Arrow);"/>
    <line x1="258.621977" y1="210.546173" x2="247.336593" y2="220.201384" style = "stroke: blue ; marker-end: url(\#Arrow);"/>
    <line x1="261.443323" y1="208.132370" x2="262.274516" y2="226.530450" style = "stroke: blue ; marker-end: url(\#Arrow);"/>
    <line x1="246.259704" y1="243.850104" x2="247.336593" y2="220.201384" style = "stroke: blue ;"/>
    <line x1="289.777338" y1="383.386772" x2="208.303400" y2="301.385642" style = "stroke: blue ;"/>
    <line x1="265.216362" y1="206.233441" x2="280.308518" y2="198.637722" style = "stroke: blue ;"/>
    <line x1="261.443323" y1="208.132370" x2="257.653458" y2="187.070851" style = "stroke: blue ;"/>
    <line x1="50.000000" y1="246.273347" x2="95.257229" y2="445.194934" style = "stroke: blue ;"/>
    <line x1="307.582816" y1="114.789656" x2="257.653458" y2="187.070851" style = "stroke: blue ; marker-end: url(\#Arrow);"/>
    <line x1="346.052124" y1="128.649085" x2="450.000000" y2="256.367993" style = "stroke: blue ;"/>
    <line x1="64.082488" y1="207.979691" x2="120.412440" y2="54.805066" style = "stroke: blue ; marker-end: url(\#Arrow);"/>
    <line x1="250.873316" y1="395.748404" x2="95.257229" y2="445.194934" style = "stroke: blue ; marker-end: url(\#Arrow);"/>
    <circle cx="289.777338" cy="383.386772" r="102.002469" stroke="yellow" fill="none" />
    <circle cx="320.065155" cy="96.719357" r="102.002469" stroke="yellow" fill="none" />
    <circle cx="188.477938" cy="269.184281" r="24.266344" stroke="yellow" fill="none" />
    <circle cx="246.259704" cy="243.850104" r="18.739229" stroke="yellow" fill="none" />
    <circle cx="50.000000" cy="246.273347" r="102.002469" stroke="yellow" fill="none" />
    <circle cx="261.443323" cy="208.132370" r="13.590538" stroke="yellow" fill="none" />
    <circle cx="162.427868" cy="246.273347" r="10.425399" stroke="yellow" fill="none" />
    <circle cx="257.653458" cy="187.070851" r="7.809244" stroke="yellow" fill="none" />
    <circle cx="208.303400" cy="301.385642" r="13.527405" stroke="yellow" fill="none" />
    <circle cx="247.336593" cy="220.201384" r="4.933997" stroke="yellow" fill="none" />
    <circle cx="261.739960" cy="271.579581" r="13.008356" stroke="yellow" fill="none" />
    <circle cx="95.257229" cy="445.194934" r="102.002469" stroke="yellow" fill="none" />
    <circle cx="450.000000" cy="256.367993" r="102.002469" stroke="yellow" fill="none" />
    <circle cx="218.262202" cy="251.613249" r="10.314627" stroke="yellow" fill="none" />
    <circle cx="280.308518" cy="198.637722" r="7.396876" stroke="yellow" fill="none" />
    <circle cx="120.412440" cy="54.805066" r="102.002469" stroke="yellow" fill="none" />
    <circle cx="262.274516" cy="226.530450" r="4.766072" stroke="yellow" fill="none" />
    <circle cx="156.372329" cy="279.564932" r="9.457847" stroke="yellow" fill="none" />
    <circle cx="306.840869" cy="240.348304" r="41.727543" stroke="yellow" fill="none" />
    <circle cx="164.067734" cy="324.930560" r="36.555841" stroke="yellow" fill="none" />
    <circle cx="230.604160" cy="277.938096" r="18.759786" stroke="yellow" fill="none" />
    <circle cx="195.987652" cy="191.279067" r="53.999985" stroke="yellow" fill="none" />
    <circle cx="269.871383" cy="191.386859" r="5.148595" stroke="yellow" fill="none" />
    <circle cx="254.740675" cy="223.601702" r="3.213554" stroke="yellow" fill="none" />
    <circle cx="157.746695" cy="263.112284" r="7.052105" stroke="yellow" fill="none" />
    </svg>

    </body>
    </html>


>>> g = knots.LinkDiagram.from_DT(knots.DT([8,10,2,12,4,6]))
>>> g.show('Tk',graph=False,withtriangles=True)

>>> g = knots.LinkDiagram.from_DT(knots.DT([8,10,2,12,4,6]))
>>> g.show('SVG',withcircles=True,withradicalcircles=True)

.. raw:: html

    <html>
    <body>

    <svg xmlns="http://www.w3.org/2000/svg" version="1.1" width="500" height="500">

    <title>A Link Diagram</title>
    <desc>A link diagram produced using circle packing.</desc>

    <defs>
      <marker id="Arrow" markerWidth="5" markerHeight="10"
        refX="5" refY="5" orient="auto">
        <path d="M 0 0 5 5 0 10 Z" style="fill: blue;"/>
      </marker>
    </defs>
    <line x1="87.400299" y1="229.035488" x2="201.355218" y2="229.035488" style = "stroke: blue ;"/>
    <line x1="237.649430" y1="237.545414" x2="229.170557" y2="270.592827" style = "stroke: blue ;"/>
    <line x1="265.068646" y1="450.000000" x2="435.056651" y2="339.048091" style = "stroke: blue ;"/>
    <line x1="229.422299" y1="331.062668" x2="246.802402" y2="343.116809" style = "stroke: blue ;"/>
    <line x1="330.507213" y1="166.818988" x2="252.721406" y2="207.891425" style = "stroke: blue ;"/>
    <line x1="217.862579" y1="290.562360" x2="229.170557" y2="270.592827" style = "stroke: blue ; marker-end: url(\#Arrow);"/>
    <line x1="261.415397" y1="428.623362" x2="246.802402" y2="343.116809" style = "stroke: blue ; marker-end: url(\#Arrow);"/>
    <line x1="215.035585" y1="295.554744" x2="184.907792" y2="287.014717" style = "stroke: blue ; marker-end: url(\#Arrow);"/>
    <line x1="349.953665" y1="156.550879" x2="179.255251" y2="50.000000" style = "stroke: blue ;"/>
    <line x1="237.649430" y1="237.545414" x2="252.721406" y2="207.891425" style = "stroke: blue ; marker-end: url(\#Arrow);"/>
    <line x1="87.400299" y1="229.035488" x2="64.943349" y2="429.002295" style = "stroke: blue ; marker-end: url(\#Arrow);"/>
    <line x1="244.482020" y1="237.091400" x2="271.812379" y2="235.275343" style = "stroke: blue ;"/>
    <line x1="228.114035" y1="335.006133" x2="222.880975" y2="350.779993" style = "stroke: blue ;"/>
    <line x1="229.705883" y1="327.411807" x2="230.840218" y2="312.808363" style = "stroke: blue ; marker-end: url(\#Arrow);"/>
    <line x1="215.035585" y1="295.554744" x2="230.840218" y2="312.808363" style = "stroke: blue ;"/>
    <line x1="229.422299" y1="331.062668" x2="215.979903" y2="318.725709" style = "stroke: blue ; marker-end: url(\#Arrow);"/>
    <line x1="265.068646" y1="450.000000" x2="222.880975" y2="350.779993" style = "stroke: blue ; marker-end: url(\#Arrow);"/>
    <line x1="349.953665" y1="156.550879" x2="271.812379" y2="235.275343" style = "stroke: blue ; marker-end: url(\#Arrow);"/>
    <line x1="215.224449" y1="300.188937" x2="215.979903" y2="318.725709" style = "stroke: blue ;"/>
    <line x1="106.901798" y1="240.631334" x2="184.907792" y2="287.014717" style = "stroke: blue ;"/>
    <line x1="230.390587" y1="235.843429" x2="201.355218" y2="229.035488" style = "stroke: blue ; marker-end: url(\#Arrow);"/>
    <line x1="366.974262" y1="193.050322" x2="435.056651" y2="339.048091" style = "stroke: blue ; marker-end: url(\#Arrow);"/>
    <line x1="105.771290" y1="193.228391" x2="179.255251" y2="50.000000" style = "stroke: blue ; marker-end: url(\#Arrow);"/>
    <line x1="225.043586" y1="445.800459" x2="64.943349" y2="429.002295" style = "stroke: blue ;"/>
    <circle cx="215.035585" cy="295.554744" r="18.483768" stroke="yellow" fill="none" />
    <circle cx="237.649430" cy="237.545414" r="23.935535" stroke="yellow" fill="none" />
    <circle cx="265.068646" cy="450.000000" r="100.611926" stroke="yellow" fill="none" />
    <circle cx="87.400299" cy="229.035488" r="100.611926" stroke="yellow" fill="none" />
    <circle cx="229.422299" cy="331.062668" r="13.405265" stroke="yellow" fill="none" />
    <circle cx="349.953665" cy="156.550879" r="100.611926" stroke="yellow" fill="none" />
    <circle cx="252.721406" cy="207.891425" r="9.328913" stroke="yellow" fill="none" />
    <circle cx="184.907792" cy="287.014717" r="12.831021" stroke="yellow" fill="none" />
    <circle cx="435.056651" cy="339.048091" r="100.611926" stroke="yellow" fill="none" />
    <circle cx="215.979903" cy="318.725709" r="4.701098" stroke="yellow" fill="none" />
    <circle cx="64.943349" cy="429.002295" r="100.611926" stroke="yellow" fill="none" />
    <circle cx="179.255251" cy="50.000000" r="100.611926" stroke="yellow" fill="none" />
    <circle cx="229.170557" cy="270.592827" r="10.174013" stroke="yellow" fill="none" />
    <circle cx="222.880975" cy="350.779993" r="7.296038" stroke="yellow" fill="none" />
    <circle cx="271.812379" cy="235.275343" r="10.283275" stroke="yellow" fill="none" />
    <circle cx="246.802402" cy="343.116809" r="7.702785" stroke="yellow" fill="none" />
    <circle cx="201.355218" cy="229.035488" r="13.342993" stroke="yellow" fill="none" />
    <circle cx="230.840218" cy="312.808363" r="4.866735" stroke="yellow" fill="none" />
    <circle cx="223.293898" cy="315.619406" r="3.169745" stroke="yellow" fill="none" />
    <circle cx="286.914288" cy="297.039133" r="53.263833" stroke="yellow" fill="none" />
    <circle cx="202.182988" cy="260.871766" r="18.504044" stroke="yellow" fill="none" />
    <circle cx="175.428544" cy="340.165758" r="41.158694" stroke="yellow" fill="none" />
    <circle cx="263.274964" cy="220.293836" r="6.955968" stroke="yellow" fill="none" />
    <circle cx="215.625769" cy="181.741095" r="36.057495" stroke="yellow" fill="none" />
    <circle cx="235.194554" cy="348.499480" r="5.078408" stroke="yellow" fill="none" />
    <circle cx="188.012225" cy="211.072212" r="17.963276" stroke="red" fill="none" />
    <circle cx="243.552430" cy="263.773240" r="12.240689" stroke="red" fill="none" />
    <circle cx="325.415589" cy="356.762600" r="47.034103" stroke="red" fill="none" />
    <circle cx="245.415369" cy="331.552796" r="8.735980" stroke="red" fill="none" />
    <circle cx="264.472805" cy="210.141083" r="7.491843" stroke="red" fill="none" />
    <circle cx="216.680441" cy="275.233110" r="8.603760" stroke="red" fill="none" />
    <circle cx="242.334908" cy="351.805987" r="6.010609" stroke="red" fill="none" />
    <circle cx="194.085879" cy="301.685069" r="11.611263" stroke="red" fill="none" />
    <circle cx="243.836537" cy="136.546410" r="39.220709" stroke="red" fill="none" />
    <circle cx="238.887195" cy="211.324766" r="10.777040" stroke="red" fill="none" />
    <circle cx="117.372851" cy="333.645907" r="41.460027" stroke="red" fill="none" />
    <circle cx="261.111388" cy="229.535745" r="6.458208" stroke="red" fill="none" />
    <circle cx="229.326405" cy="345.181628" r="4.433181" stroke="red" fill="none" />
    <circle cx="227.367978" cy="317.447471" r="3.145261" stroke="red" fill="none" />
    <circle cx="233.462600" cy="303.755166" r="8.071688" stroke="red" fill="none" />
    <circle cx="214.982402" cy="326.917168" r="6.781938" stroke="red" fill="none" />
    <circle cx="212.518383" cy="363.021623" r="14.283159" stroke="red" fill="none" />
    <circle cx="292.134165" cy="240.923861" r="18.415618" stroke="red" fill="none" />
    <circle cx="219.067019" cy="313.890639" r="3.287531" stroke="red" fill="none" />
    <circle cx="180.755918" cy="268.891847" r="13.455162" stroke="red" fill="none" />
    <circle cx="211.995349" cy="242.106339" r="10.296798" stroke="red" fill="none" />
    <circle cx="217.206479" cy="219.881250" r="12.531045" stroke="red" fill="none" />
    <circle cx="233.850826" cy="284.956038" r="11.166746" stroke="red" fill="none" />
    <circle cx="350.799406" cy="267.247914" r="46.171303" stroke="red" fill="none" />
    <circle cx="264.357406" cy="348.042362" r="16.525929" stroke="red" fill="none" />
    <circle cx="254.034333" cy="219.023471" r="6.214306" stroke="red" fill="none" />
    <circle cx="222.732458" cy="258.431525" r="9.264764" stroke="red" fill="none" />
    <circle cx="237.940774" cy="342.329941" r="4.451372" stroke="red" fill="none" />
    <circle cx="164.404272" cy="296.391489" r="18.538692" stroke="red" fill="none" />
    <circle cx="168.223732" cy="157.421270" r="39.220709" stroke="red" fill="none" />
    <circle cx="253.873048" cy="190.066534" r="15.232347" stroke="red" fill="none" />
    <circle cx="169.332350" cy="398.267465" r="41.460027" stroke="red" fill="none" />
    <circle cx="273.530843" cy="222.458349" r="7.841090" stroke="red" fill="none" />
    <circle cx="231.162275" cy="355.094367" r="5.827656" stroke="red" fill="none" />
    <circle cx="225.115675" cy="311.401103" r="3.326509" stroke="red" fill="none" />
    <circle cx="237.535265" cy="318.237224" r="7.114146" stroke="red" fill="none" />
    <circle cx="208.326530" cy="314.328361" r="7.470640" stroke="red" fill="none" />
    <circle cx="217.394313" cy="341.223094" r="8.258668" stroke="red" fill="none" />
    <circle cx="262.351990" cy="248.205922" r="12.286297" stroke="red" fill="none" />
    <circle cx="221.557000" cy="319.753461" r="3.171742" stroke="red" fill="none" />
    <circle cx="199.812050" cy="281.484091" r="9.385608" stroke="red" fill="none" />
    <circle cx="188.012225" cy="242.729920" r="13.694432" stroke="red" fill="none" />
    </svg>

    </body>
    </html>

"""


import ribbon
import closedgraph
import spider
import pivotal
import knots


# This is to run the tests in the examples.
# http://docs.python.org/library/doctest.html
if __name__ == "__main__":
    import doctest
    doctest.testmod()
