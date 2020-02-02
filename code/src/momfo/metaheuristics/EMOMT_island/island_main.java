package momfo.metaheuristics.EMOMT_island;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.OutputStreamWriter;
import java.text.DecimalFormat;
import java.util.HashMap;

import momfo.core.Operator;
import momfo.core.ProblemSet;
import momfo.core.SolutionSet;
import momfo.encodings.solutionType.IntSolutionType;
import momfo.operators.crossover.CrossoverFactory;
import momfo.operators.mutation.MutationFactory;
import momfo.operators.selection.SelectionFactory;
import momfo.problems.KnapsackSetFactory;
import momfo.problems.ProblemSetFactory;
import momfo.problems.knapsack.Knapsack;
import momfo.qualityIndicator.QualityIndicator;
import momfo.util.JMException;
import momfo.util.PseudoRandom;
import momfo.util.RandomGenerator;

public class island_main {
	public static void main(String args[]) throws IOException, JMException, ClassNotFoundException {

		// args[0]: problems, args[1]: parameter fot KP, 
		// args[2]: number of trials, args[3]: interval, args[4]: size

		NSGAII_for_island algorithm1; // The algorithm to use
		NSGAII_for_island algorithm2; // The algorithm to use

		// ProblemSet problemSets = ProblemSetFactory.getProblem(args[0]);

		ProblemSet problem1 = new ProblemSet();
		problem1.setSolutionType(new IntSolutionType(problem1));
		problem1.add(new Knapsack(2));
		algorithm1 = algorithm_setting(problem1, Integer.parseInt(args[3]), Integer.parseInt(args[4]));

		// String pf1 = "PF/" + problem1.get(0).getHType() + ".pf";

		ProblemSet problem2 = new ProblemSet();
		problem2.setSolutionType(new IntSolutionType(problem2));
		problem2.add(KnapsackSetFactory.getProblem(args[0], Double.parseDouble(args[1]) ) );
		algorithm2 = algorithm_setting(problem2, Integer.parseInt(args[3]), Integer.parseInt(args[4]));
		// String pf2 = "PF/" + problem2.get(0).getHType() + ".pf";

		// System.out.println("RunID\t" + "IGD for " + problemSets.get(0).getName() + "\t" + "IGD for "
		// 		+ problemSets.get(1).getName());
		// DecimalFormat form = new DecimalFormat("#.####E0");
		// QualityIndicator indicator1 = new QualityIndicator(problemSets.get(0), pf1);
		// QualityIndicator indicator2 = new QualityIndicator(problemSets.get(1), pf2);

		int times = Integer.parseInt(args[2]);
		String pathT1 = "result/NSGA-II-island_interval" + args[3] + "_size" + args[4] + "/knapsack_" + args[0] + "_" + args[1] + "/base/final_pops";
		String pathT2 = "result/NSGA-II-island_interval" + args[3] + "_size" + args[4] + "/knapsack_" + args[0] + "_" + args[1] + "/" + args[0] + "/final_pops" ;

		File finalObjFileT1 = new File(pathT1);
		finalObjFileT1.mkdirs();
		File finalObjFileT2 = new File(pathT2);
		finalObjFileT2.mkdirs();
		// double[] aveIGD = { 0, 0 };
		// double[][] IGDArray = new double[2][times];

		// File init_var_file = new File("result/" + problemSet.get(0).getName() +
		// "/init_pops/var");
		// init_var_file.mkdirs();
		// File final_var_file = new File("result/" + problemSet.get(0).getName() +
		// "/final_pops/var");
		// final_var_file.mkdirs();
		// File init_obj_file = new File("result/" + problemSet.get(0).getName() +
		// "/init_pops/obj");
		// init_obj_file.mkdirs();
		// File final_obj_file = new File("result/" + problemSet.get(0).getName() +
		// "/final_pops/obj");
		// final_obj_file.mkdirs();

		SolutionSet migrated_to1;
		SolutionSet migrated_to2;

		boolean criterion1;
		boolean criterion2;

		for (int i = 1; i <= times; i++) {

			RandomGenerator defaultGenerator_ = new RandomGenerator(i);
			PseudoRandom.setRandomGenerator(defaultGenerator_);

			algorithm1.initialize_island();
			algorithm2.initialize_island();

			criterion1 = algorithm1.get_criterion();
			criterion2 = algorithm2.get_criterion();

			while (criterion1 == false & criterion2 == false) {

				algorithm1.execute();
				algorithm2.execute();
				migrated_to2 = algorithm1.get_migrate_pop();
				migrated_to1 = algorithm2.get_migrate_pop();
				algorithm1.migration_gen(migrated_to1);
				algorithm2.migration_gen(migrated_to2);

				criterion1 = algorithm1.get_criterion();
				criterion2 = algorithm2.get_criterion();
			}

			// double igd1 = indicator1.getIGD(algorithm1.get_front());
			// aveIGD[0] += igd1;
			// IGDArray[0][i - 1] = igd1;

			// double igd2 = indicator2.getIGD(algorithm2.get_front());
			// aveIGD[1] += igd2;
			// IGDArray[1][i - 1] = igd2;

			// System.out.println(i + "\t" + form.format(igd1) + "\t" + form.format(igd2));

			SolutionSet[] finalPop = new SolutionSet[2];

			finalPop[0] = algorithm1.getAllSolution();
			finalPop[1] = algorithm2.getAllSolution();

			finalPop[0].printFeasibleFUN(pathT1 + "/obj" + String.valueOf(i)+ ".dat");
			finalPop[1].printFeasibleFUN(pathT2 + "/obj" + String.valueOf(i)+ ".dat");

			System.out.println(i);
		}

		System.out.println();
		// System.out.println("Average IGD for " + problemSets.get(0).getName() + ": " + form.format(aveIGD[0] / times));
		// System.out.println("Average IGD for " + problemSets.get(1).getName() + ": " + form.format(aveIGD[1] / times));

		// File result_dir = new File("result/island/100trial/" + args[1] + "-" + args[2] + "/");
		// result_dir.mkdirs();

		// FileOutputStream fos_1 = new FileOutputStream(
		// 		"result/island/100trial/" + args[1] + "-" + args[2] + "/" + args[0] + "_IGD.csv");
		// OutputStreamWriter osw_1 = new OutputStreamWriter(fos_1);
		// BufferedWriter bw_1 = new BufferedWriter(osw_1);

		// for (int t = 0; t < IGDArray[0].length; t++) {
		// 	bw_1.write(String.valueOf(IGDArray[0][t]) + "," + String.valueOf(IGDArray[1][t]));
		// 	bw_1.newLine();
		// }
		// bw_1.close();

	}

	public static NSGAII_for_island algorithm_setting(ProblemSet problemSet, int interval, int size)
			throws JMException {

		NSGAII_for_island algorithm = new NSGAII_for_island(problemSet);

		algorithm.setInputParameter("populationSize", 100);
		algorithm.setInputParameter("maxEvaluations", 100 * 1000);

		algorithm.setInputParameter("migration_interval", interval);
		algorithm.setInputParameter("migration_size", size);

		HashMap parameters; // Operator parameters
		Operator crossover; // Crossover operator
		Operator mutation; // Mutation operator
		Operator selection;

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
		parameters = null;
		selection = SelectionFactory.getSelectionOperator("BinaryTournament", parameters);

		// Add the operators to the algorithm
		algorithm.addOperator("crossover", crossover);
		algorithm.addOperator("mutation", mutation);
		algorithm.addOperator("selection", selection);

		return algorithm;

	}

}