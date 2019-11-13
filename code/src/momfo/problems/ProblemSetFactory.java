package momfo.problems;

import java.io.IOException;

import momfo.core.ProblemSet;
import momfo.core.Solution;
import momfo.problems.benchmarks.CIHS;
import momfo.problems.benchmarks.CIHS3;
import momfo.problems.benchmarks.CILS;
import momfo.problems.benchmarks.CIMS;
import momfo.problems.benchmarks.NIHS;
import momfo.problems.benchmarks.NIHS3;
import momfo.problems.benchmarks.NILS;
import momfo.problems.benchmarks.NIMS;
import momfo.problems.benchmarks.PIHS;
import momfo.problems.benchmarks.PIHS3;
import momfo.problems.benchmarks.PILS;
import momfo.problems.benchmarks.PIMS;
import momfo.util.Configuration;
import momfo.util.JMException;
import momfo.util.wrapper.XReal;

public class ProblemSetFactory {

	public static ProblemSet getProblem(String problemName) throws IOException, JMException{

		if(problemName.equalsIgnoreCase("CIHS")){
			return new CIHS().getProblem();
		} else if (problemName.equalsIgnoreCase("CIMS")){
			return new CIMS().getProblem();
		}else if (problemName.equalsIgnoreCase("CILS")){
			return new CILS().getProblem();
		} else if(problemName.equalsIgnoreCase("PIHS")){
			return new PIHS().getProblemSet();
		} else if (problemName.equalsIgnoreCase("PIMS")){
			return new PIMS().getProblem();
		}else if (problemName.equalsIgnoreCase("PILS")){
			return new PILS().getProblem();
		}  else if(problemName.equalsIgnoreCase("NIHS")){
			return new NIHS().getProblem();
		} else if (problemName.equalsIgnoreCase("NIMS")){
			return new NIMS().getProblemSet();
		}else if (problemName.equalsIgnoreCase("NILS")){
			return new NILS().getProblem();
		}else if (problemName.equalsIgnoreCase("CIHS3")){
			return new CIHS3().getProblem();
		}else if (problemName.equalsIgnoreCase("PIHS3")){
			return new PIHS3().getProblem();
		}else if (problemName.equalsIgnoreCase("NIHS3")){
			return new NIHS3().getProblem();
		}  else {
			Configuration.logger_
			.severe("ProblemSetFactory.getProblemSet. " + "Problem '" + problemName + "' not found ");
			throw new JMException("Exception in " + problemName + ".getCrossoverOperator()");
		}
	}


	public static void main(String[] args) throws JMException, IOException, ClassNotFoundException{
		String[] problemNameSet = {"CIHS","CIMS","CILS","PIHS","PIMS","PILS","NIHS","NIMS","NILS"};

//		String[] problemNameSet = {"CIHS3","PIHS3","NIHS3"};
//		String[] problemNameSet = {"PIHS3","NIHS3"};

		for(int p = 0; p < problemNameSet.length;p++){
						
			String problemName = problemNameSet[p] ;
			ProblemSet problemSet = getProblem(problemName);

			Solution sol1 = new Solution(problemSet);

			XReal offs1 = new XReal(sol1);
			for(int val = 0 ; val < sol1.getNumberOfVariables();val++){
				offs1.setValue(val, 0.3);				
			}
			
			problemSet.get(0).evaluate(sol1);

			System.out.print(problemName + "	Task1	");
			for(int o = 0;o < problemSet.get(0).getNumberOfObjectives();o++){
				System.out.print(sol1.getObjective(o)+"	");
			}

			System.out.println();
			System.out.print(problemName + "	Task2	");

			Solution sol2 = new Solution(problemSet);
			XReal offs2 = new XReal(sol2);
			sol2.setSkillFactor(1);
			for(int val = 0 ; val < sol2.getNumberOfVariables();val++){
				offs2.setValue(val, 0.3);				
			}

			
			problemSet.get(1).evaluate(sol2);

			for(int o = problemSet.get(0).getNumberOfObjectives();o <problemSet.get(0).getNumberOfObjectives()+problemSet.get(1).getNumberOfObjectives() ;o++){
				System.out.print(sol2.getObjective(o)+"	");
			}
			System.out.println();
/*			System.out.print(problemName + "	Task3	");
			
			Solution sol3 = new Solution(problemSet);
			sol3.setSkillFactor(2);

			XReal offs3 = new XReal(sol3);
			for(int val = 0 ; val < sol3.getNumberOfVariables();val++){
				offs3.setValue(val, 0.3);				
			}

			problemSet.get(2).evaluate(sol3);

			for(int o = problemSet.get(0).getNumberOfObjectives()+problemSet.get(1).getNumberOfObjectives() ;o <problemSet.get(0).getNumberOfObjectives()+problemSet.get(1).getNumberOfObjectives() +problemSet.get(2).getNumberOfObjectives()  ;o++){
				System.out.print(sol3.getObjective(o)+"	");
			}
			System.out.println();
*/
		}
	}
	
}
