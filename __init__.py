import os
import sys

class Baton:
    def __init__(self, name="baton"):
        self.__name = name
        self.__slots = {}
        self.__owners = {}
        self.__cc = {}
        self.__arg = []
        self.__clean = True
        self.__where = ""
        self.__dirty_msg = ""

    def __deepcopy(self, d):
        if not isinstance(d, dict):
            return type(d)(d)
        e = {}
        for k in d:
            if isinstance(d[k], dict):
                e[k] = self.__deepcopy(d[k])
            else:
                if d[k] is None:
                    e[k] = d[k]
                else:
                    e[k] = type(d[k])(d[k])
        return e

    def peek(self, key):
        """
        A routine can call it to get a copy of a value stored by itself or
        by some other routine. A routine can read data stored by another
        routine but not modify it.
        """
        if not key:
            return None
        if key not in self.__slots:
            return None
        cc = self.__cc.get[key]
        d = self.__slots[key]
        caller = sys._getframe().f_back.f_code.co_name
        if self.__owners[key] == caller:
            cc = False  # original copy ig it's the owner
        if cc:
            d = self.__deepcopy(d)
        return d

    def store(self, key, val, cc=True):
        """
        A routine can use it keep persistent data which it may use during a
        later call. If a routune tries to store data which was created by
        another routine (i.e modify it), it will raise exception.
        """
        caller = sys._getframe().f_back.f_code.co_name
        if key not in self.__slots:
            self.__slots[key] = None
            self.__owners[key] = caller
            self.__cc[key] = cc

        if self.__owners[key] != caller:
            raise ValueError(
                f"{caller}() tried storing in a slot " "not owned by it"
            )
        self.__slots[key] = val
        return self

    def pop_arg(self):
        """
        Use this method to get the arg passed by the previous routine.
        """
        if not self.__clean:
            raise ValueError(
                "Baton is dirty..can't call pop_arg, use "
                "baton.debug() to get details"
            )
        try:
            return self.__arg.pop()
        except IndexError:
            return None

    def push_arg(self, r):
        """
        Call it to pass argument to the next function.
        """
        self.__arg.append(r)
        return self

    def clean(self):
        """
        Tells if the baton is clean or not.
        """
        if not self.__clean:
            return None
        return self

    def dirty(self, msg=""):
        """
        Call this method to mark the baton as dirty. A dirty baton is passed
        by all functions without doing anything.
        """
        self.__clean = False
        from inspect import getframeinfo, stack

        caller = getframeinfo(stack()[1][0])
        line = str(caller.lineno)
        self.__where = f"{os.path.basename(caller.filename)}+{line}"
        self.__dirty_msg = msg
        return self

    def sanitize(self):
        """
        It sanitizes a dirty baton. A sanitized baton is one that all is
        accepted (not bypassed) by functions.
        """
        self.__clean = True
        self.__where = ""
        self.__dirty_msg = ""
        return self

    def debug(self):
        """
        Call it to print details of where and why the baton was dirtied.
        """
        return self.__name, self.__dirty_msg, self.__where

    def flush(self):
        """
        Call it before re-using the baton in the next loopback. It clears all
        the pushed arguments and sanitizes the baton. The args are cleared
        just in case a function is pushing an arg which no one is popping.
        """
        self.__arg.clear()
        self.sanitize()
