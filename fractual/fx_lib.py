import sys
import random
import numpy as np
from collections import Counter
from prob_table import PROB_TABLE, set_ost_vfa, natual_death_rate

DRUG_PERIOD = 5
DRUG_HOLIDAY = 5
DRUG_PRICE = 600
FX_DEATH_RATE_LAST = 1
BASE_AGE = 65
DISCOUNT_RATE = 0.03
DISCOUNT = 1-DISCOUNT_RATE/2
EFF_DELAY = 2

VFA_SENSI = 0.85
VFA_SPEC = 0.92

OST_SENSI = 0.73
OST_SPEC = 1

def to_status_str(ost, vfa, trt):
    if (not ost) and (not vfa) and (not trt):
        return 'no_ost_no_trt'
    elif (not ost) and (not vfa) and trt:
        return 'no_ost_trt'
    elif (not ost) and vfa and (not trt):
        return 'has_vfa_no_trt'
    elif (not ost) and vfa and trt:
        return 'has_vfa_trt'
    elif ost and (not vfa) and (not trt):
        return 'has_ost_no_trt'
    elif ost and (not vfa) and trt:
        return 'has_ost_trt'
    elif ost and vfa and (not trt):
        return 'has_vfa_no_trt'
    elif ost and vfa and trt:
        return 'has_vfa_trt'


def ost_sensi(age):
    if age < 65:
        return 0.5
    else:
        return 0.73

def ost_spec(age):
    if age < 65:
        return 0.93
    else:
        return 1






def drug_cost():
    #TODO: FIX me price
    return 1.0*DRUG_PRICE/2


def ost_cost():
    return 120

def vf_cost():
    return 86

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
    __slots__ = ('test_freq', 'do_ost_test', 'do_vf_test',
    'age', 'next_test', 'acc_utils', 'acc_cost', 'ost', 'vfa','fx', 'trt', 'ost_test', 'vfa_test',
    'vf_cnt', 'hip_cnt', 'wf_cnt', 'trt_cnt',
    'drug_end', 'drug_holiday_end',
    'last_hip', 'last_vf', 'last_wf', 'fx_rate',
    'old_fx', 'trt_len', 'trt_eff',
    'inc_cost', 'inc_utils',
    'discount'

    )
    def __init__(self, base_age=None, test_freq=None, do_ost_test=None, do_vf_test=None):
        self.test_freq = test_freq
        self.do_ost_test = do_ost_test
        self.do_vf_test = do_vf_test

        self.age = base_age
        self.next_test = None
        self.acc_utils = 0
        self.acc_cost = 0
        self.vf_cnt = 0
        self.hip_cnt = 0
        self.wf_cnt = 0
        self.trt_cnt = 0
        self.ost = False
        self.vfa = False
        self.ost, self.vfa = set_ost_vfa(self.age, self.ost, self.vfa)
        self.fx = 'no_fx'
        self.trt = False
        self.trt_len = 0
        self.trt_eff = None
        self.old_fx = None
        self.ost_test = None
        self.vfa_test = None
        self.fx_rate =  'none'
        self.drug_end = 0
        self.drug_holiday_end = 0
        self.last_hip = 0
        self.last_vf = 0
        self.last_wf = 0
        self.inc_cost = None
        self.inc_utils = None
        self.discount = 1

    def __str__(self):
        ost = 'ost' if self.ost else 'no_ost'
        vfa = 'vfa' if self.ost else 'no_vfa'
        header = "age={:5},next_test={:5}, drug_end={:6}, last_hip={:4}, last_vf={:4}, last_wf={:4}, <inc_utils={:8.3f} acc_utils={:8.3f} | inc_cost={:12.3f} acc_cost={:12.3f}> |{:6}, {:6}| fx={:6}".format(
                self.age, self.next_test, self.drug_end, self.last_hip, self.last_vf, self.last_wf, self.inc_utils, self.acc_utils, self.inc_cost, self.acc_cost, ost, vfa, self.fx)

        if self.fx != 'death':
            return "{}   trt={:6},len={:2},eff={:6}, holiday_end={:5} ost_test={:6}, vfa_test={:6}, hip_cnt={:2}, vf_cnt={:2}, wf_cnt={:2}, trt_cnt={:4}, fx_rate={:6}".format(
                header, str(self.trt),self.trt_len, str(self.trt_eff), self.drug_holiday_end, self.ost_test, self.vfa_test, self.hip_cnt, self.vf_cnt, self.wf_cnt, self.trt_cnt, self.fx_rate)
        else:
            return header



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




    def ost_result(self):
        if self.ost:
            #  if has ost, OST_SENSI chance positve test result.
            if random.random() < OST_SENSI:
            #if random.random() < ost_sensi(self.age):
                return True
            else:
                return False
        else:
            if random.random() > OST_SPEC:
                #if random.random() > ost_spec(self.age):
                trt = True
            else:
                trt = False


    def strategy1_no_screening(self):
        return False


    def lab_test_strategy(self, strategy):
        if self.fx != 'no_fx':
            trt = True
        self.ost_test = None
        self.vfa_test = None
        if

        if trt:
            self.drug_end = max(self.drug_end, self.age + DRUG_PERIOD)

        self.trt = self.age < self.drug_end
        if self.trt:
            self.trt_len += 1
        else:
            self.trt_len = 0



    def lab_test(self):
        # #TODO delete
        # print self.fx





        do_test = False
        if self.next_test is None:
            do_test = True
            self.next_test = self.age + self.test_freq
        if self.age == self.next_test:
            do_test = True
            self.next_test = self.age + self.test_freq

        trt = False
        # if there is fx, ost is test is always positive, and therefore get treatment
        #TODO: enable this
        if self.fx != 'no_fx':
            trt = True
        self.ost_test = None
        self.vfa_test = None

        if do_test:
            # if no fracture.
            if self.do_ost_test:

                if self.do_vf_test and self.ost_test == 'Neg':
                    if self.vfa:
                        if random.random() < VFA_SENSI:
                            self.vfa_test = 'Pos'
                            trt = True
                        else:
                            self.vfa_test = 'Neg'
                            trt = False
                    else:
                        if random.random() > VFA_SPEC:
                            self.vfa_test = 'Pos'
                            trt = True
                        else:
                            self.vfa_test = 'Neg'
                            trt = False
        #TODO: with drug holiday
        # if trt:
        #     self.drug_end = max(self.drug_end, self.age + DRUG_PERIOD)
        if self.age > self.drug_holiday_end:
            if trt:
                self.drug_end = self.age + DRUG_PERIOD
                self.drug_holiday_end = self.age + DRUG_PERIOD + DRUG_HOLIDAY


        self.trt = self.age < self.drug_end
        if self.trt:
            self.trt_len += 1
        # TODO: effect until drug_holiday_end
        # else:
        #     self.trt_len = 0
        if self.age >= self.drug_holiday_end:
            self.trt_len = 0


        # if self.trt is None:
        #     raise Exception("trt cannot be None")
        # if self.do_ost_test and (self.ost_test is None):
        #     raise Exception("everyone should have done OST TEST")

    def get_status_str(self):
        if self.trt_len > EFF_DELAY:
            self.trt_eff = True
        else:
            self.trt_eff = False
        return to_status_str(self.ost, self.vfa, self.trt_eff)

    def add_cost(self):
        if self.ost_test is not None:
            self.inc_cost += ost_cost()
        if self.vfa_test is not None:
            self.inc_cost += vf_cost()
        if self.trt:
            self.inc_cost += drug_cost()
            self.trt_cnt += 1

        if self.fx == 'vf':
            self.vf_cnt += 1
        elif self.fx == 'hip':
            self.hip_cnt += 1
        elif self.fx == 'wf':
            self.wf_cnt += 1

    def add_utils(self):
        self.inc_utils += get_utility(self.fx,self.age)





    def state_transition(self, prt=False):
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
            self.inc_cost += self.er_cost() + 12000


        if prt:
            ret = "{:15s}, old_fx={:5s},natural_death={:8f},no_fx={:8f},hip={:8f},vf={:8f},wf={:8f},fx_death={:8f}, new_fx={:5s}".format(self.get_status_str(), self.old_fx, natual_rate,prob_no_fix,prob_hip,prob_vf,prob_wf,prob_death, self.fx)
        # #TODO delete
        # print self.fx
        return ret




    def next_cycle(self,prt=False):
        if self.fx!='death':
            self.inc_cost = 0
            self.inc_utils = 0
            self.ost, self.vfa = set_ost_vfa(self.age, self.ost, self.vfa)
            self.lab_test()
            self.add_cost()
            self.add_utils()
            trans_prt=self.state_transition(prt)
            if self.fx == 'hip':
                self.last_hip = self.age
            elif self.fx == 'vf':
                self.last_vf = self.age
            elif self.fx == 'wf':
                self.last_wf = self.age

            self.inc_cost = self.inc_cost * self.discount
            self.inc_utils = self.inc_utils * self.discount
            self.discount *= DISCOUNT

            self.acc_cost += self.inc_cost
            self.acc_utils += self.inc_utils

        self.age += 0.5
        return trans_prt

    def do_life(self, prt=False):
        while self.age < 100:
            cycle_prt=self.next_cycle(prt)
            if prt:
                print "{:290s}, ___ {}".format(self.__str__(), cycle_prt)
            if self.fx == 'death':
                break



def do_group(sample_num=None, base_age=None, test_freq=None, do_ost_test=None, do_vf_test=None):
    print "sample_num={}, base_age={}, test_freq={}, do_ost_test={}, do_vf_test={}".format(sample_num, base_age, test_freq, do_ost_test, do_vf_test)
    counter_health = Counter()
    counter_hip = Counter()
    counter_vf = Counter()
    counter_wf = Counter()
    total_cost = 0
    total_utils = 0
    total_hip = 0
    total_vf = 0
    total_wf = 0
    total_trt = 0
    total_age = 0
    for i in xrange(sample_num):
        h = Human(base_age=base_age, test_freq=test_freq, do_ost_test=do_ost_test, do_vf_test=do_vf_test)
        h.do_life()
        total_cost += h.acc_cost
        total_utils += h.acc_utils
        total_hip += h.hip_cnt
        total_vf += h.vf_cnt
        total_wf += h.wf_cnt
        total_trt += h.trt_cnt
        total_age += h.age
        counter_hip[h.hip_cnt] +=1
        counter_vf[h.vf_cnt] +=1
        counter_wf[h.wf_cnt] +=1
        if (not h.ost) and (not h.vfa):
            counter_health[('no_ost_no_vfa')] += 1
        elif (not h.ost) and h.vfa:
            counter_health[('no_ost_vfa')] += 1
        elif h.ost and (not h.vfa):
            counter_health[('ost_no_vfa')] += 1
        elif h.ost and h.vfa:
            counter_health[('ost_vfa')] += 1
        if i%1000 == 0:
            sys.stdout.write('.')
            sys.stdout.flush()


    ave_cost = total_cost/sample_num
    ave_utils = total_utils/sample_num/2
    ave_age = total_age/sample_num
    health_str = "no_ost_no_vfa={:8d}, no_ost_vfa={:8d}, ost_no_vfa={:8d}, ost_vfa={:8d}".format(counter_health['no_ost_no_vfa'], counter_health['no_ost_vfa'], counter_health['ost_no_vfa'], counter_health['ost_vfa'])
    main_result = "samples={}, test_freq={}, do_ost_test={:8s}, do_vf_test={:8s}, ave_cost={:14.4f}, ave_utils={:14.4f}, total_hip={:8}, total_vf={:8}, total_wf={:8}, total_trt={:8}, ave_age={:4}".format(sample_num, test_freq, str(do_ost_test), str(do_vf_test), ave_cost, ave_utils, total_hip, total_vf, total_wf, total_trt, ave_age)
    print ""
    print "{:230s} {}".format(main_result, health_str)
    print counter_health
    print 'hip cnt {}'.format(counter_hip)
    print 'vf  cnt {}'.format(counter_vf)
    print 'wf  cnt {}'.format(counter_wf)
    print ""



def run_groups():
    SAMPLE_NUM = 1000*490
    do_group(SAMPLE_NUM, test_freq=5, do_ost_test=False, do_vf_test=False)
    do_group(SAMPLE_NUM, test_freq=5, do_ost_test=True, do_vf_test=False)
    do_group(SAMPLE_NUM, test_freq=5, do_ost_test=True, do_vf_test=True)

def run_one_person(base_age=None, test_freq=None, do_ost_test=None, do_vf_test=None):
    print "base_age={}, test_freq={}, do_ost_test={}, do_vf_test={}".format(base_age, test_freq, do_ost_test, do_vf_test)
    h = Human(base_age=base_age, test_freq=test_freq, do_ost_test=do_ost_test, do_vf_test=do_vf_test)
    h.do_life(prt=True)



if __name__ == '__main__':
    #run_one_person(5, False, False)
    #run_one_person(5, True, True)
    run_groups()