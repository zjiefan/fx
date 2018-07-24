import logging
import random
import os

logging.basicConfig()
log = logging.getLogger("prob_table")
log.setLevel(logging.DEBUG)



LBM_SCALE1 = 0.8
LBM_SCALE2 = 0.8

PROB_TABLE = {}
PROB_TABLE[('normal', 'no_trt')] = {}
PROB_TABLE[('normal', 'no_trt')]['no_fx'] = {}
PROB_TABLE[('normal', 'no_trt')]['no_fx']['hip'] = 0.00070024
PROB_TABLE[('normal', 'no_trt')]['no_fx']['vf']  = 0.00070024
PROB_TABLE[('normal', 'no_trt')]['no_fx']['wf']  = 0.00006299
PROB_TABLE[('normal', 'no_trt')]['hip'] = {}
PROB_TABLE[('normal', 'no_trt')]['hip']['hip'] = 0.00786026
PROB_TABLE[('normal', 'no_trt')]['hip']['vf']  = 0.00480247
PROB_TABLE[('normal', 'no_trt')]['hip']['wf']  = 0.0025
PROB_TABLE[('normal', 'no_trt')]['vf'] = {}
PROB_TABLE[('normal', 'no_trt')]['vf']['hip'] = 0.00370072
PROB_TABLE[('normal', 'no_trt')]['vf']['vf']  = 0.02480771
PROB_TABLE[('normal', 'no_trt')]['vf']['wf']  = 0.00511307
PROB_TABLE[('normal', 'no_trt')]['wf'] = {}
PROB_TABLE[('normal', 'no_trt')]['wf']['hip'] = 0.00257979
PROB_TABLE[('normal', 'no_trt')]['wf']['vf']  = 0.00220672
PROB_TABLE[('normal', 'no_trt')]['wf']['wf']  = 0.00175901

PROB_TABLE[('sick', 'no_trt')] = {}
PROB_TABLE[('sick', 'no_trt')]['no_fx'] = {}
PROB_TABLE[('sick', 'no_trt')]['no_fx']['hip'] = 0.00277684
PROB_TABLE[('sick', 'no_trt')]['no_fx']['vf']  = 0.00744093
PROB_TABLE[('sick', 'no_trt')]['no_fx']['wf']  = 0.00599948
PROB_TABLE[('sick', 'no_trt')]['hip'] = {}
PROB_TABLE[('sick', 'no_trt')]['hip']['hip'] = 0.01786026
PROB_TABLE[('sick', 'no_trt')]['hip']['vf']  = 0.00780247
PROB_TABLE[('sick', 'no_trt')]['hip']['wf']  = 0.0055
PROB_TABLE[('sick', 'no_trt')]['vf'] = {}
PROB_TABLE[('sick', 'no_trt')]['vf']['hip'] = 0.00631997
PROB_TABLE[('sick', 'no_trt')]['vf']['vf']  = 0.02672291
PROB_TABLE[('sick', 'no_trt')]['vf']['wf']  = 0.00695305
PROB_TABLE[('sick', 'no_trt')]['wf'] = {}
PROB_TABLE[('sick', 'no_trt')]['wf']['hip'] = 0.00357979
PROB_TABLE[('sick', 'no_trt')]['wf']['vf']  = 0.00320672
PROB_TABLE[('sick', 'no_trt')]['wf']['wf']  = 0.00275901

PROB_TABLE[('sick', 'trt')] = {}
PROB_TABLE[('sick', 'trt')]['no_fx'] = {}
PROB_TABLE[('sick', 'trt')]['no_fx']['hip'] = 0.0012555
PROB_TABLE[('sick', 'trt')]['no_fx']['vf']  = 0.00264944
PROB_TABLE[('sick', 'trt')]['no_fx']['wf']  = 0.00534908
PROB_TABLE[('sick', 'trt')]['hip'] = {}
PROB_TABLE[('sick', 'trt')]['hip']['hip'] = 0.00520493
PROB_TABLE[('sick', 'trt')]['hip']['vf']  = 0.00402953
PROB_TABLE[('sick', 'trt')]['hip']['wf']  = 0.00292734
PROB_TABLE[('sick', 'trt')]['vf'] = {}
PROB_TABLE[('sick', 'trt')]['vf']['hip'] = 0.0018418
PROB_TABLE[('sick', 'trt')]['vf']['vf']  = 0.01380084
PROB_TABLE[('sick', 'trt')]['vf']['wf']  = 0.00370072
PROB_TABLE[('sick', 'trt')]['wf'] = {}
PROB_TABLE[('sick', 'trt')]['wf']['hip'] = 0.00104324
PROB_TABLE[('sick', 'trt')]['wf']['vf']  = 0.00165609
PROB_TABLE[('sick', 'trt')]['wf']['wf']  = 0.00146847

LBM1_NO_TRT_SCALE = 0.7
LBL_NO_TRT_SCALE = 0.2
LBM1_TRT_SCALE = 0.7
LBL_TRT_SCALE = 0.2


PROB_TABLE[('lbm1', 'no_trt')] = {}
PROB_TABLE[('lbl',  'no_trt')] = {}
PROB_TABLE[('lbm1',    'trt')] = {}
PROB_TABLE[('lbl',     'trt')] = {}

for src in ['no_fx', 'hip', 'vf', 'wf']:
    PROB_TABLE[('lbm1', 'no_trt')][src] = {}
    PROB_TABLE[('lbl',  'no_trt')][src] = {}
    PROB_TABLE[('lbm1',    'trt')][src] = {}
    PROB_TABLE[('lbl',     'trt')][src] = {}
    for sink in ['hip', 'vf', 'wf']:
        PROB_TABLE[('lbm1', 'no_trt')][src][sink] = LBM1_NO_TRT_SCALE *(PROB_TABLE[('sick', 'no_trt')][src][sink] - PROB_TABLE[('normal', 'no_trt')][src][sink]) + PROB_TABLE[('normal', 'no_trt')][src][sink]
        PROB_TABLE[('lbl',  'no_trt')][src][sink] = LBL_NO_TRT_SCALE  *(PROB_TABLE[('sick', 'no_trt')][src][sink] - PROB_TABLE[('normal', 'no_trt')][src][sink]) + PROB_TABLE[('normal', 'no_trt')][src][sink]
        PROB_TABLE[('lbm1',    'trt')][src][sink] = LBM1_NO_TRT_SCALE *(PROB_TABLE[('sick',    'trt')][src][sink] - PROB_TABLE[('normal', 'no_trt')][src][sink]) + PROB_TABLE[('normal', 'no_trt')][src][sink]
        PROB_TABLE[('lbl',     'trt')][src][sink] = LBL_NO_TRT_SCALE  *(PROB_TABLE[('sick',    'trt')][src][sink] - PROB_TABLE[('normal', 'no_trt')][src][sink]) + PROB_TABLE[('normal', 'no_trt')][src][sink]

PROB_TABLE['vfa', 'no_trt'] = {}
PROB_TABLE['vfa', 'no_trt']['no_fx'] = {}
PROB_TABLE['vfa', 'no_trt']['no_fx']['hip'] = 0.01453593
PROB_TABLE['vfa', 'no_trt']['no_fx']['vf']  = 0.02672291
PROB_TABLE['vfa', 'no_trt']['no_fx']['wf']  = 0.0111249
PROB_TABLE['vfa', 'no_trt']['hip'] = {}
PROB_TABLE['vfa', 'no_trt']['hip']['hip'] = 0.018078598
PROB_TABLE['vfa', 'no_trt']['hip']['vf']  = 0.06051112
PROB_TABLE['vfa', 'no_trt']['hip']['wf']  = 0.004
PROB_TABLE['vfa', 'no_trt']['vf'] = {}
PROB_TABLE['vfa', 'no_trt']['vf']['hip'] = 0.00631997
PROB_TABLE['vfa', 'no_trt']['vf']['vf']  = 0.33670867
PROB_TABLE['vfa', 'no_trt']['vf']['wf']  = 0.00695305
PROB_TABLE['vfa', 'no_trt']['wf'] = {}
PROB_TABLE['vfa', 'no_trt']['wf']['hip'] = 0.00593352
PROB_TABLE['vfa', 'no_trt']['wf']['vf']  = 0.02780467
PROB_TABLE['vfa', 'no_trt']['wf']['wf']  = 0.00281442

PROB_TABLE['vfa', 'trt'] = {}
PROB_TABLE['vfa', 'trt']['no_fx'] = {}
PROB_TABLE['vfa', 'trt']['no_fx']['hip'] = 0.00639581
PROB_TABLE['vfa', 'trt']['no_fx']['vf']  = 0.0138084
PROB_TABLE['vfa', 'trt']['no_fx']['wf']  = 0.00978989
PROB_TABLE['vfa', 'trt']['hip'] = {}
PROB_TABLE['vfa', 'trt']['hip']['hip'] = 0.00795458
PROB_TABLE['vfa', 'trt']['hip']['vf']  = 0.03388623
PROB_TABLE['vfa', 'trt']['hip']['wf']  = 0.00352
PROB_TABLE['vfa', 'trt']['vf'] = {}
PROB_TABLE['vfa', 'trt']['vf']['hip'] = 0.0018418
PROB_TABLE['vfa', 'trt']['vf']['vf']  = 0.18855685
PROB_TABLE['vfa', 'trt']['vf']['wf']  = 0.00370072
PROB_TABLE['vfa', 'trt']['wf'] = {}
PROB_TABLE['vfa', 'trt']['wf']['hip'] = 0.00261075
PROB_TABLE['vfa', 'trt']['wf']['vf']  = 0.01557062
PROB_TABLE['vfa', 'trt']['wf']['wf']  = 0.00247669

def vfa_preval(age):
    if age < 60:
        return 0.033
    elif age < 70:
        return 0.046
    elif age < 80:
        return 0.106
    else:
        return 0.163

def trauma_preval(age):
    if age < 70:
        return 0.013
    else:
        return 0.029

def joint_ost_to_vfa(age, ost_level):
    if age <65:
        if ost_level == 'sick':
            return 0.264
        elif ost_level == 'lbm':
            return 0.386
        elif ost_level == 'normal':
            return 0.35
        else:
            raise Exception("unkown level")
    else:
        if ost_level == 'sick':
            return 0.379
        elif ost_level == 'lbm':
            return 0.396
        elif ost_level == 'normal':
            return 0.224
        else:
            raise Exception("unkown level")

def joint_vfa_to_trama(age):
    return 0.28



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

OST_LBM1_TO_SICK={}
OST_NORMAL_TO_LBM1={}
OST_NORMAL_TO_LBL={}
for age in [70, 80]:
    sick_inc = (OST_SICK_PREVAL[age]-OST_SICK_PREVAL[age-10])
    log.debug("at age {}, sick will increase is {:5f}, lbm1 preval is {:5f}".format(age-10, sick_inc, OST_LBM1_PREVAL[age-10]))
    if sick_inc <= 0:
        raise Exception("sick prevail reduced")
    if OST_LBM1_PREVAL[age-10] < sick_inc:
        raise Exception("sick prevail reduced")
    OST_LBM1_TO_SICK[age] = sick_inc/OST_LBM1_PREVAL[age]
    lbm1_leftover = OST_LBM1_PREVAL[age-10] - sick_inc
    log.debug("at age {}, LBM to SICK ratio is {:5f}, lbm1 preval leftover {:5f}".format(age-10, OST_LBM1_TO_SICK[age], lbm1_leftover))
    lbm1_needed = OST_LBM1_PREVAL[age] - lbm1_leftover
    log.debug("at age {}, LBM1 preval is {:5f}, lbm1 need to add {:5f}, lbl at {} is {}".format(age, OST_LBM1_PREVAL[age], lbm1_needed, age-10, OST_LBL_PREVAL[age-10]))
    if lbm1_needed < 0:
        raise Exception("lbm1 needed is negative")
    lbm1_needed_from_normal = lbm1_needed - OST_LBL_PREVAL[age-10]
    if lbm1_needed_from_normal < 0:
        raise Exception("lbm1_needed_leftover is negative")
    log.debug("at age {}, lbm1_needed_leftover for normal is {:5f}".format(age, lbm1_needed_from_normal))
    OST_NORMAL_TO_LBM1[age] = lbm1_needed_from_normal/OST_NORMAL_PREVAL[age-10]
    OST_NORMAL_TO_LBL[age] = OST_LBL_PREVAL[age]/OST_NORMAL_PREVAL[age-10]
    log.debug("OST_NORMAL_PREVAL at age {} is {}, normal to lbm1 ratio at age {} is {:5f}, to lbl ratio is {}".format(age-10, OST_NORMAL_PREVAL[age-10], age, OST_NORMAL_TO_LBM1[age], OST_NORMAL_TO_LBL[age]))







VFA_OST_NORMAL = 0.085
VFA_OST_LBM = 0.157
VFA_OST_SICK = 0.343
VFA_LBM_TO_SICK = (VFA_OST_SICK - VFA_OST_LBM)/(1-VFA_OST_LBM)
VFA_NORMAL_TO_LBM = (VFA_OST_LBM - VFA_OST_NORMAL)/(1-VFA_OST_NORMAL)


def set_ost_vfa(age, cur_ost, cur_vfa):
    p = random.random()
    pv = random.random()
    if cur_ost is None:
        if age < 60:
            band = 55
        elif age < 70:
            band = 60
        elif age < 80:
            band = 70
        else:
            band = 80
        if p < OST_SICK_PREVAL[band]:
            vfa = pv < VFA_OST_SICK
            return 'sick', vfa
        elif p < OST_SICK_PREVAL[band] + OST_LBM_PREVAL[band]:
            vfa = pv < VFA_OST_LBM
            return 'lbm', vfa
        else:
            vfa = pv < VFA_OST_NORMAL
            return 'normal', vfa
    else:
        if age in [60, 70, 80]:
            if cur_ost == 'sick':
                return cur_ost, cur_vfa
            elif cur_ost == 'lbm':
                if p < OST_SICK_NEW[age]:
                    if cur_vfa:
                        vfa = True
                    elif pv < VFA_LBM_TO_SICK:
                        vfa = True
                    else:
                        vfa = False
                    return 'sick', vfa
                else:
                    return cur_ost, cur_vfa
            else:
                if p < OST_LBM_NEW[age]:
                    if cur_vfa:
                        vfa = True
                    elif pv < VFA_NORMAL_TO_LBM:
                        vfa = True
                    else:
                        vfa = False
                    return 'lbm', vfa
                else:
                    return cur_ost, cur_vfa
    raise Exception("function error")

def natual_death_rate(age):
    #TODO: remove this
    #return 0
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

OST_DIST = []
for _ in xrange(3):
    OST_DIST.append({})
OST_DIST[1]['sick']   = [5,  22, 73] # real sick
OST_DIST[1]['lbm']    = [15, 70, 15]
OST_DIST[1]['normal'] = [100, 0,  0]

OST_DIST[2]['sick']   = [2,  25, 73]
OST_DIST[2]['lbm']    = [10, 75, 15]
OST_DIST[2]['normal'] = [100, 0,  0]


NORMALIZED_OST_DIST = [None]*3
NORMALIZED_OST_DIST[1] = {}
NORMALIZED_OST_DIST[2] = {}

for i in range(1,3):
    TOTAL = sum(OST_DIST[i]['sick'])*1.0
    NORMALIZED_OST_DIST[i]['sick'] = (OST_DIST[i]['sick'][0]/TOTAL, OST_DIST[i]['sick'][1]/TOTAL, OST_DIST[i]['sick'][2]/TOTAL)
    TOTAL = sum(OST_DIST[i]['lbm'])*1.0
    NORMALIZED_OST_DIST[i]['lbm'] = (OST_DIST[i]['lbm'][0]/TOTAL, OST_DIST[i]['lbm'][1]/TOTAL, OST_DIST[i]['lbm'][2]/TOTAL)
    TOTAL = sum(OST_DIST[i]['normal'])*1.0
    NORMALIZED_OST_DIST[i]['normal'] = (OST_DIST[i]['normal'][0]/TOTAL, OST_DIST[i]['normal'][1]/TOTAL, OST_DIST[i]['normal'][2]/TOTAL)


def get_ost_test_result(ost, threshold):
    p = random.random()
    if ost == 'sick':
        p -= NORMALIZED_OST_DIST[threshold]['sick'][0]
        if p <= 0:
            return 'normal'
        p -= NORMALIZED_OST_DIST[threshold]['sick'][1]
        if p <= 0:
            return 'lbm'
        p -= NORMALIZED_OST_DIST[threshold]['sick'][2]
        if p <= 0:
            return 'sick'
        raise Exception("bad probability")
    elif ost == 'lbm':
        p -= NORMALIZED_OST_DIST[threshold]['lbm'][0]
        if p < 0:
            return 'normal'
        p -= NORMALIZED_OST_DIST[threshold]['lbm'][1]
        if p < 0:
            return 'lbm'
        p -= NORMALIZED_OST_DIST[threshold]['lbm'][2]
        if p <= 0:
            return 'sick'
        raise Exception("bad probability")
    if ost == 'normal':
        p -= NORMALIZED_OST_DIST[threshold]['normal'][0]
        if p < 0:
            return 'normal'
        p -= NORMALIZED_OST_DIST[threshold]['normal'][1]
        if p < 0:
            return 'lbm'
        p -= NORMALIZED_OST_DIST[threshold]['normal'][2]
        if p <= 0:
            return 'sick'
        raise Exception("bad probability")
    raise Exception("bad probability")


def take_ost_trt():
    p = random.random()
    if p <= 0.25:
        return p


VFA_SENSI = 0.85
VFA_SPEC = 0.92

def get_vfa_test_result(vfa):
    p = random.random()
    if vfa:
        if p < VFA_SENSI:
            return 'Pos'
        else:
            return 'Neg'
    else:
        if random.random() > VFA_SPEC:
            return 'Pos'
        else:
            return 'Neg'




if __name__ == '__main__':
    pass
    # print OST_SICK_PREVAL
    # print OST_LBM1_PREVAL
    # print OST_LBL_PREVAL
    # print OST_NORMAL_PREVAL
    # from collections import Counter
    # c = {}
    # c[('sick', 1)] = Counter()
    # for _ in range(100000):
    #     c[('sick', 1)][get_ost_test_result('sick', 1)] += 1
    # c[('lbm', 1)] = Counter()
    # for _ in range(100000):
    #     c[('lbm', 1)][get_ost_test_result('lbm', 1)] += 1
    # c[('normal', 1)] = Counter()
    # for _ in range(100000):
    #     c[('normal', 1)][get_ost_test_result('normal', 1)] += 1

    # c[('sick', 2)] = Counter()
    # for _ in range(100000):
    #     c[('sick', 2)][get_ost_test_result('sick', 2)] += 1
    # c[('lbm', 2)] = Counter()
    # for _ in range(100000):
    #     c[('lbm', 2)][get_ost_test_result('lbm', 2)] += 1
    # c[('normal', 2)] = Counter()
    # for _ in range(100000):
    #     c[('normal', 2)][get_ost_test_result('normal', 2)] += 1

    # print NORMALIZED_OST_DIST
    # for k,v in c.iteritems():
    #     print k, v







