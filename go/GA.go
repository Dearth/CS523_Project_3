package main

import (
	"./forest"
	"flag"
)

func main() {

	fitPtr := flag.Int("fit", 1, "1 = Biomass fitness, 2 = Longevity fitness")
	mutPtr := flag.Int("mut", 1, "Number of species to mutate, max = 2")
	ffPtr := flag.Int("ff", 0, "Number of firefighters used")

	flag.Parse()

	forests := forest.NewForestGA(0, 0, 0)

	forests.Run(*fitPtr, *mutPtr, *ffPtr)

	return
}
