package momfo.problems.base;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.Map;

import momfo.core.Problem;
import momfo.core.Solution;
import momfo.core.Variable;
import momfo.util.JMException;

public class Knapsack extends Problem {

	private static int[][] profit_;
	private static int[][] weight_;

	private static String DirectoryName = "Data/Knapsack/Items/knapsack_500_";
	private static String Extension = ".csv";

	static double[] capacity_;
	private int[] sort_min_;

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

	public static void main(String[] args) {

		Knapsack a = new Knapsack(8);

		Solution d = new Solution();

		for (int i = 0; i < 250; i++) {
			// d.setValue(i*2, 1);
			// d.setValue(i*2+1, 1);
		}
		a.subscript();
		// a.repair(d,null);
		// a.evaluate(d);
		for (int i = 0; i < 2; i++) {
			System.out.print(d.getObjective(i) + "	");
		}
	}

	public int[] decodeSolution(Solution sol) throws JMException {
		Variable[] decisionVariables = sol.getDecisionVariables();
		int[] x = new int[numberOfVariables_];

		for (int i = 0; i < numberOfVariables_; i++)
			if (decisionVariables[i].getValue() < 0.5) {
				x[i] = 0;
			} else if (decisionVariables[i].getValue() >= 0.5) {
				x[i] = 1;
			}

		return x;

	}

	public void evaluate(Solution solution) throws JMException {

		int[] val = decodeSolution(solution);
		int[] f = new int[numberOfObjectives_];

		int sum;
		for (int i = 0; i < numberOfObjectives_; i++) {
			sum = 0;
			for (int j = 0; j < numberOfVariabes_; j++) {
				sum += profit_[i][j] * val[j];
			}
			f[i] = sum;
		}

		break_knapsack(val);

		for (int i = 0; i < numberOfObjectives_; i++)
			solution.setObjective(i, f[i]);

	}

	// this method read the knapsack data
	public void setItems() {

		String line_profit;
		String line_weight;

		for (int i = 1; i <= numberOfObjectives_; i++) {

			String ProfitName = DirectoryName + "profit" + String.valueOf(i) + Extension;
			String WeightName = DirectoryName + "Weight" + String.valueOf(i) + Extension;

			try (BufferedReader br_profit = new BufferedReader(new FileReader(ProfitName));
					BufferedReader br_weight = new BufferedReader(new FileReader(WeightName));) {

				capacity_[i] = 0;

				for (int j = 0; i < numberOfVariables_; j++) {
					line_profit = br_profit.readLine();
					profit_[i][j] = Integer.valueOf(line_profit);
					line_weight = br_weight.readLine();
					weight_[i][j] = Integer.valueOf(line_weight);
					capacity_[i] += weight_[i][j];
				}

				if (i == 1 | i == 2) {
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


	public void repair(Solution c, Map<String, Object> a) throws JMException {
		int[] d = new int[1];
		if (!break_knapsack(d))
			return;
		int counter = 0;
		do {
			d[sort_min_[counter++]] = 0;
		} while (break_knapsack(d));

	}

	/*
	 * if at least one Knapsack is broken, this method return true; else return
	 * false;
	 */
	public boolean break_knapsack(int[] sol) throws JMException {
		double sum = 0;
		int bit = 1;

		for (int i = 0; i < numberOfObjectives_; i++) {
			sum = 0;
			for (int j = 0; j < numberOfVariables_; j++) {

				if (sol[j] > 0.99) {
					bit = 1;
				} else if (sol[j] < 0.01) {
					bit = 0;
				}
				sum += bit * weight_[i][j];
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
