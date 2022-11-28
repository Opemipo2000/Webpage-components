import numpy
import math
import json
from database import Database

frequency = numpy.empty(60)
output_frequency = numpy.empty(60)
output_permittivity = numpy.empty(60)
output_conductivity = numpy.empty(60)
output_loss_ratio = numpy.empty(60)
permittivity = numpy.empty((60, 51))
conductivity = numpy.empty((60, 51))
database1 = Database()

omg = numpy.empty(60)
ep = numpy.empty((60, 50))
sg = numpy.empty((60, 50))
ep_imag = numpy.empty((60, 50))
vector = numpy.empty(4)

ep_cmplx = numpy.empty((60, 50), dtype='c')
ep_cal = numpy.empty((60, 50), dtype='c')
d_ep = numpy.empty((60, 50), dtype='c')
g = numpy.empty((60, 4), dtype='c')

pi = 3.1415926536
ep_0 = 8.854e-12  # physical constant[F/m]

dA = numpy.empty(4)
A = numpy.empty(4)
P = numpy.empty(4)
D = numpy.empty(4)

B = numpy.empty((4, 4))
C = numpy.empty((4, 60))
IPIV = numpy.empty(4)
Q = numpy.empty((4, 4))
PARAMETERS = numpy.empty((4, 50))


with open("Debye/parameters.json", 'r') as file:
    data = json.load(file)
    print(f"got data in backend: {data}")


sg_0 = float(data['conductivity'])
es = float(data['e-static'])
ep_infty = float(data['e-infinity'])
tau_1 = float(data['tau'])


omg_0 = 2.0 * pi * 1e9
dlt_ep_1 = es - ep_infty
tau_1_nl = tau_1 * omg_0

def initialise_values(data):
    global sg_0,es,ep_infty,tau_1
    sg_0 = float(data['conductivity'])
    es = float(data['e-static'])
    ep_infty = float(data['e-infinity'])
    tau_1 = float(data['tau'])

# Define a function we need to calculate epsilon

def ep_cal_0(omg, omg_0, ep_0, ep_infty, dlt_ep_1, tau_1_nl, sg_0):
    ep_cal_0 = (complex(ep_infty, 0.0) + complex(dlt_ep_1, 0.0) / complex(1.0, tau_1_nl * omg / omg_0)) + (
                complex(sg_0, 0.0) / complex(0.0, omg * ep_0))
    return ep_cal_0


def norm(vector):
    norm = math.sqrt(vector[0] ** 2 + vector[1] ** 2 + vector[2] ** 2 + vector[3] ** 2)
    return norm


def produce_graph_values():
    with open("Debye/parameters.json", 'r') as file:
        data = json.load(file)
        print(f"producing values with data: {data}")
        initialise_values(data)
    for i in range(1, 6000):
        frequency[0] = i
        omg[0] = 2.0 * pi * frequency[0] * 1e8

        losst1 = sg_0 / omg[0] / ep_0 + omg[0] * tau_1 * dlt_ep_1 / (1 + (omg[0] * tau_1) ** 2)
        losst2 = ep_infty + dlt_ep_1 / (1 + (omg[0] * tau_1) ** 2)

        output_frequency[0] = frequency[0] * 1e8
        j = ep_cal_0(omg[0], omg_0, ep_0, ep_infty, dlt_ep_1, tau_1_nl, sg_0)
        output_permittivity[0] = j.real
        output_conductivity[0] = -ep_0 * omg[0] * j.imag
        output_loss_ratio[0] = losst1 / losst2

        database1.update(output_permittivity[0], output_conductivity[0], output_loss_ratio[0],output_frequency[0])
        #database1.delete(output_frequency[0])
        #database1.insert(output_frequency[0],output_permittivity[0], output_conductivity[0], output_loss_ratio[0])


def tissue_conductivity_value(tissue=str):
    if tissue:
        with open(f"Tissues_parameters/{tissue}_TissueParameter.txt", 'r') as file:
            value = float(file.readlines()[1].split(" ")[0])
    else:
            value = 1

    return value


def tissue_e_static_value(tissue=str):
    if tissue:
        with open(f"Tissues_parameters/{tissue}_TissueParameter.txt",
                  'r') as file:
            value = float(file.readlines()[1].split(" ")[1])
    else:
        value = 60

    return value


def tissue_e_infinity_value(tissue=str):
    if tissue:
        with open(f"Tissues_parameters/{tissue}_TissueParameter.txt",
                  'r') as file:
            value = float(file.readlines()[1].split(" ")[2])
    else:
        value = 21.43600845

    return value


def tissue_tau_value(tissue=str):
    if tissue:
        with open(f"Tissues_parameters/{tissue}_TissueParameter.txt",
                  'r') as file:
            value = float(file.readlines()[1].split(" ")[3])
    else:
        value = 2.73953464e-11

    return value
