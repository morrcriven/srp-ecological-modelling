import numpy as np

# Parser
import Parser
def test_parser():
    """ test that parser returns the correct types
    """
    sys_args = ['--outfile', 'results/out_matrix.pkl', '--params', 'params.json']
    parser = Parser.Parser(sys_args)
    assert(isinstance(parser.args.file, str))
    assert(isinstance(parser.args.dollar_size, str))

# Landscape: LSP
from Landscape import LSP
def test_sample_0():
    lsp = LSP([1,2,3,4], [10, 20, 30, 40, 40], [0, 10, 20, 10, 30])
    for _ in np.arange(100):
        assert(lsp.sample() in [1,2,3,4])

def test_sample_1():
    for _ in np.arange(50):
        l = np.random.choice(np.arange(100), 5)
        lsp = LSP(l, [10, 20, 30, 40, 40], [0, 10, 20, 10, 30])
        for _ in np.arange(100):
            assert(lsp.sample() in l)

def test_simulate_0():
    lsp = LSP([1,2,3,4], [10, 20, 30, 40, 40], [0, 10, 20, 10, 30])
    trajectory = np.cumsum(np.array(lsp.recr_trajectory) - \
                           np.array(lsp.mort_trajectory))
    M = lsp.simulate()
    assert(M.shape == (4, 5))
    assert((M.sum(axis=0) == trajectory).all())

# def test_simulate_1():

# Landscape: GSP
from Landscape import GSP
def test_initialise_LSPs():
    gsp = GSP(np.arange(10))
    gsp.initialise_LSPs(4, 5, [10, 20, 30, 40, 40], [0, 10, 20, 10, 30])

    assert(len(gsp.LSP_list) == 4)
    for i in np.arange(4):
        assert(gsp.LSP_list[i].get_size() == 5)

def test_simulate():
    gsp = GSP(np.arange(10))
    gsp.initialise_LSPs(4, 10, [10, 20, 30, 40, 40], [0, 10, 20, 10, 30])
    trajectory = np.cumsum(np.array(gsp.LSP_list[0].recr_trajectory) \
                           - np.array(gsp.LSP_list[0].mort_trajectory))
    M = gsp.simulate()

    assert(M.shape == (4, 10, 5))
    for i in np.arange(4):
        assert((M[i].sum(axis=0) == trajectory).all())


