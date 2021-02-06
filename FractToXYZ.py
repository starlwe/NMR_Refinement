def _FractalToXYZ(a,b,c,alpha,beta,gamma,x,y,z):
    import math
    alpha = alpha * (math.pi/180)
    beta = beta * (math.pi/180)
    gamma = gamma * (math.pi/180)
    X = x*a + y*b*math.cos(gamma) + z*c*math.cos(beta)
    Y = y*b*math.sin(gamma) + z*(c*(math.cos(alpha) \
        - math.cos(beta)*math.cos(gamma)) / math.sin(gamma))
    W = math.sqrt(1-(math.cos(alpha))**2-(math.cos(beta))**2 \
        -(math.cos(gamma))**2 + 2*math.cos(alpha)*math.cos(beta)*math.cos(gamma))
    Z = z*c*W/math.sin(gamma)
    return X,Y,Z

def ConvertFractToXYZ(input_data,a,b,c,alpha,beta,gamma):
    out_data = []
    
    while input_data != []:
        out_data.append(input_data.pop(0))
        x,y,z = _FractalToXYZ(a,b,c,alpha,beta,gamma,float(input_data.pop(0)),float(input_data.pop(0)),float(input_data.pop(0)))
        out_data.append(x)
        out_data.append(y)
        out_data.append(z)
    return out_data

def ConvertXYZToFrac(input_data, a, b, c, alpha, beta, gamma):
    out_data = []
    
    while input_data != []:
        out_data.append(input_data.pop(0))
        x,y,z = _XYZToFrac(a,b,c,alpha,beta,gamma,float(input_data.pop(0)),float(input_data.pop(0)),float(input_data.pop(0)))
        out_data.append(x)
        out_data.append(y)
        out_data.append(z)
    return out_data

def _XYZToFrac(a,b,c,alpha,beta,gamma,X,Y,Z):
    import math
    alpha = alpha * (math.pi/180)
    beta = beta * (math.pi/180)
    gamma = gamma * (math.pi/180)
    W = math.sqrt(1-(math.cos(alpha))**2-(math.cos(beta))**2 \
        -(math.cos(gamma))**2 + 2*math.cos(alpha)*math.cos(beta)*math.cos(gamma))
    x = X/a - (Y*math.cos(gamma))/(a*math.sin(gamma)) - (Z*(math.cos(beta)*math.cos(gamma)**2 + \
        math.cos(beta)*math.sin(gamma)**2 - math.cos(alpha)*math.cos(gamma)))/(W*a*math.sin(gamma))
    y = Y/(b*math.sin(gamma)) - (Z*(math.cos(alpha) - math.cos(beta)*math.cos(gamma)))/(W*b*math.sin(gamma))
    z = (Z*math.sin(gamma))/(W*c)
    return x,y,z
