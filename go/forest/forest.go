package forest

import (
	"sync"
	"io"
	"math/rand"
	"time"
	"fmt"
	"sort"
	"os"
	"bufio"
	"runtime"
)

var FITNESS int
var MUTATE int
var FIRE_FIGHTERS int

var MAX_GENERATIONS int
var MAX_CA_LIFETIME int

const CA_SIZE = 250
const FOREST_SIZE = 20

const (
	DEAD = iota
	ALIVE_ONE
	ALIVE_TWO
	FIRE
)

type Forest struct {
	trees_ [CA_SIZE][CA_SIZE]int
	spawn_rate_one_ int
	spawn_rate_two_ int
	lightning_rate_ int
	fire_fighters_ int
	random_ *rand.Rand
}


func NewForest(spawn, spawn2, ff int) Forest {
	return Forest{spawn_rate_one_: spawn, spawn_rate_two_: spawn2, fire_fighters_: ff, lightning_rate_: 1, random_: rand.New(rand.NewSource(time.Now().UTC().UnixNano()))}
}

func (f *Forest) UpdateCell(x, y int, next_step *[CA_SIZE][CA_SIZE]int) {
	var x_plus, x_minus, y_plus, y_minus int

	t := f.trees_[x][y];

	switch t {
		case FIRE:
			if f.random_.Intn(100) < 50 && f.fire_fighters_ != FIRE_FIGHTERS {
				next_step[x][y] = ALIVE_ONE
				f.fire_fighters_++
			} else {
				next_step[x][y] = DEAD
			}
			break
		case DEAD:
			spawn := f.random_.Intn(100)
			if spawn < f.spawn_rate_one_ {
				next_step[x][y] = ALIVE_ONE
			} else if spawn < (f.spawn_rate_one_ + f.spawn_rate_two_) {
				next_step[x][y] = ALIVE_TWO
			} else {
				next_step[x][y] = DEAD
			}
			break
		case ALIVE_ONE:
			if f.random_.Intn(1000) == f.lightning_rate_ {
				next_step[x][y] = FIRE
			} else {
				if x == (CA_SIZE-1) {
					x_plus = 0
				} else {
					x_plus = x + 1
				}

				if x == 0 {
					x_minus = CA_SIZE - 1
				} else {
					x_minus = x - 1
				}

				if y == (CA_SIZE-1) {
					y_plus = 0
				} else {
					y_plus = y + 1
				}

				if y == 0 {
					y_minus = CA_SIZE - 1
				} else {
					y_minus = y - 1
				}

				switch {
					case f.trees_[x_plus][y_plus] == FIRE:
					case f.trees_[x_plus][y] == FIRE:
					case f.trees_[x_plus][y_minus] == FIRE:
					case f.trees_[x][y_plus] == FIRE:
					case f.trees_[x][y_minus] == FIRE:
					case f.trees_[x_minus][y_plus] == FIRE:
					case f.trees_[x_minus][y] == FIRE:
					case f.trees_[x_minus][y_minus] == FIRE:
						next_step[x][y] = FIRE
						break
					default:
						next_step[x][y] = ALIVE_ONE
				}
			}
			break
		case ALIVE_TWO:
			if f.random_.Intn(1000) == f.lightning_rate_ {
				next_step[x][y] = FIRE
			} else {
				if x == 0 {
					x_minus = CA_SIZE - 1
				} else {
					x_minus = x - 1
				}

				if y == (CA_SIZE-1) {
					y_plus = 0
				} else {
					y_plus = y + 1
				}

				if y == 0 {
					y_minus = CA_SIZE - 1
				} else {
					y_minus = y - 1
				}

				switch {
					case f.trees_[x_plus][y_plus] == FIRE:
					case f.trees_[x_plus][y] == FIRE:
					case f.trees_[x_plus][y_minus] == FIRE:
					case f.trees_[x][y_plus] == FIRE:
					case f.trees_[x][y_minus] == FIRE:
					case f.trees_[x_minus][y_plus] == FIRE:
					case f.trees_[x_minus][y] == FIRE:
					case f.trees_[x_minus][y_minus] == FIRE:
						next_step[x][y] = FIRE
						break
					default:
						next_step[x][y] = ALIVE_TWO
				}
			}
			break
		default:
			fmt.Println("Unknown state:", t)
	}
}

func (f *Forest) Update() {
	var next_step [CA_SIZE][CA_SIZE]int
	f.fire_fighters_ = 0
	for x := 0; x < CA_SIZE; x++ {
		for y := 0; y < CA_SIZE; y++ {
			f.UpdateCell(x, y, &next_step)
		}
	}

	f.trees_ = next_step
}

func (f *Forest) WriteForest(w io.Writer) (n int, err error) {
	var b int
	var e error

	n = 0
	err = nil

	for x := 0; x < CA_SIZE; x++ {
		for y := 0; y < CA_SIZE; y++ {
			switch {
				case f.trees_[x][y] == DEAD:
					b, e = io.WriteString(w, " ")
					break
				case f.trees_[x][y] == ALIVE_ONE:
					b, e = io.WriteString(w, "T")
					break
				case f.trees_[x][y] == ALIVE_TWO:
					b, e = io.WriteString(w, "Y")
					break
				case f.trees_[x][y] == FIRE:
					b, e = io.WriteString(w, "F")
					break
				default:
					fmt.Println("Unknown state:", f.trees_[x][y])
			}
			n += b

			if e != nil {
				err = e
				return
			}
		}
	}
	return
}

func (f *Forest) Biomass() (bm float64) {
	bm = 0

	for x := 0; x < CA_SIZE; x++ {
		for y := 0; y < CA_SIZE; y++ {
			if f.trees_[x][y] == ALIVE_ONE || f.trees_[x][y] == ALIVE_TWO {
				bm++
			}
		}
	}

	bm /= (CA_SIZE*CA_SIZE)

	return
}


func (f *Forest) AllDead() bool {

	for x := 0; x < CA_SIZE; x++ {
		for y := 0; y < CA_SIZE; y++ {
			if f.trees_[x][y] == ALIVE_ONE || f.trees_[x][y] == ALIVE_TWO {
				return false
			}
		}
	}

	return true
}

type ByFitness []MutatingForest

func (a ByFitness) Len() int {
	return len(a)
}

func (a ByFitness) Swap(i, j int) {
	a[i], a[j] = a[j], a[i]
}

func (a ByFitness) Less(i, j int) bool {
	return a[i].fitness_ < a[j].fitness_
}

type MutatingForest struct {
	forest_ Forest
	fitness_ float64
	rand_ *rand.Rand
}

func NewMutForest(spawn, spawn2, ff int) (mf MutatingForest) {
	mf.forest_ = NewForest(spawn, spawn2, ff)
	mf.rand_ = rand.New(rand.NewSource(time.Now().UTC().UnixNano()))

	return
}

func (m *MutatingForest) MutateSingleSpecies() {
	m.forest_.spawn_rate_one_ = m.rand_.Intn(100)
}

func (m *MutatingForest) MutateTwoSpecies() {
	m.forest_.spawn_rate_one_ = m.rand_.Intn(100)
	m.forest_.spawn_rate_two_ = m.rand_.Intn(100)
}

type ForestGA struct {
	forests_ []MutatingForest
}

func NewForestGA(spawn, spawn2, ff int) ForestGA {
	var g ForestGA
	g.forests_ = make([]MutatingForest, FOREST_SIZE)

	for i := 0; i < FOREST_SIZE; i++ {
		g.forests_[i] = NewMutForest(spawn, spawn2, ff)
	}

	return g
}

func (f *ForestGA) FitnessBiomass() {
	var wg sync.WaitGroup

	wg.Add(FOREST_SIZE)

	for i := 0; i < FOREST_SIZE; i++ {
		go func(mf *MutatingForest) {
			runtime.LockOSThread()
			defer wg.Done()
			var bm float64
			bm = 0

			for steps := 0; steps < MAX_CA_LIFETIME; steps++ {
				bm += mf.forest_.Biomass()
				mf.forest_.Update()
			}

			mf.fitness_ = bm / float64(MAX_CA_LIFETIME)

		} (&f.forests_[i])

	}

	wg.Wait()
}

func (f *ForestGA) FitnessLongevity() {
	var wg sync.WaitGroup

	wg.Add(FOREST_SIZE)

	for i:= 0; i < FOREST_SIZE; i++ {
		go func(mf *MutatingForest) {
			runtime.LockOSThread()

			defer wg.Done()

			for steps := 0; steps < MAX_CA_LIFETIME; steps++ {
				mf.forest_.Update()
				if mf.forest_.AllDead() {
					mf.fitness_ = float64(steps)
					return
				}
			}

			mf.fitness_ = float64(MAX_CA_LIFETIME)
		} (&(f.forests_[i]))
	}

	wg.Wait()

}

func (f *ForestGA) Run(fit, mut, ff int) {
	FITNESS = fit
	MUTATE = mut
	FIRE_FIGHTERS = ff

	MAX_GENERATIONS = 100
	MAX_CA_LIFETIME = 5000

	fout, err := os.Create("output.csv")
	if err != nil {
		panic(err)
	}
	defer fout.Close()
	w := bufio.NewWriter(fout)

	for steps := 0; steps < MAX_GENERATIONS; steps++ {
		if FITNESS == 1 {
			f.FitnessBiomass()
		} else {
			f.FitnessLongevity()
		}

		sort.Sort(ByFitness(f.forests_))

		for i := 0; i < FOREST_SIZE-20; i++ {
			if MUTATE == 1 {
				f.forests_[i].MutateSingleSpecies()
			} else {
				f.forests_[i].MutateTwoSpecies()
			}
		}

		for i := 0; i < FOREST_SIZE; i++ {
			_, err = fmt.Fprintf(w, "%f,", f.forests_[i].fitness_)
			if err != nil {
				panic(err)
			}
		}

		fmt.Fprintf(w, "\n")
		err = w.Flush()
		if err != nil {
			panic(err)
		}
	}

	for i := FOREST_SIZE-1 ; i > 20; i-- {
		fmt.Println(f.forests_[i].fitness_)
	}
}

func (f *ForestGA) RunProbTest() {
	FITNESS = 1
	MUTATE = 1
	FIRE_FIGHTERS = 0

	MAX_GENERATIONS = 100
	MAX_CA_LIFETIME = 5000

	fbio, err := os.Create("prob_biomass_fitness")
	if err != nil {
		panic(err)
	}
	defer fbio.Close()
	fbw := bufio.NewWriter(fbio)

	flong, err := os.Create("prob_longevity_fitness")
	if err != nil {
		panic(err)
	}
	defer flong.Close()
	flw := bufio.NewWriter(flong)

	for prob := 0; prob <= 100; prob += 5 {

		for i := 0; i < FOREST_SIZE; i++ {
			f.forests_[i].forest_.spawn_rate_one_ = prob
		}

		f.FitnessBiomass()

		for i := 0; i < FOREST_SIZE; i++ {
			_, err = fmt.Fprintf(fbw, "%f,", f.forests_[i].fitness_)
			if err != nil {
				panic(err)
			}
		}

		fmt.Fprintf(fbw, "\n")
		err = fbw.Flush()
		if err != nil {
			panic(err)
		}

		f.FitnessLongevity()

		for i := 0; i < FOREST_SIZE; i++ {
			_, err = fmt.Fprintf(flw, "%f,", f.forests_[i].fitness_)
			if err != nil {
				panic(err)
			}
		}

		fmt.Fprintf(flw, "\n")
		err = flw.Flush()
		if err != nil {
			panic(err)
		}
	}
}

func (f *ForestGA) RunFFTest() {
	FITNESS = 1
	MUTATE = 1
	FIRE_FIGHTERS = 0

	MAX_GENERATIONS = 100
	MAX_CA_LIFETIME = 5000

	fbio, err := os.Create("ff_biomass_fitness")
	if err != nil {
		panic(err)
	}
	defer fbio.Close()
	fbw := bufio.NewWriter(fbio)

	flong, err := os.Create("ff_longevity_fitness")
	if err != nil {
		panic(err)
	}
	defer flong.Close()
	flw := bufio.NewWriter(flong)

	for ff := 0; ff <= 1000; ff += 50 {

		for i := 0; i < FOREST_SIZE; i++ {
			f.forests_[i].forest_.fire_fighters_ = ff
		}

		f.FitnessBiomass()

		for i := 0; i < FOREST_SIZE; i++ {
			_, err = fmt.Fprintf(fbw, "%f,", f.forests_[i].fitness_)
			if err != nil {
				panic(err)
			}
		}

		fmt.Fprintf(fbw, "\n")
		err = fbw.Flush()
		if err != nil {
			panic(err)
		}

		f.FitnessLongevity()

		for i := 0; i < FOREST_SIZE; i++ {
			_, err = fmt.Fprintf(flw, "%f,", f.forests_[i].fitness_)
			if err != nil {
				panic(err)
			}
		}

		fmt.Fprintf(flw, "\n")
		err = flw.Flush()
		if err != nil {
			panic(err)
		}
	}
}










































