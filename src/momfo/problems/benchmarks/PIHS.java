package momfo.problems.benchmarks;

import java.io.IOException;

import momfo.core.Problem;
import momfo.core.ProblemSet;
import momfo.core.Solution;
import momfo.problems.base.IO;
import momfo.problems.base.MMZDT;
import momfo.util.JMException;
import momfo.util.fileSubscription;
import momfo.util.wrapper.XReal;


public class PIHS {

	public static ProblemSet getProblemSet() throws IOException {
		ProblemSet ps1 = getT1();
		ProblemSet ps2 = getT2();
		ProblemSet problemSet = new ProblemSet(2);

		problemSet.add(ps1.get(0));
		problemSet.add(ps2.get(0));
		return problemSet;

	}

	public static ProblemSet getT1() throws IOException {
		ProblemSet problemSet = new ProblemSet(1);

		MMZDT prob = new MMZDT(50, 1,  -100,100);
		prob.setGType("sphere");
		prob.setHType("convex");
		((Problem)prob).setName("PIHS1");

		problemSet.add(prob);
		return problemSet;
	}

	public static ProblemSet getT2() throws IOException {
		ProblemSet problemSet = new ProblemSet(1);

		MMZDT prob = new MMZDT(50, 1,  -100,100);
		prob.setGType("rastrigin");
		prob.setHType("convex");

		double[] shiftValues = IO.readShiftValuesFromFile("SVData/S_PIHS_2.txt");
		prob.setShiftValues(shiftValues);


		((Problem)prob).setName("PIHS2");

		problemSet.add(prob);
		return problemSet;
	}



	public static void main(String[] args) throws IOException, JMException, ClassNotFoundException {
		ProblemSet problem = getT1();
		Solution sol = new Solution(problem);
		XReal offs1 = new XReal(sol);

		for(int i =1;i<50;i++){
			offs1.setValue(i, 0.5);
		}
		double[][] obj = new double[501][2];

		for(int j = 0; j <= 500;j++){
			offs1.setValue(0, (double)j/500);
			problem.get(0).evaluate(sol);
			obj[j][0] = sol.getObjective(0);
			obj[j][1] = sol.getObjective(1);
		}
		fileSubscription.printToFile("do.dat", obj);
		System.out.println(sol.getObjective(0)+"	"+ sol.getObjective(1));
	}
}
