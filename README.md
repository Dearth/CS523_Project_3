# CS523_Project_3
1. Biomass vs longevity
   Over a range of p-values, for a given run, take the average biomass over every step, plotted against the longevity. Expect some maximum in the middle of biomass range.

   Q: How is this different from 3? Biomass(p_m)

2. GA - max p_m, convergence plot
   * Fitness functions
      1. f1(biomass) = average biomass / # cells
      2. f2(longevity) =  longevity
         where longevity = the # of steps until all cells are empty, capped at 5000

3. Fitness landscape for p_m vs longevity, p_m vs biomass
   
   Evaluate over interval.

4. Introduce 2nd species
   * What p values do the different species evolve?
     We would expect p1, p2 = p / 2
     p-value Distribution for single species, and for each of the 2 species (Show that they're different)
   * Covariance between the evolved growth rates of the 2 species

5a. # Fire fighters vs biomass, # fire fighters vs longevity

   For p_m, with 1 or 2 species?
   
5b. Phase transitions in the # of firefighters in either longevity or biomass?
   * Sharp transition, rate of change characterizes a phase transition, discontinuity


# Notes
Plots 1,2,3 are with a single species
Plots 1-4 without firefighters

Order of operations?
