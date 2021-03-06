#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  9 00:13:12 2017

@author: moritz
"""

import numpy as N
import numpy.fft.fftpack as F
import scipy as S
import pylab as P
import scipy.optimize as optimize


def expGauss(x, pos, wid, tConst, expMod = 0.5, amp = 1):
	'''
	x -- numpy array
	pos -- centroid position
	wid -- width
	tConst -- time constance for exponential decay
	amp -- amplitude of peak
	expMod -- modifies the amplitude of the peak -- must be a float
	
	Forumulas used:
	
	y = a * exp(-0.5 * (x-b)^2 / c^2) --traditional gaussian forumla
	exp = N.exp(-1*expMod*N.arange(0,len(y))/Const) --function that is merged with the gaussian
	
	Note if expMod is too small (i.e. goes towards zero) the function will return a flat line.
	'''
	
	expMod *= 1.0
	gNorm = amp * N.exp(-0.5*((x-pos)/(wid))**2)
	g = expBroaden(gNorm, tConst, expMod)
	return g, gNorm

def expBroaden(y, t, expMod):
    fy = F.fft(y)
    a = N.exp(-1*expMod*N.arange(0,len(y))/t)
    fa = F.fft(a)
    fy1 = fy*fa
    yb = (F.ifft(fy1).real)/N.sum(a)
    return yb

if __name__ == '__main__':

	a = N.linspace(0,100,500)
	tConstArray = N.arange(10,200,10)
	x, x1 = expGauss(a, 50, 2, 150, 2, 5)
	xN = x + 0.5-S.rand(len(a))/2
	x1N = x1 + 0.5-S.rand(len(a))/2
	
	

	# Fit the first set
	#p[0] -- amplitude, p[1] -- position, p[2] -- width
	fitfuncG = lambda p, x: p[0]*N.exp(-0.5*(x-p[1])**2/p[2]**2) # Target function
	errfuncG = lambda p, x, y: fitfuncG(p, x) - y # Distance to the target function
	p0 = [1.0, 1.0, 1.0] # Initial guess for the parameters
	p1, success = optimize.leastsq(errfuncG, p0[:], args=(a, xN))
	p1G = fitfuncG(p1,a)
	
	#P.plot(x1N,  'ro', alpha = 0.4, label = "Gaussian")
	P.plot(p1G, label = 'G-Fit')
	
	'def expGauss(x, pos, wid, tConst, expMod = 0.5, amp = 1):'
	#p[0] -- amplitude, p[1] -- position, p[2] -- width, p[3]--tConst, p[4] -- expMod
	fitfuncExpG = lambda p, x: expGauss(x, p[1], p[2], p[3], p[4], p[0])[0]
	errfuncExpG = lambda p, x, y: fitfuncExpG(p, x) - y # Distance to the target function
	p0a = [p1[0], p1[1], 10., 10., 1.] # Initial guess for the parameters
	p1a, success = optimize.leastsq(errfuncExpG, p0a[:], args=(a, xN))
	p1aG = fitfuncExpG(p1a,a)
	
	#print type(xN), type(a), len(xN), len(a)
	P.plot(xN,  'go', alpha = 0.4, label = "ExpGaussian")
	P.plot(p1aG, label = 'ExpG-Fit')
	
	P.legend()
	P.show()