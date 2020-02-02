package momfo.metaheuristics.momfea;

import java.io.File;
import java.io.IOException;
import java.util.HashMap;

import momfo.core.Algorithm;
import momfo.core.Operator;
import momfo.core.ProblemSet;
import momfo.core.Solution;
import momfo.core.SolutionSet;
import momfo.encodings.solutionType.IntSolutionType;
import momfo.operators.crossover.CrossoverFactory;
import momfo.operators.mutation.MutationFactory;
import momfo.operators.selection.SelectionFactory;
import momfo.problems.KnapsackSetFactory;
import momfo.problems.knapsack.Knapsack;
import momfo.util.JMException;
import momfo.util.PseudoRandom;
import momfo.util.RandomGenerator;
import momfo.util.comparators.LocationComparator;

public class MOMFEA_main_forKP {
	public static void main(String args[]) throws JMException, IOException, ClassNotFoundException {
		ProblemSet problemSet; // The problem to solve
		Algorithm algorithm; // The algorithm to use
		Operator crossover; // Crossover operator
		Operator mutation; // Mutation operator
		Operator selection;

		HashMap parameters; // Operator parameters

		problemSet = new ProblemSet();
		problemSet.add(new Knapsack(2));
		problemSet.add(KnapsackSetFactory.getProblem(args[0], Double.parseDouble(args[1])));
		problemSet.setSolutionType(new IntSolutionType(problemSet));

		algorithm = new MOMFEA(problemSet);

		algorithm.setInputParameter("populationSize",200);
		algorithm.setInputParameter("maxEvaluations",200 * 1000);
		algorithm.setInputParameter("rmp", 0.9);

		parameters = new HashMap();
		parameters.put("probability", 0.9);
		// parameters.put("distributionIndex", 20.0);
		crossover = CrossoverFactory.getCrossoverOperator("UniformCrossover", parameters);

		// Mutation operator
		parameters = new HashMap();
		parameters.put("probability", 1.0 / problemSet.getMaxDimension());
		// parameters.put("distributionIndex", 20.0);
		mutation = MutationFactory.getMutationOperator("BitFlipMutation", parameters);

		// Selection Operator
	    parameters = new HashMap() ;
	    parameters.put("comparator", new LocationComparator()) ;
	    selection = SelectionFactory.getSelectionOperator("BinaryTournament",
				parameters);

		// Add the operators to the algorithm
		algorithm.addOperator("crossover", crossover);
		algorithm.addOperator("mutation", mutation);
		algorithm.addOperator("selection", selection);

		int times = Integer.parseInt(args[2]);
		String pathT1 = "result/momfea/knapsack_" + args[0] + "_" + args[1] + "/base/final_pops";
		String pathT2 = "result/momfea/knapsack_" + args[0] + "_" + args[1] + "/" + args[0] + "/final_pops" ;

		File finalObjFileT1 = new File(pathT1);
		finalObjFileT1.mkdirs();
		File finalObjFileT2 = new File(pathT2);
		finalObjFileT2.mkdirs();

		for (int t = 1; t <= times; t++) {
			RandomGenerator defaultGenerator_ = new RandomGenerator(t);
			PseudoRandom.setRandomGenerator(defaultGenerator_);

			SolutionSet population = algorithm.execute();

			SolutionSet[] resPopulation = new SolutionSet[problemSet.size()];
			for (int i = 0; i < problemSet.size(); i++){
				resPopulation[i] = new SolutionSet();
			}

			for (int i = 0; i < population.size(); i++) {

				Solution sol = population.get(i);

				int pid = sol.getSkillFactor();
				int start = problemSet.get(pid).getStartObjPos();
				int end = problemSet.get(pid).getEndObjPos();

				Solution newSolution = new Solution(end - start + 1);

				for (int k = start; k <= end; k++){
					newSolution.setObjective(k - start, sol.getObjective(k));
				}

				resPopulation[pid].add(newSolution);
			}

			resPopulation[0].printFeasibleFUN(pathT1 + "/obj" + String.valueOf(t)+ ".dat");
			resPopulation[1].printFeasibleFUN(pathT2 + "/obj" + String.valueOf(t)+ ".dat");

			System.out.println(t);
		} // for

	} // main

} // momfea
