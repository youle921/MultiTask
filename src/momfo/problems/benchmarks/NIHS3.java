package momfo.problems.benchmarks;

import java.io.FileNotFoundException;
import java.io.IOException;

import momfo.core.Problem;
import momfo.core.ProblemSet;
import momfo.problems.base.MMDTLZ;
import momfo.problems.base.MMZDT;


public class NIHS3 {

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

		MMDTLZ prob = new MMDTLZ(2, 50, 1, -80,80);
		prob.setGType("rosenbrock");

		((Problem)prob).setName("NIHS1");

		problemSet.add(prob);
		return problemSet;
	}

	public static ProblemSet getT2() throws IOException {
		ProblemSet problemSet = new ProblemSet(1);

		MMZDT prob = new MMZDT(50, 1,  -80,80);
		prob.setGType("sphere");

		prob.setHType("convex");
		((Problem)prob).setName("NIHS2");

		problemSet.add(prob);
		return problemSet;
	}

	private static ProblemSet getT3() throws FileNotFoundException, IOException {
		ProblemSet problemSet = new ProblemSet(1);

		MMZDT prob = new MMZDT(50, 1,  -80,80);
		prob.setGType("happycat");

		((Problem)prob).setName("NIHS3");
		prob.setHType("concave");

		problemSet.add(prob);
		return problemSet;
	}


	public static void main(String[] args) {

	}

}
