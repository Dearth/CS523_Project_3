package main

import (
	"./forest"
	"os"
	"fmt"
	"time"
	"flag"
)

func clearScreen() {
	for i := 0; i < 100; i++ {
		fmt.Println("\n")
	}
}

func main() {
	s1 := flag.Int("s1", 1, "Species 1 spawn rate")
	s2 := flag.Int("s2", 0, "Species 1 spawn rate")
	ff := flag.Int("ff", 0, "Number of fire fighters")

	flag.Parse()

	f := forest.NewForest(*s1, *s2, *ff)

	for i := 0; i < 5000; i++ {
		clearScreen()
		f.WriteForest(os.Stdout)
		f.Update()
		time.Sleep(100*time.Millisecond)
	}

}
