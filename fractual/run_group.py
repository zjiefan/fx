import sys
from fx_lib import do_group
if __name__ == '__main__':
    sample_num = int(sys.argv[1])
    base_age = int(sys.argv[2])
    test_freq = int(sys.argv[3])
    do_ost_test = bool(int(sys.argv[4]))
    do_vf_test  = bool(int(sys.argv[5]))
    do_group(sample_num=sample_num, base_age=base_age, test_freq=test_freq, do_ost_test=do_ost_test, do_vf_test=do_vf_test)


