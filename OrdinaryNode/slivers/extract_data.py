import os, os.path
import paths as p



def num_of_lxcs():
    lxc_name_list = []
    try :
        lxc_name_list =  [name for name in os.listdir(p.lxcs) if os.path.isdir(p.lxcs + name)]
    except OSError as e:
        print "ERROR: ", e

    return len(lxc_name_list)

def extract_some_info (lxc):

    lxc_name = ""
    try:
        with open((p.lxcs + lxc + "config"), 'r') as conf:
            lxc_info  = conf.readline().split("=")
            lxc_name = lxc_info[1].strip()
    except IOError as e:
        print "ERROR: ", e

    return lxc_name


if __name__ == "__main__":
    print num_of_lxcs()
    print extract_some_info("01")