package momfo.metaheuristics.momfea;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.OutputStreamWriter;
import java.text.DecimalFormat;
import java.util.HashMap;

import momfo.core.Algorithm;
import momfo.core.Operator;
import momfo.core.ProblemSet;
import momfo.core.Solution;
import momfo.core.SolutionSet;
import momfo.operators.crossover.CrossoverFactory;
import momfo.operators.mutation.MutationFactory;
import momfo.operators.selection.SelectionFactory;
import momfo.problems.ProblemSetFactory;
import momfo.qualityIndicator.QualityIndicator;
import momfo.util.DirectoryMaker;
import momfo.util.JMException;
import momfo.util.PseudoRandom;
import momfo.util.RandomGenerator;
import momfo.util.comparators.LocationComparator;

public class MOMFEA_main {
	public static void main(String args[]) throws JMException, IOException, ClassNotFoundException {
		ProblemSet problemSet; // The problem to solve
		Algorithm algorithm; // The algorithm to use
		Operator crossover; // Crossover operator
		Operator mutation; // Mutation operator
		Operator selection;

		HashMap parameters; // Operator parameters
		int Seed = 1;



		//PseudoRandom.setRandomGenerator(new );
		problemSet = ProblemSetFactory.getProblem(args[0]);
		String pf1 = "PF/" + problemSet.get(0).getHType() + ".pf";
		String pf2 = "PF/" + problemSet.get(1).getHType() + ".pf";
		String pf3 = "sf";
		algorithm = new MOMFEA(problemSet);

		if(args[0].contains("3")){
			pf3 = "PF/" + problemSet.get(2).getHType() + ".pf";
			algorithm.setInputParameter("populationSize",300);
		} else {
			algorithm.setInputParameter("populationSize",200);
		}

		System.out.println("test");
//		algorithm.setInputParameter("maxEvaluations",6 * 1000);
		algorithm.setInputParameter("maxEvaluations",200 * 1000);

		algorithm.setInputParameter("rmp", Double.valueOf(args[1]));

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
	    parameters = new HashMap() ;
	    parameters.put("comparator", new LocationComparator()) ;
	    selection = SelectionFactory.getSelectionOperator("BinaryTournament",
				parameters);


		// Add the operators to the algorithm
		algorithm.addOperator("crossover", crossover);
		algorithm.addOperator("mutation", mutation);
		algorithm.addOperator("selection", selection);

		String name1 = problemSet.get(0).getName();
		String name2 = problemSet.get(1).getName();
		String name3 ="";

		if(args[0].contains("3")){
			name3 =  problemSet.get(2).getName();
		}
		problemSet.get(1).getName();

		DecimalFormat form = new DecimalFormat("#.####E0");
		if(args[0].contains("3")){
			System.out.println("RunID\t" + "IGD for " + name1 + "\t" + "IGD for " + name2+ "\t" + "IGD for " + name3);
		} else {
			System.out.println("RunID\t" + "IGD for " + name1 + "\t" + "IGD for " + name2);
		}
		int times = 30;
		double[] ave1Array = new double[times];
		double[] ave2Array = new double[times];
		double[] ave3Array = new double[times];

		double ave1 = 0;
		double ave2 = 0;
		double ave3 = 0;
		DirectoryMaker.Make("result/rmp"+ args[1]+"/" + args[0]+"/Task1/FinalFUN");
		DirectoryMaker.Make("result/rmp"+ args[1]+"/" + args[0]+"/Task2/FinalFUN");
		DirectoryMaker.Make("result/rmp"+ args[1]+"/" + args[0]+"/Task1/IGDHistory");
		DirectoryMaker.Make("result/rmp"+ args[1]+"/" + args[0]+"/Task2/IGDHistory");
		DirectoryMaker.Make("result/rmp"+ args[1]+"/" + args[0]+"/Task1/InverseTaskFun");
		DirectoryMaker.Make("result/rmp"+ args[1]+"/" + args[0]+"/Task2/InverseTaskFun");

		if(args[0].contains("3")){
			DirectoryMaker.Make("result/rmp"+ args[1]+"/" + args[0]+"/Task3/IGDHistory");
			DirectoryMaker.Make("result/rmp"+ args[1]+"/" + args[0]+"/Task3/FinalFUN");
			DirectoryMaker.Make("result/rmp"+ args[1]+"/" + args[0]+"/Task3/InverseTaskFun");

		}

		for (int t = 1; t <= times; t++) {
			RandomGenerator defaultGenerator_ = new RandomGenerator(Seed + t);
			PseudoRandom.setRandomGenerator(defaultGenerator_);

			SolutionSet population = algorithm.execute();

			SolutionSet Task1Pop = new SolutionSet();
			SolutionSet Task2Pop = new SolutionSet();

			for(int i =0;i<population.size();i++) {
				if(population.get(i).getSkillFactor() == 0) {
					Solution sol = new Solution(population.get(i));
					problemSet.get(1).evaluate(sol);
					int start = problemSet.get(1).getStartObjPos();
					int end = problemSet.get(1).getEndObjPos();
					Solution newsol = new Solution(end - start + 1);
					for (int k = start; k <= end; k++)
						newsol.setObjective(k - start, sol.getObjective(k));
					Task1Pop.add(newsol);


				} else if(population.get(i).getSkillFactor() == 1) {
					Solution sol = new Solution(population.get(i));
					problemSet.get(0).evaluate(sol);
					int start = problemSet.get(0).getStartObjPos();
					int end = problemSet.get(0).getEndObjPos();
					Solution newsol = new Solution(end - start + 1);
					for (int k = start; k <= end; k++)
						newsol.setObjective(k - start, sol.getObjective(k));

					Task2Pop.add(newsol);
				} else {
					throw new JMException("null");
				}
			}


//			自身のタスクの個体を相手タスクで評価した時の目的関数値が入る．
//			つまり，Task1/InverseTaskFun　にはTask1で得られた個体群をTask2で評価した時に得られる目的関数値が入力される．
			Task1Pop.printFeasibleFUN("result/rmp" +args[1] +"/"+ args[0]+"/Task1/InverseTaskFun/IGD"+String.valueOf(t)+".dat");
			Task2Pop.printFeasibleFUN("result/rmp" +args[1] +"/"+ args[0]+"/Task2/InverseTaskFun/IGD"+String.valueOf(t)+".dat");



			double[][] igdvalue = algorithm.getIGDValue();

			FileOutputStream fos_1 = new FileOutputStream("result/rmp" +args[1] +"/"+ args[0]+"/Task1/IGDHistory/IGD"+String.valueOf(t)+".dat");
			OutputStreamWriter osw_1 = new OutputStreamWriter(fos_1);
			BufferedWriter bw_1 = new BufferedWriter(osw_1);
			for(int gen = 0; gen<igdvalue[0].length;gen++){
				bw_1.write(String.valueOf(gen)+"	"+String.valueOf(igdvalue[0][gen]));
				bw_1.newLine();
			}
			bw_1.close();

			FileOutputStream fos_2 = new FileOutputStream("result/rmp" +args[1] +"/"+ args[0]+"/Task2/IGDHistory/IGD"+String.valueOf(t)+".dat");
			OutputStreamWriter osw_2 = new OutputStreamWriter(fos_2);
			BufferedWriter bw_2 = new BufferedWriter(osw_2);
			for(int gen = 0; gen<igdvalue[1].length;gen++){
				bw_2.write(String.valueOf(gen)+"	"+String.valueOf(igdvalue[1][gen]));
				bw_2.newLine();
			}
			bw_2.close();

			if(args[0].contains("3")){
				FileOutputStream fos_3 = new FileOutputStream("result/rmp" +args[1] +"/"+ args[0]+"/Task3/IGDHistory/IGD"+String.valueOf(t)+".dat");
				OutputStreamWriter osw_3 = new OutputStreamWriter(fos_3);
				BufferedWriter bw_3 = new BufferedWriter(osw_3);
				for(int gen = 0; gen<igdvalue[1].length;gen++){
					bw_3.write(String.valueOf(gen)+"	"+String.valueOf(igdvalue[1][gen]));
					bw_3.newLine();
				}
				bw_3.close();
			}



			SolutionSet[] resPopulation = new SolutionSet[problemSet.size()];
			for (int i = 0; i < problemSet.size(); i++)
				resPopulation[i] = new SolutionSet();

			for (int i = 0; i < population.size(); i++) {
				Solution sol = population.get(i);

				int pid = sol.getSkillFactor();

				int start = problemSet.get(pid).getStartObjPos();
				int end = problemSet.get(pid).getEndObjPos();

				Solution newSolution = new Solution(end - start + 1);

				for (int k = start; k <= end; k++)
					newSolution.setObjective(k - start, sol.getObjective(k));

				resPopulation[pid].add(newSolution);
			}



			QualityIndicator indicator1 = new QualityIndicator(problemSet.get(0), pf1);
			QualityIndicator indicator2 = new QualityIndicator(problemSet.get(1), pf2);
			QualityIndicator indicator3 = null;
			resPopulation[0].printFeasibleFUN("result/rmp"+ args[1] + "/"+args[0]+"/Task1/FinalFUN/FinalFUN" + String.valueOf(t)+ ".dat");
			resPopulation[1].printFeasibleFUN("result/rmp"+ args[1] + "/"+args[0]+"/Task2/FinalFUN/FinalFUN" + String.valueOf(t)+ ".dat");

			if(args[0].contains("3")){
				indicator3 = new QualityIndicator(problemSet.get(1), pf3);
				resPopulation[2].printFeasibleFUN("result/rmp"+ args[1] + "/"+args[0]+"/Task3/FinalFUN/FinalFUN" + String.valueOf(t)+ ".dat");
			}

			double igd1 =  indicator1.getIGD(resPopulation[0]);
			double igd2 = indicator2.getIGD(resPopulation[1]);
			double igd3 =0;
			if(args[0].contains("3")){
			 igd3	= indicator3.getIGD(resPopulation[2]);
			}
			ave1Array[t-1] = igd1;
			ave2Array[t-1] = igd2;
			ave3Array[t-1] = igd3;

			if(args[0].contains("3")){
				System.out.println(t + "\t" + form.format(igd1) + "\t" + form.format(igd2)+ "\t" + form.format(igd3));
			} else {
				System.out.println(t + "\t" + form.format(igd1) + "\t" + form.format(igd2));
			}

			ave1 += igd1;
			ave2 += igd2;
			ave3 += igd3;

		}
		File newfile = new File("result");
		newfile.mkdir();

		newfile = new File("result/"+ args[0]);
		newfile.mkdir();


		FileOutputStream fos_1 = new FileOutputStream("result/rmp"+ args[1] + "/"+args[0]+"/Task1/IGD.dat");
		OutputStreamWriter osw_1 = new OutputStreamWriter(fos_1);
		BufferedWriter bw_1 = new BufferedWriter(osw_1);

		for(int t = 0; t<ave1Array.length;t++){
			bw_1.write(String.valueOf(ave1Array[t]));
			bw_1.newLine();
		}
		bw_1.close();

		FileOutputStream fos_2 = new FileOutputStream("result/rmp"+ args[1] + "/"+args[0]+"/Task2/IGD.dat");
		OutputStreamWriter osw_2 = new OutputStreamWriter(fos_2);
		BufferedWriter bw_2 = new BufferedWriter(osw_2);

		for(int t = 0; t<ave2Array.length;t++){
			bw_2.write(String.valueOf(ave2Array[t]));
			bw_2.newLine();
		}
		bw_2.close();

		if(args[0].contains("3")){
			FileOutputStream fos_3 = new FileOutputStream("result/rmp"+ args[1] + "/"+args[0]+"/Task3/IGD.dat");
			OutputStreamWriter osw_3 = new OutputStreamWriter(fos_3);
			BufferedWriter bw_3 = new BufferedWriter(osw_3);

			for(int t = 0; t<ave3Array.length;t++){
				bw_3.write(String.valueOf(ave3Array[t]));
				bw_3.newLine();
			}
			bw_3.close();



			System.out.println();
			System.out.println("Average IGD for " + name1 + ": " + ave1 / times);
			System.out.println("Average IGD for " + name2 + ": " + ave2 / times);
			System.out.println("Average IGD for " + name3 + ": " + ave3 / times);

		} else {
			System.out.println();
			System.out.println("Average IGD for " + name1 + ": " + ave1 / times);
			System.out.println("Average IGD for " + name2 + ": " + ave2 / times);
		}



	}
}
