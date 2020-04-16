#!/usr/bin/awk -f
BEGIN {
    print "Content-type:text/html\n"
   
    system("python /home/jwc160/public_html/cgi-bin/testdir/test.py")

}
