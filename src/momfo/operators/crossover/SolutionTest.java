package momfo.operators.crossover;

import java.io.IOException;
import java.util.HashMap;

import momfo.core.Operator;
import momfo.core.ProblemSet;
import momfo.core.Solution;
import momfo.problems.ProblemSetFactory;
import momfo.util.JMException;

public class SolutionTest {
	
	public static void main(String[] args) throws ClassNotFoundException, IOException, JMException {
		ProblemSet problemSet = ProblemSetFactory.getProblem("CIHS");
		
		Solution solOne = new Solution(problemSet);
		Solution solTwo = new Solution(problemSet);

		
		HashMap<String, Double> parameters = new HashMap();
		parameters.put("probability", 0.9);
		parameters.put("distributionIndex", 20.0);
		parameters.put("SBXAlpha", 0.0);
		Operator Crossover = CrossoverFactory.getCrossoverOperator("SBXCrossoverWithOther", parameters);

		Solution [] parents = new Solution[2];
		for(int val = 0; val < solOne.getNumberOfVariables();val++) {
			solOne.getDecisionVariables()[val].setValue(0.3);
			solTwo.getDecisionVariables()[val].setValue(0.8);			
		}
		parents[0] = solOne;
		parents[1] = solTwo;
		
		Solution[] offspring = (Solution[]) Crossover.execute(parents);
		
		for(int val = 0; val < solOne.getNumberOfVariables();val++) {
			System.out.println(offspring[0].getDecisionVariables()[val].getValue());
		}
		
	}
	
	
}
