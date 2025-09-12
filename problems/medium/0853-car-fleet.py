class Solution(object):
    def carFleet(self, target, position, speed):
        """
        :type target: int
        :type position: List[int]
        :type speed: List[int]
        :rtype: int
        """
        if len(position) == 1 or len(speed) == 1:
            return 1
        
        cars = sorted(zip(position, speed), reverse=True)
        stk = []

        for pos, spd in cars:
            time_left = (target-pos) / float(spd)
            if not stk or time_left > stk[-1]:
                # only add cars that are slow enough, aka
                # can't catch up to car ahead (car in stk)
                stk.append(time_left)
        return len(stk)