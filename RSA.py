def ext_euclid(a, b):
    '''
    扩展欧几里得算法
    a*s + b*t = gcd(a,b)

    返回(s, t, gcd(a, b))
    '''
    old_s,s=1,0
    old_t,t=0,1
    old_r,r=a,b
    if b == 0:
        return 1, 0, a
    else:
        while(r!=0):
            q=old_r//r
            old_r,r=r,old_r-q*r
            old_s,s=s,old_s-q*s
            old_t,t=t,old_t-q*t
    return old_s, old_t, old_r
