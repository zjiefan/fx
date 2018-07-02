import sys
from fx_lib import do_group, run_one_person
if __name__ == '__main__':
    base_age = int(sys.argv[1])
    test_freq = int(sys.argv[2])
    do_ost_test = bool(int(sys.argv[3]))
    do_vf_test  = bool(int(sys.argv[4]))
    run_one_person(base_age=base_age, test_freq=test_freq, do_ost_test=do_ost_test, do_vf_test=do_vf_test)


