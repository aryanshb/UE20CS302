import pygad
import pygad.nn
import pygad.gann
import numpy

data_inputs = numpy.array([[1, 1], [1, 0], [0, 1], [0, 0]])
data_outputs = numpy.array([0, 1, 1, 0])

num_inputs = 2
num_classes = 2
num_solutions = 10
last_fitness = 0

GANN_instance = pygad.gann.GANN(
  num_solutions = num_solutions,
  num_neurons_input = num_inputs,
  num_neurons_hidden_layers = [10],
  num_neurons_output = num_classes,
  hidden_activations = ["relu"],
  output_activation = "softmax"
)

def fitness_function (solution, sol_idx):
  global GANN_instance, data_inputs, data_outputs

  predictions = pygad.nn.predict(
    last_layer = GANN_instance.population_networks[sol_idx],
    data_inputs = data_inputs
  )
  correct_predictions = numpy.where(predictions == data_outputs)[0].size
  solution_fitness = (correct_predictions / data_outputs.size) * 100

  return solution_fitness

def generation_callback(ga_instance):
  global GANN_instance, last_fitness

  population_matrices = pygad.gann.population_as_matrices(
    population_networks = GANN_instance.population_networks,
    population_vectors = ga_instance.population
  )

  GANN_instance.update_population_trained_weights(
    population_trained_weights = population_matrices
  )

  print("Generation = {generation}".format(generation = ga_instance.generations_completed))
  print("   Fitness = {fitness}".format(fitness = ga_instance.best_solution()[1]))
  print("    Change = {change}".format(change = ga_instance.best_solution()[1] - last_fitness))
  print()

  last_fitness = ga_instance.best_solution()[1].copy()

population_vectors = pygad.gann.population_as_vectors(
  population_networks = GANN_instance.population_networks
)
initial_population = population_vectors.copy()

num_parents_mating = 4
num_generations = 50
mutation_percent_genes = 10
parent_selection_type = "sss"
crossover_type = "single_point"
mutation_type = "random"
keep_parents = 1
init_range_low = -2
init_range_high = 2

ga_instance = pygad.GA(
  num_generations = num_generations,
  num_parents_mating = num_parents_mating,
  initial_population = initial_population,
  fitness_func = fitness_function,
  mutation_percent_genes = mutation_percent_genes,
  init_range_low = init_range_low,
  init_range_high = init_range_high,
  parent_selection_type = parent_selection_type,
  crossover_type = crossover_type,
  mutation_type = mutation_type,
  keep_parents = keep_parents,
  on_generation = generation_callback
)

ga_instance.run()
ga_instance.plot_fitness("Generation VS Fitness")
solution, solution_fitness, solution_idx = ga_instance.best_solution()

print()
print(f"Parameters of the best solution: {solution}")
print()
print(f"Fitness value of the best solution: {solution_fitness}")
print(f"        Index of the best solution: {solution_idx}")
print()

if ga_instance.best_solution_generation != -1:
  print(f"Best fitness value reached after {ga_instance.best_solution_generation} generations")

predictions = pygad.nn.predict(
  last_layer = GANN_instance.population_networks[solution_idx],
  data_inputs = data_inputs
)

print()
print(f"Predictions of the trained network: {predictions}")
print()

num_wrong = numpy.where(predictions != data_outputs)[0].size
num_correct = data_outputs.size - num_wrong
accuracy = (num_correct / data_outputs.size) * 100

print(f"Number of correct classifications: {num_correct}")
print(f"  Number of wrong classifications: {num_wrong}")
print(f"          Classification accuracy: {accuracy}")