package momfo.problems;

import java.io.IOException;

import momfo.core.Problem;
import momfo.problems.knapsack.Knapsack_bitflip;
import momfo.problems.knapsack.Knapsack_profitflip;
import momfo.problems.knapsack.Knapsack_scaling;
import momfo.util.Configuration;
import momfo.util.JMException;

public class KnapsackSetFactory {

	public static Problem getProblem(String problemName, double params) throws IOException, JMException{

		if(problemName.equalsIgnoreCase("Bitflip")){
			return new Knapsack_bitflip(2, params);
		} else if (problemName.equalsIgnoreCase("Scaling")){
			return new Knapsack_scaling(2, params);
		} else if (problemName.equalsIgnoreCase("Profitflip")){
			return new Knapsack_profitflip(2, params);
		}  else {
			Configuration.logger_
			.severe("ProblemSetFactory.getProblemSet. " + "Problem '" + problemName + "' not found ");
			throw new JMException("Exception in " + problemName + ".getCrossoverOperator()");
		}
	}
}
