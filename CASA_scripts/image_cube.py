import os, sys
import numpy as np
execfile('/home/sandrews/mypy/keplerian_mask/keplerian_mask.py')

def generate_kepmask(setupname, MSname, imgname):

    execfile('fconfig_'+setupname+'.py')

    # make a dirty image cube to guide the mask
    tclean(vis=MSname+'.ms', imagename=imgname+'_dirty', specmode='cube', 
           start=chanstart, width=chanwidth, nchan=nchan_out,
           outframe='LSRK', veltype='radio', restfreq=str(nu_rest/1e9)+'GHz',
           imsize=imsize, cell=cell, deconvolver='multiscale', scales=scales, 
           gain=gain, niter=0, nterms=1, interactive=False, weighting='briggs', 
           robust=robust, uvtaper=uvtaper, restoringbeam='common')

    # make a Keplerian mask
    make_mask(imgname+'_dirty.image', inc=incl, PA=PA+180, dx0=xoff, dy0=yoff,
              mstar=mstar, dist=dist, vlsr=vsys, zr=z0 / 10, 
              r_max=1.2 * r_l / dist, nbeams=1.5)

    # cleanup
    os.system('rm -rf '+dataname+'.mask')
    os.system('mv '+imgname+'_dirty.mask.image '+dataname+'.mask')

    ext = ['.image', '.mask', '.model', '.pb', '.psf', '.residual', '.sumwt']
    [os.system('rm -rf '+imgname+'_dirty'+j) for j in ext]
    
    os.system('rm -rf *.last')

    return



def clean_cube(setupname, MSname, imgname, maskname=None):

    execfile('fconfig_'+setupname+'.py')

    # if necessary, make a mask
    if maskname is None:
        foo = generate_kepmask(MSname, imgname)
        maskname = imgname+'_dirty.mask.image'

    # remove lingering files from previous runs
    ext = ['.image', '.mask', '.model', '.pb', '.psf', '.residual', '.sumwt']
    for j in ext:
        os.system('rm -rf '+imgname+j)

    # make a clean image cube
    tclean(vis=MSname, imagename=imgname, specmode='cube', datacolumn='data',
           start=chanstart, width=chanwidth, nchan=nchan_out,
           outframe='LSRK', veltype='radio', restfreq=str(nu_rest/1e9)+'GHz',  
           imsize=imsize, cell=cell, deconvolver='multiscale', scales=scales, 
           gain=gain, niter=1000000, nterms=1, interactive=False, 
           weighting='briggs', robust=robust, uvtaper=uvtaper,
           threshold=threshold, mask=maskname, restoringbeam='common')

    os.system('rm -rf *.last')

    return
