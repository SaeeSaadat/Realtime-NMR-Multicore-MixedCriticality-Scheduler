class A:
    def __init__(self):
        print("A.__init__")

    def fun(self, **kwargs):
        print("A.fun")

    def not_fun(self):
        self.fun(fuck=True)


class B(A):
    def __init__(self):
        super().__init__()
        print("B.__init__")

    def fun(self, fuck: bool = False, **kwargs):
        print("B.fun", fuck)


if __name__ == '__main__':
    A().not_fun()
    B().not_fun()
