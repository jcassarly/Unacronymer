#!/usr/bin/awk -f
BEGIN {
    print "Content-type:text/html\n"
   
    system("python /home/jwc160/public_html/cgi-bin/testdir/test.py")

getline cgidat
print cgidat
print "<body style='background-color:powderblue;'>"
print "<form action = 'test.cgi' method = 'post'>"
print " Name? <input name = sname> <br>"
print " Just to choose <select name = input>"
print "<option> Thriller </option>"
print "</select> <br>"
print "<textarea name="foo" cols="80" rows="20">TEST ME</textarea>"
print " <input type = submit>"
print "</form>"

}
