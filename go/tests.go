package main

import (
	"./forest"
)

func main() {

//	p_test := forest.NewForestGA(0, 0, 0)
	ff_test := forest.NewForestGA(57, 0, 0)

//	p_test.RunProbTest()

	ff_test.RunFFTest()

}
