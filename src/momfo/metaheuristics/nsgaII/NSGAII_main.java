package momfo.metaheuristics.nsgaII;

import java.io.BufferedWriter;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.OutputStreamWriter;
import java.text.DecimalFormat;
import java.util.HashMap;

import momfo.core.Algorithm;
import momfo.core.Operator;
import momfo.core.ProblemSet;
import momfo.core.SolutionSet;
import momfo.operators.crossover.CrossoverFactory;
import momfo.operators.mutation.MutationFactory;
import momfo.operators.selection.SelectionFactory;
import momfo.problems.ProblemSetFactory;
import momfo.qualityIndicator.QualityIndicator;
import momfo.util.JMException;

public class NSGAII_main {
	public static void main(String args[]) throws IOException, JMException, ClassNotFoundException {
		ProblemSet problemSet; // The problem to solve
		Algorithm algorithm; // The algorithm to use
		Operator crossover; // Crossover operator
		Operator mutation; // Mutation operator
		Operator selection;


		HashMap parameters; // Operator parameters

		ProblemSet problemSets = ProblemSetFactory.getProblem(args[0]);

		for(int problem_no = 0; problem_no < 2; problem_no++){

			problemSet = new ProblemSet();
			problemSet.add(problemSets.get(problem_no));

/* 			problemSet.setUnifiedLowerLimit(-50);
			problemSet.setUnifiedUpperLimit(50); */

			algorithm = new NSGAII(problemSet);


			String pf = "PF/" + problemSet.get(0).getHType() + ".pf";
		//	System.out.println(pf);

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
			parameters = null ;
			selection = SelectionFactory.getSelectionOperator("BinaryTournament", parameters) ;


			// Add the operators to the algorithm
			algorithm.addOperator("crossover", crossover);
			algorithm.addOperator("mutation", mutation);
			algorithm.addOperator("selection", selection);

			System.out.println("RunID\t" + "IGD for " + problemSet.get(0).getName());
			DecimalFormat form = new DecimalFormat("#.####E0");
			QualityIndicator indicator = new QualityIndicator(problemSet.get(0), pf);

			int times = 30;
			double aveIGD = 0;
			double[] aveIGDArray = new double[times];
			for (int i = 1; i <= times; i++) {
				SolutionSet population = algorithm.execute();
/*				Ranking ranking = new Ranking(population);
				population = ranking.getSubfront(0);*/
				double igd = indicator.getIGD(population);
				aveIGD += igd;
				aveIGDArray[i - 1] = igd;
				System.out.println(i + "\t" + form.format(igd));;
			}

			System.out.println();
			System.out.println("Average IGD for " + problemSet.get(0).getName() + ": " + form.format(aveIGD / times));

			FileOutputStream fos_1 = new FileOutputStream("result/" + problemSet.get(0).getName()+ "_IGD.csv");
			OutputStreamWriter osw_1 = new OutputStreamWriter(fos_1);
			BufferedWriter bw_1 = new BufferedWriter(osw_1);

			for(int t = 0; t<aveIGDArray.length;t++){
				bw_1.write(String.valueOf(aveIGDArray[t]));
				bw_1.write(",");
				bw_1.newLine();
			}
			bw_1.close();

		}

	}
}
