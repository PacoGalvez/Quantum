import dwavebinarycsp
from dwave.system.samplers import DWaveSampler
from dwave.system.composites import EmbeddingComposite

sampler = EmbeddingComposite(DWaveSampler())

def scheduling(time, location, length, mandatory):
    if time: 
        # En horas de Oficina
        return (location and mandatory)
    else:
        # Fuera de horario
        return (not location and not length)

csp = dwavebinarycsp.ConstraintSatisfactionProblem(dwavebinarycsp.BINARY)
csp.add_constraint(scheduling, ['time', 'location', 'length', 'mandatory'])

bqm = dwavebinarycsp.stitch(csp)
print(bqm.linear)
print(bqm.quadratic)

response = sampler.sample(bqm, num_reads = 5000)
min_energy = next(response.data(['energy']))[0]

print(response)

total = 0
for sample, energy, occurences in response.data(['sample', 'energy', 'num_occurrences']):
    total = total + occurences
    # if energy == min_energy:
    time = 'business hours' if sample['time'] else 'evenings'
    location = 'office' if sample['location'] else 'home'
    length = 'short' if sample['length'] else 'long'
    mandatory = 'mandatory' if sample['mandatory'] else 'optional'
    print("{}: During {} at {}, you can schedule a {} meeting that is {}"
                .format(occurences, time, location, length, mandatory))