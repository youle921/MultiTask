package momfo.problems.knapsack;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;

import momfo.core.Problem;
import momfo.core.Solution;
import momfo.core.Variable;
import momfo.encodings.solutionType.IntSolutionType;
import momfo.util.JMException;
import momfo.util.wrapper.XInt;

public class Knapsack extends Problem {

	protected static int[][] profit_;
	protected static int[][] weight_;

	protected static String DirectoryName = "Data/Knapsack/items/knapsack_500_";
	protected static String Extension = ".csv";

	protected double[] capacity_;
	protected int[] sort_min_;

	int decodeType = 0;//

	public void setDecodeType(int d) {
		decodeType = d;
	}

	public Knapsack(Integer numberOfObjectives) {

		numberOfVariables_ = 500;
		numberOfObjectives_ = numberOfObjectives;
		problemName_ = "Knapsack";

		profit_ = new int[numberOfObjectives_][numberOfVariables_];
		weight_ = new int[numberOfObjectives_][numberOfVariables_];
		capacity_ = new double[numberOfObjectives_];

		setItems();
		setRepairOrder();

		lowerLimit_ = new double[numberOfVariables_];
		upperLimit_ = new double[numberOfVariables_];
		for (int var = 0; var < numberOfVariables_; var++) {
			lowerLimit_[var] = 0.0;
			upperLimit_[var] = 1.0;
		} // for
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

	public void evaluate(Solution solution) throws JMException {

		XInt var = new XInt(solution);
		int[] f = new int[numberOfObjectives_];

		repair(var);

		int sum;
		for (int i = 0; i < numberOfObjectives_; i++) {
			sum = 0;
			for (int j = 0; j < numberOfVariables_; j++) {
				sum += profit_[i][j] * var.getValue(j);
			}
			f[i] = sum;
		}

		// to change to minimization problems, use objective function value multipled by -1 
		for (int i = 0; i < numberOfObjectives_; i++){
			solution.setObjective(startObjPos_ + i, -1 * f[i]);
		}			
	}

	public void repair(XInt v) throws JMException {

		for (int counter = 0; break_knapsack(v); counter++){
			v.setValue(sort_min_[counter], 0);
		}

	}

	/*
	 * if at least one Knapsack is broken, this method return true; else return
	 * false;
	 */
	public boolean break_knapsack(XInt sol) throws JMException {

		double sum ;

		for (int i = 0; i < numberOfObjectives_; i++) {

			sum = 0;
			
			for (int j = 0; j < numberOfVariables_; j++) {
				sum += sol.getValue(j) * weight_[i][j];
			}
			if (sum > capacity_[i]) {
				return true;
			}
		}
		return false;
	}

	public void subscript() {
		System.out.println("knapsack Capa : " + numberOfObjectives_);
		System.out.println("knapsack detail information : ");
		for (int i = 0; i < numberOfObjectives_; i++) {
			System.out.println("knapsack Capa : " + capacity_[i]);
			// for(int j=0;j<numberOfVariabes;j++){
			// System.out.println("Number" +j +"Item profit : " + profit_[i][j] + " weight :
			// " + weight_[i][j]);
			// }
		}
	}

}
