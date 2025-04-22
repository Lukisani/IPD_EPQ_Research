# Iterated Prisoner's Dilemma (IPD) - EPQ Research

Research Tool used for my EPQ project on the Iterated Prisoner's Dilemma

## Description
This repository contains the source code for my EPQ dissertation investigating strategy performance in the Iterated Prisoner’s Dilemma. It includes:

-  Custom implementations of adaptive Tit-for-Tat variants as well as variants of other strategies
  
-  Tournament simulations (baseline, noisy, and evolutionary)
  
-  Visualization tools for results analysis

## Author
Lukas Sanitra (Lukisani)

## Key Features
Three novel strategies:

-  AdaptiveTitForTat

-  AdaptiveTitForTat10

-  WindowedForgivenessTFT

Payoff customization: Supports standard/modified reward structures

Noise simulation: Tests robustness to stochastic errors (5–20%)

Evolutionary dynamics: Simulating natural selection over successive generations

## Credits
Classic strategy implementations (TitForTat, Alternator, etc.) follow behavioral specifications from the Axelrod tournament literature and were independently coded for this project. For reference implementations, see the [**Axelrod-Python**](https://github.com/Axelrod-Python/Axelrod) library.

## License  
This project is licensed under the MIT License - see [LICENSE.md](LICENSE.md) for details.  