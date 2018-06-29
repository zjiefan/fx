import random
import numpy as np



PROB_TABLE = {}
PROB_TABLE['no_ost_no_trt'] = {}
PROB_TABLE['no_ost_no_trt']['no_fx'] = {}
PROB_TABLE['no_ost_no_trt']['no_fx']['hip'] = 0.00070024
PROB_TABLE['no_ost_no_trt']['no_fx']['vf']  = 0.00070024
PROB_TABLE['no_ost_no_trt']['no_fx']['wf']  = 0.00006299
PROB_TABLE['no_ost_no_trt']['hip'] = {}
PROB_TABLE['no_ost_no_trt']['hip']['hip'] = 0.00786026
PROB_TABLE['no_ost_no_trt']['hip']['vf']  = 0.00480247
PROB_TABLE['no_ost_no_trt']['hip']['wf']  = 0.0025
PROB_TABLE['no_ost_no_trt']['vf'] = {}
PROB_TABLE['no_ost_no_trt']['vf']['hip'] = 0.00370072
PROB_TABLE['no_ost_no_trt']['vf']['vf']  = 0.02480771
PROB_TABLE['no_ost_no_trt']['vf']['wf']  = 0.00511307
PROB_TABLE['no_ost_no_trt']['wf'] = {}
PROB_TABLE['no_ost_no_trt']['wf']['hip'] = 0.00257979
PROB_TABLE['no_ost_no_trt']['wf']['vf']  = 0.00220672
PROB_TABLE['no_ost_no_trt']['wf']['wf']  = 0.00175901

PROB_TABLE['has_ost_no_trt'] = {}
PROB_TABLE['has_ost_no_trt']['no_fx'] = {}
PROB_TABLE['has_ost_no_trt']['no_fx']['hip'] = 0.00277684
PROB_TABLE['has_ost_no_trt']['no_fx']['vf']  = 0.00744093
PROB_TABLE['has_ost_no_trt']['no_fx']['wf']  = 0.00599948
PROB_TABLE['has_ost_no_trt']['hip'] = {}
PROB_TABLE['has_ost_no_trt']['hip']['hip'] = 0.01786026
PROB_TABLE['has_ost_no_trt']['hip']['vf']  = 0.00780247
PROB_TABLE['has_ost_no_trt']['hip']['wf']  = 0.0055
PROB_TABLE['has_ost_no_trt']['vf'] = {}
PROB_TABLE['has_ost_no_trt']['vf']['hip'] = 0.00631997
PROB_TABLE['has_ost_no_trt']['vf']['vf']  = 0.02672291
PROB_TABLE['has_ost_no_trt']['vf']['wf']  = 0.00695305
PROB_TABLE['has_ost_no_trt']['wf'] = {}
PROB_TABLE['has_ost_no_trt']['wf']['hip'] = 0.00357979
PROB_TABLE['has_ost_no_trt']['wf']['vf']  = 0.00320672
PROB_TABLE['has_ost_no_trt']['wf']['wf']  = 0.00275901

PROB_TABLE['has_ost_trt'] = {}
PROB_TABLE['has_ost_trt']['no_fx'] = {}
PROB_TABLE['has_ost_trt']['no_fx']['hip'] = 0.0012555
PROB_TABLE['has_ost_trt']['no_fx']['vf']  = 0.00264944
PROB_TABLE['has_ost_trt']['no_fx']['wf']  = 0.00534908
PROB_TABLE['has_ost_trt']['hip'] = {}
PROB_TABLE['has_ost_trt']['hip']['hip'] = 0.00520493
PROB_TABLE['has_ost_trt']['hip']['vf']  = 0.00402953
PROB_TABLE['has_ost_trt']['hip']['wf']  = 0.00292734
PROB_TABLE['has_ost_trt']['vf'] = {}
PROB_TABLE['has_ost_trt']['vf']['hip'] = 0.0018418
PROB_TABLE['has_ost_trt']['vf']['vf']  = 0.01380084
PROB_TABLE['has_ost_trt']['vf']['wf']  = 0.00370072
PROB_TABLE['has_ost_trt']['wf'] = {}
PROB_TABLE['has_ost_trt']['wf']['hip'] = 0.00104324
PROB_TABLE['has_ost_trt']['wf']['vf']  = 0.00165609
PROB_TABLE['has_ost_trt']['wf']['wf']  = 0.00146847

PROB_TABLE['no_ost_trt'] = {}
PROB_TABLE['no_ost_trt']['no_fx'] = {}
PROB_TABLE['no_ost_trt']['no_fx']['hip'] = 0.000308106
PROB_TABLE['no_ost_trt']['no_fx']['vf']  = 0.00039213
PROB_TABLE['no_ost_trt']['no_fx']['wf']  = 0.00005543
PROB_TABLE['no_ost_trt']['hip'] = {}
PROB_TABLE['no_ost_trt']['hip']['hip'] = 0.00345851
PROB_TABLE['no_ost_trt']['hip']['vf']  = 0.00268938
PROB_TABLE['no_ost_trt']['hip']['wf']  = 0.0022
PROB_TABLE['no_ost_trt']['vf'] = {}
PROB_TABLE['no_ost_trt']['vf']['hip'] = 0.001628317
PROB_TABLE['no_ost_trt']['vf']['vf']  = 0.013892318
PROB_TABLE['no_ost_trt']['vf']['wf']  = 0.004499502
PROB_TABLE['no_ost_trt']['wf'] = {}
PROB_TABLE['no_ost_trt']['wf']['hip'] = 0.001135108
PROB_TABLE['no_ost_trt']['wf']['vf']  = 0.001235763
PROB_TABLE['no_ost_trt']['wf']['wf']  = 0.001547929

PROB_TABLE['has_vf_no_trt'] = {}
PROB_TABLE['has_vf_no_trt']['no_fx'] = {}
PROB_TABLE['has_vf_no_trt']['no_fx']['hip'] = 0.01453593
PROB_TABLE['has_vf_no_trt']['no_fx']['vf']  = 0.33670867
PROB_TABLE['has_vf_no_trt']['no_fx']['wf']  = 0.0111249
PROB_TABLE['has_vf_no_trt']['hip'] = {}
PROB_TABLE['has_vf_no_trt']['hip']['hip'] = 0.018078598
PROB_TABLE['has_vf_no_trt']['hip']['vf']  = 0.06051112
PROB_TABLE['has_vf_no_trt']['hip']['wf']  = 0.004
PROB_TABLE['has_vf_no_trt']['vf'] = {}
PROB_TABLE['has_vf_no_trt']['vf']['hip'] = 0.00631997
PROB_TABLE['has_vf_no_trt']['vf']['vf']  = 0.02672291
PROB_TABLE['has_vf_no_trt']['vf']['wf']  = 0.00695305
PROB_TABLE['has_vf_no_trt']['wf'] = {}
PROB_TABLE['has_vf_no_trt']['wf']['hip'] = 0.00593352
PROB_TABLE['has_vf_no_trt']['wf']['vf']  = 0.02780467
PROB_TABLE['has_vf_no_trt']['wf']['wf']  = 0.00281442

PROB_TABLE['has_vf_trt'] = {}
PROB_TABLE['has_vf_trt']['no_fx'] = {}
PROB_TABLE['has_vf_trt']['no_fx']['hip'] = 0.00639581
PROB_TABLE['has_vf_trt']['no_fx']['vf']  = 0.18855685
PROB_TABLE['has_vf_trt']['no_fx']['wf']  = 0.00978989
PROB_TABLE['has_vf_trt']['hip'] = {}
PROB_TABLE['has_vf_trt']['hip']['hip'] = 0.00795458
PROB_TABLE['has_vf_trt']['hip']['vf']  = 0.03388623
PROB_TABLE['has_vf_trt']['hip']['wf']  = 0.00352
PROB_TABLE['has_vf_trt']['vf'] = {}
PROB_TABLE['has_vf_trt']['vf']['hip'] = 0.0018418
PROB_TABLE['has_vf_trt']['vf']['vf']  = 0.0138084
PROB_TABLE['has_vf_trt']['vf']['wf']  = 0.00370072
PROB_TABLE['has_vf_trt']['wf'] = {}
PROB_TABLE['has_vf_trt']['wf']['hip'] = 0.00261075
PROB_TABLE['has_vf_trt']['wf']['vf']  = 0.01557062
PROB_TABLE['has_vf_trt']['wf']['wf']  = 0.00247669



def to_status_str(ost, vf, trt):
    if (not ost) and (not vf) and (not trt):
        return 'no_ost_no_trt'
    elif (not ost) and (not vf) and trt:
        return 'no_ost_trt'
    elif (not ost) and vf and (not trt):
        return 'has_vf_no_trt'
    elif (not ost) and vf and trt:
        return 'has_vf_trt'
    elif ost and (not vf) and (not trt):
        return 'has_ost_no_trt'
    elif ost and (not vf) and trt:
        return 'has_ost_trt'
    elif ost and vf and (not trt):
        return 'has_vf_no_trt'
    elif ost and vf and trt:
        return 'has_vf_trt'


VF_SENSI = 0.85
VF_SPEC = 0.92
VF_PREVAL = {}
VF_PREVAL[50] = 0.017
VF_PREVAL[60] = 0.0386
VF_PREVAL[70] = 0.0647


OST_SENSI = 0.73
OST_SPEC = 1
OST_PREVAL = {}
OST_PREVAL[55] = 0.561
OST_PREVAL[60] = 0.657
OST_PREVAL[70] = 0.775
OST_PREVAL[80] = 0.876

def ost_preval(age):
    if age < 60:
        return OST_PREVAL[55]
    elif age < 70:
        return OST_PREVAL[60]
    elif age < 80:
        return OST_PREVAL[70]
    else:
        return OST_PREVAL[80]

def fx_preval(age):
    return VF_PREVAL[50]

def natual_death_rate(age):
    #TODO: remove this
    return 0
    if age < 60:
        return 0.0027879
    elif age < 65:
        return 0.0039132
    elif age < 70:
        return 0.0057923
    elif age < 75:
        return 0.0093225
    elif age < 80:
        return 0.0152604
    elif age < 85:
        return 0.0264878
    else:
        return 0.0676953

def fx_death_rate(fx, age):
    #TODO: remove this
    return 0
    if fx == 'vf':
        if age < 80:
            return 0.0335633
        else:
            return 0.0851230
    elif fx == 'hip':
        if age < 80:
            return 0.0268606
        else:
            return 0.0851230
    elif fx == 'wf':
        if age < 80:
            return 0.0045102
        else:
            return 0.031496
    else:
        raise Exception("unknown fx type")

def drug_cost():
    #TODO: FIX me price
    return 60

def er_cost(fx, age):
    if fx=='hip':
        if age < 65:
            return 28496 + 180
        else:
            return 18541 + 180
    elif fx == 'vf':
        if age < 65:
            return 27320 + 180
        else:
            return 20190 + 180
    elif fx == 'wf':
        if age < 65:
            return 5088 + 180
        else:
            return 3486 + 180
    else:
        raise Exception("unknown fx")

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
    'age', 'next_test_age', 'last_fx_age', 'utils', 'cost', 'ost', 'fx', 'trt', 'ost_test', 'vf_test',
    'vf_cnt', 'hip_cnt', 'wf_cnt', 'trt_cnt'

    )
    def __init__(self, test_freq=None, do_ost_test=None, do_vf_test=None):
        self.test_freq = test_freq
        self.do_ost_test = do_ost_test
        self.do_vf_test = do_vf_test

        self.age = 55
        self.next_test_age = None
        self.last_fx_age = 0
        self.utils = 0
        self.cost = 0
        self.vf_cnt = 0
        self.hip_cnt = 0
        self.wf_cnt = 0
        self.trt_cnt = 0
        self.ost = False
        if random.random() < ost_preval(self.age):
            self.ost = True
        self.fx = 'no_fx'
        if random.random() < fx_preval(self.age):
            self.fx = 'vf'
        self.trt = None
        self.ost_test = None
        self.vf_test = None

    def __str__(self):
        if self.fx != 'death':
            return "age={:4},next_test_age={:5},last_fx_age={:4},utils={:8},cost={:8},ost={:6},fx={:6},trt={:6},ost_test={:6},vf_test={:6},hip_cnt={},vf_cnt={},wf_cnt={},trt_cnt={}".format(
                self.age, self.next_test_age, self.last_fx_age, self.utils, self.cost, str(self.ost), self.fx, str(self.trt), self.ost_test, self.vf_test, self.hip_cnt, self.vf_cnt,self.wf_cnt,self.trt_cnt)
        else:
            return "age={:4},next_test_age={:5},last_fx_age={:4},utils={:8},cost={:8},ost={:6},fx={:6}".format(self.age, self.next_test_age, self.last_fx_age, self.utils, self.cost, str(self.ost), self.fx)

    def lab_test(self):
        # #TODO delete
        # print self.fx

        do_test = False
        if self.next_test_age is None:
            do_test = True
            self.next_test_age = self.age + self.test_freq
        if self.age == self.next_test_age:
            do_test = True
            self.next_test_age = self.age + self.test_freq

        self.trt = False
        self.ost_test = None
        self.vf_test = None

        # if there is fx, ost is test is always positive, and therefore get treatment
        #TODO: enable this
        # if self.fx != 'no_fx':
        #     self.ost_test = 'Pos'
        #     self.trt = True

        if do_test:
            # if no fracture.
            if self.do_ost_test:
                if self.ost:
                    #  if has ost, OST_SENSI chance positve test result.
                    if random.random() < OST_SENSI:
                        self.ost_test = 'Pos'
                        self.trt = True
                    else:
                        self.ost_test = 'Neg'
                        self.trt = False
                else:
                    if random.random() > OST_SPEC:
                        self.ost_test = 'Pos'
                        self.trt = True
                    else:
                        self.ost_test = 'Neg'
                        self.trt = False

                if self.do_vf_test and self.ost_test == 'Neg':
                    if self.fx == 'vf':
                        if random.random() < VF_SENSI:
                            self.vf_test = 'Pos'
                            self.trt = True
                        else:
                            self.vf_test = 'Neg'
                            self.trt = False
                    else:
                        if random.random() > VF_SPEC:
                            self.vf_test = 'Pos'
                            self.trt = True
                        else:
                            self.vf_test = 'Neg'
                            self.trt = False

            if self.trt is None:
                raise Exception("trt cannot be None")
            if self.do_ost_test and (self.ost_test is None):
                raise Exception("everyone should have done OST TEST")

    def get_status_str(self):
        has_vf = self.fx == 'vf'
        return to_status_str(self.ost, has_vf, self.trt)

    def add_cost(self):
        if self.ost_test is not None:
            self.cost += ost_cost()
        if self.vf_test is not None:
            self.cost += vf_cost()
        if self.trt:
            self.cost += drug_cost()
            self.trt_cnt += 1

        if self.fx == 'vf':
            self.vf_cnt += 1
        elif self.fx == 'hip':
            self.hip_cnt += 1
        elif self.fx == 'wf':
            self.wf_cnt += 1

    def add_utils(self):
        util = get_utility(self.fx,self.age)
        self.utils += util




    def state_transition(self, prt=False):
        ret = None
        if random.random() < natual_death_rate(self.age):
            self.fx = 'death'
            return ret
        vector = PROB_TABLE[self.get_status_str()][self.fx]
        if prt:
            ret = "use table {:20s}, {}, {}".format(self.get_status_str(), self.fx, str(vector))

        if self.fx == 'no_fx':
            prob_death = 0
        else:
            prob_death = fx_death_rate(self.fx, self.age)
        prob_hip = vector['hip']
        prob_vf = vector['vf']
        prob_wf = vector['wf']
        prob_no_fix = 1 - prob_death - prob_hip - prob_vf - prob_wf
        self.fx = np.random.choice(['no_fx', 'hip', 'vf', 'wf', 'death'], p=[prob_no_fix, prob_hip, prob_vf, prob_wf, prob_death])
        # #TODO delete
        # print self.fx
        return ret




    def next_cycle(self,prt=False):
        if self.fx!='death':
            self.lab_test()
            self.add_cost()
            self.add_utils()
            trans_prt=self.state_transition(prt)
            if self.fx not in ['no_fx', 'death']:
                # TODO: extra nursing
                self.cost += er_cost(self.fx, self.age) + 12000
        self.age += 0.5
        return trans_prt

    def do_life(self, prt=False):
        for i in xrange(89):
            cycle_prt=self.next_cycle(prt)
            if prt:
                print "{}, ____________   {}".format(self.__str__(), cycle_prt)
            if self.fx == 'death':
                break



def do_group(sample_num, test_freq=None, do_ost_test=None, do_vf_test=None):
    total_cost = 0
    total_utils = 0
    total_hip = 0
    total_vf = 0
    total_wf = 0
    total_trt = 0
    for i in xrange(sample_num):
        h = Human(test_freq=test_freq, do_ost_test=do_ost_test, do_vf_test=do_vf_test)
        h.do_life()
        total_cost += h.cost
        total_utils += h.utils
        total_hip += h.hip_cnt
        total_vf += h.vf_cnt
        total_wf += h.wf_cnt
        total_trt += h.trt_cnt

    ave_cost = total_cost/sample_num
    ave_utils = total_utils/sample_num
    print "samples={}, test_freq={}, do_ost_test={}, do_vf_test={}, ave_cost={}, ave_utils={}, total_hip={}, total_vf={}, total_wf={}, total_trt={}".format(sample_num, test_freq, do_ost_test, do_vf_test, ave_cost, ave_utils, total_hip, total_vf, total_wf, total_trt)


def run_groups():
    SAMPLE_NUM = 1000*10
    do_group(SAMPLE_NUM, test_freq=5, do_ost_test=False, do_vf_test=False)
    do_group(SAMPLE_NUM, test_freq=5, do_ost_test=True, do_vf_test=False)
    do_group(SAMPLE_NUM, test_freq=5, do_ost_test=True, do_vf_test=True)

def run_one_person():
    h = Human(test_freq=5, do_ost_test=False, do_vf_test=False)
    h.do_life(prt=True)



if __name__ == '__main__':
    run_one_person()
    #run_groups()






