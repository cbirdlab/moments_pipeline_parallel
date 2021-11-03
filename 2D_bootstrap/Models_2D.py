import numpy
import moments
import time
'''
Models for testing two population scenarios.
'''

def no_divergence(ns):
    """
    Standard neutral model, populations never diverge.
    """
    """
    #original dadi syntax
    xx = Numerics.default_grid(pts)
    phi = PhiManip.phi_1D(xx)
    phi = PhiManip.phi_1D_to_2D(xx, phi)
    fs = Spectrum.from_phi(phi, ns, (xx,xx))
    return fs
    """
    sts = moments.LinearSystem_1D.steady_state_1D(ns[0] + ns[1])
    fs = moments.Spectrum(sts)
    fs = moments.Manips.split_1D_to_2D(fs, ns[0], ns[1])
    #no integration step so there is no time for drift
    return fs

def no_mig(params, ns):
    """
    Split into two populations, no migration.

    nu1: Size of population 1 after split.
    nu2: Size of population 2 after split.
    T: Time in the past of split (in units of 2*Na generations) 
    """
    nu1, nu2, T = params
    """
    #original dadi syntax
    xx = Numerics.default_grid(pts)
    phi = PhiManip.phi_1D(xx)
    phi = PhiManip.phi_1D_to_2D(xx, phi)
    phi = Integration.two_pops(phi, xx, T, nu1, nu2, m12=0, m21=0)
    fs = Spectrum.from_phi(phi, ns, (xx,xx))
    return fs
    """
    sts = moments.LinearSystem_1D.steady_state_1D(ns[0] + ns[1])
    fs = moments.Spectrum(sts)
    fs = moments.Manips.split_1D_to_2D(fs, ns[0], ns[1])
    nomig = numpy.array([[0,0], [0,0]])
    fs.integrate([nu1,nu2], T, m=nomig, dt_fac=0.01)
    return fs

def sym_mig(params, ns):
    """
    Split into two populations, with symmetric migration.

    nu1: Size of population 1 after split.
    nu2: Size of population 2 after split.
    T: Time in the past of split (in units of 2*Na generations) 
    m: Migration rate between populations (2*Na*m)
    """
    nu1, nu2, m, T = params
    """
    #original dadi syntax
    xx = Numerics.default_grid(pts)
    phi = PhiManip.phi_1D(xx)
    phi = PhiManip.phi_1D_to_2D(xx, phi)
    phi = Integration.two_pops(phi, xx, T, nu1, nu2, m12=m, m21=m)
    fs = Spectrum.from_phi(phi, ns, (xx,xx))
    return fs
    """
    sts = moments.LinearSystem_1D.steady_state_1D(ns[0] + ns[1])
    fs = moments.Spectrum(sts)
    fs = moments.Manips.split_1D_to_2D(fs, ns[0], ns[1])
    sym_mig = numpy.array([[0,m], [m,0]])
    fs.integrate([nu1,nu2], T, m=sym_mig, dt_fac=0.01)
    return fs

def asym_mig(params, ns):
    """
    Split into two populations, with different migration rates.

    nu1: Size of population 1 after split.
    nu2: Size of population 2 after split.
    T: Time in the past of split (in units of 2*Na generations) 
    m12: Migration from pop 2 to pop 1 (2*Na*m12)
    m21: Migration from pop 1 to pop 2
	"""
    nu1, nu2, m12, m21, T = params
    """
    #original dadi syntax
    xx = Numerics.default_grid(pts)
    phi = PhiManip.phi_1D(xx)
    phi = PhiManip.phi_1D_to_2D(xx, phi)
    phi = Integration.two_pops(phi, xx, T, nu1, nu2, m12=m12, m21=m21)
    fs = Spectrum.from_phi(phi, ns, (xx,xx))
    return fs    
    """
    sts = moments.LinearSystem_1D.steady_state_1D(ns[0] + ns[1])
    fs = moments.Spectrum(sts)
    fs = moments.Manips.split_1D_to_2D(fs, ns[0], ns[1])
    asym_mig = numpy.array([[0,m12], [m21,0]])
    fs.integrate([nu1,nu2], T, m=asym_mig, dt_fac=0.01)
    return fs    

def anc_sym_mig(params, ns):
    """
    Split with symmetric migration followed by isolation.

    nu1: Size of population 1 after split.
    nu2: Size of population 2 after split.
    m: Migration between pop 2 and pop 1.
    T1: The scaled time between the split and the ancient migration (in units of 2*Na generations).
    T2: The scaled time between the ancient migration and present.
    """
    nu1, nu2, m, T1, T2 = params
    """
    #original dadi syntax
    xx = Numerics.default_grid(pts)
    phi = PhiManip.phi_1D(xx)
    phi = PhiManip.phi_1D_to_2D(xx, phi)
    phi = Integration.two_pops(phi, xx, T1, nu1, nu2, m12=m, m21=m)
    phi = Integration.two_pops(phi, xx, T2, nu1, nu2, m12=0, m21=0)
    fs = Spectrum.from_phi(phi, ns, (xx,xx))
    return fs
    """
    sts = moments.LinearSystem_1D.steady_state_1D(ns[0] + ns[1])
    fs = moments.Spectrum(sts)
    fs = moments.Manips.split_1D_to_2D(fs, ns[0], ns[1])
    sym_mig = numpy.array([[0,m], [m,0]])
    nomig = numpy.array([[0,0], [0,0]])
    fs.integrate([nu1,nu2], T1, m=sym_mig, dt_fac=0.01)
    fs.integrate([nu1,nu2], T2, m=nomig, dt_fac=0.01)
    return fs


def anc_asym_mig(params, ns):
    """
    Split with asymmetric migration followed by isolation.

    nu1: Size of population 1 after split.
    nu2: Size of population 2 after split.
    m12: Migration from pop 2 to pop 1 (2*Na*m12).
    m21: Migration from pop 1 to pop 2.
    T1: The scaled time between the split and the ancient migration (in units of 2*Na generations).
    T2: The scaled time between the ancient migration and present.
    """
    nu1, nu2, m12, m21, T1, T2 = params
    """
    #original dadi syntax
    xx = Numerics.default_grid(pts)
    phi = PhiManip.phi_1D(xx)
    phi = PhiManip.phi_1D_to_2D(xx, phi)
    phi = Integration.two_pops(phi, xx, T1, nu1, nu2, m12=m12, m21=m21)
    phi = Integration.two_pops(phi, xx, T2, nu1, nu2, m12=0, m21=0)
    fs = Spectrum.from_phi(phi, ns, (xx,xx))
    return fs
    """
    sts = moments.LinearSystem_1D.steady_state_1D(ns[0] + ns[1])
    fs = moments.Spectrum(sts)
    fs = moments.Manips.split_1D_to_2D(fs, ns[0], ns[1])
    asym_mig = numpy.array([[0,m12], [m21,0]])
    nomig = numpy.array([[0,0], [0,0]])
    fs.integrate([nu1,nu2], T1, m=asym_mig, dt_fac=0.01)
    fs.integrate([nu1,nu2], T2, m=nomig, dt_fac=0.01)
    return fs


def sec_contact_sym_mig(params, ns):
    """
    Split with no gene flow, followed by period of symmetrical gene flow.

    nu1: Size of population 1 after split.
    nu2: Size of population 2 after split.
    m: Migration between pop 2 and pop 1.
    T1: The scaled time between the split and the secondary contact (in units of 2*Na generations).
    T2: The scaled time between the secondary contact and present.
    """
    nu1, nu2, m, T1, T2 = params
    """
    #original dadi syntax
    xx = Numerics.default_grid(pts)  
    phi = PhiManip.phi_1D(xx)
    phi = PhiManip.phi_1D_to_2D(xx, phi)
    phi = Integration.two_pops(phi, xx, T1, nu1, nu2, m12=0, m21=0)
    phi = Integration.two_pops(phi, xx, T2, nu1, nu2, m12=m, m21=m)
    fs = Spectrum.from_phi(phi, ns, (xx,xx))
    return fs
    """
    sts = moments.LinearSystem_1D.steady_state_1D(ns[0] + ns[1])
    fs = moments.Spectrum(sts)
    fs = moments.Manips.split_1D_to_2D(fs, ns[0], ns[1])
    sym_mig = numpy.array([[0,m], [m,0]])
    nomig = numpy.array([[0,0], [0,0]])
    fs.integrate([nu1,nu2], T1, m=nomig, dt_fac=0.01)
    fs.integrate([nu1,nu2], T2, m=sym_mig, dt_fac=0.01)
    return fs


def sec_contact_asym_mig(params, ns):
    """
    Split with no gene flow, followed by period of asymmetrical gene flow.

    nu1: Size of population 1 after split.
    nu2: Size of population 2 after split.
    m12: Migration from pop 2 to pop 1 (2*Na*m12).
    m21: Migration from pop 1 to pop 2.
    T1: The scaled time between the split and the secondary contact (in units of 2*Na generations).
    T2: The scaled time between the secondary contact and present.
    """
    nu1, nu2, m12, m21, T1, T2 = params
    """
    #original dadi syntax
    xx = Numerics.default_grid(pts) 
    phi = PhiManip.phi_1D(xx)
    phi = PhiManip.phi_1D_to_2D(xx, phi)
    phi = Integration.two_pops(phi, xx, T1, nu1, nu2, m12=0, m21=0)
    phi = Integration.two_pops(phi, xx, T2, nu1, nu2, m12=m12, m21=m21)
    fs = Spectrum.from_phi(phi, ns, (xx,xx))
    return fs
    """
    sts = moments.LinearSystem_1D.steady_state_1D(ns[0] + ns[1])
    fs = moments.Spectrum(sts)
    fs = moments.Manips.split_1D_to_2D(fs, ns[0], ns[1])
    asym_mig = numpy.array([[0,m12], [m21,0]])
    nomig = numpy.array([[0,0], [0,0]])
    fs.integrate([nu1,nu2], T1, m=nomig, dt_fac=0.01)
    fs.integrate([nu1,nu2], T2, m=asym_mig, dt_fac=0.01)
    return fs


#######################################################################################################
#Models involving size changes

def no_mig_size(params, ns):
    """
    Split with no migration, then size change with no migration.

    nu1a: Size of population 1 after split.
    nu2a: Size of population 2 after split.
    T1: Time in the past of split (in units of 2*Na generations)
    nu1b: Size of population 1 after time interval.
    nu2b: Size of population 2 after time interval.
    T2: Time of population size change.
    """
    nu1a, nu2a, nu1b, nu2b, T1, T2 = params
    """
    #original dadi syntax
    xx = Numerics.default_grid(pts)
    phi = PhiManip.phi_1D(xx)
    phi = PhiManip.phi_1D_to_2D(xx, phi)
    phi = Integration.two_pops(phi, xx, T1, nu1a, nu2a, m12=0, m21=0)   
    phi = Integration.two_pops(phi, xx, T2, nu1b, nu2b, m12=0, m21=0)
    fs = Spectrum.from_phi(phi, ns, (xx,xx))
    return fs
    """
    sts = moments.LinearSystem_1D.steady_state_1D(ns[0] + ns[1])
    fs = moments.Spectrum(sts)
    fs = moments.Manips.split_1D_to_2D(fs, ns[0], ns[1])
    nomig = numpy.array([[0,0], [0,0]])
    fs.integrate([nu1a,nu2a], T1, m=nomig, dt_fac=0.01)
    fs.integrate([nu1b,nu2b], T2, m=nomig, dt_fac=0.01)
    return fs

def sym_mig_size(params, ns):
    """
    Split with symmetric migration, then size change with symmetric migration.

    nu1a: Size of population 1 after split.
    nu2a: Size of population 2 after split.
    T1: Time in the past of split (in units of 2*Na generations)
    nu1b: Size of population 1 after time interval.
    nu2b: Size of population 2 after time interval.
    T2: Time of population size change.
    m: Migration rate between populations (2*Na*m)
    """
    nu1a, nu2a, nu1b, nu2b, m, T1, T2 = params
    """
    #original dadi syntax
    xx = Numerics.default_grid(pts)
    phi = PhiManip.phi_1D(xx)
    phi = PhiManip.phi_1D_to_2D(xx, phi)
    phi = Integration.two_pops(phi, xx, T1, nu1a, nu2a, m12=m, m21=m)  
    phi = Integration.two_pops(phi, xx, T2, nu1b, nu2b, m12=m, m21=m)
    fs = Spectrum.from_phi(phi, ns, (xx,xx))
    return fs
    """
    sts = moments.LinearSystem_1D.steady_state_1D(ns[0] + ns[1])
    fs = moments.Spectrum(sts)
    fs = moments.Manips.split_1D_to_2D(fs, ns[0], ns[1])
    sym_mig = numpy.array([[0,m], [m,0]])
    fs.integrate([nu1a,nu2a], T1, m=sym_mig, dt_fac=0.01)
    fs.integrate([nu1b,nu2b], T2, m=sym_mig, dt_fac=0.01)
    return fs

def asym_mig_size(params, ns):
    """
    Split with different migration rates, then size change with different migration rates.

    nu1a: Size of population 1 after split.
    nu2a: Size of population 2 after split.
    T1: Time in the past of split (in units of 2*Na generations)
    nu1b: Size of population 1 after time interval.
    nu2b: Size of population 2 after time interval.
    T2: Time of population size change.
    m12: Migration from pop 2 to pop 1 (2*Na*m12)
    m21: Migration from pop 1 to pop 2
	"""
    nu1a, nu2a, nu1b, nu2b, m12, m21, T1, T2 = params
    """
    #original dadi syntax
    xx = Numerics.default_grid(pts)
    phi = PhiManip.phi_1D(xx)
    phi = PhiManip.phi_1D_to_2D(xx, phi)
    phi = Integration.two_pops(phi, xx, T1, nu1a, nu2a, m12=m12, m21=m21)
    phi = Integration.two_pops(phi, xx, T2, nu1b, nu2b, m12=m12, m21=m21)
    fs = Spectrum.from_phi(phi, ns, (xx,xx))
    return fs    
    """
    sts = moments.LinearSystem_1D.steady_state_1D(ns[0] + ns[1])
    fs = moments.Spectrum(sts)
    fs = moments.Manips.split_1D_to_2D(fs, ns[0], ns[1])
    asym_mig = numpy.array([[0,m12], [m21,0]])
    fs.integrate([nu1a,nu2a], T1, m=asym_mig, dt_fac=0.01)
    fs.integrate([nu1b,nu2b], T2, m=asym_mig, dt_fac=0.01)
    return fs

def anc_sym_mig_size(params, ns):
    """
    Split with symmetrical gene flow, followed by size change with no gene flow.  

    nu1a: Size of population 1 after split.
    nu2a: Size of population 2 after split.
    T1: Time in the past of split (in units of 2*Na generations)
    nu1b: Size of population 1 after time interval.
    nu2b: Size of population 2 after time interval.
    T2: The scale time between the ancient migration and present.
    m: Migration between pop 2 and pop 1.
    """
    nu1a, nu2a, nu1b, nu2b, m, T1, T2 = params
    """
    #original dadi syntax
    xx = Numerics.default_grid(pts)
    phi = PhiManip.phi_1D(xx)
    phi = PhiManip.phi_1D_to_2D(xx, phi)
    phi = Integration.two_pops(phi, xx, T1, nu1a, nu2a, m12=m, m21=m)
    phi = Integration.two_pops(phi, xx, T2, nu1b, nu2b, m12=0, m21=0)
    fs = Spectrum.from_phi(phi, ns, (xx,xx))
    return fs
    """
    sts = moments.LinearSystem_1D.steady_state_1D(ns[0] + ns[1])
    fs = moments.Spectrum(sts)
    fs = moments.Manips.split_1D_to_2D(fs, ns[0], ns[1])
    sym_mig = numpy.array([[0,m], [m,0]])
    nomig = numpy.array([[0,0], [0,0]])
    fs.integrate([nu1a,nu2a], T1, m=sym_mig, dt_fac=0.01)
    fs.integrate([nu1b,nu2b], T2, m=nomig, dt_fac=0.01)
    return fs


def anc_asym_mig_size(params, ns):
    """
    Split with asymmetrical gene flow, followed by size change with no gene flow.

    nu1a: Size of population 1 after split.
    nu2a: Size of population 2 after split.
    T1: Time in the past of split (in units of 2*Na generations)
    nu1b: Size of population 1 after time interval.
    nu2b: Size of population 2 after time interval.
    T2: The scale time between the ancient migration and present.
    m12: Migration from pop 2 to pop 1 (2*Na*m12).
    m21: Migration from pop 1 to pop 2.
    """
    nu1a, nu2a, nu1b, nu2b, m12, m21, T1, T2 = params
    """
    #original dadi syntax
    xx = Numerics.default_grid(pts)
    phi = PhiManip.phi_1D(xx)
    phi = PhiManip.phi_1D_to_2D(xx, phi)
    phi = Integration.two_pops(phi, xx, T1, nu1a, nu2a, m12=m12, m21=m21)
    phi = Integration.two_pops(phi, xx, T2, nu1b, nu2b, m12=0, m21=0)
    fs = Spectrum.from_phi(phi, ns, (xx,xx))
    return fs
    """
    sts = moments.LinearSystem_1D.steady_state_1D(ns[0] + ns[1])
    fs = moments.Spectrum(sts)
    fs = moments.Manips.split_1D_to_2D(fs, ns[0], ns[1])
    asym_mig = numpy.array([[0,m12], [m21,0]])
    nomig = numpy.array([[0,0], [0,0]])
    fs.integrate([nu1a,nu2a], T1, m=asym_mig, dt_fac=0.01)
    fs.integrate([nu1b,nu2b], T2, m=nomig, dt_fac=0.01)
    return fs


def sec_contact_sym_mig_size(params, ns):
    """
    Split with no gene flow, followed by size change with symmetrical gene flow.

    nu1a: Size of population 1 after split.
    nu2a: Size of population 2 after split.
    T1: The scaled time between the split and the secondary contact (in units of 2*Na generations).
    nu1b: Size of population 1 after time interval.
    nu2b: Size of population 2 after time interval.
    T2: The scale time between the secondary contact and present.
    m: Migration between pop 2 and pop 1.
    """
    nu1a, nu2a, nu1b, nu2b, m, T1, T2 = params
    """
    #original dadi syntax
    xx = Numerics.default_grid(pts)
    phi = PhiManip.phi_1D(xx)
    phi = PhiManip.phi_1D_to_2D(xx, phi)
    phi = Integration.two_pops(phi, xx, T1, nu1a, nu2a, m12=0, m21=0)
    phi = Integration.two_pops(phi, xx, T2, nu1b, nu2b, m12=m, m21=m)
    fs = Spectrum.from_phi(phi, ns, (xx,xx))
    return fs
    """
    sts = moments.LinearSystem_1D.steady_state_1D(ns[0] + ns[1])
    fs = moments.Spectrum(sts)
    fs = moments.Manips.split_1D_to_2D(fs, ns[0], ns[1])
    sym_mig = numpy.array([[0,m], [m,0]])
    nomig = numpy.array([[0,0], [0,0]])
    fs.integrate([nu1a,nu2a], T1, m=nomig, dt_fac=0.01)
    fs.integrate([nu1b,nu2b], T2, m=sym_mig, dt_fac=0.01)
    return fs


def sec_contact_asym_mig_size(params, ns):
    """
    Split with no gene flow, followed by size change with asymmetrical gene flow.

    nu1a: Size of population 1 after split.
    nu2a: Size of population 2 after split.
    T1: The scaled time between the split and the secondary contact (in units of 2*Na generations).
    nu1b: Size of population 1 after time interval.
    nu2b: Size of population 2 after time interval.
    T2: The scale time between the secondary contact and present.
    m12: Migration from pop 2 to pop 1 (2*Na*m12).
    m21: Migration from pop 1 to pop 2.
    """
    nu1a, nu2a, nu1b, nu2b, m12, m21, T1, T2 = params
    """
    #original dadi syntax
    xx = Numerics.default_grid(pts)
    phi = PhiManip.phi_1D(xx)
    phi = PhiManip.phi_1D_to_2D(xx, phi)
    phi = Integration.two_pops(phi, xx, T1, nu1a, nu2a, m12=0, m21=0)
    phi = Integration.two_pops(phi, xx, T2, nu1b, nu2b, m12=m12, m21=m21)
    fs = Spectrum.from_phi(phi, ns, (xx,xx))
    return fs
    """
    sts = moments.LinearSystem_1D.steady_state_1D(ns[0] + ns[1])
    fs = moments.Spectrum(sts)
    fs = moments.Manips.split_1D_to_2D(fs, ns[0], ns[1])
    asym_mig = numpy.array([[0,m12], [m21,0]])
    nomig = numpy.array([[0,0], [0,0]])
    fs.integrate([nu1a,nu2a], T1, m=nomig, dt_fac=0.01)
    fs.integrate([nu1b,nu2b], T2, m=asym_mig, dt_fac=0.01)
    return fs

#######################################################################################################
#Two Epoch split with changing migration rates

def sym_mig_twoepoch(params, ns):
    """
    Split into two populations, with symmetric migration. A second period of symmetric
    migration occurs, but can be a different rate. Pop size is same.

    nu1: Size of population 1 after split.
    nu2: Size of population 2 after split.
    T: Time in the past of split (in units of 2*Na generations) 
    m: Migration rate between populations (2*Na*m)
    """
    nu1, nu2, m1, m2, T1, T2 = params
    """
    #original dadi syntax
    xx = Numerics.default_grid(pts)
    phi = PhiManip.phi_1D(xx)
    phi = PhiManip.phi_1D_to_2D(xx, phi)
    phi = Integration.two_pops(phi, xx, T1, nu1, nu2, m12=m1, m21=m1)
    phi = Integration.two_pops(phi, xx, T2, nu1, nu2, m12=m2, m21=m2)
    fs = Spectrum.from_phi(phi, ns, (xx,xx))
    return fs
    """
    sts = moments.LinearSystem_1D.steady_state_1D(ns[0] + ns[1])
    fs = moments.Spectrum(sts)
    fs = moments.Manips.split_1D_to_2D(fs, ns[0], ns[1])
    sym_mig1 = numpy.array([[0,m1], [m1,0]])
    sym_mig2 = numpy.array([[0,m2], [m2,0]])
    fs.integrate([nu1,nu2], T1, m=sym_mig1, dt_fac=0.01)
    fs.integrate([nu1,nu2], T2, m=sym_mig2, dt_fac=0.01)
    return fs

def asym_mig_twoepoch(params, ns):
    """
    Split into two populations, with different migration rates. A second period of asymmetric
    migration occurs, but can be at different rates. Pop size is same.

    nu1: Size of population 1 after split.
    nu2: Size of population 2 after split.
    T: Time in the past of split (in units of 2*Na generations) 
    m12: Migration from pop 2 to pop 1 (2*Na*m12)
    m21: Migration from pop 1 to pop 2
	"""
    nu1, nu2, m12a, m21a, m12b, m21b, T1, T2 = params
    """
    #original dadi syntax
    xx = Numerics.default_grid(pts)
    phi = PhiManip.phi_1D(xx)
    phi = PhiManip.phi_1D_to_2D(xx, phi)
    phi = Integration.two_pops(phi, xx, T1, nu1, nu2, m12=m12a, m21=m21a)
    phi = Integration.two_pops(phi, xx, T2, nu1, nu2, m12=m12b, m21=m21b)
    fs = Spectrum.from_phi(phi, ns, (xx,xx))
    return fs    
    """
    sts = moments.LinearSystem_1D.steady_state_1D(ns[0] + ns[1])
    fs = moments.Spectrum(sts)
    fs = moments.Manips.split_1D_to_2D(fs, ns[0], ns[1])
    asym_mig1 = numpy.array([[0,m12a], [m21a,0]])
    asym_mig2 = numpy.array([[0,m12b], [m21b,0]])
    fs.integrate([nu1,nu2], T1, m=asym_mig1, dt_fac=0.01)
    fs.integrate([nu1,nu2], T2, m=asym_mig2, dt_fac=0.01)
    return fs

#######################################################################################################
#Three Epoch: Divergence and Isolation, Secondary Contact, Isolation

def sec_contact_sym_mig_three_epoch(params, ns):
    """
    Split with no gene flow, followed by period of symmetrical gene flow, then isolation.

    nu1: Size of population 1 after split.
    nu2: Size of population 2 after split.
    m: Migration between pop 2 and pop 1.
    T1: The scaled time between the split and the secondary contact (in units of 2*Na generations).
    T2: The scaled time between the secondary contact and third epoch.
    T3: The scaled time between the isolation and present.
    """
    nu1, nu2, m, T1, T2, T3 = params
    """
    #original dadi syntax
    xx = Numerics.default_grid(pts)
    phi = PhiManip.phi_1D(xx)
    phi = PhiManip.phi_1D_to_2D(xx, phi)
    phi = Integration.two_pops(phi, xx, T1, nu1, nu2, m12=0, m21=0)
    phi = Integration.two_pops(phi, xx, T2, nu1, nu2, m12=m, m21=m)
    phi = Integration.two_pops(phi, xx, T3, nu1, nu2, m12=0, m21=0)
    fs = Spectrum.from_phi(phi, ns, (xx,xx))
    return fs
    """
    sts = moments.LinearSystem_1D.steady_state_1D(ns[0] + ns[1])
    fs = moments.Spectrum(sts)
    fs = moments.Manips.split_1D_to_2D(fs, ns[0], ns[1])
    sym_mig = numpy.array([[0,m], [m,0]])
    nomig = numpy.array([[0,0], [0,0]])
    fs.integrate([nu1,nu2], T1, m=nomig, dt_fac=0.01)
    fs.integrate([nu1,nu2], T2, m=sym_mig, dt_fac=0.01)
    fs.integrate([nu1,nu2], T3, m=nomig, dt_fac=0.01)
    return fs

def sec_contact_asym_mig_three_epoch(params, ns):
    """
    Split with no gene flow, followed by period of asymmetrical gene flow, then isolation.

    nu1: Size of population 1 after split.
    nu2: Size of population 2 after split.
    m12: Migration from pop 2 to pop 1 (2*Na*m12).
    m21: Migration from pop 1 to pop 2.
    T1: The scaled time between the split and the secondary contact (in units of 2*Na generations).
    T2: The scaled time between the secondary contact and third epoch.
    T3: The scaled time between the isolation and present.
    """
    nu1, nu2, m12, m21, T1, T2, T3 = params
    """
    #original dadi syntax
    xx = Numerics.default_grid(pts)
    phi = PhiManip.phi_1D(xx)
    phi = PhiManip.phi_1D_to_2D(xx, phi)
    phi = Integration.two_pops(phi, xx, T1, nu1, nu2, m12=0, m21=0)
    phi = Integration.two_pops(phi, xx, T2, nu1, nu2, m12=m12, m21=m21)
    phi = Integration.two_pops(phi, xx, T2, nu1, nu2, m12=0, m21=0)
    fs = Spectrum.from_phi(phi, ns, (xx,xx))
    return fs
    """
    sts = moments.LinearSystem_1D.steady_state_1D(ns[0] + ns[1])
    fs = moments.Spectrum(sts)
    fs = moments.Manips.split_1D_to_2D(fs, ns[0], ns[1])
    asym_mig = numpy.array([[0,m12], [m21,0]])
    nomig = numpy.array([[0,0], [0,0]])
    fs.integrate([nu1,nu2], T1, m=nomig, dt_fac=0.01)
    fs.integrate([nu1,nu2], T2, m=asym_mig, dt_fac=0.01)
    fs.integrate([nu1,nu2], T3, m=nomig, dt_fac=0.01)
    return fs

def sec_contact_sym_mig_size_three_epoch(params, ns):
    """
    Split with no gene flow, followed by size change with symmetrical gene flow, then isolation.

    nu1a: Size of population 1 after split.
    nu2a: Size of population 2 after split.
    T1: The scaled time between the split and the secondary contact (in units of 2*Na generations).
    nu1b: Size of population 1 after time interval.
    nu2b: Size of population 2 after time interval.
    T2: The scale time between the secondary contact and isolation.
    T3: The scaled time between the isolation and present.
    m: Migration between pop 2 and pop 1.
    """
    nu1a, nu2a, nu1b, nu2b, m, T1, T2, T3 = params
    """
    #original dadi syntax
    xx = Numerics.default_grid(pts)
    phi = PhiManip.phi_1D(xx)
    phi = PhiManip.phi_1D_to_2D(xx, phi)
    phi = Integration.two_pops(phi, xx, T1, nu1a, nu2a, m12=0, m21=0)
    phi = Integration.two_pops(phi, xx, T2, nu1b, nu2b, m12=m, m21=m)
    phi = Integration.two_pops(phi, xx, T3, nu1b, nu2b, m12=0, m21=0)
    fs = Spectrum.from_phi(phi, ns, (xx,xx))
    return fs
    """
    sts = moments.LinearSystem_1D.steady_state_1D(ns[0] + ns[1])
    fs = moments.Spectrum(sts)
    fs = moments.Manips.split_1D_to_2D(fs, ns[0], ns[1])
    sym_mig = numpy.array([[0,m], [m,0]])
    nomig = numpy.array([[0,0], [0,0]])
    fs.integrate([nu1a,nu2a], T1, m=nomig, dt_fac=0.01)
    fs.integrate([nu1b,nu2b], T2, m=sym_mig, dt_fac=0.01)
    fs.integrate([nu1b,nu2b], T3, m=nomig, dt_fac=0.01)
    return fs

def sec_contact_asym_mig_size_three_epoch(params, ns):
    """
    Split with no gene flow, followed by size change with asymmetrical gene flow, then isolation.

    nu1a: Size of population 1 after split.
    nu2a: Size of population 2 after split.
    T1: The scaled time between the split and the secondary contact (in units of 2*Na generations).
    nu1b: Size of population 1 after time interval.
    nu2b: Size of population 2 after time interval.
    T2: The scale time between the secondary contact and isolation.
    T3: The scaled time between the isolation and present.
    m12: Migration from pop 2 to pop 1 (2*Na*m12).
    m21: Migration from pop 1 to pop 2.
    """
    nu1a, nu2a, nu1b, nu2b, m12, m21, T1, T2, T3 = params
    """
    #original dadi syntax
    xx = Numerics.default_grid(pts)
    phi = PhiManip.phi_1D(xx)
    phi = PhiManip.phi_1D_to_2D(xx, phi)
    phi = Integration.two_pops(phi, xx, T1, nu1a, nu2a, m12=0, m21=0)
    phi = Integration.two_pops(phi, xx, T2, nu1b, nu2b, m12=m12, m21=m21)
    phi = Integration.two_pops(phi, xx, T3, nu1b, nu2b, m12=0, m21=0)
    fs = Spectrum.from_phi(phi, ns, (xx,xx))
    return fs
    """
    sts = moments.LinearSystem_1D.steady_state_1D(ns[0] + ns[1])
    fs = moments.Spectrum(sts)
    fs = moments.Manips.split_1D_to_2D(fs, ns[0], ns[1])
    asym_mig = numpy.array([[0,m12], [m21,0]])
    nomig = numpy.array([[0,0], [0,0]])
    fs.integrate([nu1a,nu2a], T1, m=nomig, dt_fac=0.01)
    fs.integrate([nu1b,nu2b], T2, m=asym_mig, dt_fac=0.01)
    fs.integrate([nu1b,nu2b], T3, m=nomig, dt_fac=0.01)
    return fs

