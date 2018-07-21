class Record(object):
    __slots__ = 'inc_cost', 'inc_utils', 'ost_result', 'vfa_result', 'ost_sick_trt', 'vfa_trt'
    def __init__(self):
        self.ost_sick_trt = None
        self.ost_result = None
        self.vfa_result = None
        self.vfa_trt = None
        self.inc_cost = 0
        self.inc_utils = 0

class HumanStats(object):
    __slots__ = ('total_utils', 'total_cost', 'final_age',
                 'vf_cnt', 'hip_cnt', 'wf_cnt', 'trt_cnt')
    def __init__(self):
        self.vf_cnt = 0
        self.hip_cnt = 0
        self.wf_cnt = 0
        self.trt_cnt = 0
        self.total_cost = 0
        self.total_utils = 0


    def __str__(self):
        ret = []
        for slot in self.__slots__:
            ret.append("{}={}".format(slot, getattr(self, slot)))
        return ','.join(ret)


if __name__ == '__main__':
    h = HumanStats()
    print h

