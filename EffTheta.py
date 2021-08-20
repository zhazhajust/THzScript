def EnergeTheta(Phi . I):
#I[np.abs(Phi)<minTheta]
    ETotal = np.sum(I)
    I[np.abs(Phi)<minTheta] = 0
    I[np.abs(Phi)>maxTheta] = 0
    ETheta = np.sum(I)
    return ETheta , ETotal
