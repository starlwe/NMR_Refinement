f1 = lambda x,y,z: x
f2 = lambda x,y,z: y
f3 = lambda x,y,z: z
f4 = lambda x,y,z: -x
f5 = lambda x,y,z: -y
f6 = lambda x,y,z: -z
f7 = lambda x,y,z: (1/2) - x
f8 = lambda x,y,z: (1/2) - y
f9 = lambda x,y,z: (1/2) - z
f10 = lambda x,y,z: (1/2) + x
f11 = lambda x,y,z: (1/2) + y
f12 = lambda x,y,z: (1/2) + z
f13 = lambda x,y,z: x - y
f14 = lambda x,y,z: (1/3) + z
f15 = lambda x,y,z: -x + y
f16 = lambda x,y,z: (2/3) + z

SymTable = {
    'P21' : (2, f1, f2, f3, f4, f11, f6),
    'P21/a' : (4, f1, f2, f3, f7, f11, f6, f4, f5, f6, f10, f8, f3),
    'P21/n' : (4, f1, f2, f3, f7, f11, f9, f4, f5, f6, f10, f8, f12),
    'P31' : (3, f1, f2, f3, f5, f13, f14, f15, f4, f16),
    'P212121' : (4, f1, f2, f3, f10, f8, f6, f4, f11, f9, f7, f5, f12),
    'P21/c' : (4, f1, f2, f3, f4, f5, f6, f4, f11, f9, f1, f8, f12),
    'P1211' : (2, f1, f2, f3, f4, f11, f6),
    'I222' : (8, f1, f2, f3, f10, f11, f12, f1, f5, f6, f10, f8, f9, f4, f2,
              f6, f7, f11, f9, f4, f5, f3, f7, f8, f12)
    }
