package momfo.problems.benchmarks;

import java.io.FileNotFoundException;
import java.io.IOException;

import momfo.core.Problem;
import momfo.core.ProblemSet;
import momfo.problems.base.IO;
import momfo.problems.base.MMDTLZ;
import momfo.problems.base.MMZDT;


public class PIHS3 {

	public static ProblemSet getProblem() throws IOException {
		ProblemSet ps1 = getT1();
		ProblemSet ps2 = getT2();
		ProblemSet ps3 = getT3();

		ProblemSet problemSet = new ProblemSet(3);

		problemSet.add(ps1.get(0));
		problemSet.add(ps2.get(0));
		problemSet.add(ps3.get(0));

		return problemSet;
	}


	public static ProblemSet getT1() throws IOException {
		ProblemSet problemSet = new ProblemSet(1);

		MMZDT prob = new MMZDT( 50, 1, -100,100);
		prob.setGType("sphere");

		prob.setHType("convex");
		((Problem)prob).setName("PIHS1");

		problemSet.add(prob);
		return problemSet;
	}


	public static ProblemSet getT2() throws IOException {
		ProblemSet problemSet = new ProblemSet(1);

		MMZDT prob = new MMZDT(50, 1,  -100,100);
		prob.setGType("Rastrigin");

		prob.setHType("convex");
		((Problem)prob).setName("CIHS2");

		double[] shiftValues= IO.readShiftValuesFromFile("SVData/S_PIHS3_2.txt");
		prob.setShiftValues(shiftValues);

		problemSet.add(prob);
		return problemSet;
	}

	private static ProblemSet getT3() throws FileNotFoundException, IOException {
		ProblemSet problemSet = new ProblemSet(1);

		MMDTLZ prob = new MMDTLZ(2, 50, 1, -100,100);
		prob.setGType("bentcigar");

		((Problem)prob).setName("PIHS3");

		double[] shiftValues = IO.readShiftValuesFromFile("SVData/S_PIHS3_3.txt");
		prob.setShiftValues(shiftValues);

		problemSet.add(prob);
		return problemSet;
	}


	public static void main(String[] args) {

	}

}
