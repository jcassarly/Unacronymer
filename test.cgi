#!/usr/bin/awk -f
BEGIN {
    print "Content-type:text/html\n"

    css()

    print "	<body style='background-image: url(\"https://cmkt-image-prd.freetls.fastly.net/0.1.0/ps/1345872/910/606/m2/fpnw/wm1/kpgfzej47ojqls7icrnppf2i6okj7vzxkscocr04wm2a1dyqdra1krmr0jt1q4wx-.jpg?1465315512&s=ccfb38ad3096d4ac6a1fb07f45ad3282\");'>"
    #print "	<body style='background-image: url(\"https://images.unsplash.com/photo-1521587760476-6c12a4b040da?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&w=1000&q=80\");'>"
    print "<H1 style='color:white;' id='title'>The Magical Un-Acronymer</H1>"

    print "<div class='row'>"

    print "<div class='column' >"
    print "  <H3 class='columnHead'>Enter text here:</H3>"
    print "  <form id='yeet' action='test.cgi' method='post'>"
    print "    <textarea class='inputtext' name='in_text' placeholder='TEST ME'></textarea>"
    print "  </form>"
    print "</div>"

    print "<div class='column'>"
    print "  <center>"
    print "    <button class='button' type='submit' form='yeet'>UNACRONYM</button>"
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
    close("/tmp/unacronym-error")

    print "<div class='column'>"
    print "  <H3 class='columnHead'>Output:</H3>"
    print "  <div class='outputtext'>"
    print "  <p>"

    system("python3 /home/jwc160/public_html/cgi-bin/testdir/unacronym.py 2> /tmp/unacronym-error")

    # if the python script exited in an error, override whatever was in the replace file to print the
    # python scripts error
    "ls -lt /tmp | grep unacronym-error" | getline
    if ($5 > 0)
    {
        system("mv /tmp/unacronym-error /tmp/unacronym-replace")
    }

    #TODO: make sure to verify this file exists
    #print "\ufffd" > "/tmp/unacronym-replace"
    #close("/tmp/unacronym-replace")
    while (getline < "/tmp/unacronym-replace" > 0)
    {
        print $0
    }
    print "   </p>"
    print "  </div>"
    print "  </div>"
    print "</div>"

}

func css()
{
    print "<head>"
    print "<style>"
    print "* {"
    print "  box-sizing: border-box;"
    print "  margin:0 auto;"
    print "  margin: 10px 0px 0px 0px;"
    print "}"

    print ".row {"
    print "  display: flex;"
    print "  margin:0 auto;"
    print " align-items : center;"
    print "}"

    print "#title{"
    print "font-size:60px;"
    print "text-align:center;"
    print "}"

    print ".columnHead{"
    print "  font-size:30px;"
    print "  text-align:center;"
    print "  color: white;"
    print "}"

    print ".column {"
    print "  flex: 50%;"
    #print "  margin: 10px 50px;"
    print "  margin: auto 2%;"
    print "  padding: 10px;"
    print "}"

    print ".inputtext"
    print "{"
    print "  overflow-y: auto;"
    print "  height:500px;"
    print "  width:500px;"
    print "  font-size:14pt;"
    print "  resize: none;"
    print "  opacity: 0.8;"
    print "}"

    print ".outputtext"
    print "{"
    print "  font-size:14pt;"
    print "  background: white;"
    print "  padding: 10px;"
    print "  overflow-y: auto;"
    print "  height:500px;"
    print "  width:500px;"
    print "  opacity: 0.8;"
    print "}"

    print " .button {"
    print " display: block;"
    print " width: 100%;"
    print " padding: 14px 28px;"
    print " font-size: 16px;"
    print " cursor: pointer;"
    print " text-align: center;"
    print " background-color: white;"
    print " color: black;"
    print " border: 2px solid #4CAF50;}"

    print "</style>"
    print "</head>"
}

