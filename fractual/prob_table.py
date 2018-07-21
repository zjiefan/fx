import random

LBM_SCALE1 = 0.8
LBM_SCALE2 = 0.8

PROB_TABLE = {}
PROB_TABLE['ost_normal_no_trt'] = {}
PROB_TABLE['ost_normal_no_trt']['no_fx'] = {}
PROB_TABLE['ost_normal_no_trt']['no_fx']['hip'] = 0.00070024
PROB_TABLE['ost_normal_no_trt']['no_fx']['vf']  = 0.00070024
PROB_TABLE['ost_normal_no_trt']['no_fx']['wf']  = 0.00006299
PROB_TABLE['ost_normal_no_trt']['hip'] = {}
PROB_TABLE['ost_normal_no_trt']['hip']['hip'] = 0.00786026
PROB_TABLE['ost_normal_no_trt']['hip']['vf']  = 0.00480247
PROB_TABLE['ost_normal_no_trt']['hip']['wf']  = 0.0025
PROB_TABLE['ost_normal_no_trt']['vf'] = {}
PROB_TABLE['ost_normal_no_trt']['vf']['hip'] = 0.00370072
PROB_TABLE['ost_normal_no_trt']['vf']['vf']  = 0.02480771
PROB_TABLE['ost_normal_no_trt']['vf']['wf']  = 0.00511307
PROB_TABLE['ost_normal_no_trt']['wf'] = {}
PROB_TABLE['ost_normal_no_trt']['wf']['hip'] = 0.00257979
PROB_TABLE['ost_normal_no_trt']['wf']['vf']  = 0.00220672
PROB_TABLE['ost_normal_no_trt']['wf']['wf']  = 0.00175901

PROB_TABLE['ost_normal_trt'] = {}
PROB_TABLE['ost_normal_trt']['no_fx'] = {}
PROB_TABLE['ost_normal_trt']['no_fx']['hip'] = 0.000308106
PROB_TABLE['ost_normal_trt']['no_fx']['vf']  = 0.00039213
PROB_TABLE['ost_normal_trt']['no_fx']['wf']  = 0.00005543
PROB_TABLE['ost_normal_trt']['hip'] = {}
PROB_TABLE['ost_normal_trt']['hip']['hip'] = 0.00345851
PROB_TABLE['ost_normal_trt']['hip']['vf']  = 0.00268938
PROB_TABLE['ost_normal_trt']['hip']['wf']  = 0.0022
PROB_TABLE['ost_normal_trt']['vf'] = {}
PROB_TABLE['ost_normal_trt']['vf']['hip'] = 0.001628317
PROB_TABLE['ost_normal_trt']['vf']['vf']  = 0.013892318
PROB_TABLE['ost_normal_trt']['vf']['wf']  = 0.004499502
PROB_TABLE['ost_normal_trt']['wf'] = {}
PROB_TABLE['ost_normal_trt']['wf']['hip'] = 0.001135108
PROB_TABLE['ost_normal_trt']['wf']['vf']  = 0.001235763
PROB_TABLE['ost_normal_trt']['wf']['wf']  = 0.001547929

PROB_TABLE['ost_sick_no_trt'] = {}
PROB_TABLE['ost_sick_no_trt']['no_fx'] = {}
PROB_TABLE['ost_sick_no_trt']['no_fx']['hip'] = 0.00277684
PROB_TABLE['ost_sick_no_trt']['no_fx']['vf']  = 0.00744093
PROB_TABLE['ost_sick_no_trt']['no_fx']['wf']  = 0.00599948
PROB_TABLE['ost_sick_no_trt']['hip'] = {}
PROB_TABLE['ost_sick_no_trt']['hip']['hip'] = 0.01786026
PROB_TABLE['ost_sick_no_trt']['hip']['vf']  = 0.00780247
PROB_TABLE['ost_sick_no_trt']['hip']['wf']  = 0.0055
PROB_TABLE['ost_sick_no_trt']['vf'] = {}
PROB_TABLE['ost_sick_no_trt']['vf']['hip'] = 0.00631997
PROB_TABLE['ost_sick_no_trt']['vf']['vf']  = 0.02672291
PROB_TABLE['ost_sick_no_trt']['vf']['wf']  = 0.00695305
PROB_TABLE['ost_sick_no_trt']['wf'] = {}
PROB_TABLE['ost_sick_no_trt']['wf']['hip'] = 0.00357979
PROB_TABLE['ost_sick_no_trt']['wf']['vf']  = 0.00320672
PROB_TABLE['ost_sick_no_trt']['wf']['wf']  = 0.00275901

PROB_TABLE['ost_sick_trt'] = {}
PROB_TABLE['ost_sick_trt']['no_fx'] = {}
PROB_TABLE['ost_sick_trt']['no_fx']['hip'] = 0.0012555
PROB_TABLE['ost_sick_trt']['no_fx']['vf']  = 0.00264944
PROB_TABLE['ost_sick_trt']['no_fx']['wf']  = 0.00534908
PROB_TABLE['ost_sick_trt']['hip'] = {}
PROB_TABLE['ost_sick_trt']['hip']['hip'] = 0.00520493
PROB_TABLE['ost_sick_trt']['hip']['vf']  = 0.00402953
PROB_TABLE['ost_sick_trt']['hip']['wf']  = 0.00292734
PROB_TABLE['ost_sick_trt']['vf'] = {}
PROB_TABLE['ost_sick_trt']['vf']['hip'] = 0.0018418
PROB_TABLE['ost_sick_trt']['vf']['vf']  = 0.01380084
PROB_TABLE['ost_sick_trt']['vf']['wf']  = 0.00370072
PROB_TABLE['ost_sick_trt']['wf'] = {}
PROB_TABLE['ost_sick_trt']['wf']['hip'] = 0.00104324
PROB_TABLE['ost_sick_trt']['wf']['vf']  = 0.00165609
PROB_TABLE['ost_sick_trt']['wf']['wf']  = 0.00146847

PROB_TABLE['ost_lbm2_no_trt'] = {}
PROB_TABLE['ost_lbm2_no_trt']['no_fx'] = {}
PROB_TABLE['ost_lbm2_no_trt']['no_fx']['hip'] = LBM_SCALE2 * PROB_TABLE['ost_sick_no_trt']['no_fx']['hip']
PROB_TABLE['ost_lbm2_no_trt']['no_fx']['vf']  = LBM_SCALE2 * PROB_TABLE['ost_sick_no_trt']['no_fx']['vf']
PROB_TABLE['ost_lbm2_no_trt']['no_fx']['wf']  = LBM_SCALE2 * PROB_TABLE['ost_sick_no_trt']['no_fx']['wf']
PROB_TABLE['ost_lbm2_no_trt']['hip'] = {}
PROB_TABLE['ost_lbm2_no_trt']['hip']['hip'] = LBM_SCALE2 * PROB_TABLE['ost_sick_no_trt']['hip']['hip']
PROB_TABLE['ost_lbm2_no_trt']['hip']['vf']  = LBM_SCALE2 * PROB_TABLE['ost_sick_no_trt']['hip']['vf']
PROB_TABLE['ost_lbm2_no_trt']['hip']['wf']  = LBM_SCALE2 * PROB_TABLE['ost_sick_no_trt']['hip']['wf']
PROB_TABLE['ost_lbm2_no_trt']['vf'] = {}
PROB_TABLE['ost_lbm2_no_trt']['vf']['hip'] = LBM_SCALE2 * PROB_TABLE['ost_sick_no_trt']['vf']['hip']
PROB_TABLE['ost_lbm2_no_trt']['vf']['vf']  = LBM_SCALE2 * PROB_TABLE['ost_sick_no_trt']['vf']['vf']
PROB_TABLE['ost_lbm2_no_trt']['vf']['wf']  = LBM_SCALE2 * PROB_TABLE['ost_sick_no_trt']['vf']['wf']
PROB_TABLE['ost_lbm2_no_trt']['wf'] = {}
PROB_TABLE['ost_lbm2_no_trt']['wf']['hip'] = LBM_SCALE2 * PROB_TABLE['ost_sick_no_trt']['wf']['hip']
PROB_TABLE['ost_lbm2_no_trt']['wf']['vf']  = LBM_SCALE2 * PROB_TABLE['ost_sick_no_trt']['wf']['vf']
PROB_TABLE['ost_lbm2_no_trt']['wf']['wf']  = LBM_SCALE2 * PROB_TABLE['ost_sick_no_trt']['wf']['wf']

PROB_TABLE['ost_lbm1_trt'] = {}
PROB_TABLE['ost_lbm1_trt']['no_fx'] = {}
PROB_TABLE['ost_lbm1_trt']['no_fx']['hip'] = LBM_SCALE1 * PROB_TABLE['ost_sick_trt']['no_fx']['hip']
PROB_TABLE['ost_lbm1_trt']['no_fx']['vf']  = LBM_SCALE1 * PROB_TABLE['ost_sick_trt']['no_fx']['vf']
PROB_TABLE['ost_lbm1_trt']['no_fx']['wf']  = LBM_SCALE1 * PROB_TABLE['ost_sick_trt']['no_fx']['wf']
PROB_TABLE['ost_lbm1_trt']['hip'] = {}
PROB_TABLE['ost_lbm1_trt']['hip']['hip'] = LBM_SCALE1 * PROB_TABLE['ost_sick_trt']['hip']['hip']
PROB_TABLE['ost_lbm1_trt']['hip']['vf']  = LBM_SCALE1 * PROB_TABLE['ost_sick_trt']['hip']['vf']
PROB_TABLE['ost_lbm1_trt']['hip']['wf']  = LBM_SCALE1 * PROB_TABLE['ost_sick_trt']['hip']['wf']
PROB_TABLE['ost_lbm1_trt']['vf'] = {}
PROB_TABLE['ost_lbm1_trt']['vf']['hip'] = LBM_SCALE1 * PROB_TABLE['ost_sick_trt']['vf']['hip']
PROB_TABLE['ost_lbm1_trt']['vf']['vf']  = LBM_SCALE1 * PROB_TABLE['ost_sick_trt']['vf']['vf']
PROB_TABLE['ost_lbm1_trt']['vf']['wf']  = LBM_SCALE1 * PROB_TABLE['ost_sick_trt']['vf']['wf']
PROB_TABLE['ost_lbm1_trt']['wf'] = {}
PROB_TABLE['ost_lbm1_trt']['wf']['hip'] = LBM_SCALE1 * PROB_TABLE['ost_sick_trt']['wf']['hip']
PROB_TABLE['ost_lbm1_trt']['wf']['vf']  = LBM_SCALE1 * PROB_TABLE['ost_sick_trt']['wf']['vf']
PROB_TABLE['ost_lbm1_trt']['wf']['wf']  = LBM_SCALE1 * PROB_TABLE['ost_sick_trt']['wf']['wf']

PROB_TABLE['has_vfa_no_trt'] = {}
PROB_TABLE['has_vfa_no_trt']['no_fx'] = {}
PROB_TABLE['has_vfa_no_trt']['no_fx']['hip'] = 0.01453593
PROB_TABLE['has_vfa_no_trt']['no_fx']['vf']  = 0.02672291
PROB_TABLE['has_vfa_no_trt']['no_fx']['wf']  = 0.0111249
PROB_TABLE['has_vfa_no_trt']['hip'] = {}
PROB_TABLE['has_vfa_no_trt']['hip']['hip'] = 0.018078598
PROB_TABLE['has_vfa_no_trt']['hip']['vf']  = 0.06051112
PROB_TABLE['has_vfa_no_trt']['hip']['wf']  = 0.004
PROB_TABLE['has_vfa_no_trt']['vf'] = {}
PROB_TABLE['has_vfa_no_trt']['vf']['hip'] = 0.00631997
PROB_TABLE['has_vfa_no_trt']['vf']['vf']  = 0.33670867
PROB_TABLE['has_vfa_no_trt']['vf']['wf']  = 0.00695305
PROB_TABLE['has_vfa_no_trt']['wf'] = {}
PROB_TABLE['has_vfa_no_trt']['wf']['hip'] = 0.00593352
PROB_TABLE['has_vfa_no_trt']['wf']['vf']  = 0.02780467
PROB_TABLE['has_vfa_no_trt']['wf']['wf']  = 0.00281442

PROB_TABLE['has_vfa_trt'] = {}
PROB_TABLE['has_vfa_trt']['no_fx'] = {}
PROB_TABLE['has_vfa_trt']['no_fx']['hip'] = 0.00639581
PROB_TABLE['has_vfa_trt']['no_fx']['vf']  = 0.0138084
PROB_TABLE['has_vfa_trt']['no_fx']['wf']  = 0.00978989
PROB_TABLE['has_vfa_trt']['hip'] = {}
PROB_TABLE['has_vfa_trt']['hip']['hip'] = 0.00795458
PROB_TABLE['has_vfa_trt']['hip']['vf']  = 0.03388623
PROB_TABLE['has_vfa_trt']['hip']['wf']  = 0.00352
PROB_TABLE['has_vfa_trt']['vf'] = {}
PROB_TABLE['has_vfa_trt']['vf']['hip'] = 0.0018418
PROB_TABLE['has_vfa_trt']['vf']['vf']  = 0.18855685
PROB_TABLE['has_vfa_trt']['vf']['wf']  = 0.00370072
PROB_TABLE['has_vfa_trt']['wf'] = {}
PROB_TABLE['has_vfa_trt']['wf']['hip'] = 0.00261075
PROB_TABLE['has_vfa_trt']['wf']['vf']  = 0.01557062
PROB_TABLE['has_vfa_trt']['wf']['wf']  = 0.00247669


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

OST_PREVAL = {}
OST_PREVAL[55] = 0.561
OST_PREVAL[60] = 0.657
OST_PREVAL[70] = 0.775
OST_PREVAL[80] = 0.876
OST_PREVAL_60 = (OST_PREVAL[60] - OST_PREVAL[55])/(1-OST_PREVAL[55])
OST_PREVAL_70 = (OST_PREVAL[70] - OST_PREVAL[60])/(1-OST_PREVAL[60])
OST_PREVAL_80 = (OST_PREVAL[80] - OST_PREVAL[70])/(1-OST_PREVAL[70])

OST_SICK_PREVAL = {}
OST_SICK_PREVAL[55] = 0.068
OST_SICK_PREVAL[60] = 0.123
OST_SICK_PREVAL[70] = 0.257
OST_SICK_PREVAL[80] = 0.349

OST_LBM_PREVAL = {}
OST_LBM_PREVAL[55] = 0.493
OST_LBM_PREVAL[60] = 0.534
OST_LBM_PREVAL[70] = 0.518
OST_LBM_PREVAL[80] = 0.527
OST_SICK_NEW = {}
OST_SICK_NEW[60] = (OST_SICK_PREVAL[60] - OST_SICK_PREVAL[55])/OST_LBM_PREVAL[55]
OST_SICK_NEW[70] = (OST_SICK_PREVAL[70] - OST_SICK_PREVAL[60])/OST_LBM_PREVAL[60]
OST_SICK_NEW[80] = (OST_SICK_PREVAL[80] - OST_SICK_PREVAL[70])/OST_LBM_PREVAL[70]

OST_LBM1_PREVAL = {}
#OST_LBM1_PREVAL[55] = 0.493
OST_LBM1_PREVAL[60] = 0.454
OST_LBM1_PREVAL[70] = 0.440
OST_LBM1_PREVAL[80] = 0.448
OST_SICK_NEW = {}
OST_SICK_NEW[60] = (OST_SICK_PREVAL[60] - OST_SICK_PREVAL[55])/OST_LBM_PREVAL[55]
OST_SICK_NEW[70] = (OST_SICK_PREVAL[70] - OST_SICK_PREVAL[60])/OST_LBM_PREVAL[60]
OST_SICK_NEW[80] = (OST_SICK_PREVAL[80] - OST_SICK_PREVAL[70])/OST_LBM_PREVAL[70]

OST_LBM2_PREVAL = {}
#OST_LBM2_PREVAL[55] = 0.493
OST_LBM2_PREVAL[60] = 0.534
OST_LBM2_PREVAL[70] = 0.518
OST_LBM2_PREVAL[80] = 0.527
OST_SICK_NEW = {}
OST_SICK_NEW[60] = (OST_SICK_PREVAL[60] - OST_SICK_PREVAL[55])/OST_LBM_PREVAL[55]
OST_SICK_NEW[70] = (OST_SICK_PREVAL[70] - OST_SICK_PREVAL[60])/OST_LBM_PREVAL[60]
OST_SICK_NEW[80] = (OST_SICK_PREVAL[80] - OST_SICK_PREVAL[70])/OST_LBM_PREVAL[70]

OST_NORMAL_PREVAL = {}
OST_NORMAL_PREVAL[55] = 1 - OST_LBM_PREVAL[55] - OST_SICK_PREVAL[55]
OST_NORMAL_PREVAL[60] = 1 - OST_LBM_PREVAL[60] - OST_SICK_PREVAL[60]
OST_NORMAL_PREVAL[70] = 1 - OST_LBM_PREVAL[70] - OST_SICK_PREVAL[70]
OST_NORMAL_PREVAL[80] = 1 - OST_LBM_PREVAL[80] - OST_SICK_PREVAL[80]
OST_LBM_NEW = {}
OST_LBM_NEW[60] = (OST_SICK_PREVAL[60] - OST_SICK_PREVAL[55] + OST_LBM_PREVAL[60] - OST_LBM_PREVAL[55])/OST_NORMAL_PREVAL[55]
OST_LBM_NEW[70] = (OST_SICK_PREVAL[70] - OST_SICK_PREVAL[60] + OST_LBM_PREVAL[70] - OST_LBM_PREVAL[60])/OST_NORMAL_PREVAL[60]
OST_LBM_NEW[80] = (OST_SICK_PREVAL[80] - OST_SICK_PREVAL[70] + OST_LBM_PREVAL[80] - OST_LBM_PREVAL[70])/OST_NORMAL_PREVAL[70]
if OST_LBM_NEW[60] < 0 or OST_LBM_NEW[60] >1:
    raise Exception("OST_LBM_NEW_60 out of range")
if OST_LBM_NEW[70] < 0 or OST_LBM_NEW[70] >1:
    raise Exception("OST_LBM_NEW_70 out of range")
if OST_LBM_NEW[80] < 0 or OST_LBM_NEW[80] >1:
    raise Exception("OST_LBM_NEW_80 out of range")

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
    from collections import Counter
    c = {}
    c[('sick', 1)] = Counter()
    for _ in range(100000):
        c[('sick', 1)][get_ost_test_result('sick', 1)] += 1
    c[('lbm', 1)] = Counter()
    for _ in range(100000):
        c[('lbm', 1)][get_ost_test_result('lbm', 1)] += 1
    c[('normal', 1)] = Counter()
    for _ in range(100000):
        c[('normal', 1)][get_ost_test_result('normal', 1)] += 1

    c[('sick', 2)] = Counter()
    for _ in range(100000):
        c[('sick', 2)][get_ost_test_result('sick', 2)] += 1
    c[('lbm', 2)] = Counter()
    for _ in range(100000):
        c[('lbm', 2)][get_ost_test_result('lbm', 2)] += 1
    c[('normal', 2)] = Counter()
    for _ in range(100000):
        c[('normal', 2)][get_ost_test_result('normal', 2)] += 1

    print NORMALIZED_OST_DIST
    for k,v in c.iteritems():
        print k, v







