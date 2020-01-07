package org.uma.jmetal.problem.multiobjective;

import org.uma.jmetal.problem.binaryproblem.impl.AbstractBinaryProblem;
import org.uma.jmetal.solution.binarysolution.BinarySolution;
import org.uma.jmetal.util.JMetalException;

import java.util.Arrays;
import java.util.BitSet;
import java.util.List;
import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;

public class Knapsack extends AbstractBinaryProblem {

	private static int[][] profit_;
	private static int[][] weight_;

	private static String DirectoryName = "Data/Knapsack/Items/knapsack_500_";
	private static String Extension = ".csv";

	static double[] capacity_;
	private int[] sort_min_;

	private static int numberOfObjectives_;
	private static int numberOfVariables_;

	public Knapsack() {
        this(500, 2);
    }

    public Knapsack(Integer numberOfObjectives) {
        this(500, numberOfObjectives);
    }
	public Knapsack(Integer numberOfVariabes, Integer numberOfObjectives) {

		numberOfVariables_ = numberOfVariabes;
		numberOfObjectives_ = numberOfObjectives;

		setNumberOfVariables(numberOfVariables_);
		setNumberOfObjectives(numberOfObjectives_);
		setName("Knapsack");

		profit_ = new int[numberOfObjectives_][numberOfVariables_];
		weight_ = new int[numberOfObjectives_][numberOfVariables_];
		capacity_ = new double[numberOfObjectives_];

		setItems();
		setRepairOrder();
	}


	// this method read the knapsack data
	public void setItems() {

		String line_profit;
		String line_weight;

		for (int i = 0; i < numberOfObjectives_; i++) {

			String ProfitName = DirectoryName + "profit" + String.valueOf(i + 1) + Extension;
			String WeightName = DirectoryName + "Weight" + String.valueOf(i + 1) + Extension;

			try (BufferedReader br_profit = new BufferedReader(new FileReader(ProfitName));
					BufferedReader br_weight = new BufferedReader(new FileReader(WeightName));) {

				capacity_[i] = 0;

				for (int j = 0; j < numberOfVariables_; j++) {
					line_profit = br_profit.readLine();
					profit_[i][j] = Integer.valueOf(line_profit);
					line_weight = br_weight.readLine();
					weight_[i][j] = Integer.valueOf(line_weight);
					capacity_[i] += weight_[i][j];
				}

				if (i == 0 | i == 1) {
					capacity_[i] /= 2;
				} else {
					capacity_[i] = Double.POSITIVE_INFINITY;
				}

			} catch (IOException e) {
				e.printStackTrace();
			}

		}

	}

	public void setRepairOrder(){

		sort_min_ = new int[numberOfVariables_];
		double[] q_ = new double[numberOfVariables_];
		// variableType_ = 1;

		double max;
		int em;

		for (int i = 0; i < numberOfVariables_; i++) {
			sort_min_[i] = i;
			max = (double) profit_[0][i] / weight_[0][i];
			for (int j = 1; j < 2; j++) {
				max = Math.max(max, (double) profit_[j][i] / weight_[j][i]);
			}
			q_[i] = max;
		}
		
		for (int i = 0; i < numberOfVariables_; i++) {
			for (int j = 0; j < numberOfVariables_; j++) {
				if (q_[sort_min_[i]] < q_[sort_min_[j]]) {
					em = sort_min_[j];
					sort_min_[j] = sort_min_[i];
					sort_min_[i] = em;
				}
			}
		}

	}

    @Override
    public List<Integer> getListOfBitsPerVariable() {
        return Arrays.asList(getNumberOfVariables());
    }

    @Override
	public void evaluate(BinarySolution solution) throws JMetalException {

		BitSet var = solution.getVariable(0);
		int[] f = new int[numberOfObjectives_];

		repair(var);

		int sum;

		for (int i = 0; i < numberOfObjectives_; i++) {
			sum = 0;

			for (int j = 0; j < numberOfVariables_; j++) {
                if(var.get(i)){
                    sum += profit_[i][j];
                }
			}

			f[i] = sum;
		}

		// to change to minimization problems, use objective function value multipled by -1 
		for (int i = 0; i < numberOfObjectives_; i++){
			solution.setObjective(i, -1 * f[i]);
		}
	}

	public void repair(BitSet v) throws JMetalException {

		for (int counter = 0; break_knapsack(v); counter++){
			v.clear(sort_min_[counter]);
		}

	}

	/*
	 * if at least one Knapsack is broken, this method return true; else return
	 * false;
	 */
	public boolean break_knapsack(BitSet sol) throws JMetalException {

		double sum ;

		for (int i = 0; i < numberOfObjectives_; i++) {

			sum = 0;
			
			for (int j = 0; j < numberOfVariables_; j++) {
                if (sol.get(j)){
                    sum += weight_[i][j];
                }
			}
            
			if (sum > capacity_[i]) {
				return true;
			}
		}
		return false;
	}

}
