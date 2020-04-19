#!/usr/bin/awk -f
BEGIN {
    print "Content-type:text/html\n"

    print "<head>"
    print "<style>"
    print "* {"
    print "  box-sizing: border-box;"
    print "  margin:0 auto;"
    print "}"

    print ".row {"
    print "  display: flex;"
    print "  margin:0 auto;"
    print "}"

    print "#title{"
    print "font-size:60px;"
    print "text-align:center;"
    print "}"

    print ".columnHead{"
    print "  font-size:30px;"
    print "  text-align:center;"
    print "}"

    print ".column {"
    print "  flex: 50%;"
    print "  margin:0 auto;"
    print "  padding: 10px;"
    print "}"
    print ".inputtext"
    print "{"
    print "  overflow-y: auto;"
    print "  height:500px;"
    print "  width:500px;"
    print "  font-size:14pt;"
    print "  resize: none;"

    print "}"
    print ".outputtext"
    print "{"
    print "  font-size:14pt;"
    print "  background: white;"
    print "  padding: 10px;"
    print "  overflow-y: auto;"
    print "  height:500px;"
    print "  width:500px;"
    print "}"
    print "</style>"
    print "</head>"

    print "<body style='background-color:powderblue;'>"

    print "<H1 id='title'>The Magical Un-Acronymer</H1>"

    print "<div class='row'>"

    print "<div class='column' >"
    print "  <H3 class='columnHead'>Enter text here:</H3>"
    print "  <form id='yeet' action='test.cgi' method='post'>"
    print "    <textarea class='inputtext' name='in_text' placeholder='TEST ME'></textarea>"
    print "  </form>"
    print "</div>"

    print "<div class='column'>"
    print "  <center>"
    print "    <button type='submit' form='yeet'>Unacronym</button>"
    print "  </center>"
    print "</div>"

    getline cgidat
    sub("in_text=", "", cgidat)
    system("rm /tmp/unacronym-in")
    system("rm /tmp/unacronym-pre")
    system("rm /tmp/unacronym-replace")
    print cgidat > "/tmp/unacronym-in"
    #print "\ufffd" > "/tmp/unacronym-replace"
    #close("/tmp/unacronym-replace")
    close("/tmp/unacronym-in")
    close("/tmp/unacronym-pre")
    close("/tmp/unacronym-replace")


    print "<div class='column'>"
    print "  <H3 class='columnHead'>Output:</H3>"
    print "  <div class='outputtext'>"
    print "  <p>"
    system("python3 /home/jwc160/public_html/cgi-bin/testdir/unacronym.py")
    #TODO: make sure to verify this file exists
    #print "\ufffd" > "/tmp/unacronym-replace"
    #close("/tmp/unacronym-replace")
    while (getline < "/tmp/unacronym-replace")
    {
        print $0
    }
    print "   </p>"
    print "  </div>"
    print "  </div>"
    print "</div>"

}

