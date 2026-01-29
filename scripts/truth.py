class Unit:
    def __init__(self, s):
        self.mult = 1
        self.type = ...

class Param:
    def __init__(self, val, unit):
        self.val = val
        self.unit = unit

    def __str__(self):
        return f"{self.val} {self.unit}"

    def __repr__(self):
        return f"{self.__str__()}"

def truth():
    params = {}
    params['SwitchSpacing'] = Param(19.50, 'mm')
    params['FrameBorder'] = Param(5, 'mm')
    params['Col0Offset'] = Param(0, 'mm')
    params['Col1Offset'] = Param(4, 'mm')
    params['Col2Offset'] = Param(10, 'mm')
    params['Col3Offset'] = Param(17, 'mm')
    params['Col4Offset'] = Param(12, 'mm')
    params['Col5Offset'] = Param(9, 'mm')
    params['ThumbRadius'] = Param(92.28, 'mm')
    params['ThumbRotationAngle'] = Param(-12, 'deg')
    print(params)
    return params

truth()
