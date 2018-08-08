class Record(object):
    __slots__ = ('ost_result', 'vfa_result',
        'vf_trt_sop', 'sick_trt_sop', 'vfa_trt_sop',
        'trt',
        'inc_cost', 'inc_utils',

                )
    fmt_dict = {
        'ost_result':'5s', 'vfa_result':'5s',
        'vf_trt_sop':'5s', 'sick_trt_sop':'5s', 'vfa_trt_sop':'5s',
        'trt':'5s',
        'inc_cost':'8.1f', 'inc_utils':'6.1f',
    }
    def __init__(self):
        self.ost_result = None
        self.vfa_result = None
        self.vf_trt_sop = None
        self.sick_trt_sop = None
        self.vfa_trt_sop = None
        self.inc_cost = 0
        self.inc_utils = 0
    def __str__(self):
        ret = []
        for slot in self.__slots__:
            value = getattr(self, slot)
            fmt = self.fmt_dict.get(slot, "")
            fmt_str = "{}={:" + fmt + "}"
            if value is None:
                value =""
            if isinstance(value, bool):
                value = str(value)
            ret.append(fmt_str.format(slot, value))
        return ','.join(ret)

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

