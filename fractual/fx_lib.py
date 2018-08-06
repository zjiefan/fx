import os
import sys
import logging
import random
import numpy as np
from collections import Counter
from prob_table import PROB_TABLE, natual_death_rate, get_ost_test_result, get_vfa_test_result, take_ost_trt
from cost_table import drug_cost, ost_cost, vfa_cost, nursing_cost
from human_stats import Record, HumanStats

DRUG_PERIOD = 5
DRUG_HOLIDAY = 5

FX_DEATH_RATE_LAST = 1
BASE_AGE = 65
DISCOUNT_RATE = 0.03
DISCOUNT = 1-DISCOUNT_RATE/2
EFF_DELAY = 2


VFA_OST_NORMAL = 0.085
VFA_OST_LBL = 0.1
VFA_OST_LBM1 = 0.157
VFA_OST_SICK = 0.343


VFA_PREVAL = {}
VFA_PREVAL[50] = 0.017
VFA_PREVAL[60] = 0.0386
VFA_PREVAL[70] = 0.0647
VFA_PREVAL_60 = (VFA_PREVAL[60] - VFA_PREVAL[50])/(1-VFA_PREVAL[50])
VFA_PREVAL_70 = (VFA_PREVAL[70] - VFA_PREVAL[60])/(1-VFA_PREVAL[60])

OST_SICK_PREVAL = {}
OST_SICK_PREVAL[60] = 0.123
OST_SICK_PREVAL[70] = 0.257
OST_SICK_PREVAL[80] = 0.349


OST_LBM1_PREVAL = {}
OST_LBM1_PREVAL[60] = 0.454
OST_LBM1_PREVAL[70] = 0.440
OST_LBM1_PREVAL[80] = 0.448

OST_LBM2_PREVAL = {}
OST_LBM2_PREVAL[60] = 0.534
OST_LBM2_PREVAL[70] = 0.518
OST_LBM2_PREVAL[80] = 0.527

OST_LBL_PREVAL = {}
OST_LBL_PREVAL[60] = OST_LBM2_PREVAL[60] - OST_LBM1_PREVAL[60]
OST_LBL_PREVAL[70] = OST_LBM2_PREVAL[70] - OST_LBM1_PREVAL[70]
OST_LBL_PREVAL[80] = OST_LBM2_PREVAL[80] - OST_LBM1_PREVAL[80]

OST_NORMAL_PREVAL = {}
OST_NORMAL_PREVAL[60] = 1 - OST_LBM2_PREVAL[60] - OST_SICK_PREVAL[60]
OST_NORMAL_PREVAL[70] = 1 - OST_LBM2_PREVAL[70] - OST_SICK_PREVAL[70]
OST_NORMAL_PREVAL[80] = 1 - OST_LBM2_PREVAL[80] - OST_SICK_PREVAL[80]



def to_status_str(ost, vfa, trt):
    if vfa:
        s0 = 'vfa'
    else:
        s0 = ost
    s1 = 'trt' if trt else 'no_trt'
    return (s0, s1)


def get_utility(fx, age):
    if fx in ['no_fx', 'wf']:
        if age < 60:
            return 0.937
        elif age < 70:
            return 0.911
        elif age < 80:
            return 0.871
        elif age < 90:
            return 0.824
        else:
            return 0.8
    elif fx == 'hip':
        if age < 60:
            return 0.737
        elif age < 70:
            return 0.711
        elif age < 80:
            return 0.671
        elif age < 90:
            return 0.624
        else:
            return 0.6
    elif fx == 'vf':
        if age < 60:
            return 0.837
        elif age < 70:
            return 0.811
        elif age < 80:
            return 0.771
        elif age < 90:
            return 0.724
        else:
            return 0.7
    else:
        print fx, age
        raise Exception("unknown fx, age")





class Human(object):
    __slots__ = ('test_freq', 'strategy', 'record', 'records',
    'age', 'next_test', 'ost', 'vfa','fx', 'trt',
    'drug_end', 'drug_holiday_end',
    'last_hip', 'last_vf', 'last_wf', 'fx_rate',
    'old_fx', 'trt_len', 'trt_eff',
    'discount',
    'stats'

    )
    strategy = None
    log = logging.getLogger("Human")
    def __init__(self, base_age=None, test_freq=5):
        self.test_freq = test_freq
        self.record = Record()
        self.records = [None]*200
        self.stats = HumanStats()

        self.age = base_age
        self.next_test = None
        self.ost = None
        self.vfa = None
        self.set_ost_vfa()
        self.fx = 'no_fx'
        self.trt = False
        self.trt_len = 0
        self.trt_eff = None
        self.old_fx = None
        self.fx_rate =  'none'
        self.drug_end = 0
        self.drug_holiday_end = 0
        self.last_hip = 0
        self.last_vf = 0
        self.last_wf = 0
        self.discount = 1

    def __str__(self):
        ost = 'ost' if self.ost else 'no_ost'
        vfa = 'vfa' if self.ost else 'no_vfa'
        header = "age={:5},next_test={:5}, drug_end={:6}, last_hip={:4}, last_vf={:4}, last_wf={:4}, <inc_utils={:8.3f} acc_utils={:8.3f} | inc_cost={:12.3f} acc_cost={:12.3f}> |{:6}, {:6}| fx={:6}".format(
                self.age, self.next_test, self.drug_end, self.last_hip, self.last_vf, self.last_wf, self.record.inc_utils, self.stats.total_utils, self.inc_cost, self.acc_cost, ost, vfa, self.fx)

        if self.fx != 'death':
            return "{}   trt={:6},len={:2},eff={:6}, holiday_end={:5} ost_result={:6}, vfa_result={:6}, hip_cnt={:2}, vf_cnt={:2}, wf_cnt={:2}, trt_cnt={:4}, fx_rate={:6}".format(
                header, str(self.trt),self.trt_len, str(self.trt_eff), self.drug_holiday_end, self.ost_result, self.vfa_result, self.hip_cnt, self.vf_cnt, self.wf_cnt, self.trt_cnt, self.fx_rate)
        else:
            return header





    def set_ost_vfa(self):
        if self.ost is None:
            p = random.random()
            pv = random.random()
            if self.age < 70:
                band = 60
            elif self.age < 80:
                band = 70
            else:
                band = 80
            if p < OST_SICK_PREVAL[band]:
                self.ost = 'sick'
                self.vfa = pv < VFA_OST_SICK
                self.log.debug("initial ost %s, vfa %s", self.ost, self.vfa)
                return
            elif p < OST_SICK_PREVAL[band] + OST_LBM1_PREVAL[band]:
                self.ost = 'lbm1'
                self.vfa = pv < VFA_OST_LBM1
                self.log.debug("initial ost %s, vfa %s", self.ost, self.vfa)
                return
            elif p < OST_SICK_PREVAL[band] + OST_LBM2_PREVAL[band]:
                self.ost = 'lbl'
                self.vfa = pv < VFA_OST_LBL
                self.log.debug("initial ost %s, vfa %s", self.ost, self.vfa)
                return
            else:
                self.ost = 'normal'
                self.vfa = pv < VFA_OST_NORMAL
                self.log.debug("initial ost %s, vfa %s", self.ost, self.vfa)
                return

        else:
            if self.age in [70, 80]:
                if self.ost == 'sick': # cannot get worst
                    return
                sick_inc = (OST_SICK_PREVAL[self.age]-OST_SICK_PREVAL[self.age-10])
                last_lbm1_preval = OST_LBM1_PREVAL[self.age-10]
                self.log.debug("at age %d, sick prob increase %.5f, last lbm1 preval is %.5f", self.age, sick_inc, last_lbm1_preval)
                if sick_inc <= 0:
                    raise Exception("sick prevail reduced")
                if OST_LBM1_PREVAL[self.age-10] < sick_inc:
                    raise Exception("not enough lbm1")
                if self.ost == 'lbm1':
                    ost_lbm1_to_sick = sick_inc/last_lbm1_preval
                    p = random.random()
                    self.log.debug("prob that lbm1 turn sick at %d is %.5f, get prob %.5f", self.age, ost_lbm1_to_sick, p)
                    if p < ost_lbm1_to_sick:
                        self.log.debug("turn lbm1 to sick")
                        self.ost = 'sick'
                        # ost changes from lbm1 to sick, patients are more likely to have vfa.
                        if not self.vfa:
                            p = random.random()
                            vfa_inc = (VFA_OST_SICK - VFA_OST_LBM1)/(1-VFA_OST_LBM1)
                            self.log.debug("current vfa is false, prob to turn True is %.5f, get prob %.5f", vfa_inc, p)
                            self.vfa = p < vfa_inc
                    self.log.debug("return new ost %s, vfa %s", self.ost, self.vfa)
                    return

                old_lbm1_preval = OST_LBM1_PREVAL[self.age-10]
                lbm1_leftover = old_lbm1_preval - sick_inc
                self.log.debug("at age %d, lbm1 prevail was %.5f, sick takes %.5f, lbm preval leftover %.5f", self.age,  old_lbm1_preval, sick_inc, lbm1_leftover)
                lbm1_preval = OST_LBM1_PREVAL[self.age]
                lbm1_needed = lbm1_preval - lbm1_leftover
                self.log.debug("at age %d, lbm1 preval is %.5f, lbm leftover is %.5f, lbm1 need to add %.5f", self.age, lbm1_preval, lbm1_leftover, lbm1_needed)
                if lbm1_needed < 0:
                    raise Exception("lbm1 refill is negative")
                # all lbl convert to lbm1
                old_lbl_preval = OST_LBL_PREVAL[self.age-10]
                lbm1_needed_from_normal = lbm1_needed - old_lbl_preval
                self.log.debug("at age %d, lbm1 needed add %.5f, lbl has only %.5f, so lbm1 need %.5f from normal", self.age, lbm1_needed, old_lbl_preval, lbm1_needed_from_normal)
                if lbm1_needed_from_normal < 0:
                    raise Exception("ERROR: expected all lml convert to lbm1")
                if self.ost == 'lbl':
                    self.log.debug("ost was lbl, convert to lbm1")
                    self.ost = 'lbm1'
                    if not self.vfa:
                        vfa_inc = (VFA_OST_LBM1 - VFA_OST_LBL)/(1-VFA_OST_LBL)
                        pv = random.random()
                        self.log.debug("current vfa is false, prob to turn True is %.5f, get prob %.5f", vfa_inc, pv)
                        self.vfa = pv < vfa_inc
                    self.log.debug("return new ost %s, vfa %s", self.ost, self.vfa)
                    return
                if self.ost != 'normal':
                    self.log.error("ost %s, vfa %s", self.ost, self.vfa)
                    raise Exception("leftover has to be ost normal")
                self.log.debug("at age %d, lbm1 need %.5f from normal", self.age, lbm1_needed_from_normal)
                lbl_needed_from_normal = OST_NORMAL_PREVAL[self.age]
                old_normal_preval = OST_NORMAL_PREVAL[self.age-10]
                ost_normal_to_lbm1 = lbm1_needed_from_normal/old_normal_preval
                ost_normal_to_lbl = lbl_needed_from_normal/old_normal_preval
                self.log.debug("at age %d, old normal preval is %.5f, lbm1 takes %.5f, or prob %.5f, lbl takes %.5f, or prob %.5f",
                self.age, old_normal_preval, lbm1_needed_from_normal, ost_normal_to_lbm1, lbl_needed_from_normal, ost_normal_to_lbl)
                p = random.random()
                self.log.debug("get prob %.5f", p)
                if p < ost_normal_to_lbm1:
                    self.log.debug("promote ost to lbm1")
                    self.ost = 'lbm1'
                    if not self.vfa:
                        pv = random.random()
                        vfa_inc = (VFA_OST_LBM1 - VFA_OST_NORMAL)/(1-VFA_OST_NORMAL)
                        self.log.debug("current vfa is false, prob to turn True is %.5f, get prob %.5f", vfa_inc, pv)
                        self.vfa = pv < vfa_inc
                    self.log.debug("return new ost %s, vfa %s", self.ost, self.vfa)
                    return
                elif p < ost_normal_to_lbm1 + ost_normal_to_lbl:
                    self.ost = 'lbl'
                    if not self.vfa:
                        pv = random.random()
                        vfa_inc = (VFA_OST_LBL - VFA_OST_NORMAL)/(1-VFA_OST_NORMAL)
                        self.log.debug("current vfa is false, prob to turn True is %.5f, get prob %.5f", vfa_inc, pv)
                        self.vfa = pv < vfa_inc
                    self.log.debug("return new ost %s, vfa %s", self.ost, self.vfa)
                    return
                self.log.debug("at age %d, final return new ost %s, vfa %s", self.age, self.ost, self.vfa)



    def fx_death_rate(self):
        if self.last_vf + FX_DEATH_RATE_LAST >= self.age:
            if self.age < 80:
                self.fx_rate = 'vf_70'
                return 0.0335633
            else:
                self.fx_rate = 'vf_90'
                return 0.0851230
        elif self.last_hip + FX_DEATH_RATE_LAST >= self.age:
            if self.age < 80:
                self.fx_rate = 'hip_70'
                return 0.1112
                # return 0.0268606
            else:
                self.fx_rate = 'hip_90'
                return 0.2384
                #return 0.0851230
        elif self.last_wf + FX_DEATH_RATE_LAST >= self.age:
            if self.age < 80:
                self.fx_rate = 'wf_70'
                return 0.0045102
            else:
                self.fx_rate = 'vf_90'
                return 0.031496
        else:
            self.fx_rate = 'none'
            return 0

    def er_cost(self):
        if self.stats.hip_cnt + self.stats.vf_cnt + self.stats.wf_cnt == 0:
            if self.fx=='hip':
                if self.age < 65:
                    return 28496 + 180
                else:
                    return 18541 + 180
            elif self.fx == 'vf':
                if self.age < 65:
                    return 27320 + 180
                else:
                    return 20190 + 180
            elif self.fx == 'wf':
                if self.age < 65:
                    return 5088 + 180
                else:
                    return 3486 + 180
            else:
                raise Exception("unknown fx")
        else:
            if self.stats.hip_cnt >= 1:
                if self.age < 65:
                    return 90855
                else:
                    return 42991
            elif self.stats.vf_cnt >= 1:
                if self.age < 65:
                    return 84933
                else:
                    return 44526
            elif self.stats.wf_cnt >=1:
                if self.age < 65:
                    return 52732
                else:
                    return 41987
            else:
                raise Exception("unknown fx")


    def lab_test(self):
        trt_sop = False
        if self.fx != 'no_fx':
            trt_sop = True
        self.record.ost_result = None
        self.record.vfa_result = None

        do_test = False
        if self.next_test is None:
            do_test = True
            self.next_test = self.age + self.test_freq
        if self.age == self.next_test:
            do_test = True
            self.next_test = self.age + self.test_freq

        self.record = Record()
        if do_test and not trt_sop:
            if self.strategy == 0:
                pass
            else:
    #            self.record.ost_result = get_ost_test_result(self.ost, self.threshold)
                self.record.ost_result = self.ost
                if self.record.ost_result == 'sick':
                    trt_sop = take_ost_trt()
                if self.strategy == 1:
                    pass
                else:
                    if not trt_sop:
                        if self.strategy == 2:
                            if self.record.ost_result in ['lbm1']:
                                self.record.vfa_result = get_vfa_test_result(self.vfa)
                                if self.record.vfa_result:
                                    trt_sop = True
                        elif self.strategy == 3:
                            if self.record.ost_result in ['lbm1', 'lbl']:
                                self.record.vfa_result = get_vfa_test_result(self.vfa)
                                if self.record.vfa_result:
                                    trt_sop = True
                        else:
                            self.log.error("unexpected strategy %d", self.strategy)
                            raise Exception("unknown strategy")

        if trt_sop:
            self.drug_end = max(self.drug_end, self.age + DRUG_PERIOD)

        self.trt = self.age < self.drug_end
        if self.trt:
            self.trt_len += 1
        else:
            self.trt_len = 0



    def get_status_str(self):
        if self.trt_len > EFF_DELAY:
            self.trt_eff = True
        else:
            self.trt_eff = False
        return to_status_str(self.ost, self.vfa, self.trt_eff)

    def add_cost(self):
        if self.record.ost_result is not None:
            self.record.inc_cost += ost_cost()
        if self.record.vfa_result is not None:
            self.record.inc_cost += vfa_cost()
        if self.trt:
            self.record.inc_cost += drug_cost()
            self.stats.trt_cnt += 1

        if self.fx == 'vf':
            self.stats.vf_cnt += 1
        elif self.fx == 'hip':
            self.stats.hip_cnt += 1
        elif self.fx == 'wf':
            self.stats.wf_cnt += 1

    def add_utils(self):
        self.record.inc_utils += get_utility(self.fx,self.age)

    def state_transition(self):
        ret = None
        natual_rate = natual_death_rate(self.age)
        prob_death = self.fx_death_rate()
        self.old_fx = self.fx
        status_str = self.get_status_str()
        vector = PROB_TABLE[status_str][self.old_fx]
        prob_hip = vector['hip']
        prob_vf = vector['vf']
        prob_wf = vector['wf']
        prob_no_fix = 1 - prob_death - prob_hip - prob_vf - prob_wf

        nature_death = False
        if random.random() < natual_rate:
            nature_death = True

        if nature_death:
            self.fx = 'death'
        else:
            self.fx = np.random.choice(['no_fx', 'hip', 'vf', 'wf', 'death'], p=[prob_no_fix, prob_hip, prob_vf, prob_wf, prob_death])

        if self.fx not in ['no_fx', 'death']:
            # TODO: extra nursing
            self.record.inc_cost += self.er_cost() + nursing_cost()


        return ret




    def next_cycle(self):
        if self.fx!='death':
            self.set_ost_vfa()
            self.lab_test()
            self.add_cost()
            self.add_utils()
            trans_prt=self.state_transition()
            if self.fx == 'hip':
                self.last_hip = self.age
            elif self.fx == 'vf':
                self.last_vf = self.age
            elif self.fx == 'wf':
                self.last_wf = self.age

            self.stats.total_cost += self.record.inc_cost *self.discount
            self.stats.total_utils = self.record.inc_utils * self.discount
            self.discount *= DISCOUNT

            self.records[int(self.age*2)] = self.record
            self.record = Record()

        self.age += 0.5
        return trans_prt

    def do_life(self):
        while self.age < 100:
            self.next_cycle()
            if self.fx == 'death':
                break



# def do_group(sample_num=None, base_age=None, test_freq=None, do_ost_test=None, do_vf_test=None):
#     print "sample_num={}, base_age={}, test_freq={}, do_ost_test={}, do_vf_test={}".format(sample_num, base_age, test_freq, do_ost_test, do_vf_test)
#     counter_health = Counter()
#     counter_hip = Counter()
#     counter_vf = Counter()
#     counter_wf = Counter()
#     total_cost = 0
#     total_utils = 0
#     total_hip = 0
#     total_vf = 0
#     total_wf = 0
#     total_trt = 0
#     total_age = 0
#     for i in xrange(sample_num):
#         h = Human(base_age=base_age, test_freq=test_freq, do_ost_test=do_ost_test, do_vf_test=do_vf_test)
#         h.do_life()
#         total_cost += h.acc_cost
#         total_utils += h.acc_utils
#         total_hip += h.hip_cnt
#         total_vf += h.vf_cnt
#         total_wf += h.wf_cnt
#         total_trt += h.trt_cnt
#         total_age += h.age
#         counter_hip[h.hip_cnt] +=1
#         counter_vf[h.vf_cnt] +=1
#         counter_wf[h.wf_cnt] +=1
#         if (not h.ost) and (not h.vfa):
#             counter_health[('no_ost_no_vfa')] += 1
#         elif (not h.ost) and h.vfa:
#             counter_health[('no_ost_vfa')] += 1
#         elif h.ost and (not h.vfa):
#             counter_health[('ost_no_vfa')] += 1
#         elif h.ost and h.vfa:
#             counter_health[('ost_vfa')] += 1
#         if i%1000 == 0:
#             sys.stdout.write('.')
#             sys.stdout.flush()


#     ave_cost = total_cost/sample_num
#     ave_utils = total_utils/sample_num/2
#     ave_age = total_age/sample_num
#     health_str = "no_ost_no_vfa={:8d}, no_ost_vfa={:8d}, ost_no_vfa={:8d}, ost_vfa={:8d}".format(counter_health['no_ost_no_vfa'], counter_health['no_ost_vfa'], counter_health['ost_no_vfa'], counter_health['ost_vfa'])
#     main_result = "samples={}, test_freq={}, do_ost_test={:8s}, do_vf_test={:8s}, ave_cost={:14.4f}, ave_utils={:14.4f}, total_hip={:8}, total_vf={:8}, total_wf={:8}, total_trt={:8}, ave_age={:4}".format(sample_num, test_freq, str(do_ost_test), str(do_vf_test), ave_cost, ave_utils, total_hip, total_vf, total_wf, total_trt, ave_age)
#     print ""
#     print "{:230s} {}".format(main_result, health_str)
#     print counter_health
#     print 'hip cnt {}'.format(counter_hip)
#     print 'vf  cnt {}'.format(counter_vf)
#     print 'wf  cnt {}'.format(counter_wf)
#     print ""



# def run_groups():
#     SAMPLE_NUM = 1000*490
#     do_group(SAMPLE_NUM, test_freq=5, do_ost_test=False, do_vf_test=False)
#     do_group(SAMPLE_NUM, test_freq=5, do_ost_test=True, do_vf_test=False)
#     do_group(SAMPLE_NUM, test_freq=5, do_ost_test=True, do_vf_test=True)

# def run_one_person(base_age=None, test_freq=None, do_ost_test=None, do_vf_test=None):
#     print "base_age={}, test_freq={}, do_ost_test={}, do_vf_test={}".format(base_age, test_freq, do_ost_test, do_vf_test)
#     h = Human(base_age=base_age, test_freq=test_freq, do_ost_test=do_ost_test, do_vf_test=do_vf_test)
#     h.do_life(prt=True)



if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--strategy', type=int, choices=[0, 1, 2, 3])
    parser.add_argument("--log_level", type=str, choices=['debug'])
    args = parser.parse_args()
    if args.log_level == 'debug':
        print("set debug logger")
        logging.basicConfig(level=logging.DEBUG)
        Human.log.setLevel(logging.DEBUG)
    Human.strategy = args.strategy
    h = Human(65)
    h.do_life()


