package main

import (
	"./forest"
)

func main() {
	forests := forest.NewForestGA()

	forests.Run()

	return
}
