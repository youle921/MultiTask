package momfo.metaheuristics.nsgaII;

import java.io.File;
import java.io.IOException;
import java.text.DecimalFormat;
import java.util.HashMap;

import momfo.core.Operator;
import momfo.core.Problem;
import momfo.core.ProblemSet;
import momfo.core.SolutionSet;
import momfo.encodings.solutionType.IntSolutionType;
import momfo.operators.crossover.CrossoverFactory;
import momfo.operators.mutation.MutationFactory;
import momfo.operators.selection.SelectionFactory;
import momfo.problems.ProblemSetFactory;
import momfo.problems.KnapsackSetFactory;
import momfo.problems.ProblemSetFactory;
import momfo.problems.knapsack.Knapsack;
import momfo.qualityIndicator.QualityIndicator;
import momfo.util.JMException;
import momfo.util.PseudoRandom;
import momfo.util.RandomGenerator;

public class NSGAII_main {
	public static void main(String args[]) throws IOException, JMException, ClassNotFoundException {
		ProblemSet problemSet; // The problem to solve
		NSGAII algorithm; // The algorithm to use
		Operator crossover; // Crossover operator
		Operator mutation; // Mutation operator
		Operator selection;

		HashMap parameters; // Operator parameters

		// int objective = 2;
		// Problem kp = KnapsackSetFactory.getProblem(args[0], Double.parseDouble(args[1]));
		problemSet = ProblemSetFactory.getProblem(args[0]);
		// problemSet = new ProblemSet();
		// problemSet.add(kp);
		// problemSet.setSolutionType(new IntSolutionType(problemSet));

		algorithm = new NSGAII(problemSet);

		String pf = "PF/" + problemSet.get(0).getHType() + ".pf";
		System.out.println(pf);

		algorithm.setInputParameter("populationSize", 100);
		algorithm.setInputParameter("maxEvaluations", 100 * 1000);

		parameters = new HashMap();
		parameters.put("probability", 0.9);
		parameters.put("distributionIndex", 20.0);
		crossover = CrossoverFactory.getCrossoverOperator("SBXCrossover", parameters);

		// Mutation operator
		parameters = new HashMap();
		parameters.put("probability", 1.0 / problemSet.getMaxDimension());
		parameters.put("distributionIndex", 20.0);
		mutation = MutationFactory.getMutationOperator("PolynomialMutation", parameters);

		// Selection Operator
		parameters = null;
		selection = SelectionFactory.getSelectionOperator("BinaryTournament2", parameters);

		// Add the operators to the algorithm
		algorithm.addOperator("crossover", crossover);
		algorithm.addOperator("mutation", mutation);
		algorithm.addOperator("selection", selection);

		System.out.println("RunID\t" + "IGD for " + problemSet.get(0).getName());
		DecimalFormat form = new DecimalFormat("#.####E0");
		QualityIndicator indicator = new QualityIndicator(problemSet.get(0), pf);

		int times = Integer.parseInt(args[2]);
		// double aveIGD = 0;
		// double[] aveIGDArray = new double[times];

		// String path = "result/knapsack_" + args[0] + "_" + args[1];
		String path = "result/CIHS_baseline";

		File init_var_file = new File("result/" + problemSet.get(0).getName() +
		"/init_pops/var");
		init_var_file.mkdirs();
		File final_var_file = new File("result/" + problemSet.get(0).getName() +
		"/final_pops/var");
		final_var_file.mkdirs();
		File init_obj_file = new File("result/" + problemSet.get(0).getName() +
		"/init_pops/obj");
		init_obj_file.mkdirs();
		File finalObjFile = new File(path + "/final_pops");
		finalObjFile.mkdirs();

		for (int i = 1; i <= times; i++) {

			RandomGenerator defaultGenerator_ = new RandomGenerator(i);
			PseudoRandom.setRandomGenerator(defaultGenerator_);

			algorithm.initialize();

			// algorithm.setPath(path, i);
			// algorithm.execute();
			SolutionSet population = algorithm.execute();
			// Ranking ranking = new Ranking(population);
			// population = ranking.getSubfront(0);
			double igd = indicator.getIGD(population);
			// aveIGD += igd;
			// aveIGDArray[i - 1] = igd;
			System.out.println(i + "\t" + form.format(igd));
			System.out.println(i);
		}

		// System.out.println();
		// System.out.println("Average IGD for " + problemSet.get(0).getName() + ": " +
		// form.format(aveIGD / times));

		// FileOutputStream fos_1 = new FileOutputStream("result/" +
		// problemSet.get(0).getName()+ "_IGD_v2.csv");
		// OutputStreamWriter osw_1 = new OutputStreamWriter(fos_1);
		// BufferedWriter bw_1 = new BufferedWriter(osw_1);

		// for(int t = 0; t<aveIGDArray.length;t++){
		// bw_1.write(String.valueOf(aveIGDArray[t]));
		// bw_1.newLine();
		// }
		// bw_1.close();

	}
}
