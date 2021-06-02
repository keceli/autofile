""" test autofile.fs
"""
import os
import tempfile
import numpy
import pytest

import automol
import autofile.fs

PREFIX = tempfile.mkdtemp()
print(PREFIX)


def test__species():
    """ test autofile.fs.species
    """
    prefix = os.path.join(PREFIX, 'species')
    os.mkdir(prefix)

    locs = ['InChI=1S/C2H2F2/c3-1-2-4/h1-2H/b2-1+', 0, 1]
    spc_fs = autofile.fs.species(prefix)

    assert not spc_fs[-1].exists(locs)
    spc_fs[-1].create(locs)
    assert spc_fs[-1].exists(locs)


def test__reaction():
    """ test autofile.fs.reaction
    """
    prefix = os.path.join(PREFIX, 'reaction')
    os.mkdir(prefix)

    locs = [
        [['InChI=1S/C2H5O2/c1-2-4-3/h3H,1-2H2'],
         ['InChI=1S/C2H4/c1-2/h1-2H2', 'InChI=1S/HO2/c1-2/h1H']],
        [[0], [0, 0]],
        [[2], [1, 2]],
        2
    ]
    rxn_fs = autofile.fs.reaction(prefix)

    assert not rxn_fs[-1].exists(locs)
    rxn_fs[-1].create(locs)
    assert rxn_fs[-1].exists(locs)


# def test__transition_state():
#     """ test autofile.fs.transition_state
#     """
#     prefix = os.path.join(PREFIX, 'ts')
#     os.mkdir(prefix)
#
#     ts_fs = autofile.fs.transition_state(prefix)
#
#     assert not ts_fs[0].exists()
#     ts_fs[0].create()
#     assert ts_fs[0].exists()


def test__transition_state():
    """ test autofile.fs.transition_state
    """
    prefix = os.path.join(PREFIX, 'ts')
    os.mkdir(prefix)

    ts_fs = autofile.fs.transition_state(prefix)

    locs = [0]

    assert not ts_fs[-1].exists(locs)
    ts_fs[-1].create(locs)
    assert ts_fs[-1].exists(locs)

    # ref_vma = ()
    # ts_fs[-1].file.vmatrix.write(ref_vma, locs)
    # assert ts_fs[-1].file.vmatrix.read(locs) == ref_vma


def test__theory():
    """ test autofile.fs.theory
    """
    prefix = os.path.join(PREFIX, 'theory')
    os.mkdir(prefix)

    thy_fs = autofile.fs.theory(prefix)
    locs = ['hf', 'sto-3g', 'U']

    ref_ene = 5.7
    thy_fs[-1].create(locs)
    thy_fs[-1].file.energy.write(ref_ene, locs)
    assert thy_fs[-1].file.energy.read(locs) == ref_ene


def test__conformer():
    """ test autofile.fs.conformer
    """
    prefix = os.path.join(PREFIX, 'conformer')
    os.mkdir(prefix)

    locs = [
        autofile.schema.generate_new_ring_id(),
        autofile.schema.generate_new_conformer_id()]

    cnf_fs = autofile.fs.conformer(prefix)
    assert not cnf_fs[-1].exists(locs)
    cnf_fs[-1].create(locs)
    assert cnf_fs[-1].exists(locs)

    ref_inf_obj1 = autofile.schema.info_objects.conformer_trunk(1)
    ref_inf_obj2 = autofile.schema.info_objects.conformer_branch(1)
    cnf_fs[0].file.info.write(ref_inf_obj1)
    cnf_fs[1].file.info.write(ref_inf_obj2, [locs[0]])

    inf_obj1 = cnf_fs[0].file.info.read()
    inf_obj2 = cnf_fs[1].file.info.read([locs[0]])
    assert inf_obj1 == ref_inf_obj1
    assert inf_obj2 == ref_inf_obj2

    ref_ene = 5.7
    cnf_fs[-1].file.energy.write(ref_ene, locs)
    ene = cnf_fs[-1].file.energy.read(locs)
    assert numpy.isclose(ene, ref_ene)


def test__single_point():
    """ test autofile.fs.single_point
    """
    prefix = os.path.join(PREFIX, 'single_point')
    os.mkdir(prefix)

    sp_fs = autofile.fs.single_point(prefix)
    locs = ['hf', 'sto-3g', 'U']

    ref_ene = 5.7
    sp_fs[-1].create(locs)
    sp_fs[-1].file.energy.write(ref_ene, locs)
    assert sp_fs[-1].file.energy.read(locs) == ref_ene
    sp_fs[-1].removable = True
    sp_fs[-1].file.energy.removable = True
    sp_fs[-1].file.energy.remove(locs)
    sp_fs[-1].remove(locs)
    assert not sp_fs[-1].exists(locs)


def test__high_spin():
    """ test autofile.fs.high_spin
    """
    prefix = os.path.join(PREFIX, 'high_spin')
    os.mkdir(prefix)

    sp_fs = autofile.fs.high_spin(prefix)
    locs = ['hf', 'sto-3g', 'U']

    ref_ene = 5.7
    sp_fs[-1].create(locs)
    sp_fs[-1].file.energy.write(ref_ene, locs)
    assert sp_fs[-1].file.energy.read(locs) == ref_ene
    sp_fs[-1].removable = True
    sp_fs[-1].file.energy.removable = True
    sp_fs[-1].file.energy.remove(locs)
    sp_fs[-1].remove(locs)
    assert not sp_fs[-1].exists(locs)


def test__zmatrix():
    """ test autofile.fs.zmatrix
    """
    prefix = os.path.join(PREFIX, 'zmatrix')
    os.mkdir(prefix)

    zma_fs = autofile.fs.zmatrix(prefix)
    locs = [0]

    ref_zma = (
        ('O', (None, None, None), (None, None, None), (None, None, None)),
        ('H', (0, None, None), ('R1', None, None), (1.84779, None, None)))

    zma_fs[-1].create(locs)
    zma_fs[-1].file.zmatrix.write(ref_zma, locs)
    assert automol.zmat.almost_equal(
        zma_fs[-1].file.zmatrix.read(locs), ref_zma)

    ref_rxn = automol.reac.Reaction(
        rxn_cls=automol.par.ReactionClass.Typ.HYDROGEN_ABSTRACTION,
        forw_tsg=(
            {0: ('C', 0, None), 1: ('H', 0, None), 2: ('H', 0, None),
             3: ('H', 0, None), 4: ('H', 0, None), 5: ('O', 0, None),
             6: ('H', 0, None)},
            {frozenset({5, 6}): (1, None), frozenset({0, 3}): (1, None),
             frozenset({4, 5}): (0.1, None),
             frozenset({0, 1}): (1, None), frozenset({0, 2}): (1, None),
             frozenset({0, 4}): (0.9, None)}),
        back_tsg=(
            {0: ('O', 0, None), 1: ('H', 0, None), 2: ('H', 0, None),
             3: ('C', 0, None), 4: ('H', 0, None), 5: ('H', 0, None),
             6: ('H', 0, None)},
            {frozenset({0, 2}): (0.9, None),
             frozenset({2, 3}): (0.1, None),
             frozenset({3, 6}): (1, None), frozenset({0, 1}): (1, None),
             frozenset({3, 4}): (1, None), frozenset({3, 5}): (1, None)}),
        rcts_keys=((0, 1, 2, 3, 4), (5, 6)),
        prds_keys=((0, 1, 2), (3, 4, 5, 6)),
    )

    zma_fs[-1].file.reaction.write(ref_rxn, locs)
    rxn = zma_fs[-1].file.reaction.read(locs)

    assert rxn == ref_rxn


def test__scan():
    """ test autofile.fs.scan
    """
    prefix = os.path.join(PREFIX, 'scan')
    os.mkdir(prefix)

    scn_fs = autofile.fs.scan(prefix)
    locs = [['d3', 'd4'], [2, 3]]

    ref_inp_str = '<input string>'
    scn_fs[-1].create(locs)
    scn_fs[-1].file.geometry_input.write(ref_inp_str, locs)
    assert scn_fs[-1].file.geometry_input.read(locs) == ref_inp_str

    inf_obj = autofile.schema.info_objects.scan_branch(
        {'d4': numpy.array([0, 2])})
    scn_fs[1].create(['d4'])
    scn_fs[1].file.info.write(inf_obj, ['d4'])
    assert scn_fs[1].file.info.read(['d4']) == inf_obj


def test__cscan():
    """ test autofile.fs.cscan
    """
    prefix = os.path.join(PREFIX, 'cscan')
    os.mkdir(prefix)

    scn_fs = autofile.fs.cscan(prefix)
    locs = [{'R1': 1., 'A2': 2.3}, ['D3', 'D4'], [1.2, 2.9]]

    ref_inp_str = '<input string>'
    scn_fs[-1].create(locs)
    scn_fs[-1].file.geometry_input.write(ref_inp_str, locs)
    assert scn_fs[-1].file.geometry_input.read(locs) == ref_inp_str


def test__tau():
    """ test autofile.fs.tau
    """
    prefix = os.path.join(PREFIX, 'tau')
    os.mkdir(prefix)

    locs = [autofile.schema.generate_new_tau_id()]
    tau_fs = autofile.fs.tau(prefix)

    assert not tau_fs[-1].exists(locs)
    tau_fs[-1].create(locs)
    assert tau_fs[-1].exists(locs)

    inf_obj = autofile.schema.info_objects.tau_trunk(0, {})
    tau_fs[0].file.info.write(inf_obj)


def test__vrctst():
    """ test autofile.fs.vrctst
    """

    prefix = os.path.join(PREFIX, 'vrctst')
    os.mkdir(prefix)

    vrc_fs = autofile.fs.vrctst(prefix)
    locs = [0]

    ref_tst_str = '<TST STR>'
    ref_divsur_str = '<DIVSUR STR>'
    ref_molpro_str = '<MOLPRO STR>'
    ref_tml_str = '<TML STR>'
    ref_struct_str = '<STRUCT STR>'
    ref_pot_str = '<POT STR>'
    ref_flux_str = '<FLUX STR>'

    vrc_fs[-1].create(locs)
    vrc_fs[-1].file.vrctst_tst.write(ref_tst_str, locs)
    vrc_fs[-1].file.vrctst_divsur.write(ref_divsur_str, locs)
    vrc_fs[-1].file.vrctst_molpro.write(ref_molpro_str, locs)
    vrc_fs[-1].file.vrctst_tml.write(ref_tml_str, locs)
    vrc_fs[-1].file.vrctst_struct.write(ref_struct_str, locs)
    vrc_fs[-1].file.vrctst_pot.write(ref_pot_str, locs)
    vrc_fs[-1].file.vrctst_flux.write(ref_flux_str, locs)

    tst_str = vrc_fs[-1].file.vrctst_tst.read(locs)
    divsur_str = vrc_fs[-1].file.vrctst_divsur.read(locs)
    molpro_str = vrc_fs[-1].file.vrctst_molpro.read(locs)
    tml_str = vrc_fs[-1].file.vrctst_tml.read(locs)
    struct_str = vrc_fs[-1].file.vrctst_struct.read(locs)
    pot_str = vrc_fs[-1].file.vrctst_pot.read(locs)
    flux_str = vrc_fs[-1].file.vrctst_flux.read(locs)

    assert ref_tst_str == tst_str
    assert ref_divsur_str == divsur_str
    assert ref_molpro_str == molpro_str
    assert ref_tml_str == tml_str
    assert ref_struct_str == struct_str
    assert ref_pot_str == pot_str
    assert ref_flux_str == flux_str


def test__energy_transfer():
    """ test autofile.fs.energy_transfer
    """
    prefix = os.path.join(PREFIX, 'ETRANS')
    os.mkdir(prefix)

    etrans_fs = autofile.fs.energy_transfer(prefix)

    # Create filesys
    bath_locs = ['InChI=1S/N2/c1-2', 0, 1]
    thy_locs = ['hf', 'sto-3g', 'R']
    locs = bath_locs + thy_locs
    etrans_fs[-1].create(locs)

    ref_eps = 300.0
    ref_sig = 3.50
    ref_inp_str = '<INP STR>'
    ref_temp_str = '<TEMP STR>'
    ref_traj = (
        ((('H', (0.0, 0.0, 0.0)),), 'comment 1'),
        ((('H', (0.0, 0.0, 0.0)),), 'comment 2')
    )

    etrans_fs[-1].file.lennard_jones_epsilon.write(ref_eps, locs)
    etrans_fs[-1].file.lennard_jones_sigma.write(ref_sig, locs)
    etrans_fs[-1].file.lennard_jones_input.write(ref_inp_str, locs)
    etrans_fs[-1].file.lennard_jones_elstruct.write(ref_temp_str, locs)
    etrans_fs[-1].file.trajectory.write(ref_traj, locs)
    assert numpy.isclose(
        etrans_fs[-1].file.lennard_jones_epsilon.read(locs), ref_eps)
    assert numpy.isclose(
        etrans_fs[-1].file.lennard_jones_sigma.read(locs), ref_sig)
    assert etrans_fs[-1].file.lennard_jones_input.read(locs) == ref_inp_str
    assert etrans_fs[-1].file.lennard_jones_elstruct.read(locs) == ref_temp_str
    assert etrans_fs[-1].file.trajectory.read(locs) == ref_traj


def test__run():
    """ test autofile.fs.run
    """
    prefix = os.path.join(PREFIX, 'run')
    os.mkdir(prefix)

    run_fs = autofile.fs.run(prefix)

    ref_inp_str = '<input string>'
    run_fs[-1].create(['gradient'])
    run_fs[-1].file.input.write(ref_inp_str, ['gradient'])
    assert run_fs[-1].file.input.read(['gradient']) == ref_inp_str


def test__build():
    """ test autofile.fs.build
    """
    prefix = os.path.join(PREFIX, 'build')
    os.mkdir(prefix)

    build_fs = autofile.fs.build(prefix)

    ref_inp_str = '<input string>'
    build_fs[-1].create(['MESS', 'C2H5O', 0])
    build_fs[-1].file.input.write(ref_inp_str, ['MESS', 'C2H5O', 0])
    assert build_fs[-1].file.input.read(['MESS', 'C2H5O', 0]) == ref_inp_str


def test__json_io():
    """ test autofile.json_.read_json and write_json
    """
    prefix = os.path.join(PREFIX, 'tau')
    file_path = os.path.join(prefix, 'test.json')
    jsona = {'a': 1}
    jsonb = {'b': 2}
    autofile.json_.write_json(jsona, file_path)
    autofile.json_.write_json(jsonb, file_path)
    assert autofile.json_.read_json(file_path) == jsonb
    with pytest.raises(IOError):
        json_err = {'eek'}
        autofile.json_.write_json(json_err, file_path)
        # assert autofile.json_.read_json(file_path) == jsonb
    # with pytest.raises(IOError):
    # json_err = 'not_a_json'
    # autofile.io_.write_file(file_path, json_err)
    # assert autofile.json_.read_json(file_path) == jsonb


def test__json_tau_save():
    """ test <fs>.json.<property>.write
    """
    prefix = os.path.join(PREFIX, 'tau')
    tau_fs = autofile.fs.tau(prefix)
    save_path = tau_fs[-1].root.path()
    print(tau_fs[-1].json_path())
    tau_fs[-1].root.create()
    tau_fs[-1].json_create()
    print(tau_fs[-1].json_existing())
    print(tau_fs[-1].json_path())
    locs = [autofile.schema.generate_new_tau_id()]
    print(tau_fs[-1].exists(locs))
    print(tau_fs[-1].json_path(locs))
    sp_locs = ['hf', 'sto-3g', 'U']
    ref_ene = 5.7
    print(tau_fs[-1].json.energy.exists(locs))
    tau_fs[-1].json.energy.write(ref_ene, locs)
    assert tau_fs[-1].json.energy.exists(locs)
    print(tau_fs[-1].json.geometry.exists(locs))
    print(tau_fs[-1].json.gradient.exists(locs))
    print(tau_fs[-1].json.geometry_info.exists(locs))
    assert tau_fs[-1].json.energy.read(locs) == ref_ene

    tau_fs[-1].json_existing(locs=locs)
    tau_fs[-1].json.energy.write_all([ref_ene], [locs])
    tau_fs[-1].json.energy.read_all([locs])
    sp_save_fs = autofile.fs.single_point(
        save_path, json_layer=locs)
    sp_save_fs[-1].json_existing()
    sp_save_fs[-1].json_existing(locs=sp_locs)
    tau_fs[-1].json_existing(locs=sp_locs, json_layer=locs)
    sp_ene = 5.5
    print(sp_save_fs[-1].json.energy.exists(sp_locs))
    sp_save_fs[-1].json.energy.write(sp_ene, sp_locs)
    assert sp_save_fs[-1].json.energy.exists(sp_locs)
    assert sp_save_fs[-1].json.energy.read(sp_locs) == sp_ene
    sp_save_fs[-1].json_existing()
    sp_save_fs[-1].json_existing(locs=sp_locs)
    tau_fs[-1].json_existing(locs=sp_locs, json_layer=locs)


if __name__ == '__main__':
    # test__species()
    # test__reaction()
    # test__transition_state()
    # test__theory()
    test__conformer()
    # test__tau()
    # test__single_point()
    # test__high_spin()
    # test__energy_transfer()
    # test__json_io()
    # test__json_tau_save()
    # test__vrctst()
    # test__instab()
    # test__scan()
    # test__run()
    # test__build()
    # test__cscan()
    # test__zmatrix()
