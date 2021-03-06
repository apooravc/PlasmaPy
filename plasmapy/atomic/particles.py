from typing import Set, Dict, List, Optional, Union
from astropy import units as u, constants as const
import numpy as np


class _ParticleZooClass():
    r"""Creates an object with taxonomy information for special particles.

    The _taxonomy_dict attribute contains the name of each classification
    (e.g., 'lepton', 'baryon', 'matter', etc.) as the keys and a set of
    particle symbol strings of the particles belonging to that classification.

    The attributes of this class provide sets of strings representing
    particles in the corresponding category.

    Examples
    --------
    >>> ParticleZoo = _ParticleZooClass()
    >>> 'e-' in ParticleZoo.leptons
    True
    >>> 'nu_e' in ParticleZoo.antineutrinos
    False
    >>> 'mu+' in ParticleZoo.antiparticles
    True
    """

    def __init__(self):

        leptons = {'e-', 'mu-', 'tau-', 'nu_e', 'nu_mu', 'nu_tau'}

        antileptons = {'e+', 'mu+', 'tau+', 'anti_nu_e',
                       'anti_nu_mu', 'anti_nu_tau'}

        baryons = {'p+', 'n'}

        antibaryons = {'p-', 'antineutron'}

        particles = leptons | baryons

        antiparticles = antileptons | antibaryons

        fermions = leptons | antileptons | baryons | antibaryons

        bosons = set()

        neutrinos = {lepton for lepton in leptons if 'nu' in lepton}

        antineutrinos = {antilepton for antilepton in antileptons
                         if 'nu' in antilepton}

        self._taxonomy_dict = {
            'lepton': leptons,
            'antilepton': antileptons,
            'baryon': baryons,
            'antibaryon': antibaryons,
            'fermion': fermions,
            'boson': bosons,
            'neutrino': neutrinos,
            'antineutrinos': antineutrinos,
            'matter': particles,
            'antimatter': antiparticles,
        }

    @property
    def leptons(self) -> Set[str]:
        r"""Returns a set of strings representing leptons."""
        return self._taxonomy_dict['lepton']

    @property
    def antileptons(self) -> Set[str]:
        r"""Returns a set of strings representing antileptons."""
        return self._taxonomy_dict['antilepton']

    @property
    def baryons(self) -> Set[str]:
        r"""Returns a set of strings representing baryons."""
        return self._taxonomy_dict['baryon']

    @property
    def antibaryons(self) -> Set[str]:
        r"""Returns a set of strings representing antibaryons."""
        return self._taxonomy_dict['antibaryon']

    @property
    def fermions(self) -> Set[str]:
        r"""Returns a set of strings representing fermions."""
        return self._taxonomy_dict['fermion']

    @property
    def bosons(self) -> Set[str]:
        r"""Returns a set of strings representing bosons."""
        return self._taxonomy_dict['boson']

    @property
    def neutrinos(self) -> Set[str]:
        r"""Returns a set of strings representing neutrinos."""
        return self._taxonomy_dict['neutrino']

    @property
    def antineutrinos(self) -> Set[str]:
        r"""Returns a set of strings representing antineutrinos."""
        return self._taxonomy_dict['antineutrinos']

    @property
    def particles(self) -> Set[str]:
        r"""Returns a set of strings representing particles (as
        opposed to antiparticles)."""
        return self._taxonomy_dict['matter']

    @property
    def antiparticles(self) -> Set[str]:
        r"""Returns a set of strings representing antiparticles."""
        return self._taxonomy_dict['antimatter']

    @property
    def everything(self) -> Set[str]:
        r"""Returns a set of strings representing all particles and
        antiparticles"""
        return \
            self._taxonomy_dict['matter'] | self._taxonomy_dict['antimatter']


ParticleZoo = _ParticleZooClass()


def _create_Particles_dict() -> Dict[str, dict]:
    """Create a dictionary of dictionaries that contains physical
    information for particles and antiparticles that are not
    elements or ions.

    The keys of the top-level dictionary are the standard
    particle symbols. The values of the top-level dictionary
    are dictionaries for each particle or antiparticle with
    strings such as 'name', 'mass', and 'spin' as the keys
    and the corresponding atomic properties as symbols."""

    symbols_and_names = [
        ('e-', 'electron'),
        ('e+', 'positron'),
        ('mu-', 'muon'),
        ('mu+', 'antimuon'),
        ('tau-', 'tau'),
        ('tau+', 'antitau'),
        ('nu_e', 'electron neutrino'),
        ('anti_nu_e', 'electron antineutrino'),
        ('nu_mu', 'muon neutrino'),
        ('anti_nu_mu', 'muon antineutrino'),
        ('nu_tau', 'tau neutrino'),
        ('anti_nu_tau', 'tau antineutrino'),
        ('p+', 'proton'),
        ('p-', 'antiproton'),
        ('n', 'neutron'),
        ('antineutron', 'antineutron'),
    ]

    Particles = dict()

    for thing in ParticleZoo.everything:
        Particles[thing] = dict()

    for symbol, name in symbols_and_names:
        Particles[symbol]['name'] = name

    for fermion in ParticleZoo.fermions:
        Particles[fermion]['spin'] = 0.5

    for boson in ParticleZoo.bosons:  # coveralls: ignore
        Particles[boson]['spin'] = 0

    for lepton in ParticleZoo.leptons:
        Particles[lepton]['class'] = 'lepton'
        Particles[lepton]['lepton number'] = 1
        Particles[lepton]['baryon number'] = 0
        if lepton not in ParticleZoo.neutrinos:
            Particles[lepton]['charge'] = -1
        else:
            Particles[lepton]['charge'] = 0

    for antilepton in ParticleZoo.antileptons:
        Particles[antilepton]['class'] = 'antilepton'
        Particles[antilepton]['lepton number'] = -1
        Particles[antilepton]['baryon number'] = 0
        if antilepton not in ParticleZoo.antineutrinos:
            Particles[antilepton]['charge'] = 1
        else:
            Particles[antilepton]['charge'] = 0

    for baryon in ParticleZoo.baryons:
        Particles[baryon]['class'] = 'baryon'
        Particles[baryon]['lepton number'] = 0
        Particles[baryon]['baryon number'] = 1

    for antibaryon in ParticleZoo.antibaryons:
        Particles[antibaryon]['class'] = 'antibaryon'
        Particles[antibaryon]['lepton number'] = 0
        Particles[antibaryon]['baryon number'] = -1

    for thing in ParticleZoo.leptons | ParticleZoo.antileptons:
        if 'e' in thing:
            Particles[thing]['generation'] = 1
        elif 'mu' in thing:
            Particles[thing]['generation'] = 2
        elif 'tau' in thing:
            Particles[thing]['generation'] = 3

    for thing in ParticleZoo.leptons | ParticleZoo.antileptons:
        if 'nu' not in thing:
            if 'e' in thing:
                Particles[thing]['mass'] = const.m_e
            elif 'mu' in thing:
                Particles[thing]['mass'] = 1.883_531_594e-28 * u.kg
                Particles[thing]['half-life'] = 2.1969811e-6 * u.s
            elif 'tau' in thing:
                Particles[thing]['mass'] = 3.167_47e-27 * u.kg
                Particles[thing]['half-life'] = 2.906e-13 * u.s

    # Neutrinos are now known to have a tiny but non-zero mass, but
    # it is not known what the masses of the neutrinos actually are.
    # Setting the neutrino mass to None here will

    for thing in ParticleZoo.neutrinos | ParticleZoo.antineutrinos:
        Particles[thing]['mass'] = None

    for thing in ['p+', 'p-']:
        Particles[thing]['mass'] = const.m_p

    Particles['p+']['charge'] = 1
    Particles['p-']['charge'] = -1

    for thing in ['n', 'antineutron']:
        Particles[thing]['mass'] = const.m_n
        Particles[thing]['half-life'] = 881.5 * u.s
        Particles[thing]['charge'] = 0

    for thing in ParticleZoo.everything:
        if 'half-life' not in Particles[thing].keys():
            Particles[thing]['half-life'] = np.inf * u.s

    for particle in ParticleZoo.particles:
        Particles[particle]['antimatter'] = False

    for antiparticle in ParticleZoo.antiparticles:
        Particles[antiparticle]['antimatter'] = True

    return Particles


_Particles = _create_Particles_dict()


if __name__ == "__main__":  # coveralls: ignore
    from pprint import pprint
    print("Particles:")
    pprint(_Particles)
