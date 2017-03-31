import forest
import random
import operator

FOREST_SIZE = 250
MAX_GEN = 300
MAX_POPULATION = 20
MAX_LIFETIME = 5000

class FitnessTests(Enum):
	BIOMASS = 0
	LONGEVITY = 1

class MutableForest(Forest):
	def __init__(self, species=1):
		super().__init__(Forest(FOREST_SIZE,FOREST_SIZE, 0, 0))
		self.fitness=0
		self.species
	
	def __lt__(self, other):
		return self.fitness < other.fitness

	def mutateSpecies(self):
		if self.species == 1:
			self.spawn_rate_one = random.randit(0, 100)
		else:
			self.spawn_rate_one = random.randit(0, 100)
			self.spawn_rate_two = random.randit(0, 100)
			

class GA:
	def __init__(self, species=1, fitness=BIOMASS, pop=MAX_POPULATION):
		forests = [MutableForest(species) for i in range(pop)]
		self.fitness_test = fitness

	def fitnessBiomass(self):
		for i in range(len(self.forests)):
			biomass = 0
			for steps in range(MAX_LIFETIME):
				self.forests[i].step()
				biomass += self.forests[i].biomass()

			self.forests[i].fitness = biomass / MAX_LIFETIME

	def fitnessLongevity(self):
		for i in range(len(self.forests)):
			for steps in range(MAX_LIFETIME)
				self.forests[i].step()

				if(self.forests[i].is_dead()):
					break
				
				self.forests[i].fitness = steps

			

	def run(self):
		random.seed(None)
		
		with open('output.csv', 'w') as fout:

			for trials in range(MAX_GEN):
				if self.fitness_test == BIOMASS:
					self.fitnessBiomass()
				else 
					self.fitnessLongevity()
			
				self.forests.sort()

				for i in range(len(self.forests)-1):
					self.forests[i].mutateSpecies()
					fout.write(str(self.forests[i].fitness)+',')

				fout.write('\n')

		print self.forests[MAX_POPULATION-1].spawn_rate_one
		print self.forests[MAX_POPULATION-1].spawn_rate_two


def main():
	ga = GA()
	
	ga.run()

if __name__ == "__main__":
	main()
