#!/usr/bin/awk -f
BEGIN {
    print "Content-type:text/html\n"

    system("python /home/jwc160/public_html/cgi-bin/testdir/test.py")



    print "<body style='background-color:powderblue;'>"
    print "<form  action='test.cgi' method='post'>"
    print "<textarea id='input_text' name='foo' cols='80' rows='20' placeholder='TEST ME'></textarea>"
    print " <input type = submit>"
    print "</form>"

    getline cgidat
    system("rm /tmp/unacronym-in")
    system("rm /tmp/unacronym-pre")
    #system("rm /tmp/unacronym-replace")
    print cgidat > "/tmp/unacronym-in"
    system("python3 /home/jwc160/public_html/cgi-bin/testdir/un-acronym.py")

    print "<p>"
    while (getline < "/tmp/unacronym-replace")
    {
        print $0
    }
    print "</p>"

}
