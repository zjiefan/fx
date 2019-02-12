import os
import sys
import logging
import random
import numpy as np
import multiprocessing
from collections import Counter
from prob_table import PROB_TABLE, get_natual_death_rate, get_ost_test_result, get_vfa_test_result, take_ost_trt
from cost_table import drug_cost, ost_cost, vfa_cost, nursing_cost
from human_stats import Record, HumanStats

DRUG_PERIOD = 5
DRUG_HOLIDAY = 5

FX_DEATH_RATE_LAST = 1
BASE_AGE = 65
DISCOUNT_RATE = 0.03
DISCOUNT = 1-DISCOUNT_RATE/2
EFF_DELAY = 2

VF_SCALE = float(os.environ['VF_SCALE'])

VFA_OST_NORMAL = 0.085 * VF_SCALE
VFA_OST_LBL = 0.1 * VF_SCALE
VFA_OST_LBM1 = 0.157 * VF_SCALE
VFA_OST_SICK = 0.343 * VF_SCALE


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
    __slots__ = (
    'test_freq', 'strategy',
    'age', 'next_test', 'ost', 'vfa','fx',
    'drug_end', 'drug_holiday_end',
    'last_hip', 'last_vf', 'last_wf', 'fx_rate',
    'old_fx', 'trt_len', 'trt_eff',
    'discount',

    'ost_result', 'vfa_result',
    'vf_trt_sop', 'sick_trt_sop', 'vfa_trt_sop',
    'trt',
    'inc_cost', 'inc_utils',

    'total_utils', 'total_cost', 'final_age',
    'vf_cnt', 'hip_cnt', 'wf_cnt', 'trt_cnt',
    'prob_vector',
    'vfa_treatment_prob',
    'drug_scale', 'perfect_vf',

    )

    print_slots = (
        ('age', '5.1f'),
        ('ost', '6s'),
        ('vfa', '5s'),
        ('ost_result','6s'),
        ('vfa_result','6s'),

        ('fx', '6s'),
        ('last_hip', '5.1f'),
        ('last_vf', '5.1f'),
        ('last_wf', '5.1f'),
        ('hip_cnt', '2d'),
        ('vf_cnt', '2d'),
        ('wf_cnt', '2d'),
        ('vf_trt_sop','5s'),
        ('sick_trt_sop','5s'),
        ('vfa_trt_sop','5s'),
        ('drug_end', '5.1f'),
        ('trt', '5s'),
        ('inc_cost', '8.1f'),
        ('inc_utils', '6.1f'),
        ('total_cost','8.1f'),
        ('total_utils','8.4f'),
        ('trt_len', '4.1f'),
        ('drug_holiday_end', '5.1f'),
        ('trt_eff', '5s'),
        ('prob_vector', 's')


        )
    log = logging.getLogger("Human")
    def __init__(self, base_age=None, test_freq=5, strategy=None, vfa_treatment_prob=None, drug_scale=1.0, perfect_vf=0):
        self.test_freq = test_freq
        self.strategy = strategy
        self.vfa_treatment_prob = vfa_treatment_prob
        self.drug_scale=drug_scale
        self.perfect_vf = perfect_vf

        self.age = base_age
        self.next_test = None
        self.ost = None
        self.vfa = None
        self.set_ost_vfa()
        self.fx = 'no_fx'
        # self.trt = False
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

        self.ost_result = None
        self.vfa_result = None
        self.vf_trt_sop = None
        self.sick_trt_sop = None
        self.vfa_trt_sop = None
        self.trt = None
        self.inc_cost = 0
        self.inc_utils = 0

        self.vf_cnt = 0
        self.hip_cnt = 0
        self.wf_cnt = 0
        self.trt_cnt = 0
        self.total_cost = 0
        self.total_utils = 0


    def __str__(self):
        ret = []
        for slot, fmt in self.print_slots:
            value = getattr(self, slot)
            fmt_str = "{}={:" + fmt + "}"
            if value is None:
                value =""
            if value == 0:
                fmt = fmt[0] + 's'
                value = ""
            fmt_str = "{}={:" + fmt + "}"
            if isinstance(value, bool):
                value = str(value)
            ret.append(fmt_str.format(slot, value))
        return '  '.join(ret)





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



    def get_fx_death_rate(self):
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
        if self.hip_cnt + self.vf_cnt + self.wf_cnt == 0:
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
            if self.hip_cnt >= 1:
                if self.age < 65:
                    return 90855
                else:
                    return 42991
            elif self.vf_cnt >= 1:
                if self.age < 65:
                    return 84933
                else:
                    return 44526
            elif self.wf_cnt >=1:
                if self.age < 65:
                    return 52732
                else:
                    return 41987
            else:
                raise Exception("unknown fx")


    def lab_test(self):
        if self.fx != 'no_fx':
            self.vf_trt_sop = True

        do_test = False
        if self.next_test is None:
            do_test = True
            self.next_test = self.age + self.test_freq
        if self.age == self.next_test:
            do_test = True
            self.next_test = self.age + self.test_freq

        if self.vf_trt_sop:
            do_test = False
        if self.age < self.drug_end:
            do_test = False


        if do_test and self.strategy:
            self.ost_result = self.ost
            if self.strategy == 4:
                vfa_types = ('sick', 'lbm1')
            elif self.strategy == 5:
                vfa_types = ('sick', 'lbm1', 'lbl')
            else:
                self.log.error("unexpected strategy %d", self.strategy)
                raise Exception("unknown strategy")
            if self.ost_result in vfa_types:
                self.vfa_result = get_vfa_test_result(self.vfa, self.perfect_vf)
                if self.vfa_result == 'Pos':
                    self.vfa_trt_sop = (random.random() < self.vfa_treatment_prob)
                elif self.ost_result == 'sick':
                    self.sick_trt_sop = take_ost_trt()

        if self.vf_trt_sop or self.sick_trt_sop or self.vfa_trt_sop:
            self.drug_end = max(self.drug_end, self.age + DRUG_PERIOD)

        if self.age < self.drug_end:
            self.trt = True
        if self.trt:
            self.trt_len += 1
        else:
            self.trt_len = 0

        if self.trt_len > EFF_DELAY:
            self.drug_holiday_end = self.age + 5
        if self.age <= self.drug_holiday_end:
            self.trt_eff = True
        else:
            self.trt_eff = None



    def get_status_str(self):
        return to_status_str(self.ost, self.vfa, self.trt_eff)

    def add_cost(self):
        if self.ost_result is not None:
            self.inc_cost += ost_cost()
        if self.vfa_result is not None:
            self.inc_cost += vfa_cost()
        if self.trt:
            self.inc_cost += drug_cost()*self.drug_scale
            self.trt_cnt += 1

        if self.fx not in ['no_fx', 'death']:
            # TODO: extra nursing
            self.inc_cost += self.er_cost() + nursing_cost()


        if self.fx == 'vf':
            self.vf_cnt += 1
        elif self.fx == 'hip':
            self.hip_cnt += 1
        elif self.fx == 'wf':
            self.wf_cnt += 1

    def add_utils(self):
        self.inc_utils += get_utility(self.fx,self.age)

    def state_transition(self):
        ret = None
        status_str = self.get_status_str()
        natual_death_rate = get_natual_death_rate(self.age)
        fx_death_rate = self.get_fx_death_rate()
        self.old_fx = self.fx
        self.log.debug("at age %.1f, status str is %s", self.age, status_str)
        vector = PROB_TABLE[status_str][self.old_fx]
        prob_hip = vector['hip']
        prob_vf = vector['vf']
        prob_wf = vector['wf']
        prob_no_fix = 1 - fx_death_rate - prob_hip - prob_vf - prob_wf

        self.log.debug("get trans prob no_fx %.5f, hip %.5f, vf %.5f, wf %.5f, natual_death_rate %.5f, fx_death_rate %.5f", prob_no_fix, prob_hip, prob_vf, prob_wf, natual_death_rate, fx_death_rate)
        self.prob_vector = "(no=%6.3f%% h%6.3f%% v%6.3f%% w%6.3f%% n_death%6.3f%% f_death%6.3f%%)"%(prob_no_fix*100, prob_hip*100, prob_vf*100, prob_wf*100, natual_death_rate*100, fx_death_rate*100)
        nature_death = False
        if random.random() < natual_death_rate:
            nature_death = True

        if nature_death:
            self.fx = 'death'
        else:
            self.fx = np.random.choice(['no_fx', 'hip', 'vf', 'wf', 'death'], p=[prob_no_fix, prob_hip, prob_vf, prob_wf, fx_death_rate])
        self.log.debug("transition result %s", self.fx)



        return ret




    def next_cycle(self):
        if self.fx!='death':
            self.set_ost_vfa()
            self.lab_test()
            self.add_cost()
            self.add_utils()
            self.state_transition()


            if self.fx == 'hip':
                self.last_hip = self.age
            elif self.fx == 'vf':
                self.last_vf = self.age
            elif self.fx == 'wf':
                self.last_wf = self.age
            self.total_cost += self.inc_cost *self.discount
            self.total_utils += self.inc_utils * self.discount
            self.log.info("%s", self)

            self.ost_result = None
            self.vfa_result = None
            self.vf_trt_sop = None
            self.sick_trt_sop = None
            self.vfa_trt_sop = None
            self.trt = None
            self.inc_cost = 0
            self.inc_utils = 0


        self.age += 0.5
        return

    def do_life(self):
        while self.age < 100:
            self.next_cycle()
            if self.fx == 'death':
                break


class GroupResult(object):
    __slots__ = (
                'total_cost', 'total_utils', 'total_hip_cnt', 'total_vf_cnt', 'total_wf_cnt',
                'total_trt_cnt', 'total_age', 'person_cnt',
                'counter_hip', 'counter_wf', 'counter_vf',
                )

    average_list = ('cost', 'utils', 'hip_cnt', 'vf_cnt', 'wf_cnt', 'trt_cnt', 'age')

    def __init__(self):
        self.counter_hip = Counter()
        self.counter_vf = Counter()
        self.counter_wf = Counter()
        self.total_cost = 0
        self.total_utils = 0
        self.total_hip_cnt = 0
        self.total_vf_cnt = 0
        self.total_wf_cnt = 0
        self.total_trt_cnt = 0
        self.total_age = 0
        self.person_cnt = 0

    def __str__(self):
        ret = []
        for slot in self.__slots__:
            value = getattr(self, slot)
            ret.append("{}={:6}".format(slot, value))
        return ','.join(ret)

    def __iadd__(self, other):
        for slot in self.__slots__:
            value = getattr(self, slot)
            other_value = getattr(other, slot)
            setattr(self, slot, value + other_value)
        return self

    def __add__(self, other):
        ret = GroupResult()
        for slot in self.__slots__:
            value = getattr(self, slot)
            other_value = getattr(other, slot)
            setattr(self, slot, value + other_value)
        return ret

    def average(self):
        ret = []
        for slot in self.average_list:
            name = 'total_' + slot
            value = getattr(self, name)
            ret.append("average_{}={:10.4f}".format(slot, value*1.0/self.person_cnt))
        return ',    '.join(ret)



def do_group((sample_num, base_age, test_freq, strategy,vfa_treatment_prob, drug_scale, perfect_vf)):
    # print "sample_num={}, strategy={}".format(sample_num, strategy)
    result = GroupResult()
    for i in xrange(sample_num):
        h = Human(base_age=base_age,test_freq=test_freq, strategy=strategy, vfa_treatment_prob=vfa_treatment_prob, drug_scale=drug_scale, perfect_vf=perfect_vf)
        h.do_life()
        result.person_cnt += 1
        result.total_cost += h.total_cost
        result.total_utils += h.total_utils
        result.total_hip_cnt += h.hip_cnt
        result.total_vf_cnt += h.vf_cnt
        result.total_wf_cnt += h.wf_cnt
        result.total_trt_cnt += h.trt_cnt
        result.total_age += h.age
        result.counter_hip[h.hip_cnt] +=1
        result.counter_vf[h.vf_cnt] +=1
        result.counter_wf[h.wf_cnt] +=1

        if i & 0xfff == 0:
            sys.stdout.write('.')
            sys.stdout.flush()

    return result

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--strategy', type=int, choices=[4, 5], required=True)
    parser.add_argument("--population", type=int, required=True)
    parser.add_argument("--start_age", type=int, required=True)
    parser.add_argument("--test_freq", type=int, required=True)
    parser.add_argument("--vfa_treatment_prob", type=float, required=True)
    parser.add_argument("--drug_scale", type=float, required=True)
    parser.add_argument("--perfect_vf", type=int, required=True)

    args = parser.parse_args()

    cpu_count = multiprocessing.cpu_count()
    per_cpu_run = args.population/cpu_count
    print "strategy {}, population {}, start_age {}, test_freq {}, vfa_treatment_prob {}, drug_scale {}, perfect_vf {} vf_scale {}".format(
        args.strategy, args.population, args.start_age, args.test_freq, args.vfa_treatment_prob, args.drug_scale, args.perfect_vf, VF_SCALE)
    print "with {} cpu(s), each cpu process {} persons".format(cpu_count, per_cpu_run)

    data= []
    for _ in xrange(cpu_count):
        data.append((per_cpu_run, args.start_age, args.test_freq, args.strategy, args.vfa_treatment_prob, args.drug_scale, args.perfect_vf))


    p = multiprocessing.Pool(cpu_count)
    results = p.map(do_group, data)
    total = GroupResult()
    for result in results:
        # print result
        total += result
    print ''
    # print total
    print total.average()
    print ''
    print ''


    # parser = argparse.ArgumentParser()
    # parser.add_argument('--strategy', type=int, choices=[0, 1, 2, 3])
    # parser.add_argument("--log_level", type=str, choices=['debug'])
    # args = parser.parse_args()
    # if args.log_level == 'debug':
    #     print("set debug logger")
    #     logging.basicConfig(level=logging.DEBUG)
    #     Human.log.setLevel(logging.INFO)
    # Human.strategy = args.strategy
    # h = Human(65)
    # h.do_life()


